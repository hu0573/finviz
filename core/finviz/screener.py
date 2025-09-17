"""
FinViz股票筛选功能

提供基于FinViz的股票筛选功能，支持多种筛选条件和表格类型。
"""

import json
import pathlib
import urllib.request
from urllib.parse import parse_qs as urlparse_qs
from urllib.parse import urlencode, urlparse
from typing import Dict, List, Optional, Union

from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from .helper_functions import scraper_functions as scrape
from .helper_functions.display_functions import create_table_string
from .helper_functions.error_handling import InvalidTableType, NoResults
from .helper_functions.request_functions import (Connector,
                                                       http_request_get,
                                                       sequential_data_scrape)

TABLE_TYPES = {
    # 主要表格类型（基于实际筛选器分布）
    "Descriptive": "111",    # 描述性筛选器：交易所、板块、市值等
    "Fundamental": "161",    # 基本面筛选器：财务指标、估值指标
    "Technical": "171",      # 技术分析筛选器：RSI、SMA、技术指标
    "News": "181",          # 新闻筛选器：新闻相关
    "ETF": "181",           # ETF筛选器：ETF和基金相关
    
    # 兼容性映射（保持向后兼容）
    "Overview": "111",      # 等同于Descriptive
    "Financial": "161",     # 等同于Fundamental
    "Valuation": "121",     # 估值筛选器（Fundamental的子集）
    "Ownership": "131",     # 持股信息（Descriptive的子集）
    "Performance": "141",   # 表现数据（Technical的子集）
    "Custom": "152",        # 自定义列
}


class Screener(object):
    """FinViz股票筛选器类"""

    @classmethod
    def init_from_url(cls, url: str, rows: Optional[int] = None):
        """
        从URL初始化筛选器
        
        Args:
            url: FinViz筛选器URL
            rows: 返回行数限制
            
        Returns:
            Screener: 筛选器实例
        """
        split_query = urlparse_qs(urlparse(url).query)

        tickers = split_query["t"][0].split(",") if "t" in split_query else None
        filters = split_query["f"][0].split(",") if "f" in split_query else None
        custom = split_query["c"][0].split(",") if "c" in split_query else None
        order = split_query["o"][0] if "o" in split_query else ""
        signal = split_query["s"][0] if "s" in split_query else ""

        table = "Overview"
        if "v" in split_query:
            table_numbers_types = {v: k for k, v in TABLE_TYPES.items()}
            table_number_string = split_query["v"][0][0:3]
            try:
                table = table_numbers_types[table_number_string]
            except KeyError:
                raise InvalidTableType(split_query["v"][0])

        return cls(tickers, filters, rows, order, signal, table, custom)

    def __init__(
        self,
        tickers: Optional[List[str]] = None,
        filters: Optional[List[str]] = None,
        rows: Optional[int] = None,
        order: str = "",
        signal: str = "",
        table: Optional[str] = None,
        custom: Optional[List[str]] = None,
        user_agent: str = generate_user_agent(),
        request_method: str = "sequential",
    ):
        """
        初始化筛选器
        
        Args:
            tickers: 股票代码列表，如 ['AAPL', 'AMD', 'WMT']
            filters: 筛选条件列表，如 ['exch_nasd', 'idx_sp500', 'fa_div_none']
            rows: 返回行数限制
            order: 排序方式，如 '-price' 表示按价格降序
            signal: 信号筛选，如 'n_majornews'
            table: 表格类型，如 'Performance'
            custom: 自定义列，如 ['1', '21', '23', '45']
            user_agent: 用户代理字符串
            request_method: 请求方法，'sequential' 或 'async'
        """
        if tickers is None:
            self._tickers = []
        else:
            self._tickers = tickers

        if filters is None:
            self._filters = []
        else:
            self._filters = filters

        if table is None:
            self._table = "111"
        else:
            self._table = self.__check_table(table)

        if custom is None:
            self._custom = []
        else:
            self._table = "152"
            self._custom = custom

            if (
                "0" not in self._custom
            ):  # 0 (No.) is required for the sequence algorithm to work
                self._custom = ["0"] + self._custom

        self._rows = rows
        self._order = order
        self._signal = signal
        self._user_agent = user_agent
        self._request_method = request_method

        self.analysis = []
        self.data = self.__search_screener()

    def __call__(
        self,
        tickers: Optional[List[str]] = None,
        filters: Optional[List[str]] = None,
        rows: Optional[int] = None,
        order: str = "",
        signal: str = "",
        table: Optional[str] = None,
        custom: Optional[List[str]] = None,
    ):
        """
        添加更多筛选条件
        
        Example:
            stock_list = Screener(filters=['cap_large'])
            stock_list(filters=['fa_div_high'], table='Performance')
        """
        if tickers:
            [self._tickers.append(item) for item in tickers]

        if filters:
            [self._filters.append(item) for item in filters]

        if table:
            self._table = self.__check_table(table)

        if order:
            self._order = order

        if signal:
            self._signal = signal

        if rows:
            self._rows = rows

        if custom:
            self._custom = custom

        self.analysis = []
        self.data = self.__search_screener()

    add = __call__

    def __str__(self):
        """返回可读的表格表示"""
        table_list = [self.headers]

        for row in self.data:
            table_list.append([row[col] or "" for col in self.headers])

        return create_table_string(table_list)

    def __repr__(self):
        """返回参数值的字符串表示"""
        values = (
            f"tickers: {tuple(self._tickers)}\n"
            f"filters: {tuple(self._filters)}\n"
            f"rows: {self._rows}\n"
            f"order: {self._order}\n"
            f"signal: {self._signal}\n"
            f"table: {self._table}\n"
            f"table: {self._custom}"
        )

        return values

    def __len__(self):
        """返回总行数"""
        return int(self._rows)

    def __getitem__(self, position):
        """返回特定行数据"""
        return self.data[position]

    get = __getitem__

    @staticmethod
    def __check_table(input_table: str) -> str:
        """检查表格类型输入是否正确"""
        try:
            table = TABLE_TYPES[input_table]
            return table
        except KeyError:
            raise InvalidTableType(input_table)
    
    @staticmethod
    def get_optimal_table_type(filters: List[str]) -> str:
        """
        根据筛选器类型自动选择最优表格类型
        
        Args:
            filters: 筛选器列表
            
        Returns:
            str: 最优表格类型名称
        """
        if not filters:
            return "Descriptive"
        
        # 筛选器前缀与表格类型的对应关系
        filter_type_mapping = {
            'ta_': 'Technical',      # 技术指标
            'fa_': 'Fundamental',    # 财务指标
            'etf_': 'ETF',          # ETF筛选器
            'n_': 'News',           # 新闻筛选器
        }
        
        # 基础筛选器前缀
        descriptive_prefixes = [
            'exch_', 'idx_', 'sec_', 'ind_', 'geo_', 'cap_', 
            'sh_', 'an_', 'earningsdate', 'ipodate'
        ]
        
        # 检查筛选器类型
        for filter_id in filters:
            for prefix, table_type in filter_type_mapping.items():
                if filter_id.startswith(prefix):
                    return table_type
            
            # 检查是否是基础筛选器
            for prefix in descriptive_prefixes:
                if filter_id.startswith(prefix):
                    return "Descriptive"
        
        # 默认返回描述性表格
        return "Descriptive"

    @staticmethod
    def load_filter_dict(reload: bool = True) -> Dict:
        """
        获取可用的筛选器选项字典
        
        Args:
            reload: 是否重新加载筛选器选项
            
        Returns:
            Dict: 筛选器选项字典，按类别组织
        """
        # Get location of filter.json
        json_directory = pathlib.Path(__file__).parent
        json_file = pathlib.Path.joinpath(json_directory, "filters.json")

        # Reload the filters JSON file if present and requested
        if reload and json_file.is_file():
            with open(json_file, "r") as fp:
                return json.load(fp)

        # Get html from main filter page, ft=4 ensures all filters are present
        hdr = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) "
            "Chrome/23.0.1271.64 Safari/537.11"
        }
        url = "https://finviz.com/screener.ashx?ft=4"
        req = urllib.request.Request(url, headers=hdr)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")

        # Parse html and locate table we are interested in.
        bs = BeautifulSoup(html, "html.parser")
        filters_table = None
        for td in bs.find_all("td"):
            if td.get_text().strip() == "Exchange":
                filters_table = td.find_parent("table")
        if filters_table is None:
            raise Exception("Could not locate filter parameters")

        # Delete all div tags, we don't need them
        for div in filters_table.find_all("div"):
            div.decompose()

        # Populate dict with filtering options and corresponding filter tags
        filter_dict = {}
        td_list = filters_table.find_all("td")

        for i in range(0, len(td_list) - 2, 2):
            current_dict = {}
            if td_list[i].get_text().strip() == "":
                continue

            # Even td elements contain filter name (as shown on web page)
            filter_text = td_list[i].get_text().strip()

            # Odd td elements contain the filter tag and options
            selections = td_list[i + 1].find("select")
            if selections is None:
                continue
            filter_name = selections.get("data-filter")
            if filter_name is None:
                continue
            filter_name = filter_name.strip()

            # Store filter options for current filter
            options = selections.find_all("option", {"value": True})
            for opt in options:
                # Encoded filter string
                value = opt.get("value").strip()

                # String shown in pull-down menu
                text = opt.get_text()

                # Filter out unwanted items
                if value is None or "Elite" in text:
                    continue

                # Make filter string and store in dict
                current_dict[text] = f"{filter_name}_{value}"

            # Store current filter dict
            filter_dict[filter_text] = current_dict

        # Save filter dict to finviz directory
        try:
            with open(json_file, "w") as fp:
                json.dump(filter_dict, fp)
        except Exception as e:
            print(e)
            print("Unable to write to file{}".format(json_file))

        return filter_dict

    def __check_rows(self):
        """检查用户输入的行数是否正确"""
        self._total_rows = scrape.get_total_rows(self._page_content)

        if self._total_rows == 0:
            raise NoResults(self._url.split("?")[1])
        elif self._rows is None or self._rows > self._total_rows:
            return self._total_rows
        else:
            return self._rows

    def __get_table_headers(self):
        """获取表头"""
        headers = []

        # 尝试新的表头结构 (thead tr th)
        header_elements = self._page_content.cssselect('thead tr th')
        
        if not header_elements:
            # 尝试旧的结构 (tr[valign="middle"] td)
            header_elements = self._page_content.cssselect('tr[valign="middle"] td')
        
        for header_element in header_elements:
            # Use normalize-space to extract text content while ignoring internal elements
            header_text = header_element.xpath("normalize-space()")
            
            if header_text:
                headers.append(header_text)
        
        return headers

    def __search_screener(self):
        """从FinViz筛选器获取数据"""
        self._page_content, self._url = http_request_get(
            "https://finviz.com/screener.ashx",
            payload={
                "v": self._table,
                "t": ",".join(self._tickers),
                "f": ",".join(self._filters),
                "o": self._order,
                "s": self._signal,
                "c": ",".join(self._custom),
            },
            user_agent=self._user_agent,
        )

        self._rows = self.__check_rows()
        self.headers = self.__get_table_headers()

        if self._request_method == "async":
            async_connector = Connector(
                scrape.get_table,
                scrape.get_page_urls(self._page_content, self._rows, self._url),
                self._user_agent,
                self.headers,
                self._rows,
                css_select=True,
            )
            pages_data = async_connector.run_connector()
        else:
            pages_data = sequential_data_scrape(
                scrape.get_table,
                scrape.get_page_urls(self._page_content, self._rows, self._url),
                self._user_agent,
                self.headers,
                self._rows,
            )

        data = []
        for page in pages_data:
            for row in page:
                data.append(row)

        return data


# ==================== 便捷函数 ====================

def get_screener_data(filters: Optional[List[str]] = None,
                     rows: Optional[int] = None,
                     order: str = "",
                     signal: str = "",
                     table: Optional[str] = None,
                     custom: Optional[List[str]] = None,
                     auto_table: bool = True) -> Dict:
    """
    获取筛选器数据
    
    Args:
        filters: 筛选条件列表，如 ['idx_sp500', 'sec_technology']
        rows: 返回行数限制
        order: 排序方式，如 '-price' 表示按价格降序
        signal: 信号筛选，如 'n_majornews'
        table: 表格类型，可选值: Descriptive, Fundamental, Technical, News, ETF
        custom: 自定义列，如 ['1', '21', '23']
        auto_table: 是否自动选择表格类型，默认True
        
    Returns:
        Dict: 包含表头和数据行的字典
    """
    try:
        # 自动选择表格类型
        if auto_table and table is None and filters:
            table = Screener.get_optimal_table_type(filters)
        elif table is None:
            table = "Descriptive"  # 默认表格类型
            
        screener = Screener(
            filters=filters,
            rows=rows,
            order=order,
            signal=signal,
            table=table,
            custom=custom
        )
        return {
            "headers": screener.headers,
            "data": screener.data,
            "total_rows": len(screener.data)
        }
    except Exception as e:
        return {
            "error": f"获取筛选器数据失败: {str(e)}",
            "headers": [],
            "data": [],
            "total_rows": 0
        }


def get_screener_from_url(url: str, rows: Optional[int] = None) -> Dict:
    """
    从URL初始化筛选器
    
    Args:
        url: FinViz筛选器URL
        rows: 返回行数限制
        
    Returns:
        Dict: 包含表头和数据行的字典
    """
    try:
        screener = Screener.init_from_url(url, rows)
        return {
            "headers": screener.headers,
            "data": screener.data,
            "total_rows": len(screener.data)
        }
    except Exception as e:
        return {
            "error": f"从URL获取筛选器数据失败: {str(e)}",
            "headers": [],
            "data": [],
            "total_rows": 0
        }


def get_filter_options() -> Dict:
    """
    获取可用的筛选器选项
    
    Returns:
        Dict: 筛选器选项字典，按类别组织
    """
    try:
        return Screener.load_filter_dict()
    except Exception as e:
        return {"error": f"获取筛选器选项失败: {str(e)}"}



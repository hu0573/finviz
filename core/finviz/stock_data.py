"""
FinViz股票数据功能

提供基于FinViz的股票数据获取功能，包括股票基本信息、新闻、内部交易等。
"""

from datetime import datetime
from typing import Dict, List, Tuple
from lxml import etree

from .helper_functions.request_functions import http_request_get
from .helper_functions.scraper_functions import get_table

STOCK_URL = "https://finviz.com/quote.ashx"
NEWS_URL = "https://finviz.com/news.ashx"
CRYPTO_URL = "https://finviz.com/crypto_performance.ashx"
STOCK_PAGE = {}


def get_page(ticker):
    """获取股票页面数据"""
    global STOCK_PAGE

    if ticker not in STOCK_PAGE:
        STOCK_PAGE[ticker], _ = http_request_get(
            url=STOCK_URL, payload={"t": ticker}, parse=True
        )


def get_stock(ticker: str) -> Dict:
    """
    获取股票详细信息
    
    Args:
        ticker: 股票代码，如 'AAPL'
        
    Returns:
        Dict: 包含股票详细信息的字典，包括价格、市值、财务数据等
        
    Example:
        >>> data = get_stock('AAPL')
        >>> print(data['Price'])  # 当前价格
    """
    try:
        get_page(ticker)
        page_parsed = STOCK_PAGE[ticker]

        # 获取基本信息 - 使用新的页面结构
        data = {}
        
        # 获取股票代码
        ticker_element = page_parsed.cssselect('.quote-header_ticker-wrapper_ticker')
        if ticker_element:
            data["Ticker"] = ticker_element[0].text.strip()
        
        # 获取公司名称
        company_element = page_parsed.cssselect('.quote-header_ticker-wrapper_company a')
        if company_element:
            data["Company"] = company_element[0].text.strip()
            company_link = company_element[0].get("href")
            data["Website"] = company_link if company_link and company_link.startswith("http") else None
        
        # 获取行业信息 - 从标签链接中提取
        tab_links = page_parsed.cssselect('.tab-link')
        for link in tab_links:
            href = link.get("href", "")
            if "sec_" in href:
                data["Sector"] = link.text.strip()
            elif "ind_" in href:
                data["Industry"] = link.text.strip()
            elif "geo_" in href:
                data["Country"] = link.text.strip()

        # 获取股票数据表格
        all_rows = [
            row.xpath("td//text()")
            for row in page_parsed.cssselect('tr[class="table-dark-row"]')
        ]

        for row in all_rows:
            for column in range(0, len(row) - 1, 2):
                if column + 1 < len(row):
                    key = row[column].strip()
                    value = row[column + 1].strip()
                    
                    # 处理特殊情况
                    if key == "EPS next Y" and "EPS next Y" in data.keys():
                        data["EPS growth next Y"] = value
                        continue
                    elif key == "Volatility":
                        vols = value.split()
                        if len(vols) >= 2:
                            data["Volatility (Week)"] = vols[0]
                            data["Volatility (Month)"] = vols[1]
                        continue
                    
                    data[key] = value

        return data
    except Exception as e:
        return {"error": f"获取股票数据失败: {str(e)}"}


def get_news(ticker: str) -> List[Tuple[str, str, str, str]]:
    """
    获取股票相关新闻
    
    Args:
        ticker: 股票代码，如 'AAPL'
        
    Returns:
        List[Tuple]: 新闻列表，每个元素包含 (时间, 标题, 链接, 来源)
        
    Example:
        >>> news = get_news('AAPL')
        >>> for time, title, url, source in news[:3]:
        ...     print(f"{time}: {title}")
    """
    try:
        get_page(ticker)
        page_parsed = STOCK_PAGE[ticker]
        news_table = page_parsed.cssselect('table[id="news-table"]')

        if len(news_table) == 0:
            return []

        rows = news_table[0].xpath("./tr[not(@id)]")

        results = []
        current_date = None
        
        for row in rows:
            tds = row.xpath("./td")
            if len(tds) < 2:
                continue
                
            # 获取时间文本并清理
            time_text = tds[0].xpath("text()")[0] if tds[0].xpath("text()") else ""
            raw_timestamp = time_text.strip()
            
            # 解析时间格式
            try:
                if "Today" in raw_timestamp:
                    # 处理 "Today 06:00AM" 格式
                    time_part = raw_timestamp.replace("Today", "").strip()
                    parsed_timestamp = datetime.strptime(time_part, "%I:%M%p").replace(
                        year=datetime.now().year,
                        month=datetime.now().month,
                        day=datetime.now().day
                    )
                    current_date = parsed_timestamp.date()
                elif len(raw_timestamp) > 8 and "-" in raw_timestamp:
                    # 处理 "Dec-15-24 06:00AM" 格式
                    parsed_timestamp = datetime.strptime(raw_timestamp, "%b-%d-%y %I:%M%p")
                    current_date = parsed_timestamp.date()
                else:
                    # 处理 "06:00AM" 格式（使用当前日期）
                    if current_date is None:
                        current_date = datetime.now().date()
                    parsed_timestamp = datetime.strptime(raw_timestamp, "%I:%M%p").replace(
                        year=current_date.year,
                        month=current_date.month,
                        day=current_date.day
                    )
            except ValueError:
                # 如果时间解析失败，跳过这条新闻
                continue
            
            # 获取新闻信息
            news_link = tds[1].cssselect('a[class="tab-link-news"]')
            if not news_link:
                continue
                
            title = news_link[0].xpath("text()")[0] if news_link[0].xpath("text()") else ""
            url = news_link[0].get("href", "")
            
            # 获取来源信息
            source_span = tds[1].cssselect('div[class="news-link-right"] span')
            source = source_span[0].xpath("text()")[0][1:] if source_span and source_span[0].xpath("text()") else ""

            results.append((
                parsed_timestamp.strftime("%Y-%m-%d %H:%M"),
                title,
                url,
                source
            ))

        return results
    except Exception as e:
        return [("error", f"获取新闻失败: {str(e)}", "", "")]


def get_insider(ticker: str) -> List[Dict]:
    """
    获取内部交易信息
    
    Args:
        ticker: 股票代码，如 'AAPL'
        
    Returns:
        List[Dict]: 内部交易记录列表
        
    Example:
        >>> insider = get_insider('AAPL')
        >>> print(f"内部交易记录数: {len(insider)}")
    """
    try:
        get_page(ticker)
        page_parsed = STOCK_PAGE[ticker]
        outer_table = page_parsed.cssselect('table[class="body-table insider-trading-table"]')

        if len(outer_table) == 0:
            return []

        table = outer_table[0]
        headers = table[0].xpath("td//text()")

        data = [dict(zip(
            headers,
            [etree.tostring(elem, method="text", encoding="unicode") for elem in row]
        )) for row in table[1:]]

        return data
    except Exception as e:
        return [{"error": f"获取内部交易信息失败: {str(e)}"}]


def get_analyst_price_targets(ticker: str, last_ratings: int = 5) -> List[Dict]:
    """
    获取分析师价格目标
    
    Args:
        ticker: 股票代码，如 'AAPL'
        last_ratings: 获取最近几条评级，默认5条
        
    Returns:
        List[Dict]: 分析师评级列表
        
    Example:
        >>> targets = get_analyst_price_targets('AAPL', 3)
        >>> for target in targets:
        ...     print(f"{target['date']}: {target['rating']}")
    """
    try:
        analyst_price_targets = []

        get_page(ticker)
        page_parsed = STOCK_PAGE[ticker]
        table = page_parsed.cssselect(
            'table[class="js-table-ratings fullview-ratings-outer"]'
        )[0]

        for row in table:
            rating = row.xpath("td//text()")
            rating = [val.replace("→", "->").replace("$", "") for val in rating if val != "\n"]
            rating[0] = datetime.strptime(rating[0], "%b-%d-%y").strftime("%Y-%m-%d")

            data = {
                "date": rating[0],
                "category": rating[1],
                "analyst": rating[2],
                "rating": rating[3],
            }
            if len(rating) == 5:
                if "->" in rating[4]:
                    rating.extend(rating[4].replace(" ", "").split("->"))
                    del rating[4]
                    data["target_from"] = float(rating[4])
                    data["target_to"] = float(rating[5])
                else:
                    data["target"] = float(rating[4])

            analyst_price_targets.append(data)

        return analyst_price_targets[:last_ratings]
    except Exception as e:
        return [{"error": f"获取分析师评级失败: {str(e)}"}]


def get_all_news() -> List[Tuple[str, str, str]]:
    """
    获取所有新闻
    
    Returns:
        List[Tuple]: 所有新闻列表，每个元素包含 (日期, 标题, 链接)
        
    Example:
        >>> all_news = get_all_news()
        >>> print(f"总新闻数: {len(all_news)}")
    """
    try:
        page_parsed, _ = http_request_get(url=NEWS_URL, parse=True)
        all_dates = [
            row.text_content() for row in page_parsed.cssselect('td[class="nn-date"]')
        ]
        all_headlines = [
            row.text_content() for row in page_parsed.cssselect('a[class="nn-tab-link"]')
        ]
        all_links = [
            row.get("href") for row in page_parsed.cssselect('a[class="nn-tab-link"]')
        ]

        return list(zip(all_dates, all_headlines, all_links))
    except Exception as e:
        return [("error", f"获取所有新闻失败: {str(e)}", "")]


def get_crypto(pair: str) -> Dict:
    """
    获取加密货币数据
    
    Args:
        pair: 加密货币对，如 'BTC-USD'
        
    Returns:
        Dict: 加密货币数据
    """
    try:
        page_parsed, _ = http_request_get(url=CRYPTO_URL, parse=True)
        page_html, _ = http_request_get(url=CRYPTO_URL, parse=False)
        crypto_headers = page_parsed.cssselect('tr[valign="middle"]')[0].xpath("td//text()")
        crypto_table_data = get_table(page_html, crypto_headers)

        return crypto_table_data[pair]
    except Exception as e:
        return {"error": f"获取加密货币数据失败: {str(e)}"}

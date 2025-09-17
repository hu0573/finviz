"""
FinViz股票筛选服务

提供基于FinViz的股票筛选功能，支持多种筛选条件和表格类型。
"""

from typing import Dict, List, Optional, Union
from finviz.screener import Screener


class ScreenerService:
    """FinViz股票筛选服务类"""
    
    def get_screener_data(self, 
                         filters: Optional[List[str]] = None,
                         rows: Optional[int] = None,
                         order: str = "",
                         signal: str = "",
                         table: str = "Overview",
                         custom: Optional[List[str]] = None) -> Dict:
        """
        获取筛选器数据
        
        Args:
            filters: 筛选条件列表，如 ['idx_sp500', 'sec_technology']
            rows: 返回行数限制
            order: 排序方式，如 '-price' 表示按价格降序
            signal: 信号筛选，如 'n_majornews'
            table: 表格类型，可选值: Overview, Valuation, Ownership, Performance, Custom, Financial, Technical
            custom: 自定义列，如 ['1', '21', '23']
            
        Returns:
            Dict: 包含表头和数据行的字典
            
        Example:
            >>> service = ScreenerService()
            >>> result = service.get_screener_data(filters=['idx_sp500'], rows=10)
            >>> print(f"表头: {result['headers']}")
            >>> print(f"数据行数: {len(result['data'])}")
        """
        try:
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
    
    def get_screener_from_url(self, url: str, rows: Optional[int] = None) -> Dict:
        """
        从URL初始化筛选器
        
        Args:
            url: FinViz筛选器URL
            rows: 返回行数限制
            
        Returns:
            Dict: 包含表头和数据行的字典
            
        Example:
            >>> service = ScreenerService()
            >>> url = "https://finviz.com/screener.ashx?v=111&f=idx_sp500"
            >>> result = service.get_screener_from_url(url, rows=5)
            >>> print(f"从URL获取的数据行数: {len(result['data'])}")
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
    
    def get_filter_options(self) -> Dict:
        """
        获取可用的筛选器选项
        
        Returns:
            Dict: 筛选器选项字典，按类别组织
            
        Example:
            >>> service = ScreenerService()
            >>> filters = service.get_filter_options()
            >>> print(f"筛选器类别数: {len(filters)}")
            >>> print(f"行业选项: {list(filters.get('Industry', {}).keys())[:5]}")
        """
        try:
            return Screener.load_filter_dict()
        except Exception as e:
            return {"error": f"获取筛选器选项失败: {str(e)}"}
    
    def get_sp500_stocks(self, rows: int = 20) -> Dict:
        """
        获取S&P 500股票列表
        
        Args:
            rows: 返回行数限制，默认20
            
        Returns:
            Dict: S&P 500股票数据
            
        Example:
            >>> service = ScreenerService()
            >>> sp500 = service.get_sp500_stocks(10)
            >>> print(f"S&P 500股票数: {len(sp500['data'])}")
        """
        return self.get_screener_data(filters=['idx_sp500'], rows=rows)
    
    def get_technology_stocks(self, rows: int = 20) -> Dict:
        """
        获取科技股列表
        
        Args:
            rows: 返回行数限制，默认20
            
        Returns:
            Dict: 科技股数据
            
        Example:
            >>> service = ScreenerService()
            >>> tech = service.get_technology_stocks(10)
            >>> print(f"科技股数: {len(tech['data'])}")
        """
        return self.get_screener_data(filters=['sec_technology'], rows=rows)
    
    def get_high_volume_stocks(self, rows: int = 20) -> Dict:
        """
        获取高成交量股票列表
        
        Args:
            rows: 返回行数限制，默认20
            
        Returns:
            Dict: 高成交量股票数据
            
        Example:
            >>> service = ScreenerService()
            >>> high_vol = service.get_high_volume_stocks(10)
            >>> print(f"高成交量股票数: {len(high_vol['data'])}")
        """
        return self.get_screener_data(filters=['sh_avgvol_o500'], rows=rows, order='-volume')
    
    def get_oversold_stocks(self, rows: int = 20) -> Dict:
        """
        获取超卖股票列表（RSI < 30）
        
        Args:
            rows: 返回行数限制，默认20
            
        Returns:
            Dict: 超卖股票数据
            
        Example:
            >>> service = ScreenerService()
            >>> oversold = service.get_oversold_stocks(10)
            >>> print(f"超卖股票数: {len(oversold['data'])}")
        """
        return self.get_screener_data(filters=['ta_rsi_os30'], rows=rows)
    
    def get_overbought_stocks(self, rows: int = 20) -> Dict:
        """
        获取超买股票列表（RSI > 70）
        
        Args:
            rows: 返回行数限制，默认20
            
        Returns:
            Dict: 超买股票数据
            
        Example:
            >>> service = ScreenerService()
            >>> overbought = service.get_overbought_stocks(10)
            >>> print(f"超买股票数: {len(overbought['data'])}")
        """
        return self.get_screener_data(filters=['ta_rsi_ob70'], rows=rows)

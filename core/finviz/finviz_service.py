"""
FinViz服务门面类

统一封装FinViz的所有功能，包括股票数据获取和股票筛选。
"""

from typing import Dict, List, Optional, Tuple, Union
from .stock_data_service import StockDataService
from .screener_service import ScreenerService


class FinVizService:
    """FinViz服务门面类，统一暴露所有FinViz功能"""
    
    def __init__(self):
        """初始化服务"""
        self.stock_data_service = StockDataService()
        self.screener_service = ScreenerService()
    
    # ==================== 股票数据获取功能 ====================
    
    def get_stock(self, ticker: str) -> Dict:
        """
        获取股票详细信息
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            Dict: 包含股票详细信息的字典，包括价格、市值、财务数据等
        """
        return self.stock_data_service.get_stock(ticker)
    
    def get_news(self, ticker: str) -> List[Tuple[str, str, str, str]]:
        """
        获取股票相关新闻
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            List[Tuple]: 新闻列表，每个元素包含 (时间, 标题, 链接, 来源)
        """
        return self.stock_data_service.get_news(ticker)
    
    def get_insider(self, ticker: str) -> List[Dict]:
        """
        获取内部交易信息
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            List[Dict]: 内部交易记录列表
        """
        return self.stock_data_service.get_insider(ticker)
    
    def get_analyst_price_targets(self, ticker: str, last_ratings: int = 5) -> List[Dict]:
        """
        获取分析师价格目标
        
        Args:
            ticker: 股票代码，如 'AAPL'
            last_ratings: 获取最近几条评级，默认5条
            
        Returns:
            List[Dict]: 分析师评级列表
        """
        return self.stock_data_service.get_analyst_price_targets(ticker, last_ratings)
    
    def get_all_news(self) -> List[Tuple[str, str, str]]:
        """
        获取所有新闻
        
        Returns:
            List[Tuple]: 所有新闻列表，每个元素包含 (日期, 标题, 链接)
        """
        return self.stock_data_service.get_all_news()
    
    # ==================== 股票筛选功能 ====================
    
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
        """
        return self.screener_service.get_screener_data(filters, rows, order, signal, table, custom)
    
    def get_screener_from_url(self, url: str, rows: Optional[int] = None) -> Dict:
        """
        从URL初始化筛选器
        
        Args:
            url: FinViz筛选器URL
            rows: 返回行数限制
            
        Returns:
            Dict: 包含表头和数据行的字典
        """
        return self.screener_service.get_screener_from_url(url, rows)
    
    def get_filter_options(self) -> Dict:
        """
        获取可用的筛选器选项
        
        Returns:
            Dict: 筛选器选项字典，按类别组织
        """
        return self.screener_service.get_filter_options()
    
    # ==================== 便捷筛选方法 ====================
    
    def get_sp500_stocks(self, rows: int = 20) -> Dict:
        """
        获取S&P 500股票列表
        
        Args:
            rows: 返回行数限制，默认20
            
        Returns:
            Dict: S&P 500股票数据
        """
        return self.screener_service.get_sp500_stocks(rows)
    
    def get_technology_stocks(self, rows: int = 20) -> Dict:
        """
        获取科技股列表
        
        Args:
            rows: 返回行数限制，默认20
            
        Returns:
            Dict: 科技股数据
        """
        return self.screener_service.get_technology_stocks(rows)
    
    def get_high_volume_stocks(self, rows: int = 20) -> Dict:
        """
        获取高成交量股票列表
        
        Args:
            rows: 返回行数限制，默认20
            
        Returns:
            Dict: 高成交量股票数据
        """
        return self.screener_service.get_high_volume_stocks(rows)
    
    def get_oversold_stocks(self, rows: int = 20) -> Dict:
        """
        获取超卖股票列表（RSI < 30）
        
        Args:
            rows: 返回行数限制，默认20
            
        Returns:
            Dict: 超卖股票数据
        """
        return self.screener_service.get_oversold_stocks(rows)
    
    def get_overbought_stocks(self, rows: int = 20) -> Dict:
        """
        获取超买股票列表（RSI > 70）
        
        Args:
            rows: 返回行数限制，默认20
            
        Returns:
            Dict: 超买股票数据
        """
        return self.screener_service.get_overbought_stocks(rows)
    
    # ==================== 组合功能方法 ====================
    
    def get_stock_with_news(self, ticker: str) -> Dict:
        """
        获取股票信息和相关新闻
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            Dict: 包含股票信息和新闻的字典
        """
        stock_data = self.get_stock(ticker)
        news_data = self.get_news(ticker)
        
        return {
            "stock": stock_data,
            "news": news_data,
            "news_count": len(news_data)
        }
    
    def get_stock_analysis(self, ticker: str) -> Dict:
        """
        获取股票完整分析信息
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            Dict: 包含股票信息、新闻、内部交易和分析师评级的字典
        """
        stock_data = self.get_stock(ticker)
        news_data = self.get_news(ticker)
        insider_data = self.get_insider(ticker)
        analyst_data = self.get_analyst_price_targets(ticker)
        
        return {
            "stock": stock_data,
            "news": news_data,
            "insider_trading": insider_data,
            "analyst_ratings": analyst_data,
            "summary": {
                "news_count": len(news_data),
                "insider_count": len(insider_data),
                "analyst_count": len(analyst_data)
            }
        }

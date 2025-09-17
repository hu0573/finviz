"""
FinViz股票数据服务

提供基于FinViz的股票数据获取功能，包括股票基本信息、新闻、内部交易等。
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import finviz.main_func as main_func


class StockDataService:
    """FinViz股票数据服务类"""
    
    def get_stock(self, ticker: str) -> Dict:
        """
        获取股票详细信息
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            Dict: 包含股票详细信息的字典，包括价格、市值、财务数据等
            
        Example:
            >>> service = StockDataService()
            >>> data = service.get_stock('AAPL')
            >>> print(data['Price'])  # 当前价格
        """
        try:
            return main_func.get_stock(ticker)
        except Exception as e:
            return {"error": f"获取股票数据失败: {str(e)}"}
    
    def get_news(self, ticker: str) -> List[Tuple[str, str, str, str]]:
        """
        获取股票相关新闻
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            List[Tuple]: 新闻列表，每个元素包含 (时间, 标题, 链接, 来源)
            
        Example:
            >>> service = StockDataService()
            >>> news = service.get_news('AAPL')
            >>> for time, title, url, source in news[:3]:
            ...     print(f"{time}: {title}")
        """
        try:
            return main_func.get_news(ticker)
        except Exception as e:
            return [("error", f"获取新闻失败: {str(e)}", "", "")]
    
    def get_insider(self, ticker: str) -> List[Dict]:
        """
        获取内部交易信息
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            List[Dict]: 内部交易记录列表
            
        Example:
            >>> service = StockDataService()
            >>> insider = service.get_insider('AAPL')
            >>> print(f"内部交易记录数: {len(insider)}")
        """
        try:
            return main_func.get_insider(ticker)
        except Exception as e:
            return [{"error": f"获取内部交易信息失败: {str(e)}"}]
    
    def get_analyst_price_targets(self, ticker: str, last_ratings: int = 5) -> List[Dict]:
        """
        获取分析师价格目标
        
        Args:
            ticker: 股票代码，如 'AAPL'
            last_ratings: 获取最近几条评级，默认5条
            
        Returns:
            List[Dict]: 分析师评级列表
            
        Example:
            >>> service = StockDataService()
            >>> targets = service.get_analyst_price_targets('AAPL', 3)
            >>> for target in targets:
            ...     print(f"{target['date']}: {target['rating']}")
        """
        try:
            return main_func.get_analyst_price_targets(ticker, last_ratings)
        except Exception as e:
            return [{"error": f"获取分析师评级失败: {str(e)}"}]
    
    def get_all_news(self) -> List[Tuple[str, str, str]]:
        """
        获取所有新闻
        
        Returns:
            List[Tuple]: 所有新闻列表，每个元素包含 (日期, 标题, 链接)
            
        Example:
            >>> service = StockDataService()
            >>> all_news = service.get_all_news()
            >>> print(f"总新闻数: {len(all_news)}")
        """
        try:
            return main_func.get_all_news()
        except Exception as e:
            return [("error", f"获取所有新闻失败: {str(e)}", "")]

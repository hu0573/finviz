#!/usr/bin/env python3
"""
MCP集成示例

展示如何在MCP项目中集成FinViz服务。
"""

from typing import Dict, List, Optional
from core.finviz import FinVizService


class StockService:
    """MCP主服务类示例"""
    
    def __init__(self):
        """初始化所有服务"""
        # 初始化FinViz服务
        self.finviz_service = FinVizService()
        
        # 这里还可以初始化其他服务
        # self.yfinance_service = YFinanceService()
        # self.tiger_service = TigerService()
    
    # ==================== FinViz股票数据方法 ====================
    
    def get_finviz_stock(self, ticker: str) -> Dict:
        """
        获取FinViz股票数据
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            Dict: 股票详细信息
        """
        return self.finviz_service.get_stock(ticker)
    
    def get_finviz_news(self, ticker: str) -> List:
        """
        获取FinViz股票新闻
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            List: 新闻列表
        """
        return self.finviz_service.get_news(ticker)
    
    def get_finviz_insider(self, ticker: str) -> List:
        """
        获取FinViz内部交易信息
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            List: 内部交易记录
        """
        return self.finviz_service.get_insider(ticker)
    
    def get_finviz_analyst_ratings(self, ticker: str, last_ratings: int = 5) -> List:
        """
        获取FinViz分析师评级
        
        Args:
            ticker: 股票代码，如 'AAPL'
            last_ratings: 获取最近几条评级
            
        Returns:
            List: 分析师评级列表
        """
        return self.finviz_service.get_analyst_price_targets(ticker, last_ratings)
    
    # ==================== FinViz筛选器方法 ====================
    
    def get_finviz_screener(self, 
                           filters: Optional[List[str]] = None,
                           rows: int = 20,
                           order: str = "",
                           table: str = "Overview") -> Dict:
        """
        获取FinViz筛选器数据
        
        Args:
            filters: 筛选条件列表
            rows: 返回行数
            order: 排序方式
            table: 表格类型
            
        Returns:
            Dict: 筛选器数据
        """
        return self.finviz_service.get_screener_data(
            filters=filters,
            rows=rows,
            order=order,
            table=table
        )
    
    def get_finviz_sp500(self, rows: int = 20) -> Dict:
        """
        获取S&P 500股票列表
        
        Args:
            rows: 返回行数
            
        Returns:
            Dict: S&P 500股票数据
        """
        return self.finviz_service.get_sp500_stocks(rows)
    
    def get_finviz_tech_stocks(self, rows: int = 20) -> Dict:
        """
        获取科技股列表
        
        Args:
            rows: 返回行数
            
        Returns:
            Dict: 科技股数据
        """
        return self.finviz_service.get_technology_stocks(rows)
    
    def get_finviz_filter_options(self) -> Dict:
        """
        获取FinViz筛选器选项
        
        Returns:
            Dict: 筛选器选项
        """
        return self.finviz_service.get_filter_options()
    
    # ==================== 组合功能方法 ====================
    
    def get_finviz_stock_analysis(self, ticker: str) -> Dict:
        """
        获取FinViz股票完整分析
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            Dict: 包含股票信息、新闻、内部交易和分析师评级的完整分析
        """
        return self.finviz_service.get_stock_analysis(ticker)
    
    def get_finviz_stock_with_news(self, ticker: str) -> Dict:
        """
        获取FinViz股票信息和新闻
        
        Args:
            ticker: 股票代码，如 'AAPL'
            
        Returns:
            Dict: 包含股票信息和新闻的字典
        """
        return self.finviz_service.get_stock_with_news(ticker)


def test_mcp_integration():
    """测试MCP集成"""
    print("=== 测试MCP集成示例 ===\n")
    
    # 初始化主服务
    stock_service = StockService()
    
    # 测试股票数据获取
    print("1. 测试股票数据获取:")
    stock_data = stock_service.get_finviz_stock('AAPL')
    if 'error' not in stock_data:
        print(f"   ✅ 成功获取苹果股票数据")
        print(f"   价格: ${stock_data.get('Price', 'N/A')}")
        print(f"   市值: {stock_data.get('Market Cap', 'N/A')}")
    else:
        print(f"   ❌ 错误: {stock_data['error']}")
    
    print()
    
    # 测试筛选器功能
    print("2. 测试筛选器功能:")
    sp500_data = stock_service.get_finviz_sp500(5)
    if 'error' not in sp500_data:
        print(f"   ✅ 成功获取S&P 500数据")
        print(f"   股票数: {len(sp500_data['data'])}")
    else:
        print(f"   ❌ 错误: {sp500_data['error']}")
    
    print()
    
    # 测试组合功能
    print("3. 测试组合功能:")
    analysis = stock_service.get_finviz_stock_analysis('AAPL')
    if 'stock' in analysis and 'error' not in analysis['stock']:
        print(f"   ✅ 成功获取完整分析")
        print(f"   新闻数: {analysis['summary']['news_count']}")
    else:
        print(f"   ❌ 错误: 无法获取完整分析")
    
    print("\n=== MCP集成测试完成 ===")


if __name__ == "__main__":
    test_mcp_integration()

#!/usr/bin/env python3
"""
测试新的MCP架构结构

验证FinViz服务在新架构下的功能是否正常。
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.finviz import FinVizService


def test_finviz_service():
    """测试FinViz服务功能"""
    print("=== 测试FinViz服务新架构 ===\n")
    
    # 初始化服务
    service = FinVizService()
    
    # 测试股票数据获取
    print("1. 测试股票数据获取:")
    try:
        stock_data = service.get_stock('AAPL')
        if 'error' not in stock_data:
            print(f"   ✅ 成功获取苹果股票数据")
            print(f"   公司: {stock_data.get('Company', 'N/A')}")
            print(f"   价格: ${stock_data.get('Price', 'N/A')}")
            print(f"   市值: {stock_data.get('Market Cap', 'N/A')}")
        else:
            print(f"   ❌ 错误: {stock_data['error']}")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    print()
    
    # 测试新闻获取
    print("2. 测试新闻获取:")
    try:
        news_data = service.get_news('AAPL')
        if news_data and 'error' not in news_data[0]:
            print(f"   ✅ 成功获取 {len(news_data)} 条新闻")
            print(f"   最新新闻: {news_data[0][1][:50]}...")
        else:
            print(f"   ❌ 错误: {news_data[0][1] if news_data else '无数据'}")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    print()
    
    # 测试筛选器功能
    print("3. 测试筛选器功能:")
    try:
        screener_data = service.get_sp500_stocks(5)
        if 'error' not in screener_data:
            print(f"   ✅ 成功获取S&P 500股票数据")
            print(f"   表头: {screener_data['headers']}")
            print(f"   数据行数: {len(screener_data['data'])}")
            if screener_data['data']:
                first_stock = screener_data['data'][0]
                print(f"   第一只股票: {first_stock.get('Ticker', 'N/A')} - {first_stock.get('Company', 'N/A')}")
        else:
            print(f"   ❌ 错误: {screener_data['error']}")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    print()
    
    # 测试筛选器选项
    print("4. 测试筛选器选项:")
    try:
        filter_options = service.get_filter_options()
        if 'error' not in filter_options:
            print(f"   ✅ 成功获取筛选器选项")
            print(f"   筛选器类别数: {len(filter_options)}")
            print(f"   主要类别: {list(filter_options.keys())[:5]}")
        else:
            print(f"   ❌ 错误: {filter_options['error']}")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    print()
    
    # 测试组合功能
    print("5. 测试组合功能:")
    try:
        analysis = service.get_stock_analysis('AAPL')
        if 'stock' in analysis and 'error' not in analysis['stock']:
            print(f"   ✅ 成功获取股票完整分析")
            print(f"   新闻数: {analysis['summary']['news_count']}")
            print(f"   内部交易数: {analysis['summary']['insider_count']}")
            print(f"   分析师评级数: {analysis['summary']['analyst_count']}")
        else:
            print(f"   ❌ 错误: 无法获取完整分析")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_finviz_service()

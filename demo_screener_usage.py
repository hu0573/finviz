#!/usr/bin/env python3
"""
FinViz筛选器使用演示脚本

展示如何使用FinViz筛选器进行各种股票筛选
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.finviz import FinVizService


def demo_basic_usage():
    """演示基本使用方法"""
    print("=== FinViz筛选器基本使用演示 ===\n")
    
    service = FinVizService()
    
    # 1. 获取S&P 500股票
    print("1. 获取S&P 500股票:")
    result = service.get_screener_data(filters=['idx_sp500'], rows=5)
    if 'error' not in result:
        print(f"   找到 {result['total_rows']} 只S&P 500股票")
        for i, stock in enumerate(result['data'][:3], 1):
            print(f"   {i}. {stock.get('Ticker', 'N/A')} - {stock.get('Company', 'N/A')}")
    else:
        print(f"   错误: {result['error']}")
    
    print()


def demo_value_investing():
    """演示价值投资筛选"""
    print("=== 价值投资筛选演示 ===\n")
    
    service = FinVizService()
    
    # 寻找低估值、高股息的大盘股
    filters = [
        'idx_sp500',           # S&P 500
        'cap_large',           # 大型股
        'fa_pe_low',           # 低市盈率
        'fa_div_high',         # 高股息收益率
        'fa_pb_u3'             # 市净率低于3
    ]
    
    print("筛选条件: S&P 500 + 大型股 + 低市盈率 + 高股息 + 低市净率")
    result = service.get_screener_data(
        filters=filters,
        table='Valuation',
        order='-dividend',     # 按股息收益率降序
        rows=5
    )
    
    if 'error' not in result and result['total_rows'] > 0:
        print(f"找到 {result['total_rows']} 只价值股:")
        for i, stock in enumerate(result['data'], 1):
            ticker = stock.get('Ticker', 'N/A')
            company = stock.get('Company', 'N/A')
            pe = stock.get('P/E', 'N/A')
            dividend = stock.get('Dividend', 'N/A')
            pb = stock.get('P/B', 'N/A')
            print(f"   {i}. {ticker} - {company}")
            print(f"      市盈率: {pe}, 股息: {dividend}, 市净率: {pb}")
    else:
        print(f"未找到符合条件的价值股: {result.get('error', '无数据')}")
    
    print()


def demo_growth_stocks():
    """演示成长股筛选"""
    print("=== 成长股筛选演示 ===\n")
    
    service = FinVizService()
    
    # 寻找科技成长股
    filters = [
        'sec_technology',      # 科技板块
        'cap_mid',             # 中型股
        'fa_pe_u25',           # 市盈率低于25
        'fa_peg_u2',           # PEG比率低于2
        'fa_div_none',         # 不分红（成长股特征）
        'sh_avgvol_o500'       # 平均成交量超过50万股
    ]
    
    print("筛选条件: 科技板块 + 中型股 + 合理估值 + 高流动性")
    result = service.get_screener_data(
        filters=filters,
        table='Financial',
        order='-market_cap',   # 按市值降序
        rows=5
    )
    
    if 'error' not in result and result['total_rows'] > 0:
        print(f"找到 {result['total_rows']} 只成长股:")
        for i, stock in enumerate(result['data'], 1):
            ticker = stock.get('Ticker', 'N/A')
            company = stock.get('Company', 'N/A')
            pe = stock.get('P/E', 'N/A')
            peg = stock.get('PEG', 'N/A')
            market_cap = stock.get('Market Cap', 'N/A')
            print(f"   {i}. {ticker} - {company}")
            print(f"      市盈率: {pe}, PEG: {peg}, 市值: {market_cap}")
    else:
        print(f"未找到符合条件的成长股: {result.get('error', '无数据')}")
    
    print()


def demo_technical_analysis():
    """演示技术分析筛选"""
    print("=== 技术分析筛选演示 ===\n")
    
    service = FinVizService()
    
    # 寻找技术面强势的股票
    filters = [
        'ta_rsi_oversold',     # RSI超卖
        'ta_ma_sma50',         # 价格高于50日移动平均线
        'ta_highlow52w_b0to10h', # 距离52周高点0-10%
        'sh_avgvol_o1000'      # 平均成交量超过100万股
    ]
    
    print("筛选条件: RSI超卖 + 价格高于50日均线 + 接近52周高点 + 高成交量")
    result = service.get_screener_data(
        filters=filters,
        table='Technical',
        order='-change',       # 按涨跌幅降序
        rows=5
    )
    
    if 'error' not in result and result['total_rows'] > 0:
        print(f"找到 {result['total_rows']} 只技术面强势股票:")
        for i, stock in enumerate(result['data'], 1):
            ticker = stock.get('Ticker', 'N/A')
            company = stock.get('Company', 'N/A')
            price = stock.get('Price', 'N/A')
            change = stock.get('Change', 'N/A')
            rsi = stock.get('RSI (14)', 'N/A')
            print(f"   {i}. {ticker} - {company}")
            print(f"      价格: {price}, 涨跌幅: {change}, RSI: {rsi}")
    else:
        print(f"未找到符合技术条件的股票: {result.get('error', '无数据')}")
    
    print()


def demo_signal_screening():
    """演示信号筛选"""
    print("=== 信号筛选演示 ===\n")
    
    service = FinVizService()
    
    # 获取涨幅榜股票
    print("1. 涨幅榜股票:")
    result = service.get_screener_data(filters=['signal_tpgainers'], rows=5)
    if 'error' not in result and result['total_rows'] > 0:
        print(f"   找到 {result['total_rows']} 只涨幅榜股票:")
        for i, stock in enumerate(result['data'][:3], 1):
            ticker = stock.get('Ticker', 'N/A')
            company = stock.get('Company', 'N/A')
            change = stock.get('Change', 'N/A')
            print(f"   {i}. {ticker} - {company} ({change})")
    else:
        print(f"   错误: {result.get('error', '无数据')}")
    
    print()
    
    # 获取新高股票
    print("2. 创新高股票:")
    result = service.get_screener_data(filters=['signal_newhigh'], rows=5)
    if 'error' not in result and result['total_rows'] > 0:
        print(f"   找到 {result['total_rows']} 只创新高股票:")
        for i, stock in enumerate(result['data'][:3], 1):
            ticker = stock.get('Ticker', 'N/A')
            company = stock.get('Company', 'N/A')
            price = stock.get('Price', 'N/A')
            print(f"   {i}. {ticker} - {company} (${price})")
    else:
        print(f"   错误: {result.get('error', '无数据')}")
    
    print()


def demo_table_types():
    """演示不同表格类型"""
    print("=== 表格类型演示 ===\n")
    
    service = FinVizService()
    
    table_types = [
        ('Overview', '概览'),
        ('Valuation', '估值'),
        ('Financial', '财务'),
        ('Technical', '技术')
    ]
    
    for table_type, description in table_types:
        print(f"{description}表格 ({table_type}):")
        result = service.get_screener_data(
            filters=['idx_sp500'], 
            table=table_type, 
            rows=3
        )
        
        if 'error' not in result and result['total_rows'] > 0:
            print(f"   表头: {result['headers'][:5]}...")  # 显示前5个表头
            print(f"   数据行数: {result['total_rows']}")
        else:
            print(f"   错误: {result.get('error', '无数据')}")
        print()


def demo_ordering():
    """演示排序功能"""
    print("=== 排序功能演示 ===\n")
    
    service = FinVizService()
    
    # 按市值降序排列
    print("1. 按市值降序排列:")
    result = service.get_screener_data(
        filters=['idx_sp500'],
        order='-market_cap',
        rows=5
    )
    
    if 'error' not in result and result['total_rows'] > 0:
        print(f"   找到 {result['total_rows']} 只股票:")
        for i, stock in enumerate(result['data'][:3], 1):
            ticker = stock.get('Ticker', 'N/A')
            company = stock.get('Company', 'N/A')
            market_cap = stock.get('Market Cap', 'N/A')
            print(f"   {i}. {ticker} - {company} (市值: {market_cap})")
    else:
        print(f"   错误: {result.get('error', '无数据')}")
    
    print()
    
    # 按价格升序排列
    print("2. 按价格升序排列:")
    result = service.get_screener_data(
        filters=['idx_sp500'],
        order='price',
        rows=5
    )
    
    if 'error' not in result and result['total_rows'] > 0:
        print(f"   找到 {result['total_rows']} 只股票:")
        for i, stock in enumerate(result['data'][:3], 1):
            ticker = stock.get('Ticker', 'N/A')
            company = stock.get('Company', 'N/A')
            price = stock.get('Price', 'N/A')
            print(f"   {i}. {ticker} - {company} (价格: ${price})")
    else:
        print(f"   错误: {result.get('error', '无数据')}")
    
    print()


def demo_url_functionality():
    """演示URL功能"""
    print("=== URL功能演示 ===\n")
    
    service = FinVizService()
    
    # 从FinViz URL获取数据
    url = "https://finviz.com/screener.ashx?v=111&f=idx_sp500,cap_large&o=-market_cap"
    print(f"从URL获取数据: {url}")
    
    result = service.get_screener_from_url(url, rows=5)
    if 'error' not in result and result['total_rows'] > 0:
        print(f"   成功获取 {result['total_rows']} 只股票:")
        for i, stock in enumerate(result['data'][:3], 1):
            ticker = stock.get('Ticker', 'N/A')
            company = stock.get('Company', 'N/A')
            market_cap = stock.get('Market Cap', 'N/A')
            print(f"   {i}. {ticker} - {company} (市值: {market_cap})")
    else:
        print(f"   错误: {result.get('error', '无数据')}")
    
    print()


def demo_filter_options():
    """演示筛选器选项获取"""
    print("=== 筛选器选项演示 ===\n")
    
    service = FinVizService()
    
    # 获取所有筛选器选项
    filter_options = service.get_filter_options()
    if 'error' not in filter_options:
        print(f"获取到 {len(filter_options)} 个筛选器类别:")
        
        # 显示主要类别
        main_categories = [
            'Exchange', 'Index', 'Sector', 'Industry', 'Market Cap',
            'Price', 'P/E', 'P/B', 'P/S', 'Dividend', 'RSI (14)',
            'SMA20', 'SMA50', 'SMA200', 'Signal'
        ]
        
        for category in main_categories:
            if category in filter_options:
                options_count = len(filter_options[category])
                print(f"   {category}: {options_count} 个选项")
        
        print(f"\n   其他类别: {len(filter_options) - len(main_categories)} 个")
    else:
        print(f"错误: {filter_options['error']}")
    
    print()


def main():
    """主函数"""
    print("FinViz筛选器使用演示")
    print("=" * 50)
    print()
    
    try:
        # 运行各种演示
        demo_basic_usage()
        demo_value_investing()
        demo_growth_stocks()
        demo_technical_analysis()
        demo_signal_screening()
        demo_table_types()
        demo_ordering()
        demo_url_functionality()
        demo_filter_options()
        
        print("=" * 50)
        print("演示完成！")
        print("\n更多使用方法请参考 screener_guide.md 文档")
        
    except Exception as e:
        print(f"演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
测试网页筛选器设置

验证用户在FinViz网页上设置的筛选条件
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.finviz.screener import get_screener_data


def test_web_filter():
    """测试网页筛选器设置"""
    print("🔍 测试网页筛选器设置")
    print("=" * 50)
    
    # 从网页获取的筛选器
    web_filters = ['ta_beta_o0', 'ta_highlow50d_a20h', 'ta_highlow52w_b5h', 'ta_sma20_pb20', 'ta_sma200_pb70']
    
    print(f"筛选器: {', '.join(web_filters)}")
    print("预期结果: 8条数据")
    print("筛选条件:")
    print("  - Beta: Over 0")
    print("  - 50-Day High/Low: 20% or more above Low")
    print("  - 52-Week High/Low: 5% or more below High")
    print("  - 20-Day SMA: Price 20% below SMA20")
    print("  - 200-Day SMA: Price 70% below SMA200")
    print()
    
    try:
        # 执行筛选
        result = get_screener_data(
            filters=web_filters,
            rows=10,
            auto_table=True
        )
        
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
            return
        
        total_rows = result.get('total_rows', 0)
        data = result.get('data', [])
        headers = result.get('headers', [])
        
        print(f"✅ 成功获取数据")
        print(f"   总行数: {total_rows}")
        print(f"   表头: {', '.join(headers)}")
        print()
        
        if data:
            print("📊 筛选结果:")
            for i, stock in enumerate(data, 1):
                ticker = stock.get('Ticker', 'N/A')
                company = stock.get('Company', 'N/A')
                sector = stock.get('Sector', 'N/A')
                industry = stock.get('Industry', 'N/A')
                country = stock.get('Country', 'N/A')
                market_cap = stock.get('Market Cap', 'N/A')
                pe = stock.get('P/E', 'N/A')
                price = stock.get('Price', 'N/A')
                change = stock.get('Change', 'N/A')
                volume = stock.get('Volume', 'N/A')
                
                print(f"   {i}. {ticker} - {company}")
                print(f"      板块: {sector} | 行业: {industry} | 国家: {country}")
                print(f"      市值: {market_cap} | 市盈率: {pe} | 价格: {price}")
                print(f"      涨跌幅: {change} | 成交量: {volume}")
                print()
        else:
            print("❌ 没有找到数据")
        
        # 验证是否与网页结果一致
        expected_tickers = ['AEMD', 'BGMS', 'CDT', 'NAKA', 'NVVE', 'SDST', 'TNFA', 'YYGH']
        actual_tickers = [stock.get('Ticker') for stock in data if stock.get('Ticker')]
        
        if total_rows == 8:
            print("✅ 验证成功: 数据行数与网页一致")
            print(f"   网页股票: {', '.join(expected_tickers)}")
            print(f"   API股票: {', '.join(actual_tickers)}")
            
            # 检查股票代码匹配度
            matched = set(expected_tickers) & set(actual_tickers)
            if len(matched) >= 6:  # 至少匹配6个
                print(f"✅ 股票匹配度: {len(matched)}/8 ({len(matched)/8*100:.1f}%)")
            else:
                print(f"⚠️  股票匹配度较低: {len(matched)}/8 ({len(matched)/8*100:.1f}%)")
        elif total_rows == 0:
            print("❌ 验证失败: 没有返回数据")
        else:
            print(f"⚠️  验证失败: 数据行数不匹配 (期望: 8, 实际: {total_rows})")
            
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()


def test_individual_filters():
    """测试单个筛选器"""
    print("\n🔍 测试单个筛选器")
    print("=" * 50)
    
    filters_to_test = [
        ('ta_beta_o0', 'Beta: Over 0'),
        ('ta_highlow50d_a20h', '50-Day High/Low: 20% or more above Low'),
        ('ta_highlow52w_b5h', '52-Week High/Low: 5% or more below High'),
        ('ta_sma20_pb20', '20-Day SMA: Price 20% below SMA20'),
        ('ta_sma200_pb70', '200-Day SMA: Price 70% below SMA200')
    ]
    
    for filter_code, description in filters_to_test:
        print(f"\n测试: {description}")
        print(f"筛选器代码: {filter_code}")
        
        try:
            result = get_screener_data(
                filters=[filter_code],
                rows=5,
                auto_table=True
            )
            
            if 'error' in result:
                print(f"   ❌ 错误: {result['error']}")
            else:
                total_rows = result.get('total_rows', 0)
                print(f"   ✅ 成功: 找到 {total_rows} 只股票")
                
                if result.get('data'):
                    sample = result['data'][0]
                    print(f"      示例: {sample.get('Ticker', 'N/A')} - {sample.get('Company', 'N/A')}")
                    
        except Exception as e:
            print(f"   ❌ 异常: {e}")


def main():
    """主函数"""
    print("FinViz网页筛选器验证测试")
    print("=" * 60)
    
    # 测试网页筛选器组合
    test_web_filter()
    
    # 测试单个筛选器
    test_individual_filters()
    
    print("\n" + "=" * 60)
    print("测试完成")


if __name__ == "__main__":
    main()

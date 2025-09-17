#!/usr/bin/env python3
"""
FinViz 筛选器自动测试脚本

此脚本用于自动测试所有筛选器，无需用户交互。
每个筛选器随机选择一个选项进行测试。
"""

import sys
import os
import json
import random
import time
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.finviz.screener import get_screener_data


def load_filters():
    """加载筛选器配置"""
    filters_file = project_root / "core" / "finviz" / "filters.json"
    try:
        with open(filters_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载筛选器配置失败: {e}")
        return {}


def get_random_option(filter_options):
    """从筛选器选项中随机选择一个"""
    # 过滤掉空值和"Any"选项
    valid_options = {k: v for k, v in filter_options.items() 
                   if v and k != "Any" and v != ""}
    
    if not valid_options:
        return None, None
    
    option_name, option_value = random.choice(list(valid_options.items()))
    return option_name, option_value


def generate_filter_code(filter_name, option_value):
    """生成筛选器代码"""
    # 简化的筛选器代码映射
    filter_mapping = {
        "Exchange": "exch",
        "Index": "idx", 
        "Sector": "sec",
        "Industry": "ind",
        "Country": "geo",
        "Market Cap.": "cap",
        "P/E": "fa_pe",
        "Forward P/E": "fa_fpe",
        "PEG": "fa_peg",
        "P/S": "fa_ps",
        "P/B": "fa_pb",
        "Price/Cash": "fa_pc",
        "Price/Free Cash Flow": "fa_pfcf",
        "EV/EBITDA": "fa_ev",
        "EV/Sales": "fa_evs",
        "Dividend Growth": "fa_div",
        "EPS GrowthThis Year": "fa_epsyoy",
        "EPS GrowthNext Year": "fa_epsyoy1",
        "EPS GrowthQtr Over Qtr": "fa_epsqoq",
        "EPS Growth TTM": "fa_epsttm",
        "EPS GrowthPast 3 Years": "fa_eps3y",
        "EPS GrowthPast 5 Years": "fa_eps5y",
        "EPS GrowthNext 5 Years": "fa_eps5y1",
        "Sales GrowthQtr Over Qtr": "fa_salesqoq",
        "Sales Growth TTM": "fa_salesttm",
        "Sales GrowthPast 3 Years": "fa_sales3y",
        "Sales GrowthPast 5 Years": "fa_sales5y",
        "Earnings & Revenue Surprise": "fa_earnings",
        "Dividend Yield": "fa_divyield",
        "Return on Assets": "fa_roa",
        "Return on Equity": "fa_roe",
        "Return on Invested Capital": "fa_roic",
        "Current Ratio": "fa_curratio",
        "Quick Ratio": "fa_quickratio",
        "LT Debt/Equity": "fa_ltdebteq",
        "Debt/Equity": "fa_debteq",
        "Gross Margin": "fa_grossm",
        "Operating Margin": "fa_operm",
        "Net Profit Margin": "fa_netm",
        "Payout Ratio": "fa_payout",
        "InsiderOwnership": "sh_insiderown",
        "InsiderTransactions": "sh_insidertrans",
        "InstitutionalOwnership": "sh_instown",
        "InstitutionalTransactions": "sh_insttrans",
        "Short Float": "sh_short",
        "Analyst Recom.": "an_recom",
        "Option/Short": "sh_option",
        "Earnings Date": "earningsdate",
        "Performance": "ta_perf",
        "Performance 2": "ta_perf2",
        "Volatility": "ta_volatility",
        "RSI (14)": "ta_rsi",
        "Gap": "ta_gap",
        "20-Day Simple Moving Average": "ta_sma20",
        "50-Day Simple Moving Average": "ta_sma50",
        "200-Day Simple Moving Average": "ta_sma200",
        "Change": "ta_change",
        "Change from Open": "ta_changeopen",
        "20-Day High/Low": "ta_highlow20",
        "50-Day High/Low": "ta_highlow50",
        "52-Week High/Low": "ta_highlow52w",
        "All-Time High/Low": "ta_highlowall",
        "Pattern": "ta_pattern",
        "Candlestick": "ta_candlestick",
        "Beta": "ta_beta",
        "Average True Range": "ta_atr",
        "Average Volume": "ta_avgvol",
        "Relative Volume": "ta_relvol",
        "Current Volume": "ta_volume",
        "Trades": "ta_trades",
        "Price $": "ta_price",
        "Target Price": "ta_targetprice",
        "IPO Date": "ipo",
        "Shares Outstanding": "sh_outstand",
        "Float": "sh_float",
        "After-Hours Close": "ta_afterhours",
        "After-Hours Change": "ta_afterhourschange",
        "Latest News": "n_news",
        "Single Category": "etf_category",
        "Asset Type": "etf_assettype",
        "Sponsor": "etf_sponsor",
        "Net Expense Ratio": "etf_expense",
        "Net Fund Flows": "etf_flows",
        "Annualized Return": "etf_return",
        "Tags": "etf_tags"
    }
    
    filter_code = filter_mapping.get(filter_name)
    if not filter_code:
        return None
    
    return f"{filter_code}_{option_value}"


def test_filter(filter_name, filter_options):
    """测试单个筛选器"""
    print(f"测试: {filter_name}")
    
    # 随机选择选项
    option_name, option_value = get_random_option(filter_options)
    if not option_value:
        print(f"  跳过: 没有有效选项")
        return False, "没有有效选项"
    
    print(f"  选择: {option_name} -> {option_value}")
    
    # 生成筛选器代码
    filter_code = generate_filter_code(filter_name, option_value)
    if not filter_code:
        print(f"  跳过: 无法生成筛选器代码")
        return False, "无法生成筛选器代码"
    
    print(f"  代码: {filter_code}")
    
    # 执行测试
    try:
        result = get_screener_data(filters=[filter_code], rows=5)
        count = result.get('total_rows', 0)
        print(f"  结果: {count} 只股票")
        return True, f"成功，找到 {count} 只股票"
    except Exception as e:
        error_msg = str(e)
        print(f"  错误: {error_msg}")
        return False, error_msg


def main():
    """主函数"""
    print("FinViz 筛选器自动测试")
    print("=" * 40)
    
    # 加载筛选器
    filters = load_filters()
    if not filters:
        print("无法加载筛选器配置")
        return
    
    print(f"加载了 {len(filters)} 个筛选器")
    
    # 设置测试参数
    max_test = 10  # 默认测试前10个筛选器
    delay = 1.0    # 延迟1秒
    
    print(f"将测试前 {max_test} 个筛选器，间隔 {delay} 秒")
    
    # 执行测试
    success_count = 0
    results = []
    filter_names = list(filters.keys())[:max_test]
    
    for i, filter_name in enumerate(filter_names, 1):
        print(f"\n进度: {i}/{max_test}")
        success, message = test_filter(filter_name, filters[filter_name])
        results.append({
            'filter_name': filter_name,
            'success': success,
            'message': message
        })
        
        if success:
            success_count += 1
        
        # 添加延迟
        if i < max_test:
            time.sleep(delay)
    
    # 打印结果
    print(f"\n{'='*40}")
    print(f"测试完成: {success_count}/{max_test} 成功")
    print(f"成功率: {success_count/max_test*100:.1f}%")
    
    # 显示失败的筛选器
    failed_filters = [r for r in results if not r['success']]
    if failed_filters:
        print(f"\n失败的筛选器:")
        for result in failed_filters:
            print(f"  - {result['filter_name']}: {result['message']}")
    
    # 保存结果
    output_file = project_root / "script" / "auto_test_results.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n测试结果已保存到: {output_file}")
    except Exception as e:
        print(f"保存结果失败: {e}")


if __name__ == "__main__":
    main()

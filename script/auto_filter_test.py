#!/usr/bin/env python3
"""
FinViz 筛选器自动测试脚本

此脚本用于自动测试所有筛选器，测试每个筛选器的前两个选项。
如果返回空数据，则记录为异常需要手动检查调试。
"""

import sys
import os
import json
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


def get_first_two_options(filter_options):
    """获取筛选器选项的前两个有效选项"""
    # 过滤掉空值和"Any"选项
    valid_options = {k: v for k, v in filter_options.items() 
                   if v and k != "Any" and v != ""}
    
    if not valid_options:
        return []
    
    # 返回前两个选项
    options = list(valid_options.items())[:2]
    return options


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


def test_filter_option(filter_name, option_name, option_value):
    """测试单个筛选器选项"""
    print(f"  测试选项: {option_name} -> {option_value}")
    
    # 生成筛选器代码
    filter_code = generate_filter_code(filter_name, option_value)
    if not filter_code:
        print(f"    跳过: 无法生成筛选器代码")
        return False, "无法生成筛选器代码", 0
    
    print(f"    代码: {filter_code}")
    
    # 执行测试
    try:
        result = get_screener_data(filters=[filter_code], rows=5)
        count = result.get('total_rows', 0)
        print(f"    结果: {count} 只股票")
        
        if count == 0:
            return False, "返回空数据，需要手动检查调试", count
        else:
            return True, f"成功，找到 {count} 只股票", count
            
    except Exception as e:
        error_msg = str(e)
        print(f"    错误: {error_msg}")
        return False, error_msg, 0


def test_filter(filter_name, filter_options):
    """测试单个筛选器的前两个选项"""
    print(f"\n测试筛选器: {filter_name}")
    
    # 获取前两个选项
    options = get_first_two_options(filter_options)
    if not options:
        print(f"  跳过: 没有有效选项")
        return {
            'filter_name': filter_name,
            'status': 'skipped',
            'message': '没有有效选项',
            'options_tested': 0,
            'successful_options': 0,
            'empty_results': 0,
            'errors': 0
        }
    
    print(f"  找到 {len(options)} 个选项进行测试")
    
    results = {
        'filter_name': filter_name,
        'status': 'completed',
        'message': '',
        'options_tested': len(options),
        'successful_options': 0,
        'empty_results': 0,
        'errors': 0,
        'option_results': []
    }
    
    # 测试每个选项
    for option_name, option_value in options:
        success, message, count = test_filter_option(filter_name, option_name, option_value)
        
        option_result = {
            'option_name': option_name,
            'option_value': option_value,
            'success': success,
            'message': message,
            'count': count
        }
        results['option_results'].append(option_result)
        
        if success:
            results['successful_options'] += 1
        elif count == 0:
            results['empty_results'] += 1
        else:
            results['errors'] += 1
        
        # 添加延迟避免请求过于频繁
        time.sleep(0.5)
    
    # 设置总体状态
    if results['empty_results'] > 0:
        results['status'] = 'has_empty_results'
        results['message'] = f"有 {results['empty_results']} 个选项返回空数据"
    elif results['errors'] > 0:
        results['status'] = 'has_errors'
        results['message'] = f"有 {results['errors']} 个选项出现错误"
    else:
        results['status'] = 'all_successful'
        results['message'] = f"所有 {results['successful_options']} 个选项测试成功"
    
    return results


def main():
    """主函数"""
    print("FinViz 筛选器自动测试 - 测试每个筛选器的前两个选项")
    print("=" * 60)
    
    # 加载筛选器
    filters = load_filters()
    if not filters:
        print("无法加载筛选器配置")
        return
    
    print(f"加载了 {len(filters)} 个筛选器")
    
    # 设置测试参数
    max_test = 85  # 测试所有85个筛选器
    delay = 1.0    # 延迟1秒
    
    print(f"将测试前 {max_test} 个筛选器，每个筛选器测试前两个选项")
    print(f"筛选器间间隔 {delay} 秒，选项间间隔 0.5 秒")
    
    # 执行测试
    results = []
    filter_names = list(filters.keys())[:max_test]
    
    # 统计信息
    total_filters = 0
    successful_filters = 0
    filters_with_empty_results = 0
    filters_with_errors = 0
    total_options_tested = 0
    total_empty_results = 0
    
    for i, filter_name in enumerate(filter_names, 1):
        print(f"\n进度: {i}/{max_test}")
        result = test_filter(filter_name, filters[filter_name])
        results.append(result)
        
        total_filters += 1
        total_options_tested += result.get('options_tested', 0)
        total_empty_results += result.get('empty_results', 0)
        
        if result['status'] == 'all_successful':
            successful_filters += 1
        elif result['status'] == 'has_empty_results':
            filters_with_empty_results += 1
        elif result['status'] == 'has_errors':
            filters_with_errors += 1
        
        # 添加延迟
        if i < max_test:
            time.sleep(delay)
    
    # 打印结果
    print(f"\n{'='*60}")
    print("测试完成统计:")
    print(f"  总筛选器数: {total_filters}")
    print(f"  完全成功的筛选器: {successful_filters}")
    print(f"  有空结果的筛选器: {filters_with_empty_results}")
    print(f"  有错误的筛选器: {filters_with_errors}")
    print(f"  总测试选项数: {total_options_tested}")
    print(f"  返回空数据的选项数: {total_empty_results}")
    
    # 显示有空结果的筛选器（需要手动检查调试）
    empty_result_filters = [r for r in results if r['status'] == 'has_empty_results']
    if empty_result_filters:
        print(f"\n⚠️  需要手动检查调试的筛选器（返回空数据）:")
        for result in empty_result_filters:
            print(f"  - {result['filter_name']}: {result['message']}")
            for option_result in result['option_results']:
                if option_result['count'] == 0:
                    print(f"    选项: {option_result['option_name']} -> {option_result['option_value']}")
    
    # 显示有错误的筛选器
    error_filters = [r for r in results if r['status'] == 'has_errors']
    if error_filters:
        print(f"\n❌ 有错误的筛选器:")
        for result in error_filters:
            print(f"  - {result['filter_name']}: {result['message']}")
            for option_result in result['option_results']:
                if not option_result['success'] and option_result['count'] != 0:
                    print(f"    选项: {option_result['option_name']} -> {option_result['option_value']}")
                    print(f"    错误: {option_result['message']}")
    
    # 保存详细结果
    output_file = project_root / "script" / "filter_test_results.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_filters': total_filters,
                    'successful_filters': successful_filters,
                    'filters_with_empty_results': filters_with_empty_results,
                    'filters_with_errors': filters_with_errors,
                    'total_options_tested': total_options_tested,
                    'total_empty_results': total_empty_results
                },
                'results': results
            }, f, ensure_ascii=False, indent=2)
        print(f"\n📄 详细测试结果已保存到: {output_file}")
    except Exception as e:
        print(f"保存结果失败: {e}")
    
    # 生成需要手动检查的筛选器列表
    if empty_result_filters:
        manual_check_file = project_root / "script" / "manual_check_filters.json"
        try:
            manual_check_data = []
            for result in empty_result_filters:
                for option_result in result['option_results']:
                    if option_result['count'] == 0:
                        manual_check_data.append({
                            'filter_name': result['filter_name'],
                            'option_name': option_result['option_name'],
                            'option_value': option_result['option_value'],
                            'filter_code': generate_filter_code(result['filter_name'], option_result['option_value'])
                        })
            
            with open(manual_check_file, 'w', encoding='utf-8') as f:
                json.dump(manual_check_data, f, ensure_ascii=False, indent=2)
            print(f"📋 需要手动检查的筛选器列表已保存到: {manual_check_file}")
        except Exception as e:
            print(f"保存手动检查列表失败: {e}")


if __name__ == "__main__":
    main()

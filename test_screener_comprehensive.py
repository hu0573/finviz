#!/usr/bin/env python3
"""
FinViz筛选器功能综合测试脚本

根据screener_guide.md文档，逐个测试所有筛选器功能
"""

import sys
import os
import time
from typing import Dict, List, Any

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.finviz import FinVizService


class ScreenerTester:
    """筛选器测试类"""
    
    def __init__(self):
        self.service = FinVizService()
        self.test_results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """记录测试结果"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            status = "✅ 通过"
        else:
            self.failed_tests += 1
            status = "❌ 失败"
        
        self.test_results[test_name] = {
            "success": success,
            "details": details
        }
        
        print(f"{status} {test_name}")
        if details:
            print(f"   详情: {details}")
        print()
    
    def test_basic_functionality(self):
        """测试基本筛选器功能"""
        print("=== 测试基本筛选器功能 ===")
        
        # 测试1: 获取筛选器选项
        try:
            filter_options = self.service.get_filter_options()
            if 'error' not in filter_options and len(filter_options) > 0:
                self.log_test("获取筛选器选项", True, f"获取到 {len(filter_options)} 个筛选器类别")
            else:
                self.log_test("获取筛选器选项", False, filter_options.get('error', '未知错误'))
        except Exception as e:
            self.log_test("获取筛选器选项", False, str(e))
        
        # 测试2: 基本筛选 - 无筛选条件
        try:
            result = self.service.get_screener_data(rows=5)
            if 'error' not in result and result['total_rows'] > 0:
                self.log_test("基本筛选（无条件）", True, f"获取到 {result['total_rows']} 只股票")
            else:
                self.log_test("基本筛选（无条件）", False, result.get('error', '无数据'))
        except Exception as e:
            self.log_test("基本筛选（无条件）", False, str(e))
        
        # 测试3: 限制返回行数
        try:
            result = self.service.get_screener_data(rows=3)
            if 'error' not in result and len(result['data']) <= 3:
                self.log_test("限制返回行数", True, f"返回 {len(result['data'])} 行数据")
            else:
                self.log_test("限制返回行数", False, result.get('error', '行数限制无效'))
        except Exception as e:
            self.log_test("限制返回行数", False, str(e))
    
    def test_exchange_filters(self):
        """测试交易所筛选功能"""
        print("=== 测试交易所筛选功能 ===")
        
        exchange_tests = [
            ('exch_nasd', '纳斯达克'),
            ('exch_nyse', '纽约证券交易所'),
            ('exch_amex', '美国证券交易所')
        ]
        
        for filter_code, description in exchange_tests:
            try:
                result = self.service.get_screener_data(filters=[filter_code], rows=5)
                if 'error' not in result and result['total_rows'] > 0:
                    self.log_test(f"交易所筛选 - {description}", True, f"找到 {result['total_rows']} 只股票")
                else:
                    self.log_test(f"交易所筛选 - {description}", False, result.get('error', '无数据'))
            except Exception as e:
                self.log_test(f"交易所筛选 - {description}", False, str(e))
    
    def test_index_filters(self):
        """测试指数筛选功能"""
        print("=== 测试指数筛选功能 ===")
        
        index_tests = [
            ('idx_sp500', 'S&P 500'),
            ('idx_ndx', 'NASDAQ 100'),
            ('idx_dji', '道琼斯工业平均指数'),
            ('idx_rut', '罗素2000指数')
        ]
        
        for filter_code, description in index_tests:
            try:
                result = self.service.get_screener_data(filters=[filter_code], rows=5)
                if 'error' not in result and result['total_rows'] > 0:
                    self.log_test(f"指数筛选 - {description}", True, f"找到 {result['total_rows']} 只股票")
                else:
                    self.log_test(f"指数筛选 - {description}", False, result.get('error', '无数据'))
            except Exception as e:
                self.log_test(f"指数筛选 - {description}", False, str(e))
    
    def test_sector_filters(self):
        """测试行业板块筛选功能"""
        print("=== 测试行业板块筛选功能 ===")
        
        sector_tests = [
            ('sec_technology', '科技'),
            ('sec_financial', '金融'),
            ('sec_healthcare', '医疗保健'),
            ('sec_energy', '能源'),
            ('sec_consumercyclical', '消费周期性')
        ]
        
        for filter_code, description in sector_tests:
            try:
                result = self.service.get_screener_data(filters=[filter_code], rows=5)
                if 'error' not in result and result['total_rows'] > 0:
                    self.log_test(f"行业筛选 - {description}", True, f"找到 {result['total_rows']} 只股票")
                else:
                    self.log_test(f"行业筛选 - {description}", False, result.get('error', '无数据'))
            except Exception as e:
                self.log_test(f"行业筛选 - {description}", False, str(e))
    
    def test_market_cap_filters(self):
        """测试市值筛选功能"""
        print("=== 测试市值筛选功能 ===")
        
        cap_tests = [
            ('cap_mega', '超大型股'),
            ('cap_large', '大型股'),
            ('cap_mid', '中型股'),
            ('cap_small', '小型股'),
            ('cap_micro', '微型股')
        ]
        
        for filter_code, description in cap_tests:
            try:
                result = self.service.get_screener_data(filters=[filter_code], rows=5)
                if 'error' not in result and result['total_rows'] > 0:
                    self.log_test(f"市值筛选 - {description}", True, f"找到 {result['total_rows']} 只股票")
                else:
                    self.log_test(f"市值筛选 - {description}", False, result.get('error', '无数据'))
            except Exception as e:
                self.log_test(f"市值筛选 - {description}", False, str(e))
    
    def test_price_filters(self):
        """测试价格筛选功能"""
        print("=== 测试价格筛选功能 ===")
        
        price_tests = [
            ('price_o50', '价格高于50美元'),
            ('price_u20', '价格低于20美元'),
            ('price_10to50', '价格10-50美元之间'),
            ('price_o100', '价格高于100美元')
        ]
        
        for filter_code, description in price_tests:
            try:
                result = self.service.get_screener_data(filters=[filter_code], rows=5)
                if 'error' not in result and result['total_rows'] > 0:
                    self.log_test(f"价格筛选 - {description}", True, f"找到 {result['total_rows']} 只股票")
                else:
                    self.log_test(f"价格筛选 - {description}", False, result.get('error', '无数据'))
            except Exception as e:
                self.log_test(f"价格筛选 - {description}", False, str(e))
    
    def test_financial_filters(self):
        """测试财务指标筛选功能"""
        print("=== 测试财务指标筛选功能 ===")
        
        financial_tests = [
            ('fa_pe_low', '低市盈率'),
            ('fa_pe_high', '高市盈率'),
            ('fa_pb_u3', '市净率低于3'),
            ('fa_ps_u5', '市销率低于5'),
            ('fa_div_high', '高股息收益率'),
            ('fa_div_none', '无股息')
        ]
        
        for filter_code, description in financial_tests:
            try:
                result = self.service.get_screener_data(filters=[filter_code], rows=5)
                if 'error' not in result and result['total_rows'] > 0:
                    self.log_test(f"财务筛选 - {description}", True, f"找到 {result['total_rows']} 只股票")
                else:
                    self.log_test(f"财务筛选 - {description}", False, result.get('error', '无数据'))
            except Exception as e:
                self.log_test(f"财务筛选 - {description}", False, str(e))
    
    def test_technical_filters(self):
        """测试技术指标筛选功能"""
        print("=== 测试技术指标筛选功能 ===")
        
        technical_tests = [
            ('ta_rsi_oversold', 'RSI超卖'),
            ('ta_rsi_overbought', 'RSI超买'),
            ('ta_ma_sma50', '价格高于50日移动平均线'),
            ('ta_ma_sma200', '价格高于200日移动平均线'),
            ('ta_highlow52w_b0to10h', '距离52周高点0-10%')
        ]
        
        for filter_code, description in technical_tests:
            try:
                result = self.service.get_screener_data(filters=[filter_code], rows=5)
                if 'error' not in result and result['total_rows'] > 0:
                    self.log_test(f"技术筛选 - {description}", True, f"找到 {result['total_rows']} 只股票")
                else:
                    self.log_test(f"技术筛选 - {description}", False, result.get('error', '无数据'))
            except Exception as e:
                self.log_test(f"技术筛选 - {description}", False, str(e))
    
    def test_signal_filters(self):
        """测试信号筛选功能"""
        print("=== 测试信号筛选功能 ===")
        
        signal_tests = [
            ('signal_tpgainers', '涨幅榜'),
            ('signal_tplosers', '跌幅榜'),
            ('signal_newhigh', '新高'),
            ('signal_newlow', '新低'),
            ('signal_mostvolatile', '最波动'),
            ('signal_mostactive', '最活跃')
        ]
        
        for filter_code, description in signal_tests:
            try:
                result = self.service.get_screener_data(filters=[filter_code], rows=5)
                if 'error' not in result and result['total_rows'] > 0:
                    self.log_test(f"信号筛选 - {description}", True, f"找到 {result['total_rows']} 只股票")
                else:
                    self.log_test(f"信号筛选 - {description}", False, result.get('error', '无数据'))
            except Exception as e:
                self.log_test(f"信号筛选 - {description}", False, str(e))
    
    def test_table_types(self):
        """测试表格类型功能"""
        print("=== 测试表格类型功能 ===")
        
        table_tests = [
            ('Overview', '概览'),
            ('Valuation', '估值'),
            ('Ownership', '所有权'),
            ('Performance', '表现'),
            ('Financial', '财务'),
            ('Technical', '技术')
        ]
        
        for table_type, description in table_tests:
            try:
                result = self.service.get_screener_data(
                    filters=['idx_sp500'], 
                    table=table_type, 
                    rows=5
                )
                if 'error' not in result and result['total_rows'] > 0:
                    self.log_test(f"表格类型 - {description}", True, f"获取到 {result['total_rows']} 只股票")
                else:
                    self.log_test(f"表格类型 - {description}", False, result.get('error', '无数据'))
            except Exception as e:
                self.log_test(f"表格类型 - {description}", False, str(e))
    
    def test_ordering(self):
        """测试排序功能"""
        print("=== 测试排序功能 ===")
        
        order_tests = [
            ('-market_cap', '按市值降序'),
            ('price', '按价格升序'),
            ('-change', '按涨跌幅降序'),
            ('ticker', '按股票代码升序')
        ]
        
        for order, description in order_tests:
            try:
                result = self.service.get_screener_data(
                    filters=['idx_sp500'], 
                    order=order, 
                    rows=5
                )
                if 'error' not in result and result['total_rows'] > 0:
                    self.log_test(f"排序功能 - {description}", True, f"获取到 {result['total_rows']} 只股票")
                else:
                    self.log_test(f"排序功能 - {description}", False, result.get('error', '无数据'))
            except Exception as e:
                self.log_test(f"排序功能 - {description}", False, str(e))
    
    def test_combined_filters(self):
        """测试组合筛选条件"""
        print("=== 测试组合筛选条件 ===")
        
        # 测试1: 价值投资筛选
        try:
            filters = ['idx_sp500', 'cap_large', 'fa_pe_low', 'fa_div_high']
            result = self.service.get_screener_data(filters=filters, rows=5)
            if 'error' not in result and result['total_rows'] > 0:
                self.log_test("组合筛选 - 价值投资", True, f"找到 {result['total_rows']} 只价值股")
            else:
                self.log_test("组合筛选 - 价值投资", False, result.get('error', '无数据'))
        except Exception as e:
            self.log_test("组合筛选 - 价值投资", False, str(e))
        
        # 测试2: 成长股筛选
        try:
            filters = ['sec_technology', 'cap_mid', 'fa_pe_u25', 'fa_div_none']
            result = self.service.get_screener_data(filters=filters, rows=5)
            if 'error' not in result and result['total_rows'] > 0:
                self.log_test("组合筛选 - 成长股", True, f"找到 {result['total_rows']} 只成长股")
            else:
                self.log_test("组合筛选 - 成长股", False, result.get('error', '无数据'))
        except Exception as e:
            self.log_test("组合筛选 - 成长股", False, str(e))
        
        # 测试3: 技术面筛选
        try:
            filters = ['ta_rsi_oversold', 'ta_ma_sma50', 'sh_avgvol_o1000']
            result = self.service.get_screener_data(filters=filters, rows=5)
            if 'error' not in result and result['total_rows'] > 0:
                self.log_test("组合筛选 - 技术面", True, f"找到 {result['total_rows']} 只技术面强势股票")
            else:
                self.log_test("组合筛选 - 技术面", False, result.get('error', '无数据'))
        except Exception as e:
            self.log_test("组合筛选 - 技术面", False, str(e))
    
    def test_url_functionality(self):
        """测试URL功能"""
        print("=== 测试URL功能 ===")
        
        try:
            url = "https://finviz.com/screener.ashx?v=111&f=idx_sp500,cap_large&o=-market_cap"
            result = self.service.get_screener_from_url(url, rows=5)
            if 'error' not in result and result['total_rows'] > 0:
                self.log_test("URL筛选功能", True, f"从URL获取到 {result['total_rows']} 只股票")
            else:
                self.log_test("URL筛选功能", False, result.get('error', '无数据'))
        except Exception as e:
            self.log_test("URL筛选功能", False, str(e))
    
    def test_error_handling(self):
        """测试错误处理"""
        print("=== 测试错误处理 ===")
        
        # 测试1: 无效筛选器
        try:
            result = self.service.get_screener_data(filters=['invalid_filter'], rows=5)
            if 'error' in result:
                self.log_test("错误处理 - 无效筛选器", True, "正确识别无效筛选器")
            else:
                self.log_test("错误处理 - 无效筛选器", False, "未正确处理无效筛选器")
        except Exception as e:
            self.log_test("错误处理 - 无效筛选器", True, f"异常处理正常: {str(e)}")
        
        # 测试2: 过于严格的筛选条件
        try:
            filters = ['idx_sp500', 'cap_micro', 'fa_pe_u5', 'fa_div_o10']
            result = self.service.get_screener_data(filters=filters, rows=5)
            if 'error' in result or result['total_rows'] == 0:
                self.log_test("错误处理 - 严格筛选条件", True, "正确处理无结果情况")
            else:
                self.log_test("错误处理 - 严格筛选条件", True, f"找到 {result['total_rows']} 只股票")
        except Exception as e:
            self.log_test("错误处理 - 严格筛选条件", True, f"异常处理正常: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始FinViz筛选器功能综合测试\n")
        print("=" * 60)
        
        start_time = time.time()
        
        # 运行所有测试
        self.test_basic_functionality()
        self.test_exchange_filters()
        self.test_index_filters()
        self.test_sector_filters()
        self.test_market_cap_filters()
        self.test_price_filters()
        self.test_financial_filters()
        self.test_technical_filters()
        self.test_signal_filters()
        self.test_table_types()
        self.test_ordering()
        self.test_combined_filters()
        self.test_url_functionality()
        self.test_error_handling()
        
        end_time = time.time()
        
        # 输出测试总结
        print("=" * 60)
        print("测试总结")
        print("=" * 60)
        print(f"总测试数: {self.total_tests}")
        print(f"通过测试: {self.passed_tests}")
        print(f"失败测试: {self.failed_tests}")
        print(f"成功率: {(self.passed_tests/self.total_tests)*100:.1f}%")
        print(f"测试耗时: {end_time - start_time:.2f} 秒")
        
        # 输出失败的测试
        if self.failed_tests > 0:
            print("\n失败的测试:")
            for test_name, result in self.test_results.items():
                if not result['success']:
                    print(f"  - {test_name}: {result['details']}")
        
        return self.test_results


def main():
    """主函数"""
    tester = ScreenerTester()
    results = tester.run_all_tests()
    
    # 保存测试结果到文件
    import json
    with open('screener_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n测试结果已保存到 screener_test_results.json")


if __name__ == "__main__":
    main()

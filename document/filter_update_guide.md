# Finviz筛选器更新指南

## 概述

本指南详细说明了如何从Finviz网站获取最新的筛选器数据并更新本地的`filters.json`文件。这个过程确保了筛选器数据与Finviz网站保持同步。

## 更新流程

### 1. 获取网页源码

首先需要从Finviz筛选器页面下载HTML源码：

**目标URL**: https://finviz.com/screener.ashx?v=111&ft=4

可以使用以下方法获取源码：
- 浏览器开发者工具保存HTML
- 使用curl命令：`curl -o screener_webpage.html "https://finviz.com/screener.ashx?v=111&ft=4"`
- 使用Python requests库

### 2. 提取筛选器数据

创建Python脚本来解析HTML并提取筛选器信息：

```python
#!/usr/bin/env python3
"""
脚本用于从Finviz网页源码中提取筛选器数据并更新filters.json
"""

import re
import json
from bs4 import BeautifulSoup

def extract_filters_from_html(html_content):
    """从HTML内容中提取筛选器数据"""
    soup = BeautifulSoup(html_content, 'html.parser')
    filters = {}
    
    # 查找所有带有data-filter属性的select元素
    select_elements = soup.find_all('select', {'data-filter': True})
    
    for select in select_elements:
        filter_name = select.get('data-filter')
        options = {}
        
        # 提取所有option元素
        option_elements = select.find_all('option')
        for option in option_elements:
            value = option.get('value', '')
            text = option.get_text(strip=True)
            
            if value and text:
                # 跳过"Any"选项，因为它在filters.json中通常用空字符串表示
                if value == '' and text == 'Any':
                    options['Any'] = f"{filter_name}_"
                elif value != '':
                    # 处理HTML实体
                    text = text.replace('&amp;', '&')
                    options[text] = f"{filter_name}_{value}"
        
        if options:
            filters[filter_name] = options
    
    return filters

def read_html_file(file_path):
    """读取HTML文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    # 读取网页源码
    html_content = read_html_file('/path/to/screener_webpage.html')
    
    # 提取筛选器数据
    filters = extract_filters_from_html(html_content)
    
    # 打印提取的筛选器信息
    print("提取的筛选器数据:")
    for filter_name, options in filters.items():
        print(f"\n{filter_name}:")
        for option_name, option_value in options.items():
            print(f"  {option_name}: {option_value}")
    
    # 保存到JSON文件
    with open('/path/to/extracted_filters.json', 'w', encoding='utf-8') as f:
        json.dump(filters, f, indent=2, ensure_ascii=False)
    
    print(f"\n筛选器数据已保存到 extracted_filters.json")
    print(f"总共提取了 {len(filters)} 个筛选器")

if __name__ == "__main__":
    main()
```

### 3. 合并和更新筛选器

创建脚本来合并现有筛选器和新的筛选器数据：

```python
#!/usr/bin/env python3
"""
脚本用于对比现有filters.json和从网页提取的筛选器数据，并生成更新的filters.json
"""

import json
import re

def load_json_file(file_path):
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_old_format_to_new(old_filters):
    """将旧格式转换为新格式"""
    new_filters = {}
    
    for filter_name, options in old_filters.items():
        new_options = {}
        for option_name, option_value in options.items():
            # 处理旧格式中的前缀
            if option_value.startswith(filter_name.lower() + '_'):
                # 移除前缀，只保留值部分
                value_part = option_value[len(filter_name.lower()) + 1:]
                new_options[option_name] = f"{filter_name}_{value_part}"
            else:
                new_options[option_name] = option_value
        new_filters[filter_name] = new_options
    
    return new_filters

def merge_filters(old_filters, new_filters):
    """合并旧的和新的筛选器数据"""
    merged = {}
    
    # 获取所有筛选器名称
    all_filter_names = set(old_filters.keys()) | set(new_filters.keys())
    
    for filter_name in all_filter_names:
        old_options = old_filters.get(filter_name, {})
        new_options = new_filters.get(filter_name, {})
        
        # 合并选项，新的选项优先
        merged_options = {}
        
        # 先添加旧选项
        for option_name, option_value in old_options.items():
            merged_options[option_name] = option_value
        
        # 然后添加/覆盖新选项
        for option_name, option_value in new_options.items():
            merged_options[option_name] = option_value
        
        merged[filter_name] = merged_options
    
    return merged

def main():
    # 加载现有filters.json
    print("加载现有filters.json...")
    old_filters = load_json_file('/path/to/core/finviz/filters.json')
    
    # 加载从网页提取的筛选器数据
    print("加载从网页提取的筛选器数据...")
    new_filters = load_json_file('/path/to/extracted_filters.json')
    
    # 转换旧格式
    print("转换旧格式...")
    old_filters_converted = convert_old_format_to_new(old_filters)
    
    # 合并筛选器
    print("合并筛选器数据...")
    merged_filters = merge_filters(old_filters_converted, new_filters)
    
    # 统计信息
    print(f"\n统计信息:")
    print(f"旧筛选器数量: {len(old_filters)}")
    print(f"新筛选器数量: {len(new_filters)}")
    print(f"合并后筛选器数量: {len(merged_filters)}")
    
    # 显示新增的筛选器
    new_filter_names = set(new_filters.keys()) - set(old_filters.keys())
    if new_filter_names:
        print(f"\n新增的筛选器: {sorted(new_filter_names)}")
    
    # 显示删除的筛选器
    removed_filter_names = set(old_filters.keys()) - set(new_filters.keys())
    if removed_filter_names:
        print(f"\n删除的筛选器: {sorted(removed_filter_names)}")
    
    # 保存合并后的筛选器
    output_file = '/path/to/updated_filters.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_filters, f, indent=2, ensure_ascii=False)
    
    print(f"\n合并后的筛选器数据已保存到: {output_file}")
    
    # 显示一些示例筛选器
    print(f"\n示例筛选器:")
    for i, (filter_name, options) in enumerate(merged_filters.items()):
        if i >= 3:  # 只显示前3个
            break
        print(f"{filter_name}: {len(options)} 个选项")
        for j, (option_name, option_value) in enumerate(options.items()):
            if j >= 3:  # 每个筛选器只显示前3个选项
                print(f"  ... 还有 {len(options) - 3} 个选项")
                break
            print(f"  {option_name}: {option_value}")

if __name__ == "__main__":
    main()
```

### 4. 执行更新

完整的更新流程：

```bash
# 1. 备份原始文件
cp core/finviz/filters.json core/finviz/filters.json.backup

# 2. 运行提取脚本
python extract_filters.py

# 3. 运行合并脚本
python update_filters.py

# 4. 更新filters.json
cp updated_filters.json core/finviz/filters.json

# 5. 清理临时文件
rm extract_filters.py update_filters.py extracted_filters.json updated_filters.json
```

## 筛选器数据结构

### 格式说明

更新后的`filters.json`文件采用以下格式：

```json
{
  "筛选器名称": {
    "选项显示名称": "筛选器名称_选项值",
    "选项显示名称2": "筛选器名称_选项值2"
  }
}
```

### 示例

```json
{
  "exch": {
    "Any": "exch_",
    "AMEX": "exch_amex",
    "CBOE": "exch_cboe",
    "NASDAQ": "exch_nasd",
    "NYSE": "exch_nyse",
    "Custom (Elite only)": "exch_modal"
  },
  "fa_pe": {
    "Any": "fa_pe_",
    "Low (<15)": "fa_pe_low",
    "Profitable (>0)": "fa_pe_profitable",
    "High (>50)": "fa_pe_high"
  }
}
```

## 筛选器类别

更新后的筛选器包含以下主要类别：

### 基础筛选器
- `exch`: 交易所
- `idx`: 指数
- `sec`: 行业板块
- `ind`: 具体行业
- `geo`: 地理位置
- `cap`: 市值

### 财务分析筛选器 (fa_*)
- `fa_pe`: 市盈率
- `fa_fpe`: 前瞻市盈率
- `fa_peg`: PEG比率
- `fa_ps`: 市销率
- `fa_pb`: 市净率
- `fa_roe`: 净资产收益率
- `fa_roa`: 总资产收益率
- `fa_grossmargin`: 毛利率
- `fa_opermargin`: 营业利润率
- `fa_netmargin`: 净利润率

### 技术分析筛选器 (ta_*)
- `ta_sma20`: 20日简单移动平均线
- `ta_sma50`: 50日简单移动平均线
- `ta_sma200`: 200日简单移动平均线
- `ta_rsi`: 相对强弱指数
- `ta_beta`: 贝塔系数
- `ta_volatility`: 波动率

### 股票筛选器 (sh_*)
- `sh_price`: 股价
- `sh_float`: 流通股
- `sh_outstanding`: 总股本
- `sh_avgvol`: 平均成交量
- `sh_curvol`: 当前成交量
- `sh_relvol`: 相对成交量

### ETF筛选器 (etf_*)
- `etf_category`: ETF类别
- `etf_assettype`: 资产类型
- `etf_sponsor`: 发行商
- `etf_netexpense`: 净费用率
- `etf_fundflows`: 资金流向
- `etf_return`: 收益率
- `etf_tags`: 标签

## 注意事项

1. **备份重要性**: 更新前务必备份原始`filters.json`文件
2. **格式一致性**: 确保所有筛选器选项都遵循`筛选器名_选项值`的格式
3. **HTML实体处理**: 注意处理HTML中的特殊字符（如`&amp;`）
4. **数据完整性**: 合并时保留所有现有选项，同时添加新选项
5. **测试验证**: 更新后建议测试筛选器功能是否正常

## 更新频率建议

- **定期更新**: 建议每月检查一次Finviz网站是否有新的筛选器
- **重大变更**: 当Finviz网站进行重大更新时及时更新
- **功能扩展**: 当需要新的筛选功能时主动更新

## 故障排除

### 常见问题

1. **HTML解析失败**: 检查HTML文件是否完整下载
2. **筛选器缺失**: 确认网页源码中包含所有筛选器元素
3. **格式错误**: 验证JSON格式是否正确
4. **编码问题**: 确保文件使用UTF-8编码

### 调试技巧

- 使用浏览器开发者工具检查筛选器HTML结构
- 逐步运行脚本并检查中间结果
- 对比更新前后的筛选器数量变化
- 验证关键筛选器的选项是否完整

---

*最后更新: 2025年1月17日*
*基于Finviz网站: https://finviz.com/screener.ashx?v=111&ft=4*

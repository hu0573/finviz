# FinViz 表格类型分析报告

## 概述

本文档详细分析了 FinViz 筛选器系统中表格类型的设计原理，以及为什么技术指标（如RSI）需要特定的表格类型才能正确显示。

## 问题背景

在测试 RSI 筛选器时发现，只有在使用 "Technical" 表格类型时才能看到 RSI 的实际数值，而在 "Overview" 表格类型中 RSI 显示为 "N/A"。这引发了对 FinViz 表格类型设计的深入探索。

## 核心发现

### 1. FinViz 没有真正的 "All" 类型表格

虽然前端界面看起来有 "All" 选项，但经过深入分析发现：

- **所有排序选项都使用 `v=111`** (Overview 类型)
- **没有包含所有列的 "All" 类型表格**
- **不同类型的指标分散在不同表格中**

### 2. 表格类型与列的关系

| 表格类型 | 代码 | 主要列 | 包含RSI | 包含技术指标 |
|----------|------|--------|---------|--------------|
| Overview | 111 | 基础信息、市值、P/E | ❌ | ❌ |
| Valuation | 121 | 估值指标 (P/E, P/S, P/B等) | ❌ | ❌ |
| Ownership | 131 | 持股信息 (内部持股、机构持股等) | ❌ | ❌ |
| Performance | 141 | 表现数据 (周、月、年表现等) | ❌ | ❌ |
| Custom | 152 | 自定义列 | ❌ | ❌ |
| Financial | 161 | 财务指标 (ROA, ROE, 利润率等) | ❌ | ❌ |
| **Technical** | **171** | **技术指标** | **✅** | **✅** |
| ETF | 181 | ETF信息 | ❌ | ❌ |
| Fund | 191 | 基金信息 | ❌ | ❌ |

### 3. 技术指标分布

**Technical 表格类型 (v=171) 包含的技术指标：**
- Beta (贝塔系数)
- ATR (平均真实波幅)
- SMA20 (20日简单移动平均)
- SMA50 (50日简单移动平均)
- SMA200 (200日简单移动平均)
- 52W High (52周最高价)
- 52W Low (52周最低价)
- **RSI (相对强弱指数)**
- Price (价格)
- Change (变化)
- Change from Open (开盘变化)
- Gap (跳空)
- Volume (成交量)

## 设计原理分析

### 1. 数据分离策略

FinViz 采用数据分离策略，将不同类型的指标分散在不同表格中：

- **提高加载速度**: 避免单个表格包含过多列
- **改善用户体验**: 用户可以根据需要选择相关指标
- **优化性能**: 减少数据传输量

### 2. 表格类型选择逻辑

```python
# 根据筛选器类型选择表格类型
if 'ta_' in filter_id:  # 技术指标筛选器
    table_type = 'Technical'
elif 'fa_' in filter_id:  # 财务指标筛选器
    table_type = 'Financial'  # 或 'Valuation'
elif 'sh_' in filter_id:  # 股票筛选器
    table_type = 'Ownership'  # 或 'Overview'
```

### 3. 筛选器与表格类型的对应关系

| 筛选器前缀 | 推荐表格类型 | 说明 |
|------------|--------------|------|
| `ta_*` | Technical | 技术分析指标 |
| `fa_*` | Financial/Valuation | 财务分析指标 |
| `sh_*` | Ownership | 股票信息 |
| `exch_*`, `sec_*`, `idx_*` | Overview | 基础筛选器 |
| `etf_*` | ETF | ETF相关指标 |

## 实际测试验证

### 1. RSI 筛选器测试

```python
# ❌ 错误用法 - Overview 类型不显示 RSI
result = get_screener_data(filters=['ta_rsi_os30'], table='Overview')
# 结果: RSI 列显示为 "N/A"

# ✅ 正确用法 - Technical 类型显示 RSI
result = get_screener_data(filters=['ta_rsi_os30'], table='Technical')
# 结果: RSI 列显示实际数值，如 18.68, 28.15 等
```

### 2. 不同表格类型的列对比

**Overview 表格 (v=111):**
```
['No.', 'Ticker', 'Company', 'Sector', 'Industry', 'Country', 'Market Cap', 'P/E', 'Price', 'Change', 'Volume']
```

**Technical 表格 (v=171):**
```
['No.', 'Ticker', 'Beta', 'ATR', 'SMA20', 'SMA50', 'SMA200', '52W High', '52W Low', 'RSI', 'Price', 'Change', 'Change from Open', 'Gap', 'Volume']
```

### 3. 筛选器功能验证

| 筛选器类型 | 测试条件 | 表格类型 | 结果 | 验证 |
|------------|----------|----------|------|------|
| RSI超卖 | `ta_rsi_os30` | Technical | ✅ 正常 | RSI < 30 |
| RSI超买 | `ta_rsi_ob70` | Technical | ✅ 正常 | RSI > 70 |
| 交易所 | `exch_nasd` | Overview | ✅ 正常 | 纳斯达克股票 |
| 板块 | `sec_technology` | Overview | ✅ 正常 | 科技股 |
| 市盈率 | `fa_pe_low` | Overview | ✅ 正常 | P/E < 15 |

## 最佳实践建议

### 1. 筛选器使用指南

```python
# 技术指标筛选器
def get_technical_stocks():
    return get_screener_data(
        filters=['ta_rsi_os30', 'ta_sma20_above'],
        table='Technical',
        rows=20
    )

# 财务指标筛选器
def get_financial_stocks():
    return get_screener_data(
        filters=['fa_pe_low', 'fa_roe_high'],
        table='Financial',  # 或 'Valuation'
        rows=20
    )

# 基础筛选器
def get_basic_stocks():
    return get_screener_data(
        filters=['exch_nasd', 'sec_technology', 'cap_large'],
        table='Overview',
        rows=20
    )
```

### 2. 自动表格类型选择

可以基于筛选器类型自动选择表格类型：

```python
def get_optimal_table_type(filters):
    """根据筛选器类型自动选择最优表格类型"""
    for filter_id in filters:
        if filter_id.startswith('ta_'):
            return 'Technical'
        elif filter_id.startswith('fa_'):
            return 'Financial'
        elif filter_id.startswith('sh_'):
            return 'Ownership'
        elif filter_id.startswith('etf_'):
            return 'ETF'
    return 'Overview'  # 默认使用 Overview
```

### 3. 组合筛选器策略

当使用多种类型的筛选器时：

```python
# 策略1: 使用包含最多相关列的表格类型
def get_combined_stocks():
    return get_screener_data(
        filters=['exch_nasd', 'sec_technology', 'ta_rsi_os30'],
        table='Technical',  # 选择包含技术指标的表格
        rows=20
    )

# 策略2: 分步筛选
def get_combined_stocks_step_by_step():
    # 第一步: 基础筛选
    basic_result = get_screener_data(
        filters=['exch_nasd', 'sec_technology'],
        table='Overview',
        rows=100
    )
    
    # 第二步: 技术指标筛选
    technical_result = get_screener_data(
        filters=['ta_rsi_os30'],
        table='Technical',
        rows=20
    )
    
    return technical_result
```

## 常见问题解答

### Q1: 为什么 RSI 在 Overview 表格中显示为 "N/A"？

**A**: 因为 FinViz 将技术指标（包括 RSI）专门放在 Technical 表格中，Overview 表格不包含这些列。

### Q2: 是否有包含所有列的 "All" 类型表格？

**A**: 没有。FinViz 采用数据分离策略，将不同类型的指标分散在不同表格中，以提高性能和用户体验。

### Q3: 如何选择正确的表格类型？

**A**: 根据筛选器类型选择：
- 技术指标筛选器 → Technical
- 财务指标筛选器 → Financial/Valuation
- 基础筛选器 → Overview
- ETF筛选器 → ETF

### Q4: 可以同时使用多种表格类型吗？

**A**: 不可以。每次请求只能使用一种表格类型，但可以通过分步筛选的方式实现多类型筛选。

## 技术实现细节

### 1. 表格类型映射

```python
TABLE_TYPES = {
    "Overview": "111",
    "Valuation": "121",
    "Ownership": "131",
    "Performance": "141",
    "Custom": "152",
    "Financial": "161",
    "Technical": "171",
}
```

### 2. HTTP 请求参数

```python
payload = {
    "v": self._table,        # 表格类型代码
    "t": ",".join(self._tickers),
    "f": ",".join(self._filters),  # 筛选器列表
    "o": self._order,
    "s": self._signal,
    "c": ",".join(self._custom),
}
```

### 3. 响应数据结构

不同表格类型返回不同的列结构，但都包含基本的股票信息（Ticker, Company, Price等）。

## 总结

1. **FinViz 设计理念**: 数据分离，提高性能
2. **表格类型选择**: 根据筛选器类型自动选择
3. **技术指标**: 必须使用 Technical 表格类型
4. **最佳实践**: 明确筛选器类型，选择对应表格类型

这种设计虽然增加了使用复杂度，但提供了更好的性能和更清晰的数据组织方式。

---

*最后更新: 2025年1月17日*  
*基于 FinViz 网站实际测试结果*

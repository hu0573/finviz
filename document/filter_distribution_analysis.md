# FinViz 筛选器分布分析

## 概述

通过实际查看FinViz网站，发现了筛选器的真实分布情况。筛选器被分为5个主要表格类型：Descriptive、Fundamental、Technical、News、ETF。

## 筛选器分布详情

### 1. Descriptive 表格类型 (描述性筛选器)

**基础信息和市场数据筛选器**

| 筛选器名称 | 选项 | 说明 |
|------------|------|------|
| Exchange | Any | 交易所筛选 |
| Index | Any | 指数筛选 |
| Sector | Any | 行业板块筛选 |
| Industry | Any | 具体行业筛选 |
| Country | Any | 国家筛选 |
| Market Cap. | Any | 市值筛选 |
| Dividend Yield | Any | 股息收益率筛选 |
| Short Float | Any | 空头流通股筛选 |
| Analyst Recom. | Any | 分析师推荐筛选 |
| Option/Short | Any | 期权/做空筛选 |
| Earnings Date | Any | 财报日期筛选 |
| Average Volume | Any | 平均成交量筛选 |
| Relative Volume | Any | 相对成交量筛选 |
| Current Volume | Any | 当前成交量筛选 |
| Trades | Elite only | 交易量筛选（付费功能） |
| Price $ | Any | 股价筛选 |
| Target Price | Any | 目标价筛选 |
| IPO Date | Any | IPO日期筛选 |
| Shares Outstanding | Any | 总股本筛选 |
| Float | Any | 流通股筛选 |

**对应代码**: `v=111` (Overview)

### 2. Fundamental 表格类型 (基本面筛选器)

**财务和估值指标筛选器**

| 筛选器名称 | 选项 | 说明 |
|------------|------|------|
| P/E | Any | 市盈率筛选 |
| Forward P/E | Any | 前瞻市盈率筛选 |
| PEG | Any | PEG比率筛选 |
| P/S | Any | 市销率筛选 |
| P/B | Any | 市净率筛选 |
| Price/Cash | Any | 价格/现金比筛选 |
| Price/Free Cash Flow | Any | 价格/自由现金流比筛选 |
| EV/EBITDA | Any | 企业价值/EBITDA筛选 |
| EV/Sales | Any | 企业价值/销售额筛选 |
| Dividend Growth | Any | 股息增长筛选 |
| EPS Growth This Year | Any | 今年EPS增长筛选 |
| EPS Growth Next Year | Any | 明年EPS增长筛选 |
| EPS Growth Qtr Over Qtr | Any | 季度EPS增长筛选 |
| EPS Growth TTM | Any | 过去12个月EPS增长筛选 |
| EPS Growth Past 3 Years | Any | 过去3年EPS增长筛选 |
| EPS Growth Past 5 Years | Any | 过去5年EPS增长筛选 |
| EPS Growth Next 5 Years | Any | 未来5年EPS增长筛选 |
| Sales Growth Qtr Over Qtr | Any | 季度销售增长筛选 |
| Sales Growth TTM | Any | 过去12个月销售增长筛选 |
| Sales Growth Past 3 Years | Any | 过去3年销售增长筛选 |
| Sales Growth Past 5 Years | Any | 过去5年销售增长筛选 |
| Earnings & Revenue Surprise | Any | 盈利和收入惊喜筛选 |
| Return on Assets | Any | 资产回报率筛选 |
| Return on Equity | Any | 股本回报率筛选 |
| Return on Invested Capital | Any | 投资资本回报率筛选 |
| Current Ratio | Any | 流动比率筛选 |
| Quick Ratio | Any | 速动比率筛选 |
| LT Debt/Equity | Any | 长期债务/股本比筛选 |
| Debt/Equity | Any | 债务/股本比筛选 |
| Gross Margin | Any | 毛利率筛选 |
| Operating Margin | Any | 营业利润率筛选 |
| Net Profit Margin | Any | 净利润率筛选 |
| Payout Ratio | Any | 派息比率筛选 |
| Insider Ownership | Any | 内部持股筛选 |
| Insider Transactions | Any | 内部交易筛选 |
| Institutional Ownership | Any | 机构持股筛选 |
| Institutional Transactions | Any | 机构交易筛选 |

**对应代码**: `v=161` (Financial) 或 `v=121` (Valuation)

### 3. Technical 表格类型 (技术分析筛选器)

**技术指标和价格行为筛选器**

| 筛选器名称 | 选项 | 说明 |
|------------|------|------|
| Performance | Any | 表现筛选 |
| Performance 2 | Any | 表现筛选2 |
| Volatility | Any | 波动率筛选 |
| RSI (14) | Any | 相对强弱指数筛选 |
| Gap | Any | 跳空筛选 |
| 20-Day Simple Moving Average | Any | 20日简单移动平均筛选 |
| 50-Day Simple Moving Average | Any | 50日简单移动平均筛选 |
| 200-Day Simple Moving Average | Any | 200日简单移动平均筛选 |
| Change | Any | 变化筛选 |
| Change from Open | Any | 开盘变化筛选 |
| 20-Day High/Low | Any | 20日高低点筛选 |
| 50-Day High/Low | Any | 50日高低点筛选 |
| 52-Week High/Low | Any | 52周高低点筛选 |
| All-Time High/Low | Any | 历史高低点筛选 |
| Pattern | Any | 形态筛选 |
| Candlestick | Any | K线形态筛选 |
| Beta | Any | 贝塔系数筛选 |
| Average True Range | Any | 平均真实波幅筛选 |
| After-Hours Close | Any | 盘后收盘价筛选 |
| After-Hours Change | Any | 盘后变化筛选 |

**对应代码**: `v=171` (Technical)

### 4. News 表格类型 (新闻筛选器)

**新闻和事件筛选器**

| 筛选器名称 | 选项 | 说明 |
|------------|------|------|
| Latest News | Any | 最新新闻筛选 |
| News Keywords | Any | 新闻关键词筛选 |

**对应代码**: 可能是 `v=181` 或专门的新闻表格

### 5. ETF 表格类型 (ETF筛选器)

**ETF和基金相关筛选器**

| 筛选器名称 | 选项 | 说明 |
|------------|------|------|
| Single Category | Any | 单一类别筛选 |
| Asset Type | Any | 资产类型筛选 |
| ETF Type | Elite only | ETF类型筛选（付费功能） |
| Sector/Theme | Elite only | 板块/主题筛选（付费功能） |
| Region | Elite only | 地区筛选（付费功能） |
| Bond Type | Elite only | 债券类型筛选（付费功能） |
| Average Maturity | Elite only | 平均到期日筛选（付费功能） |
| Quant Type | Elite only | 量化类型筛选（付费功能） |
| Commodity Type | Elite only | 商品类型筛选（付费功能） |
| ESG Type | Elite only | ESG类型筛选（付费功能） |
| Dividend Type | Elite only | 股息类型筛选（付费功能） |
| Structure Type | Elite only | 结构类型筛选（付费功能） |
| Active/Passive | Elite only | 主动/被动筛选（付费功能） |
| Inverse/Leveraged | Elite only | 反向/杠杆筛选（付费功能） |
| Growth/Value | Elite only | 成长/价值筛选（付费功能） |
| Market Cap. (ETF) | Elite only | ETF市值筛选（付费功能） |
| Developed/Emerging | Elite only | 发达/新兴市场筛选（付费功能） |
| Currency | Elite only | 货币筛选（付费功能） |
| Index Weighting | Elite only | 指数权重筛选（付费功能） |
| Sponsor | Any | 发行商筛选 |
| Net Expense Ratio | Any | 净费用率筛选 |
| Net Fund Flows | Any | 净资金流向筛选 |
| Annualized Return | Any | 年化回报筛选 |
| Net Asset Value% | Elite only | 净资产价值百分比筛选（付费功能） |
| Tags | Any | 标签筛选 |
| Held By | Elite only | 持有者筛选（付费功能） |

**对应代码**: `v=181` (ETF)

## 表格类型映射更新

基于实际发现，更新表格类型映射：

```python
TABLE_TYPES = {
    "Descriptive": "111",    # 描述性筛选器
    "Fundamental": "161",    # 基本面筛选器 (Financial)
    "Technical": "171",      # 技术分析筛选器
    "News": "181",          # 新闻筛选器
    "ETF": "181",           # ETF筛选器
    # 兼容性映射
    "Overview": "111",      # 等同于Descriptive
    "Financial": "161",     # 等同于Fundamental
    "Valuation": "121",     # 估值筛选器（可能是Fundamental的子集）
    "Ownership": "131",     # 持股信息（可能是Descriptive的子集）
    "Performance": "141",   # 表现数据（可能是Technical的子集）
    "Custom": "152",        # 自定义列
}
```

## 筛选器前缀与表格类型对应关系

| 筛选器前缀 | 表格类型 | 说明 |
|------------|----------|------|
| `exch_*`, `idx_*`, `sec_*`, `ind_*`, `geo_*`, `cap_*` | Descriptive | 基础筛选器 |
| `fa_*` | Fundamental | 财务指标筛选器 |
| `ta_*` | Technical | 技术指标筛选器 |
| `n_*` | News | 新闻筛选器 |
| `etf_*` | ETF | ETF筛选器 |
| `sh_*` | Descriptive | 股票信息筛选器 |

## 最佳实践建议

### 1. 根据筛选器类型选择表格

```python
def get_optimal_table_type(filters):
    """根据筛选器类型自动选择最优表格类型"""
    for filter_id in filters:
        if filter_id.startswith('ta_'):
            return 'Technical'
        elif filter_id.startswith('fa_'):
            return 'Fundamental'
        elif filter_id.startswith('etf_'):
            return 'ETF'
        elif filter_id.startswith('n_'):
            return 'News'
        elif filter_id.startswith(('exch_', 'idx_', 'sec_', 'ind_', 'geo_', 'cap_', 'sh_')):
            return 'Descriptive'
    return 'Descriptive'  # 默认使用描述性表格
```

### 2. 组合筛选器策略

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
        table='Descriptive',
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

### 3. 付费功能处理

```python
def filter_elite_only_filters(filters):
    """过滤掉需要付费的筛选器"""
    elite_filters = [
        'trades', 'etf_type', 'sector_theme', 'region', 'bond_type',
        'average_maturity', 'quant_type', 'commodity_type', 'esg_type',
        'dividend_type', 'structure_type', 'active_passive', 'inverse_leveraged',
        'growth_value', 'market_cap_etf', 'developed_emerging', 'currency',
        'index_weighting', 'net_asset_value', 'held_by'
    ]
    
    return [f for f in filters if not any(elite in f for elite in elite_filters)]
```

## 重要发现总结

1. **筛选器分布清晰**: 5个主要表格类型覆盖了所有筛选器
2. **付费功能标识**: 明确标识了需要Elite账户的筛选器
3. **表格类型选择**: 可以根据筛选器类型自动选择最优表格类型
4. **兼容性保持**: 保持了与现有代码的兼容性

## 后续建议

1. **更新业务代码**: 根据新的表格类型映射更新代码
2. **优化筛选器选择**: 实现自动表格类型选择功能
3. **处理付费功能**: 添加付费功能检测和处理逻辑
4. **完善文档**: 更新所有相关文档以反映新的发现

---

*最后更新: 2025年1月17日*  
*基于FinViz网站实际筛选器分布*

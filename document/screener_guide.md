# FinViz 筛选器使用指南

## 概述

FinViz 筛选器是一个强大的股票筛选工具，支持 100+ 种筛选条件，可以帮助您快速找到符合特定投资标准的股票。本指南将详细介绍如何使用筛选器的各种功能。

## 快速开始

### 基本用法

```python
from core.finviz import FinVizService

# 创建服务实例
service = FinVizService()

# 基本筛选：获取 S&P 500 中的股票
filters = ['idx_sp500']
result = service.get_screener_data(filters=filters, rows=20)
print(f"找到 {result['total_rows']} 只股票")
```

### 获取所有可用筛选选项

```python
# 获取所有可用的筛选器选项
filter_options = service.get_filter_options()
print(filter_options)
```

## 筛选器类别详解

### 1. 交易所筛选 (Exchange)

筛选在特定交易所交易的股票。

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `exch_` | 所有交易所 |
| AMEX | `exch_amex` | 美国证券交易所 |
| CBOE | `exch_cboe` | 芝加哥期权交易所 |
| NASDAQ | `exch_nasd` | 纳斯达克 |
| NYSE | `exch_nyse` | 纽约证券交易所 |

**使用示例：**
```python
# 筛选纳斯达克股票
filters = ['exch_nasd']
result = service.get_screener_data(filters=filters)
```

### 2. 指数筛选 (Index)

筛选属于特定指数的股票。

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `idx_` | 所有指数 |
| S&P 500 | `idx_sp500` | 标准普尔500指数 |
| NASDAQ 100 | `idx_ndx` | 纳斯达克100指数 |
| DJIA | `idx_dji` | 道琼斯工业平均指数 |
| RUSSELL 2000 | `idx_rut` | 罗素2000指数 |

**使用示例：**
```python
# 筛选 S&P 500 中的科技股
filters = ['idx_sp500', 'sec_technology']
result = service.get_screener_data(filters=filters)
```

### 3. 行业板块筛选 (Sector)

按行业板块筛选股票。

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `sec_` | 所有行业 |
| Basic Materials | `sec_basicmaterials` | 基础材料 |
| Communication Services | `sec_communicationservices` | 通信服务 |
| Consumer Cyclical | `sec_consumercyclical` | 消费周期性 |
| Consumer Defensive | `sec_consumerdefensive` | 消费防御性 |
| Energy | `sec_energy` | 能源 |
| Financial | `sec_financial` | 金融 |
| Healthcare | `sec_healthcare` | 医疗保健 |
| Industrials | `sec_industrials` | 工业 |
| Real Estate | `sec_realestate` | 房地产 |
| Technology | `sec_technology` | 科技 |
| Utilities | `sec_utilities` | 公用事业 |

**使用示例：**
```python
# 筛选科技和金融板块
filters = ['sec_technology', 'sec_financial']
result = service.get_screener_data(filters=filters)
```

### 4. 具体行业筛选 (Industry)

按具体行业筛选股票。包含数百个具体行业，如：

- 广告代理 (Advertising Agencies)
- 航空航天与国防 (Aerospace & Defense)
- 农业投入品 (Agricultural Inputs)
- 航空公司 (Airlines)
- 机场与航空服务 (Airports & Air Services)
- 等等...

**使用示例：**
```python
# 筛选航空公司股票
filters = ['ind_airlines']
result = service.get_screener_data(filters=filters)
```

### 5. 市值筛选 (Market Cap)

按市值大小筛选股票。

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `cap_` | 所有市值 |
| Mega (>$200bln) | `cap_mega` | 超大型股 (>2000亿美元) |
| Large ($10bln to $200bln) | `cap_large` | 大型股 (100-2000亿美元) |
| Mid ($2bln to $10bln) | `cap_mid` | 中型股 (20-100亿美元) |
| Small ($300mln to $2bln) | `cap_small` | 小型股 (3-20亿美元) |
| Micro ($50mln to $300mln) | `cap_micro` | 微型股 (0.5-3亿美元) |
| Nano (<$50mln) | `cap_nano` | 纳米股 (<0.5亿美元) |

**使用示例：**
```python
# 筛选大型科技股
filters = ['cap_large', 'sec_technology']
result = service.get_screener_data(filters=filters)
```

### 6. 价格筛选 (Price)

按股票价格筛选。

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `price_` | 所有价格 |
| Under $1 | `sh_price_u1` | 低于1美元 |
| Under $2 | `sh_price_u2` | 低于2美元 |
| Under $5 | `sh_price_u5` | 低于5美元 |
| Under $10 | `sh_price_u10` | 低于10美元 |
| Under $15 | `sh_price_u15` | 低于15美元 |
| Under $20 | `sh_price_u20` | 低于20美元 |
| Under $30 | `sh_price_u30` | 低于30美元 |
| Under $40 | `sh_price_u40` | 低于40美元 |
| Under $50 | `sh_price_u50` | 低于50美元 |
| Over $1 | `sh_price_o1` | 高于1美元 |
| Over $2 | `sh_price_o2` | 高于2美元 |
| Over $5 | `sh_price_o5` | 高于5美元 |
| Over $10 | `sh_price_o10` | 高于10美元 |
| Over $15 | `sh_price_o15` | 高于15美元 |
| Over $20 | `sh_price_o20` | 高于20美元 |
| Over $30 | `sh_price_o30` | 高于30美元 |
| Over $40 | `sh_price_o40` | 高于40美元 |
| Over $50 | `sh_price_o50` | 高于50美元 |
| Between $1 and $5 | `sh_price_1to5` | 1-5美元之间 |
| Between $5 and $10 | `sh_price_5to10` | 5-10美元之间 |
| Between $10 and $15 | `sh_price_10to15` | 10-15美元之间 |
| Between $15 and $20 | `sh_price_15to20` | 15-20美元之间 |
| Between $20 and $30 | `sh_price_20to30` | 20-30美元之间 |
| Between $30 and $40 | `sh_price_30to40` | 30-40美元之间 |
| Between $40 and $50 | `sh_price_40to50` | 40-50美元之间 |
| Between $50 and $100 | `sh_price_50to100` | 50-100美元之间 |
| Over $100 | `sh_price_o100` | 高于100美元 |

**使用示例：**
```python
# 筛选价格在10-50美元之间的股票
filters = ['sh_price_10to50']
result = service.get_screener_data(filters=filters)
```

### 7. 财务指标筛选 (Financial)

#### 7.1 市盈率 (P/E)

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `fa_pe_` | 所有市盈率 |
| Low (<15) | `fa_pe_low` | 低市盈率 (<15) |
| Profitable (>0) | `fa_pe_profitable` | 盈利 (>0) |
| High (>50) | `fa_pe_high` | 高市盈率 (>50) |
| Under 5 | `fa_pe_u5` | 低于5 |
| Under 10 | `fa_pe_u10` | 低于10 |
| Under 15 | `fa_pe_u15` | 低于15 |
| Under 20 | `fa_pe_u20` | 低于20 |
| Under 25 | `fa_pe_u25` | 低于25 |
| Under 30 | `fa_pe_u30` | 低于30 |
| Under 35 | `fa_pe_u35` | 低于35 |
| Under 40 | `fa_pe_u40` | 低于40 |
| Under 45 | `fa_pe_u45` | 低于45 |
| Under 50 | `fa_pe_u50` | 低于50 |
| Over 5 | `fa_pe_o5` | 高于5 |
| Over 10 | `fa_pe_o10` | 高于10 |
| Over 15 | `fa_pe_o15` | 高于15 |
| Over 20 | `fa_pe_o20` | 高于20 |
| Over 25 | `fa_pe_o25` | 高于25 |
| Over 30 | `fa_pe_o30` | 高于30 |
| Over 35 | `fa_pe_o35` | 高于35 |
| Over 40 | `fa_pe_o40` | 高于40 |
| Over 45 | `fa_pe_o45` | 高于45 |
| Over 50 | `fa_pe_o50` | 高于50 |

#### 7.2 市净率 (P/B)

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `fa_pb_` | 所有市净率 |
| Under 1 | `fa_pb_u1` | 低于1 |
| Under 3 | `fa_pb_u3` | 低于3 |
| Under 5 | `fa_pb_u5` | 低于5 |
| Under 10 | `fa_pb_u10` | 低于10 |
| Under 15 | `fa_pb_u15` | 低于15 |
| Under 20 | `fa_pb_u20` | 低于20 |
| Under 25 | `fa_pb_u25` | 低于25 |
| Under 30 | `fa_pb_u30` | 低于30 |
| Over 1 | `fa_pb_o1` | 高于1 |
| Over 3 | `fa_pb_o3` | 高于3 |
| Over 5 | `fa_pb_o5` | 高于5 |
| Over 10 | `fa_pb_o10` | 高于10 |
| Over 15 | `fa_pb_o15` | 高于15 |
| Over 20 | `fa_pb_o20` | 高于20 |
| Over 25 | `fa_pb_o25` | 高于25 |
| Over 30 | `fa_pb_o30` | 高于30 |

#### 7.3 市销率 (P/S)

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `fa_ps_` | 所有市销率 |
| Under 1 | `fa_ps_u1` | 低于1 |
| Under 3 | `fa_ps_u3` | 低于3 |
| Under 5 | `fa_ps_u5` | 低于5 |
| Under 10 | `fa_ps_u10` | 低于10 |
| Under 15 | `fa_ps_u15` | 低于15 |
| Under 20 | `fa_ps_u20` | 低于20 |
| Under 25 | `fa_ps_u25` | 低于25 |
| Under 30 | `fa_ps_u30` | 低于30 |
| Over 1 | `fa_ps_o1` | 高于1 |
| Over 3 | `fa_ps_o3` | 高于3 |
| Over 5 | `fa_ps_o5` | 高于5 |
| Over 10 | `fa_ps_o10` | 高于10 |
| Over 15 | `fa_ps_o15` | 高于15 |
| Over 20 | `fa_ps_o20` | 高于20 |
| Over 25 | `fa_ps_o25` | 高于25 |
| Over 30 | `fa_ps_o30` | 高于30 |

#### 7.4 PEG比率

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `fa_peg_` | 所有PEG比率 |
| Under 1 | `fa_peg_u1` | 低于1 |
| Under 2 | `fa_peg_u2` | 低于2 |
| Under 3 | `fa_peg_u3` | 低于3 |
| Over 1 | `fa_peg_o1` | 高于1 |
| Over 2 | `fa_peg_o2` | 高于2 |
| Over 3 | `fa_peg_o3` | 高于3 |

#### 7.5 股息收益率 (Dividend Yield)

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `fa_div_` | 所有股息收益率 |
| None (0%) | `fa_div_none` | 无股息 |
| High (>5%) | `fa_div_high` | 高股息 (>5%) |
| Very High (>10%) | `fa_div_veryhigh` | 很高股息 (>10%) |
| Over 1% | `fa_div_o1` | 高于1% |
| Over 2% | `fa_div_o2` | 高于2% |
| Over 3% | `fa_div_o3` | 高于3% |
| Over 4% | `fa_div_o4` | 高于4% |
| Over 5% | `fa_div_o5` | 高于5% |
| Over 6% | `fa_div_o6` | 高于6% |
| Over 7% | `fa_div_o7` | 高于7% |
| Over 8% | `fa_div_o8` | 高于8% |
| Over 9% | `fa_div_o9` | 高于9% |
| Over 10% | `fa_div_o10` | 高于10% |

**使用示例：**
```python
# 筛选低市盈率、高股息收益率的股票
filters = ['fa_pe_low', 'fa_div_high']
result = service.get_screener_data(filters=filters)
```

### 8. 技术指标筛选 (Technical)

#### 8.1 相对强弱指数 (RSI)

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `ta_rsi_` | 所有RSI |
| Oversold (<30) | `ta_rsi_os30` | 超卖 (<30) |
| Overbought (>70) | `ta_rsi_ob70` | 超买 (>70) |
| Under 20 | `ta_rsi_u20` | 低于20 |
| Under 30 | `ta_rsi_u30` | 低于30 |
| Under 40 | `ta_rsi_u40` | 低于40 |
| Under 50 | `ta_rsi_u50` | 低于50 |
| Over 50 | `ta_rsi_o50` | 高于50 |
| Over 60 | `ta_rsi_o60` | 高于60 |
| Over 70 | `ta_rsi_o70` | 高于70 |
| Over 80 | `ta_rsi_o80` | 高于80 |

#### 8.2 移动平均线 (Moving Average)

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `ta_ma_` | 所有移动平均线 |
| Price above SMA20 | `ta_sma20_pa` | 价格高于20日简单移动平均线 |
| Price above SMA50 | `ta_sma50_pa` | 价格高于50日简单移动平均线 |
| Price above SMA200 | `ta_sma200_pa` | 价格高于200日简单移动平均线 |
| Price below SMA20 | `ta_sma20_pb` | 价格低于20日简单移动平均线 |
| Price below SMA50 | `ta_sma50_pb` | 价格低于50日简单移动平均线 |
| Price below SMA200 | `ta_sma200_pb` | 价格低于200日简单移动平均线 |
| SMA20 above SMA50 | `ta_sma20_sa50` | 20日SMA高于50日SMA |
| SMA50 above SMA200 | `ta_sma50_sa200` | 50日SMA高于200日SMA |
| SMA20 below SMA50 | `ta_sma20_sb50` | 20日SMA低于50日SMA |
| SMA50 below SMA200 | `ta_sma50_sb200` | 50日SMA低于200日SMA |

#### 8.3 52周高低点

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `ta_highlow52w_` | 所有52周高低点 |
| 0-10% from high | `ta_highlow52w_b0to10h` | 距离52周高点0-10% |
| 10% or more below High | `ta_highlow52w_b10h` | 距离52周高点10%以上 |
| 20% or more below High | `ta_highlow52w_b20h` | 距离52周高点20%以上 |
| 30% or more below High | `ta_highlow52w_b30h` | 距离52周高点30%以上 |
| 40% or more below High | `ta_highlow52w_b40h` | 距离52周高点40%以上 |
| 50% or more below High | `ta_highlow52w_b50h` | 距离52周高点50%以上 |
| 0-10% above Low | `ta_highlow52w_a0to10h` | 距离52周低点0-10% |
| 10% or more above Low | `ta_highlow52w_a10h` | 距离52周低点10%以上 |
| 20% or more above Low | `ta_highlow52w_a20h` | 距离52周低点20%以上 |
| 30% or more above Low | `ta_highlow52w_a30h` | 距离52周低点30%以上 |
| 40% or more above Low | `ta_highlow52w_a40h` | 距离52周低点40%以上 |
| 50% or more above Low | `ta_highlow52w_a50h` | 距离52周低点50%以上 |

**使用示例：**
```python
# 筛选技术面强势的股票：RSI超卖且价格高于50日移动平均线
filters = ['ta_rsi_os30', 'ta_sma50_pa']
result = service.get_screener_data(filters=filters)
```

### 9. 股票数量筛选 (Shares)

#### 9.1 流通股数量

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `sh_float_` | 所有流通股数量 |
| Under 10M | `sh_float_u10` | 低于1000万股 |
| Under 20M | `sh_float_u20` | 低于2000万股 |
| Under 50M | `sh_float_u50` | 低于5000万股 |
| Under 100M | `sh_float_u100` | 低于1亿股 |
| Under 200M | `sh_float_u200` | 低于2亿股 |
| Over 10M | `sh_float_o10` | 高于1000万股 |
| Over 20M | `sh_float_o20` | 高于2000万股 |
| Over 50M | `sh_float_o50` | 高于5000万股 |
| Over 100M | `sh_float_o100` | 高于1亿股 |
| Over 200M | `sh_float_o200` | 高于2亿股 |

#### 9.2 总股本

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `sh_outstanding_` | 所有总股本 |
| Under 10M | `sh_outstanding_u10` | 低于1000万股 |
| Under 20M | `sh_outstanding_u20` | 低于2000万股 |
| Under 50M | `sh_outstanding_u50` | 低于5000万股 |
| Under 100M | `sh_outstanding_u100` | 低于1亿股 |
| Under 200M | `sh_outstanding_u200` | 低于2亿股 |
| Over 10M | `sh_outstanding_o10` | 高于1000万股 |
| Over 20M | `sh_outstanding_o20` | 高于2000万股 |
| Over 50M | `sh_outstanding_o50` | 高于5000万股 |
| Over 100M | `sh_outstanding_o100` | 高于1亿股 |
| Over 200M | `sh_outstanding_o200` | 高于2亿股 |

#### 9.3 成交量

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `sh_curvol_` | 所有成交量 |
| Over 100K | `sh_curvol_o100` | 高于10万股 |
| Over 500K | `sh_curvol_o500` | 高于50万股 |
| Over 1M | `sh_curvol_o1000` | 高于100万股 |
| Over 2M | `sh_curvol_o2000` | 高于200万股 |
| Over 5M | `sh_curvol_o5000` | 高于500万股 |
| Over 10M | `sh_curvol_o10000` | 高于1000万股 |
| Over 20M | `sh_curvol_o20000` | 高于2000万股 |
| Over 50M | `sh_curvol_o50000` | 高于5000万股 |
| Over 100M | `sh_curvol_o100000` | 高于1亿股 |

#### 9.4 平均成交量

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `sh_avgvol_` | 所有平均成交量 |
| Over 100K | `sh_avgvol_o100` | 高于10万股 |
| Over 500K | `sh_avgvol_o500` | 高于50万股 |
| Over 1M | `sh_avgvol_o1000` | 高于100万股 |
| Over 2M | `sh_avgvol_o2000` | 高于200万股 |
| Over 5M | `sh_avgvol_o5000` | 高于500万股 |
| Over 10M | `sh_avgvol_o10000` | 高于1000万股 |
| Over 20M | `sh_avgvol_o20000` | 高于2000万股 |
| Over 50M | `sh_avgvol_o50000` | 高于5000万股 |
| Over 100M | `sh_avgvol_o100000` | 高于1亿股 |

**使用示例：**
```python
# 筛选高流动性的股票：平均成交量超过100万股
filters = ['sh_avgvol_o1000']
result = service.get_screener_data(filters=filters)
```

### 10. 模式筛选 (Pattern)

FinViz 提供技术分析模式识别。

| 选项 | 筛选代码 | 说明 |
|------|----------|------|
| Any | `ta_pattern_` | 所有模式 |
| Horizontal S/R | `ta_pattern_horizontal` | 水平支撑阻力 |
| Horizontal S/R (Strong) | `ta_pattern_horizontal2` | 水平支撑阻力（强） |
| TL Resistance | `ta_pattern_tlresistance` | 趋势线阻力 |
| TL Resistance (Strong) | `ta_pattern_tlresistance2` | 趋势线阻力（强） |
| TL Support | `ta_pattern_tlsupport` | 趋势线支撑 |
| TL Support (Strong) | `ta_pattern_tlsupport2` | 趋势线支撑（强） |
| Wedge Up | `ta_pattern_wedgeup` | 上升楔形 |
| Wedge Up (Strong) | `ta_pattern_wedgeup2` | 上升楔形（强） |
| Wedge Down | `ta_pattern_wedgedown` | 下降楔形 |
| Wedge Down (Strong) | `ta_pattern_wedgedown2` | 下降楔形（强） |
| Triangle Ascending | `ta_pattern_wedgeresistance` | 上升三角形 |
| Triangle Ascending (Strong) | `ta_pattern_wedgeresistance2` | 上升三角形（强） |
| Triangle Descending | `ta_pattern_wedgesupport` | 下降三角形 |
| Triangle Descending (Strong) | `ta_pattern_wedgesupport2` | 下降三角形（强） |
| Wedge | `ta_pattern_wedge` | 楔形 |
| Wedge (Strong) | `ta_pattern_wedge2` | 楔形（强） |
| Channel Up | `ta_pattern_channelup` | 上升通道 |
| Channel Up (Strong) | `ta_pattern_channelup2` | 上升通道（强） |
| Channel Down | `ta_pattern_channeldown` | 下降通道 |
| Channel Down (Strong) | `ta_pattern_channeldown2` | 下降通道（强） |
| Channel | `ta_pattern_channel` | 通道 |
| Channel (Strong) | `ta_pattern_channel2` | 通道（强） |
| Double Top | `ta_pattern_doubletop` | 双顶 |
| Double Bottom | `ta_pattern_doublebottom` | 双底 |
| Multiple Top | `ta_pattern_multipletop` | 多重顶 |
| Multiple Bottom | `ta_pattern_multiplebottom` | 多重底 |
| Head & Shoulders | `ta_pattern_headandshoulders` | 头肩顶 |
| Head & Shoulders Inverse | `ta_pattern_headandshouldersinv` | 头肩底 |

**使用示例：**
```python
# 筛选双底模式
filters = ['ta_pattern_doublebottom']
result = service.get_screener_data(filters=filters)
```

## 表格类型

筛选器支持多种表格类型，每种类型显示不同的数据列。

### 可用表格类型

| 表格类型 | 代码 | 说明 |
|----------|------|------|
| Overview | `Overview` | 概览（默认）- 显示基本信息 |
| Valuation | `Valuation` | 估值 - 显示估值指标 |
| Ownership | `Ownership` | 所有权 - 显示机构持股信息 |
| Performance | `Performance` | 表现 - 显示价格表现数据 |
| Financial | `Financial` | 财务 - 显示财务数据 |
| Technical | `Technical` | 技术 - 显示技术指标 |
| Custom | `Custom` | 自定义 - 用户自定义列 |

**使用示例：**
```python
# 使用估值表格类型
result = service.get_screener_data(
    filters=['idx_sp500'], 
    table='Valuation'
)
```

### 自定义列 (Custom)

当使用 `Custom` 表格类型时，可以指定要显示的列。

```python
# 自定义列示例
custom_columns = ['1', '21', '23', '45']  # 列编号
result = service.get_screener_data(
    filters=['idx_sp500'],
    table='Custom',
    custom=custom_columns
)
```

## 排序选项

### 排序语法

- 升序：`column_name`（如 `price`）
- 降序：`-column_name`（如 `-price`）

### 常用排序字段

| 字段 | 说明 |
|------|------|
| `ticker` | 股票代码 |
| `company` | 公司名称 |
| `sector` | 行业板块 |
| `industry` | 具体行业 |
| `country` | 国家 |
| `market_cap` | 市值 |
| `price` | 价格 |
| `change` | 涨跌幅 |
| `volume` | 成交量 |
| `pe` | 市盈率 |
| `pb` | 市净率 |
| `ps` | 市销率 |
| `peg` | PEG比率 |
| `dividend` | 股息收益率 |

**使用示例：**
```python
# 按市值降序排列
result = service.get_screener_data(
    filters=['idx_sp500'],
    order='-market_cap'
)

# 按价格升序排列
result = service.get_screener_data(
    filters=['idx_sp500'],
    order='price'
)
```

## 实际使用示例

### 示例1：寻找价值投资机会

```python
# 寻找低估值、高股息的大盘股
filters = [
    'idx_sp500',           # S&P 500
    'cap_large',           # 大型股
    'fa_pe_low',           # 低市盈率
    'fa_div_high',         # 高股息收益率
    'fa_pb_u3'             # 市净率低于3
]

result = service.get_screener_data(
    filters=filters,
    table='Valuation',
    order='-dividend',     # 按股息收益率降序
    rows=20
)

print(f"找到 {result['total_rows']} 只价值股")
for stock in result['data'][:5]:  # 显示前5只
    print(f"{stock['Ticker']}: {stock['Company']} - 股息: {stock.get('Dividend', 'N/A')}")
```

### 示例2：技术面筛选

```python
# 寻找技术面强势的股票
filters = [
    'ta_rsi_os30',         # RSI超卖
    'ta_sma50_pa',         # 价格高于50日移动平均线
    'ta_highlow52w_b0to10h', # 距离52周高点0-10%
    'sh_avgvol_o1000'      # 平均成交量超过100万股
]

result = service.get_screener_data(
    filters=filters,
    table='Technical',
    order='-change',       # 按涨跌幅降序
    rows=15
)

print(f"找到 {result['total_rows']} 只技术面强势股票")
```

### 示例3：成长股筛选

```python
# 寻找成长股
filters = [
    'sec_technology',      # 科技板块
    'cap_mid',             # 中型股
    'fa_pe_u25',           # 市盈率低于25
    'fa_peg_u2',           # PEG比率低于2
    'sh_avgvol_o500'       # 平均成交量超过50万股
]

result = service.get_screener_data(
    filters=filters,
    table='Financial',
    order='-market_cap',   # 按市值降序
    rows=25
)

print(f"找到 {result['total_rows']} 只成长股")
```

### 示例4：从URL获取筛选器

```python
# 从FinViz网站URL获取筛选器数据
url = "https://finviz.com/screener.ashx?v=111&f=idx_sp500,cap_large&o=-market_cap"
result = service.get_screener_from_url(url, rows=30)

print(f"从URL获取到 {result['total_rows']} 只股票")
```

### 示例5：组合多个筛选条件

```python
# 复杂的筛选条件组合
filters = [
    'exch_nasd',           # 纳斯达克
    'sec_technology',      # 科技板块
    'cap_mid',             # 中型股
    'sh_price_10to100',    # 价格10-100美元
    'fa_pe_u30',           # 市盈率低于30
    'fa_div_none',         # 不分红（成长股特征）
    'ta_rsi_nob70',        # RSI低于70（非超买）
    'sh_avgvol_o1000',     # 平均成交量超过100万股
    'sh_float_o50'         # 流通股超过5000万股
]

result = service.get_screener_data(
    filters=filters,
    table='Overview',
    order='-market_cap',
    rows=50
)

print(f"找到 {result['total_rows']} 只符合条件的科技股")
```

## 高级功能

### 1. 动态筛选器选项获取

```python
# 获取所有可用的筛选器选项
filter_options = service.get_filter_options()

# 查看特定类别的选项
if 'Market Cap' in filter_options:
    print("市值选项：")
    for option, code in filter_options['Market Cap'].items():
        print(f"  {option}: {code}")
```

### 2. 错误处理

```python
try:
    result = service.get_screener_data(filters=['invalid_filter'])
    if 'error' in result:
        print(f"筛选器错误: {result['error']}")
    else:
        print(f"成功获取 {result['total_rows']} 只股票")
except Exception as e:
    print(f"发生错误: {str(e)}")
```

### 3. 性能优化

```python
# 限制返回行数以提高性能
result = service.get_screener_data(
    filters=['idx_sp500'],
    rows=100  # 只返回前100只股票
)

# 使用合适的表格类型
result = service.get_screener_data(
    filters=['idx_sp500'],
    table='Overview'  # 使用概览表格，数据量较小
)
```

## 最佳实践

### 1. 筛选条件组合建议

- **价值投资**：低市盈率 + 高股息收益率 + 低市净率
- **成长投资**：科技板块 + 中等市值 + 合理估值
- **技术分析**：RSI指标 + 移动平均线 + 成交量
- **基本面分析**：财务指标 + 行业分析 + 市值筛选

### 2. 性能优化建议

- 合理设置 `rows` 参数，避免获取过多数据
- 使用 `Overview` 表格类型进行初步筛选
- 避免使用过于复杂的筛选条件组合
- 考虑使用缓存机制存储常用筛选结果

### 3. 数据验证

```python
# 验证筛选结果
result = service.get_screener_data(filters=['idx_sp500'])

if result['total_rows'] == 0:
    print("没有找到符合条件的股票")
elif result['total_rows'] > 1000:
    print("结果过多，建议添加更多筛选条件")
else:
    print(f"找到 {result['total_rows']} 只符合条件的股票")
    
    # 检查数据完整性
    if result['headers'] and result['data']:
        print("数据获取成功")
    else:
        print("数据获取失败")
```

## 常见问题

### Q1: 为什么筛选结果为空？

**可能原因：**
- 筛选条件过于严格
- 使用了无效的筛选代码
- 网络连接问题

**解决方案：**
```python
# 逐步放宽筛选条件
filters = ['idx_sp500']  # 先使用基本条件
result = service.get_screener_data(filters=filters)

if result['total_rows'] > 0:
    print("基本筛选成功，可以添加更多条件")
else:
    print("请检查筛选条件是否正确")
```

### Q2: 如何获取更多股票数据？

```python
# 增加返回行数
result = service.get_screener_data(
    filters=['idx_sp500'],
    rows=500  # 增加行数限制
)

# 或者分页获取
page1 = service.get_screener_data(filters=['idx_sp500'], rows=100)
# 可以添加排序条件来获取不同页面的数据
```

### Q3: 如何自定义显示列？

```python
# 使用自定义表格类型
custom_columns = ['1', '2', '3', '4', '5']  # 列编号
result = service.get_screener_data(
    filters=['idx_sp500'],
    table='Custom',
    custom=custom_columns
)
```

### Q4: 筛选器选项如何更新？

```python
# 重新加载筛选器选项
filter_options = service.get_filter_options()
# 这会自动从FinViz网站获取最新的筛选器选项
```

## 总结

FinViz 筛选器是一个功能强大的股票筛选工具，支持：

- **100+ 种筛选条件**：涵盖基本面、技术面、市场数据等各个方面
- **多种表格类型**：满足不同分析需求
- **灵活的排序选项**：按任意字段排序
- **自定义列显示**：根据需要显示特定数据
- **信号筛选**：预定义的技术分析信号
- **URL支持**：可以从FinViz网站URL直接获取筛选器

通过合理组合这些筛选条件，您可以快速找到符合特定投资策略的股票，提高投资决策效率。

记住，筛选器只是工具，最终的投资决策还需要结合深入的基本面分析、技术分析和市场研究。

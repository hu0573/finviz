# FinViz 筛选器内部逻辑详解

## 概述

本文档详细解释了 FinViz 筛选器系统的内部工作原理，包括筛选器ID的生成、存储格式、以及业务代码如何使用这些筛选器。

## 筛选器系统架构

### 1. 数据流向

```
FinViz 网站 HTML → 提取脚本 → filters.json → 业务代码 → HTTP 请求
```

### 2. 关键组件

- **HTML 源码**: FinViz 筛选器页面的原始 HTML
- **提取脚本**: `script/update_filters.py` - 从 HTML 提取筛选器数据
- **存储文件**: `core/finviz/filters.json` - 筛选器数据存储
- **业务代码**: `core/finviz/screener.py` - 使用筛选器发起请求

## 筛选器ID生成机制

### 1. HTML 结构分析

FinViz 筛选器页面的 HTML 结构如下：

```html
<td>
  <span class="screener-combo-title">Exchange</span>
</td>
<td>
  <select id="fs_exch" data-filter="exch" data-url="v=111&ft=4">
    <option value="">Any</option>
    <option value="amex">AMEX</option>
    <option value="nasd">NASDAQ</option>
    <option value="nyse">NYSE</option>
  </select>
</td>
```

### 2. 关键属性

- **`id`**: 筛选器元素的唯一标识符，格式为 `fs_xxx`
- **`data-filter`**: 筛选器类型标识符，这是生成筛选器ID的关键
- **`value`**: 选项的具体值
- **文本内容**: 用户看到的显示名称

### 3. 筛选器ID构建规则

筛选器ID的构建遵循以下规则：

```
完整筛选器ID = data-filter属性值 + "_" + option的value属性值
```

**示例**：
- `data-filter="exch"` + `value="nasd"` → `"exch_nasd"`
- `data-filter="idx"` + `value="sp500"` → `"idx_sp500"`
- `data-filter="sec"` + `value="technology"` → `"sec_technology"`

## 存储格式详解

### 1. filters.json 结构

```json
{
  "筛选器显示名称": {
    "选项显示名称": "完整筛选器ID",
    "选项显示名称2": "完整筛选器ID2"
  }
}
```

### 2. 实际示例

```json
{
  "Exchange": {
    "Any": "",
    "AMEX": "exch_amex",
    "CBOE": "exch_cboe",
    "NASDAQ": "exch_nasd",
    "NYSE": "exch_nyse",
    "Custom (Elite only)": "exch_modal"
  },
  "Index": {
    "Any": "",
    "S&P 500": "idx_sp500",
    "NASDAQ 100": "idx_ndx",
    "DJIA": "idx_dji",
    "RUSSELL 2000": "idx_rut",
    "Custom (Elite only)": "idx_modal"
  }
}
```

### 3. 特殊处理

- **"Any" 选项**: 通常对应空字符串 `""`，表示不应用该筛选器
- **"Custom (Elite only)" 选项**: 对应 `modal` 值，需要付费账户

## 业务代码使用流程

### 1. 筛选器加载

在 `screener.py` 的 `load_filter_dict()` 方法中：

```python
@staticmethod
def load_filter_dict(reload: bool = True) -> Dict:
    # 从 filters.json 加载筛选器数据
    with open(json_file, "r") as fp:
        return json.load(fp)
```

### 2. 筛选器应用

用户通过业务代码使用筛选器：

```python
# 用户友好的方式
screener = Screener(filters=['exch_nasd', 'idx_sp500'])

# 或者通过便捷函数
result = get_screener_data(filters=['exch_nasd', 'idx_sp500'])
```

### 3. HTTP 请求构建

在 `__search_screener()` 方法中：

```python
def __search_screener(self):
    self._page_content, self._url = http_request_get(
        "https://finviz.com/screener.ashx",
        payload={
            "v": self._table,
            "t": ",".join(self._tickers),
            "f": ",".join(self._filters),  # 直接使用完整筛选器ID
            "o": self._order,
            "s": self._signal,
            "c": ",".join(self._custom),
        },
        user_agent=self._user_agent,
    )
```

## 筛选器分类体系

### 1. 基础筛选器

| 前缀 | 含义 | 示例 |
|------|------|------|
| `exch` | 交易所 | `exch_nasd` (纳斯达克) |
| `idx` | 指数 | `idx_sp500` (标普500) |
| `sec` | 行业板块 | `sec_technology` (科技) |
| `ind` | 具体行业 | `ind_software` (软件) |
| `geo` | 地理位置 | `geo_usa` (美国) |
| `cap` | 市值 | `cap_large` (大盘股) |

### 2. 财务分析筛选器 (fa_*)

| 筛选器 | 含义 | 示例 |
|--------|------|------|
| `fa_pe` | 市盈率 | `fa_pe_low` (低市盈率) |
| `fa_fpe` | 前瞻市盈率 | `fa_fpe_high` (高前瞻市盈率) |
| `fa_peg` | PEG比率 | `fa_peg_under1` (PEG < 1) |
| `fa_ps` | 市销率 | `fa_ps_low` (低市销率) |
| `fa_pb` | 市净率 | `fa_pb_under1` (市净率 < 1) |
| `fa_roe` | 净资产收益率 | `fa_roe_high` (高ROE) |
| `fa_roa` | 总资产收益率 | `fa_roa_positive` (正ROA) |

### 3. 技术分析筛选器 (ta_*)

| 筛选器 | 含义 | 示例 |
|--------|------|------|
| `ta_sma20` | 20日移动平均 | `ta_sma20_above` (价格高于20日均线) |
| `ta_sma50` | 50日移动平均 | `ta_sma50_below` (价格低于50日均线) |
| `ta_sma200` | 200日移动平均 | `ta_sma200_above` (价格高于200日均线) |
| `ta_rsi` | 相对强弱指数 | `ta_rsi_oversold` (RSI超卖) |
| `ta_beta` | 贝塔系数 | `ta_beta_high` (高贝塔) |
| `ta_volatility` | 波动率 | `ta_volatility_high` (高波动率) |

### 4. 股票筛选器 (sh_*)

| 筛选器 | 含义 | 示例 |
|--------|------|------|
| `sh_price` | 股价 | `sh_price_under5` (股价 < $5) |
| `sh_float` | 流通股 | `sh_float_low` (低流通股) |
| `sh_outstanding` | 总股本 | `sh_outstanding_high` (高总股本) |
| `sh_avgvol` | 平均成交量 | `sh_avgvol_over2m` (平均成交量 > 200万) |
| `sh_curvol` | 当前成交量 | `sh_curvol_over1m` (当前成交量 > 100万) |
| `sh_relvol` | 相对成交量 | `sh_relvol_over2` (相对成交量 > 2) |

### 5. ETF筛选器 (etf_*)

| 筛选器 | 含义 | 示例 |
|--------|------|------|
| `etf_category` | ETF类别 | `etf_category_equity` (股票ETF) |
| `etf_assettype` | 资产类型 | `etf_assettype_stocks` (股票资产) |
| `etf_sponsor` | 发行商 | `etf_sponsor_ishares` (iShares) |
| `etf_netexpense` | 净费用率 | `etf_netexpense_low` (低费用率) |
| `etf_fundflows` | 资金流向 | `etf_fundflows_positive` (正资金流入) |
| `etf_return` | 收益率 | `etf_return_high` (高收益率) |

## 提取脚本工作原理

### 1. 关键修复

原始的 `update_filters.py` 脚本存在以下问题：
- 只提取了选项的 `value` 属性，没有获取 `data-filter` 属性
- 生成的筛选器ID不完整，无法被业务代码正确使用

### 2. 修复后的逻辑

```python
def extract_filters_from_html(self, html_content: str) -> Dict[str, Dict[str, str]]:
    # 查找所有筛选器select元素
    filter_selects = soup.find_all('select', {'id': re.compile(r'^fs_')})
    
    for select in filter_selects:
        # 获取筛选器的data-filter属性（关键修复）
        filter_name = select.get('data-filter', '')
        if not filter_name:
            continue
        
        # 获取筛选器显示名称
        filter_label = self._get_filter_label(select, soup)
        
        # 提取选项并构建完整筛选器ID
        options = {}
        option_elements = select.find_all('option')
        
        for option in option_elements:
            option_value = option.get('value', '')
            option_text = option.get_text(strip=True)
            
            # 构建完整的筛选器ID
            if option_value:
                full_filter_id = f"{filter_name}_{option_value}"
            else:
                full_filter_id = ""  # 空值保持为空
            
            options[option_text] = full_filter_id
        
        filters_data[filter_label] = options
```

### 3. 修复效果

**修复前**：
```json
{
  "Exchange": {
    "AMEX": "amex",
    "NASDAQ": "nasd"
  }
}
```

**修复后**：
```json
{
  "Exchange": {
    "AMEX": "exch_amex",
    "NASDAQ": "exch_nasd"
  }
}
```

## 实际使用示例

### 1. 基础筛选

```python
from core.finviz.screener import get_screener_data

# 筛选纳斯达克交易所的股票
result = get_screener_data(filters=['exch_nasd'])

# 筛选标普500成分股
result = get_screener_data(filters=['idx_sp500'])

# 筛选科技板块股票
result = get_screener_data(filters=['sec_technology'])
```

### 2. 组合筛选

```python
# 筛选纳斯达克交易所的科技股
result = get_screener_data(filters=['exch_nasd', 'sec_technology'])

# 筛选大盘股且市盈率低的股票
result = get_screener_data(filters=['cap_large', 'fa_pe_low'])

# 筛选高成交量且RSI超卖的股票
result = get_screener_data(filters=['sh_avgvol_over2m', 'ta_rsi_oversold'])
```

### 3. 复杂筛选

```python
# 筛选符合多个条件的股票
filters = [
    'exch_nasd',           # 纳斯达克交易所
    'sec_technology',      # 科技板块
    'cap_large',           # 大盘股
    'fa_pe_low',           # 低市盈率
    'fa_roe_high',         # 高净资产收益率
    'ta_sma20_above',      # 价格高于20日均线
    'sh_avgvol_over1m'     # 平均成交量超过100万
]

result = get_screener_data(filters=filters, rows=50)
```

## 调试和故障排除

### 1. 常见问题

**问题**: 筛选器不生效
**原因**: 筛选器ID格式不正确
**解决**: 检查 `filters.json` 中的筛选器ID是否包含正确的前缀

**问题**: 提取脚本报错
**原因**: HTML结构发生变化
**解决**: 更新脚本中的选择器或解析逻辑

**问题**: 业务代码返回空结果
**原因**: 筛选条件过于严格
**解决**: 放宽筛选条件或检查筛选器ID是否正确

### 2. 调试技巧

```python
# 1. 检查筛选器数据
from core.finviz.screener import get_filter_options
filters = get_filter_options()
print(filters['Exchange'])  # 查看交易所筛选器

# 2. 测试单个筛选器
result = get_screener_data(filters=['exch_nasd'], rows=5)
print(f"找到 {result['total_rows']} 只股票")

# 3. 逐步添加筛选条件
filters = ['exch_nasd']
result1 = get_screener_data(filters=filters, rows=5)
print(f"仅交易所筛选: {result1['total_rows']} 只")

filters.append('sec_technology')
result2 = get_screener_data(filters=filters, rows=5)
print(f"添加板块筛选: {result2['total_rows']} 只")
```

## 表格类型与筛选器

### 1. 表格类型选择

FinViz 将不同类型的指标分散在不同表格中，选择合适的表格类型对筛选器功能至关重要：

| 筛选器类型 | 推荐表格类型 | 说明 |
|------------|--------------|------|
| 技术指标 (`ta_*`) | Technical | RSI, SMA, Beta等技术指标 |
| 财务指标 (`fa_*`) | Financial/Valuation | P/E, ROE, 利润率等财务指标 |
| 基础筛选器 | Overview | 交易所、板块、市值等基础筛选 |
| 持股信息 (`sh_*`) | Ownership | 内部持股、机构持股等 |
| ETF筛选器 (`etf_*`) | ETF | ETF相关指标 |

### 2. 技术指标特殊处理

**重要**: 技术指标筛选器（如RSI）必须使用Technical表格类型：

```python
# ❌ 错误用法 - RSI显示为N/A
result = get_screener_data(filters=['ta_rsi_os30'], table='Overview')

# ✅ 正确用法 - RSI显示实际数值
result = get_screener_data(filters=['ta_rsi_os30'], table='Technical')
```

### 3. 自动表格类型选择

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
    return 'Overview'  # 默认使用Overview
```

## 最佳实践

### 1. 筛选器更新

- 定期运行 `script/update_filters.py` 更新筛选器数据
- 更新前备份现有的 `filters.json` 文件
- 测试更新后的筛选器功能是否正常

### 2. 表格类型选择

- 技术指标筛选器使用Technical表格类型
- 财务指标筛选器使用Financial表格类型
- 基础筛选器使用Overview表格类型
- 根据筛选器类型自动选择表格类型

### 3. 性能优化

- 避免使用过于严格的筛选条件
- 合理设置返回行数限制
- 使用异步请求方法处理大量数据
- 选择合适的表格类型减少数据传输

### 4. 错误处理

- 始终检查筛选器数据的完整性
- 提供有意义的错误信息
- 实现筛选器的验证机制
- 检查表格类型与筛选器的匹配性

## 总结

FinViz 筛选器系统通过以下机制实现：

1. **HTML 解析**: 从 FinViz 网站提取筛选器结构
2. **ID 生成**: 将 `data-filter` 和 `value` 组合成完整筛选器ID
3. **数据存储**: 以用户友好的格式存储在 `filters.json` 中
4. **业务使用**: 通过完整筛选器ID发起 HTTP 请求

这种设计既保证了用户界面的友好性，又确保了与 FinViz API 的兼容性。

---

*最后更新: 2025年1月17日*  
*基于 FinViz 网站: https://finviz.com/screener.ashx?v=111&ft=4*

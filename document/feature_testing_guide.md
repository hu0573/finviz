# FinViz Python API 功能详细测试指南

## 概述
本文档详细列出了FinViz Python API项目支持的所有功能，并对每个功能进行逐一测试，记录详细的测试结果。这将帮助我们了解当前项目的状态，并为后续的修复和改进提供指导。

## 测试环境
- **Python版本**: 3.13.2
- **操作系统**: macOS 15.0 (ARM64)
- **虚拟环境**: 已激活
- **依赖版本**: 已更新到兼容版本

---

## 1. 核心模块功能

### 1.1 模块导入功能
**功能描述**: 验证所有核心模块和类能够正常导入

**测试代码**:
```python
import finviz
from finviz.screener import Screener
from finviz.portfolio import Portfolio
from finviz.main_func import get_stock, get_news, get_all_news, get_insider, get_analyst_price_targets
```

**测试结果**: ✅ **通过**
- finviz 模块导入成功
- Screener 类导入成功
- Portfolio 类导入成功
- 主要功能函数导入成功

**状态**: 正常

---

## 2. 股票数据获取功能

### 2.1 获取单个股票信息 (get_stock)
**功能描述**: 获取指定股票的详细信息，包括价格、市值、P/E比等财务数据

**测试代码**:
```python
import finviz
stock_data = finviz.get_stock('AAPL')
```

**测试结果**: ❌ **失败**
- **错误信息**: `IndexError: list index out of range`
- **错误位置**: `main_func.py:35` - `title = page_parsed.cssselect('table[class="fullview-title"]')[0]`
- **原因分析**: FinViz网站结构发生变化，CSS选择器无法找到对应的元素
- **影响**: 无法获取股票基本信息
- **详细测试**: 实际测试确认错误，CSS选择器 `'table[class="fullview-title"]'` 无法找到元素

**状态**: 需要修复

### 2.2 获取内部交易信息 (get_insider)
**功能描述**: 获取指定股票的内部交易信息

**测试代码**:
```python
import finviz
insider_data = finviz.get_insider('AAPL')
```

**测试结果**: ⚠️ **部分可用**
- **实际结果**: 函数执行成功，返回空列表 `[]`
- **数据类型**: `<class 'list'>`
- **原因分析**: 虽然函数能执行，但可能由于网页结构变化或没有内部交易数据而返回空结果
- **影响**: 功能可用但无数据返回

**状态**: 需要进一步调查

### 2.3 获取分析师价格目标 (get_analyst_price_targets)
**功能描述**: 获取分析师对指定股票的价格目标和评级

**测试代码**:
```python
import finviz
analyst_data = finviz.get_analyst_price_targets('AAPL', last_ratings=5)
```

**测试结果**: ⚠️ **部分可用**
- **实际结果**: 函数执行成功，返回空列表 `[]`
- **数据类型**: `<class 'list'>`
- **原因分析**: 虽然函数能执行，但可能由于网页结构变化或没有分析师数据而返回空结果
- **影响**: 功能可用但无数据返回

**状态**: 需要进一步调查

---

## 3. 新闻功能

### 3.1 获取股票相关新闻 (get_news)
**功能描述**: 获取指定股票的相关新闻

**测试代码**:
```python
import finviz
news = finviz.get_news('AAPL')
```

**测试结果**: ❌ **失败**
- **错误信息**: `ValueError: time data '\n            Today 06:00AM\n      ' does not match format '%b-%d-%y %I:%M%p'`
- **错误位置**: `main_func.py:113` - 时间格式解析错误
- **原因分析**: 网页中的时间格式发生变化，从 `'%b-%d-%y %I:%M%p'` 变为 `'Today 06:00AM'` 格式
- **影响**: 无法正确解析新闻时间戳

**状态**: 需要修复时间格式解析

### 3.2 获取所有新闻 (get_all_news)
**功能描述**: 获取FinViz网站上的所有新闻

**测试代码**:
```python
import finviz
all_news = finviz.get_all_news()
```

**测试结果**: ⚠️ **部分可用**
- **实际结果**: 函数执行成功，返回空列表 `[]`
- **数据类型**: `<class 'list'>`
- **数据条数**: 0
- **原因分析**: 可能由于网页结构变化导致新闻数据无法正确解析
- **影响**: 功能可用但无数据返回

**状态**: 需要进一步调查

---

## 4. 股票筛选器功能

### 4.1 基本筛选器创建
**功能描述**: 创建股票筛选器对象，支持多种筛选条件

**测试代码**:
```python
from finviz.screener import Screener
screener = Screener(filters=['idx_sp500'], rows=5)
```

**测试结果**: ✅ **通过**
- 筛选器对象创建成功
- 能够设置筛选条件和行数限制
- 基本结构正常

**状态**: 正常

### 4.2 筛选器数据获取
**功能描述**: 获取筛选器返回的股票数据

**测试代码**:
```python
from finviz.screener import Screener
screener = Screener(filters=['idx_sp500'], rows=5)
data = screener.data
headers = screener.headers
```

**测试结果**: ⚠️ **部分可用**
- 能够获取数据列表，但表头为空 `[]`
- 数据行数正确，但内容可能不完整
- **原因分析**: 网页结构变化导致表头解析失败

**状态**: 需要修复

### 4.3 筛选器URL初始化
**功能描述**: 从URL字符串初始化筛选器

**测试代码**:
```python
from finviz.screener import Screener
url = "https://finviz.com/screener.ashx?v=111&f=idx_sp500&o=-ticker"
screener = Screener.init_from_url(url)
```

**测试结果**: ⚠️ **部分可用**
- **实际结果**: URL初始化成功，筛选器对象创建正常
- **筛选器行数**: 3 (符合预期)
- **表头**: `[]` (空列表)
- **数据行数**: 3 (符合预期)
- **原因分析**: URL解析正常，但数据解析有问题
- **影响**: 能创建筛选器但数据不完整

**状态**: 需要修复数据解析

### 4.4 筛选器数据导出 (to_csv)
**功能描述**: 将筛选器数据导出为CSV文件

**测试代码**:
```python
from finviz.screener import Screener
screener = Screener(filters=['idx_sp500'], rows=5)
screener.to_csv("test_output.csv")
```

**测试结果**: ✅ **可用**
- **实际结果**: CSV导出功能正常
- **CSV结果**: `None` (正常返回值)
- **文件创建**: 能够成功创建CSV文件
- **原因分析**: 导出功能本身正常，但由于数据解析问题，导出的内容可能不完整

**状态**: 基本可用，但需要修复数据解析

### 4.5 筛选器数据导出 (to_sqlite)
**功能描述**: 将筛选器数据导出为SQLite数据库

**测试代码**:
```python
from finviz.screener import Screener
screener = Screener(filters=['idx_sp500'], rows=5)
screener.to_sqlite("test_output.db")
```

**测试结果**: ❌ **失败**
- **错误信息**: `sqlite3.OperationalError: near ")": syntax error`
- **错误位置**: `save_data.py:58` - SQL创建语句语法错误
- **原因分析**: 由于表头为空列表，导致SQL CREATE语句语法错误
- **影响**: 无法创建SQLite数据库

**状态**: 需要修复SQL语句生成逻辑

### 4.6 图表下载功能 (get_charts)
**功能描述**: 下载筛选器中股票的图表

**测试代码**:
```python
from finviz.screener import Screener
screener = Screener(filters=['idx_sp500'], rows=3)
screener.get_charts(period='d', size='l', chart_type='c', ta='1')
```

**测试结果**: ❌ **未测试**
- 需要先解决数据解析问题

**状态**: 待测试

### 4.7 股票详情获取 (get_ticker_details)
**功能描述**: 获取筛选器中所有股票的详细信息

**测试代码**:
```python
from finviz.screener import Screener
screener = Screener(filters=['idx_sp500'], rows=3)
details = screener.get_ticker_details()
```

**测试结果**: ❌ **未测试**
- 需要先解决数据解析问题

**状态**: 待测试

### 4.8 筛选器过滤器字典加载
**功能描述**: 加载可用的筛选器选项字典

**测试代码**:
```python
from finviz.screener import Screener
filters = Screener.load_filter_dict()
```

**测试结果**: ❌ **失败**
- **错误信息**: `AttributeError: 'NoneType' object has no attribute 'get'`
- **错误位置**: `screener.py:277` - `filter_name = selections.get("data-filter").strip()`
- **原因分析**: 网页结构变化导致筛选器选项无法正确解析，`selections` 为 `None`
- **影响**: 无法获取可用的筛选器选项

**状态**: 需要修复网页解析逻辑

---

## 5. 投资组合功能

### 5.1 投资组合登录和初始化
**功能描述**: 登录FinViz并初始化投资组合对象

**测试代码**:
```python
from finviz.portfolio import Portfolio
portfolio = Portfolio('email@example.com', 'password', 'portfolio_name')
```

**测试结果**: ❌ **未测试**
- 需要真实的FinViz账户凭据
- 无法进行实际测试

**状态**: 需要真实凭据测试

### 5.2 投资组合数据获取
**功能描述**: 获取投资组合中的股票数据

**测试代码**:
```python
# 需要先成功登录
portfolio_data = portfolio.data
```

**测试结果**: ❌ **未测试**
- 依赖登录功能

**状态**: 需要真实凭据测试

### 5.3 从CSV创建投资组合
**功能描述**: 从CSV文件创建新的投资组合

**测试代码**:
```python
# 需要先成功登录
portfolio.create_portfolio('new_portfolio', 'portfolio.csv')
```

**测试结果**: ❌ **未测试**
- 依赖登录功能

**状态**: 需要真实凭据测试

---

## 6. 辅助功能

### 6.1 HTTP请求功能
**功能描述**: 发送HTTP请求到FinViz网站

**测试代码**:
```python
from finviz.helper_functions.request_functions import http_request_get
page_content, url = http_request_get("https://finviz.com", parse=False)
```

**测试结果**: ✅ **通过**
- HTTP请求功能正常
- 能够成功连接到FinViz网站
- 返回正确的页面内容

**状态**: 正常

### 6.2 异步连接器
**功能描述**: 使用异步方式发送多个HTTP请求

**测试代码**:
```python
from finviz.helper_functions.request_functions import Connector
# 需要更多测试代码
```

**测试结果**: ❌ **失败**
- **错误信息**: `AttributeError: 'bytes' object has no attribute 'text'`
- **错误位置**: 异步请求处理函数中
- **原因分析**: 异步连接器返回的是bytes对象，但测试代码期望的是Response对象
- **影响**: 异步连接器功能需要正确的处理函数

**状态**: 需要修复处理函数

### 6.3 数据保存功能
**功能描述**: 将数据保存为CSV或SQLite格式

**测试代码**:
```python
from finviz.helper_functions.save_data import export_to_csv, export_to_db
# 需要测试数据
```

**测试结果**: ✅ **可用**
- **CSV保存**: 功能正常，能够成功创建CSV文件
- **SQLite保存**: 功能正常，能够成功创建SQLite数据库
- **测试数据**: 使用标准测试数据验证功能正常
- **影响**: 数据保存功能完全可用

**状态**: 正常

### 6.4 错误处理功能
**功能描述**: 处理各种异常情况

**测试代码**:
```python
from finviz.helper_functions.error_handling import NoResults, InvalidTableType
# 测试异常类
```

**测试结果**: ✅ **通过**
- 异常类定义正确
- 能够正常导入和使用

**状态**: 正常

---

## 7. 配置功能

### 7.1 连接配置
**功能描述**: 配置连接参数

**测试代码**:
```python
from finviz.config import connection_settings
print(connection_settings)
```

**测试结果**: ✅ **通过**
- 配置参数正确加载
- 默认值合理

**状态**: 正常

---

## 测试总结

### 功能状态统计
- **✅ 正常功能**: 6个
- **⚠️ 部分可用**: 5个  
- **❌ 需要修复**: 7个
- **❌ 未测试**: 3个

### 详细测试结果

#### ✅ 正常功能 (6个)
1. **模块导入功能** - 所有核心模块正常导入
2. **HTTP请求功能** - 网络请求功能正常
3. **筛选器基本创建** - 能够创建筛选器对象
4. **筛选器CSV导出** - CSV导出功能正常
5. **数据保存功能** - CSV和SQLite保存功能正常
6. **错误处理功能** - 异常类定义正确

#### ⚠️ 部分可用功能 (5个)
1. **get_insider** - 函数执行成功但返回空数据
2. **get_analyst_price_targets** - 函数执行成功但返回空数据
3. **get_all_news** - 函数执行成功但返回空数据
4. **筛选器数据获取** - 能获取数据但表头为空
5. **筛选器URL初始化** - URL解析正常但数据解析有问题

#### ❌ 需要修复功能 (7个)
1. **get_stock** - CSS选择器失效
2. **get_news** - 时间格式解析错误
3. **筛选器SQLite导出** - SQL语句语法错误
4. **筛选器过滤器字典加载** - 网页解析失败
5. **异步连接器** - 处理函数类型错误
6. **图表下载功能** - 依赖数据解析问题
7. **股票详情获取** - 依赖数据解析问题

### 主要问题分析
1. **网页结构变化**: FinViz网站结构发生变化，导致CSS选择器失效
2. **时间格式变化**: 新闻时间格式从 `'%b-%d-%y %I:%M%p'` 变为 `'Today 06:00AM'` 格式
3. **数据解析失败**: 表头解析失败，导致后续数据处理问题
4. **SQL语句错误**: 空表头导致SQL CREATE语句语法错误

### 修复优先级
1. **高优先级**: 
   - 修复get_stock功能的CSS选择器
   - 修复筛选器表头解析
   - 修复get_news的时间格式解析

2. **中优先级**: 
   - 修复筛选器SQLite导出
   - 修复筛选器过滤器字典加载
   - 修复异步连接器处理函数

3. **低优先级**: 
   - 完善未测试功能
   - 增强错误处理
   - 优化性能

### 下一步计划
1. **分析FinViz网站当前结构** - 检查CSS选择器和HTML结构
2. **更新CSS选择器** - 适配新的网页结构
3. **修复时间格式解析** - 支持新的时间格式
4. **修复数据解析逻辑** - 确保表头和数据正确解析
5. **增强错误处理** - 添加更好的异常处理机制
6. **完善测试覆盖** - 添加更多测试用例

### 修复建议
1. **使用浏览器开发者工具** 检查FinViz网站当前结构
2. **实现多种时间格式支持** 处理不同的时间格式
3. **添加数据验证** 确保解析的数据完整性
4. **实现降级处理** 当主要功能失败时提供备用方案
5. **添加详细日志** 便于调试和问题定位

---

*本文档将随着测试和修复的进展持续更新*

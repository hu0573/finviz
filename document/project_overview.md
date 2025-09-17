# FinViz Python API 项目整体情况

## 项目概述

这是一个非官方的 Python API，用于从 FinViz 网站获取金融数据。FinViz 是一个提供市场信息可视化的金融网站，为交易者和投资者提供股票、期货和外汇对的数据分析工具。

## 项目基本信息

- **项目名称**: finviz-platform
- **版本**: 0.0.1
- **作者**: Alberto Rincones (code4road@gmail.com)
- **描述**: Finviz 爬虫，具有额外的数据科学功能
- **Python 版本要求**: >= 3.8
- **许可证**: 见 LICENSE 文件

## 项目结构

```
finviz/
├── __init__.py                 # 主模块入口，导出核心功能
├── config.py                   # 连接配置设置
├── main_func.py                # 主要功能函数（股票数据、新闻、分析师评级等）
├── screener.py                 # 股票筛选器类
├── portfolio.py                # 投资组合管理类
├── helper_functions/           # 辅助功能模块
│   ├── __init__.py
│   ├── display_functions.py    # 显示功能
│   ├── error_handling.py       # 错误处理
│   ├── request_functions.py    # HTTP 请求功能
│   ├── save_data.py           # 数据保存功能
│   └── scraper_functions.py   # 网页抓取功能
└── tests/                      # 测试文件
    └── test_screener.py       # 筛选器测试
```

## 核心功能模块

### 1. 主要功能 (main_func.py)
- **get_stock(ticker)**: 获取单个股票的详细数据
- **get_insider(ticker)**: 获取内部交易信息
- **get_news(ticker)**: 获取股票相关新闻
- **get_all_news()**: 获取所有新闻
- **get_analyst_price_targets(ticker)**: 获取分析师价格目标
- **get_crypto(pair)**: 获取加密货币数据

### 2. 股票筛选器 (screener.py)
- **Screener 类**: 从 FinViz 筛选器获取股票数据
- 支持多种筛选条件（市值、行业、技术指标等）
- 支持多种表格类型（概览、估值、所有权、表现等）
- 支持数据导出（CSV、SQLite）
- 支持图表下载
- 支持异步和顺序请求模式

### 3. 投资组合管理 (portfolio.py)
- **Portfolio 类**: 管理 FinViz 投资组合
- 支持登录和认证
- 支持从 CSV 文件创建投资组合
- 支持投资组合数据获取和显示

### 4. 辅助功能模块

#### 请求功能 (request_functions.py)
- HTTP 请求处理
- 异步连接器
- 重试机制
- 用户代理管理

#### 抓取功能 (scraper_functions.py)
- 表格数据提取
- 页面 URL 生成
- 图表图片下载
- 分析师评级数据提取

#### 错误处理 (error_handling.py)
- 自定义异常类
- 连接超时处理
- 无效数据验证

## 依赖项

### 核心依赖
- **lxml**: XML/HTML 解析
- **requests**: HTTP 请求库
- **aiohttp**: 异步 HTTP 客户端
- **beautifulsoup4**: HTML 解析
- **urllib3**: URL 处理
- **cssselect**: CSS 选择器
- **user_agent**: 用户代理生成
- **tqdm**: 进度条显示
- **tenacity**: 重试机制

### 开发依赖
- **wheel**: 包构建工具
- **setuptools**: 包管理工具

## 主要特性

### 1. 数据获取能力
- 股票基本信息（价格、市值、P/E 比等）
- 技术指标数据
- 财务数据
- 新闻和分析师评级
- 内部交易信息
- 加密货币数据

### 2. 筛选功能
- 支持 100+ 种筛选条件
- 多种排序选项
- 自定义表格列
- 信号筛选

### 3. 数据导出
- CSV 格式导出
- SQLite 数据库导出
- 图表图片下载

### 4. 性能优化
- 异步请求支持
- 连接池管理
- 重试机制
- 进度显示

## 使用示例

### 基本股票筛选
```python
from finviz.screener import Screener

# 筛选 S&P 500 中的股票
filters = ['idx_sp500']
stock_list = Screener(filters=filters, order='ticker')
print(stock_list)

# 导出到 CSV
stock_list.to_csv("sp500.csv")
```

### 获取股票详情
```python
import finviz

# 获取苹果股票信息
stock_data = finviz.get_stock('AAPL')
print(stock_data)

# 获取新闻
news = finviz.get_news('AAPL')
print(news)
```

### 投资组合管理
```python
from finviz.portfolio import Portfolio

# 登录并获取投资组合
portfolio = Portfolio('email@example.com', 'password', 'portfolio_name')
print(portfolio)
```

## 测试覆盖

项目包含单元测试，主要测试：
- 筛选器功能稳定性
- 数据获取准确性
- 异步请求处理
- 错误处理机制

## 配置选项

### 连接设置 (config.py)
- 并发连接数: 30
- 连接超时: 30秒

### 环境变量
- `DISABLE_TQDM=1`: 禁用进度条显示

## 注意事项

### 重要限制
1. **数据延迟**: FinViz 数据有延迟（NASDAQ 15分钟，NYSE/AMEX 20分钟）
2. **使用目的**: 仅用于金融分析、研究和数据抓取，不应用于实时交易
3. **服务条款**: 使用此库获取 FinViz 数据违反其服务条款和 robots.txt

### 安全考虑
- 使用 HTTPS 请求
- 禁用 SSL 警告（仅用于开发环境）
- 实现请求频率限制

## 项目状态

- **开发状态**: 活跃维护
- **测试状态**: 有基本单元测试
- **文档状态**: 有 README 和代码注释
- **版本控制**: 使用 Git

## 潜在改进建议

### 性能优化
1. 实现更智能的缓存机制
2. 优化异步请求的并发控制
3. 添加数据压缩支持

### 功能增强
1. 添加更多数据源支持
2. 实现实时数据流
3. 添加数据验证和清洗功能

### 安全改进
1. 实现更严格的请求频率限制
2. 添加用户认证和授权
3. 实现数据加密存储

### 代码质量
1. 增加测试覆盖率
2. 添加类型注解
3. 实现更好的错误处理和日志记录

## 总结

这是一个功能完整的 FinViz 数据抓取库，提供了丰富的金融数据获取和分析功能。项目结构清晰，代码组织良好，具有良好的可扩展性。虽然存在一些使用限制和安全考虑，但对于金融数据分析和研究来说是一个有价值的工具。

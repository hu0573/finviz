# FinViz Python API 项目整体情况

## 项目概述

这是一个为MCP（Model Context Protocol）集成而设计的FinViz Python API项目。该项目专注于从FinViz网站获取核心金融数据，提供股票数据获取和股票筛选器功能。项目采用现代化的架构设计，作为金融数据模块整合到更大的MCP项目中。

## 项目基本信息

- **项目名称**: finviz-platform
- **版本**: 0.0.1
- **作者**: Alberto Rincones (code4road@gmail.com)
- **描述**: 为MCP集成优化的FinViz数据获取模块
- **Python 版本要求**: >= 3.8
- **许可证**: 见 LICENSE 文件
- **项目目标**: MCP集成准备，提供标准化的JSON格式金融数据

## MCP集成背景

### 什么是MCP？
MCP（Model Context Protocol）是一个开放标准，用于连接AI助手与外部数据源和工具。它允许AI模型安全地访问和操作各种外部资源。

### 项目在MCP生态系统中的角色
此FinViz Python API项目将作为**金融数据模块**整合到更大的MCP项目中，为AI助手提供：

- **实时股票数据获取**：通过MCP协议为AI提供股票基本信息、价格、财务数据等
- **股票筛选和分析**：支持复杂的筛选条件，帮助AI进行股票分析和推荐
- **新闻和市场信息**：提供最新的股票相关新闻和分析师评级
- **标准化数据接口**：所有数据以JSON格式返回，便于MCP协议传输

### 集成优势
- **模块化设计**：独立的金融数据模块，易于集成和维护
- **标准化输出**：统一的JSON格式，与MCP协议完美兼容
- **高性能**：异步请求支持，满足MCP的实时性要求
- **错误处理**：完善的异常处理机制，确保MCP服务的稳定性

## 项目结构

### MCP架构整合后的结构
```
core/finviz/
├── __init__.py                 # 模块入口，只暴露FinVizService
├── finviz_service.py           # 唯一入口文件（门面类）
├── stock_data.py               # 股票数据功能（整合原main_func.py）
├── screener.py                 # 筛选器功能（整合原screener.py）
├── config.py                   # 连接配置设置
├── filters.json                # 筛选器选项数据
├── helper_functions/           # 辅助功能模块
│   ├── __init__.py
│   ├── display_functions.py    # 显示功能
│   ├── error_handling.py       # 错误处理
│   ├── request_functions.py    # HTTP 请求功能
│   └── scraper_functions.py   # 网页抓取功能
└── tests/                      # 测试文件
    └── test_screener.py       # 筛选器测试
```

### 架构设计亮点
- ✅ **单一入口**: `finviz_service.py` 作为唯一入口，命名清晰
- ✅ **功能整合**: 直接整合核心功能，架构简洁高效
- ✅ **结构清晰**: 3个核心文件，职责明确
- ✅ **MCP兼容**: 完全符合MCP架构规范

## 核心功能模块

### 1. 门面服务 (finviz_service.py)
- **FinVizService 类**: 统一入口，整合所有FinViz功能
- **get_stock(ticker)**: 获取单个股票的详细数据 ✅
- **get_news(ticker)**: 获取股票相关新闻 ✅
- **get_insider(ticker)**: 获取内部交易信息 ✅
- **get_analyst_price_targets(ticker)**: 获取分析师价格目标 ✅
- **get_all_news()**: 获取所有新闻 ✅
- **get_screener_data()**: 获取筛选器数据 ✅
- **get_stock_analysis()**: 获取股票完整分析 ✅

### 2. 股票数据功能 (stock_data.py)
- **get_stock(ticker)**: 获取单个股票的详细数据 ✅
- **get_insider(ticker)**: 获取内部交易信息 ✅
- **get_news(ticker)**: 获取股票相关新闻 ✅
- **get_all_news()**: 获取所有新闻 ✅
- **get_analyst_price_targets(ticker)**: 获取分析师价格目标 ✅
- **get_crypto(pair)**: 获取加密货币数据 ✅

### 3. 股票筛选器 (screener.py)
- **Screener 类**: 从 FinViz 筛选器获取股票数据 ✅
- **get_screener_data()**: 便捷筛选器数据获取 ✅
- **get_screener_from_url()**: 从URL获取筛选器数据 ✅
- **get_filter_options()**: 获取筛选器选项 ✅
- 支持多种筛选条件（市值、行业、技术指标等）✅
- 支持多种表格类型（概览、估值、所有权、表现等）✅
- 支持异步和顺序请求模式 ✅

### 4. 辅助功能模块

#### 请求功能 (request_functions.py)
- HTTP 请求处理 ✅
- 异步连接器 ✅
- 重试机制 ✅
- 用户代理管理 ✅

#### 抓取功能 (scraper_functions.py)
- 表格数据提取 ✅
- 页面 URL 生成 ✅
- 分析师评级数据提取 ✅

#### 错误处理 (error_handling.py)
- 自定义异常类 ✅
- 连接超时处理 ✅
- 无效数据验证 ✅

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
- 股票基本信息（价格、市值、P/E 比等）✅
- 技术指标数据 ✅
- 财务数据 ✅
- 新闻和分析师评级 ✅
- 内部交易信息 ✅

### 2. 筛选功能
- 支持 100+ 种筛选条件 ✅
- 多种排序选项 ✅
- 自定义表格列 ✅
- 信号筛选 ✅

### 3. MCP集成特性
- 标准化的JSON格式数据输出
- 无文件操作依赖
- 优化的错误处理机制
- 为MCP协议优化的API接口

### 4. 性能优化
- 异步请求支持 ✅
- 连接池管理 ✅
- 重试机制 ✅
- 进度显示 ✅

## 使用示例

### 基本股票筛选
```python
from core.finviz import FinVizService

service = FinVizService()

# 筛选 S&P 500 中的股票
filters = ['idx_sp500']
screener_data = service.get_screener_data(filters=filters, rows=20)
print(screener_data)  # 返回JSON格式数据

# 或者使用其他筛选条件
filters = ['idx_sp500', 'sec_technology']
screener_data = service.get_screener_data(filters=filters, rows=10)
print(screener_data)  # 返回JSON格式数据
```

### 获取股票详情
```python
from core.finviz import FinVizService

service = FinVizService()

# 获取苹果股票信息
stock_data = service.get_stock('AAPL')
print(stock_data)  # 返回JSON格式数据

# 获取新闻
news = service.get_news('AAPL')
print(news)  # 返回JSON格式数据

# 获取完整分析
analysis = service.get_stock_analysis('AAPL')
print(analysis)  # 包含股票、新闻、内部交易、分析师评级
```

### MCP集成示例
```python
# 在MCP服务器中使用
from core.finviz import FinVizService

def get_financial_data(ticker: str) -> dict:
    """MCP函数：获取股票数据"""
    try:
        service = FinVizService()
        stock_data = service.get_stock(ticker)
        news_data = service.get_news(ticker)
        return {
            "stock": stock_data,
            "news": news_data,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }

# 或者使用组合功能
def get_complete_analysis(ticker: str) -> dict:
    """MCP函数：获取完整股票分析"""
    try:
        service = FinVizService()
        analysis = service.get_stock_analysis(ticker)
        return {
            "analysis": analysis,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
```

## 测试覆盖

项目包含单元测试，主要测试：
- 筛选器功能稳定性 ✅
- 数据获取准确性 ✅
- 异步请求处理 ✅
- 错误处理机制 ✅
- 架构兼容性 ✅
- MCP集成功能 ✅

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

- **开发状态**: ✅ 核心功能完成，已准备好用于MCP集成
- **测试状态**: ✅ 所有功能通过全面测试
- **文档状态**: ✅ 完整，包含使用指南和集成说明
- **版本控制**: 使用 Git
- **MCP集成状态**: ✅ 已完成，所有核心功能正常工作


## 总结

这是一个为MCP集成而设计的FinViz数据抓取库，专注于核心的股票数据获取和筛选器功能。项目采用现代化的架构设计，完全符合MCP规范。

**项目特色**：
- **单一入口设计**：`finviz_service.py`作为唯一入口，使用简单
- **功能整合优化**：直接整合核心功能，减少调用链，提高性能
- **MCP完美兼容**：标准化的JSON数据输出格式，完善的错误处理机制
- **代码质量优秀**：完善的类型注解、文档字符串和测试覆盖

**架构优势**：
- 简洁高效的文件结构，职责明确
- 统一的API接口，易于集成和使用
- 灵活的筛选功能，满足不同使用场景
- 完善的错误处理机制，确保服务稳定性

此项目为MCP生态系统提供了强大而优雅的金融数据获取能力，是金融数据模块的理想选择。

## 相关文档

更多技术细节和开发指南请参考：
- 📖 [修复心得与经验总结](./repair_insights.md) - 包含完整的技术方法论、具体案例分析和未来维护指南
- 📖 [重构总结](./REFACTOR_SUMMARY.md) - 详细的架构设计和实现总结

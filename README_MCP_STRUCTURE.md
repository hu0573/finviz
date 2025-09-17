# FinViz MCP架构重构说明

## 概述

本项目已按照MCP（Model Context Protocol）架构进行了重构，将FinViz功能整合到标准的MCP服务结构中。

## 新架构结构

```
finviz/
├── core/                           # 核心业务层
│   ├── __init__.py
│   └── finviz/                     # FinViz服务模块
│       ├── __init__.py
│       ├── finviz_service.py       # 门面类，统一暴露所有功能
│       ├── stock_data_service.py   # 股票数据服务
│       ├── screener_service.py     # 股票筛选服务
│       └── [原有文件]              # 保持原有的实现文件
├── document/                       # 文档目录
├── test_new_structure.py          # 新架构测试文件
└── [其他文件]                      # 保持原有结构
```

## 服务层设计

### 1. StockDataService (股票数据服务)
负责所有股票数据获取功能：
- `get_stock(ticker)` - 获取股票详细信息
- `get_news(ticker)` - 获取股票新闻
- `get_insider(ticker)` - 获取内部交易信息
- `get_analyst_price_targets(ticker)` - 获取分析师评级
- `get_all_news()` - 获取所有新闻

### 2. ScreenerService (筛选服务)
负责所有股票筛选功能：
- `get_screener_data()` - 通用筛选器数据获取
- `get_screener_from_url()` - 从URL初始化筛选器
- `get_filter_options()` - 获取筛选器选项
- `get_sp500_stocks()` - 获取S&P 500股票
- `get_technology_stocks()` - 获取科技股
- `get_high_volume_stocks()` - 获取高成交量股票
- `get_oversold_stocks()` - 获取超卖股票
- `get_overbought_stocks()` - 获取超买股票

### 3. FinVizService (门面类)
统一封装所有FinViz功能，提供：
- 所有股票数据获取方法
- 所有筛选器方法
- 组合功能方法（如`get_stock_analysis()`）

## 使用方法

### 基本使用
```python
from core.finviz import FinVizService

# 初始化服务
service = FinVizService()

# 获取股票数据
stock_data = service.get_stock('AAPL')
print(f"苹果股价: ${stock_data['Price']}")

# 获取新闻
news = service.get_news('AAPL')
print(f"新闻数量: {len(news)}")

# 获取S&P 500股票
sp500 = service.get_sp500_stocks(10)
print(f"S&P 500股票数: {len(sp500['data'])}")
```

### 高级使用
```python
# 获取完整股票分析
analysis = service.get_stock_analysis('AAPL')
print(f"新闻数: {analysis['summary']['news_count']}")
print(f"分析师评级数: {analysis['summary']['analyst_count']}")

# 自定义筛选
custom_screener = service.get_screener_data(
    filters=['sec_technology', 'ta_rsi_os30'],  # 科技股且RSI超卖
    rows=20,
    order='-volume'  # 按成交量降序
)
```

## 与MCP项目集成

### 1. 目录结构集成
将`core/finviz/`目录复制到MCP项目的`core/`目录下，与`yfinance`和`tiger`同级。

### 2. 主服务集成
在MCP项目的`main_service.py`中添加：
```python
from core.finviz import FinVizService

class StockService:
    def __init__(self):
        # ... 其他服务初始化
        self.finviz_service = FinVizService()
    
    # 暴露FinViz方法
    def get_finviz_stock(self, ticker: str):
        return self.finviz_service.get_stock(ticker)
    
    def get_finviz_screener(self, filters: List[str], rows: int = 20):
        return self.finviz_service.get_screener_data(filters=filters, rows=rows)
    
    # ... 其他方法
```

### 3. 帮助文档生成
运行帮助文档生成脚本，自动为FinViz方法生成MCP工具文档。

## 测试验证

运行测试文件验证功能：
```bash
python test_new_structure.py
```

## 优势

1. **标准化架构**: 符合MCP项目的标准结构
2. **模块化设计**: 功能按服务分离，便于维护
3. **统一接口**: 门面类提供统一的API接口
4. **易于扩展**: 可以轻松添加新的服务或功能
5. **向后兼容**: 保持原有功能不变

## 注意事项

1. 原有的`finviz/`目录仍然保留，确保向后兼容
2. 新的服务层是对原有功能的封装，不改变核心逻辑
3. 所有方法都包含详细的文档字符串，便于MCP工具文档生成
4. 错误处理已增强，返回标准化的错误信息

## 下一步

1. 将`core/finviz/`目录集成到MCP项目中
2. 在`main_service.py`中添加FinViz服务
3. 运行帮助文档生成脚本
4. 测试MCP工具功能

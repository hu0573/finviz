# FinViz Scripts

本目录包含两个核心脚本，用于 FinViz 筛选器的测试和更新。

## 脚本说明

### 1. `auto_filter_test.py` - 筛选器测试脚本

**功能**: 自动测试所有 FinViz 筛选器功能

**特点**:
- ✅ 全自动运行，无需用户交互
- ✅ 随机测试每个筛选器的一个选项
- ✅ 智能过滤空值和"Any"选项
- ✅ 自动保存测试结果到JSON文件
- ✅ 实时显示测试进度和结果

**使用方法**:
```bash
cd script
python auto_filter_test.py
```

**测试参数**:
- 默认测试前10个筛选器
- 每次测试间隔1秒
- 结果自动保存到 `auto_test_results.json`

**测试结果示例**:
```
FinViz 筛选器自动测试
========================================
加载了 85 个筛选器
将测试前 10 个筛选器，间隔 1.0 秒

进度: 1/10
测试: Exchange
  选择: Custom (Elite only) -> modal
  代码: exch_modal
  结果: 5 只股票

...

========================================
测试完成: 10/10 成功
成功率: 100.0%
```

### 2. `update_filters.py` - 筛选器更新脚本

**功能**: 从 FinViz 网站更新筛选器配置

**特点**:
- ✅ 自动下载最新的筛选器配置
- ✅ 智能比较新旧配置差异
- ✅ 自动备份现有配置
- ✅ 支持增量更新和完整更新

**使用方法**:
```bash
cd script
python update_filters.py
```

**更新选项**:
- 只下载页面源码（不更新文件）
- 提取筛选器数据（不保存）
- 比较现有筛选器
- 执行完整更新流程（带备份）

## 筛选器类型

脚本会处理以下类型的筛选器：

### 基础筛选器
- **Exchange**: 交易所（NASDAQ, NYSE, AMEX等）
- **Index**: 指数（S&P 500, NASDAQ 100等）
- **Sector**: 行业板块（Technology, Healthcare等）
- **Industry**: 具体行业（Software, Pharmaceuticals等）
- **Country**: 国家（USA, China, Japan等）
- **Market Cap.**: 市值（Large, Mid, Small等）

### 财务指标筛选器
- **P/E**: 市盈率
- **Forward P/E**: 前瞻市盈率
- **PEG**: PEG比率
- **P/S**: 市销率
- **P/B**: 市净率
- **Price/Cash**: 价格/现金流
- **Price/Free Cash Flow**: 价格/自由现金流
- **EV/EBITDA**: 企业价值倍数
- **EV/Sales**: 企业价值/销售额

### 增长指标筛选器
- **EPS Growth**: 每股收益增长率
- **Sales Growth**: 销售额增长率
- **Dividend Growth**: 股息增长率

### 盈利能力筛选器
- **Return on Assets**: 资产回报率
- **Return on Equity**: 股本回报率
- **Return on Invested Capital**: 投资资本回报率
- **Gross Margin**: 毛利率
- **Operating Margin**: 营业利润率
- **Net Profit Margin**: 净利润率

### 财务健康筛选器
- **Current Ratio**: 流动比率
- **Quick Ratio**: 速动比率
- **LT Debt/Equity**: 长期债务/股本
- **Debt/Equity**: 债务/股本

### 所有权筛选器
- **InsiderOwnership**: 内部人持股
- **InsiderTransactions**: 内部人交易
- **InstitutionalOwnership**: 机构持股
- **InstitutionalTransactions**: 机构交易
- **Short Float**: 空头比例

### 技术分析筛选器
- **Performance**: 表现指标
- **Volatility**: 波动率
- **RSI (14)**: 相对强弱指数
- **Gap**: 跳空
- **Moving Averages**: 移动平均线
- **High/Low**: 高低点
- **Pattern**: 技术形态
- **Candlestick**: K线形态
- **Beta**: 贝塔系数

### 交易筛选器
- **Average Volume**: 平均成交量
- **Relative Volume**: 相对成交量
- **Current Volume**: 当前成交量
- **Trades**: 交易次数
- **Price $**: 价格范围

### ETF筛选器
- **Single Category**: 单一类别
- **Asset Type**: 资产类型
- **Sponsor**: 发起人
- **Net Expense Ratio**: 净费用率
- **Net Fund Flows**: 净资金流
- **Annualized Return**: 年化回报

## 自定义配置

### 测试脚本配置

编辑 `auto_filter_test.py` 文件中的参数：

```python
max_test = 10  # 测试筛选器数量
delay = 1.0    # 延迟时间（秒）
```

### 更新脚本配置

编辑 `update_filters.py` 文件中的参数：

```python
# 更新选项
backup = True  # 是否备份现有配置
reload = True  # 是否重新加载配置
```

## 故障排除

### 常见问题

1. **导入错误**
   ```
   ModuleNotFoundError: No module named 'core'
   ```
   **解决方案**: 确保在 `script` 目录下运行脚本

2. **网络超时**
   ```
   Connection timeout
   ```
   **解决方案**: 增加延迟时间或检查网络连接

3. **筛选器代码错误**
   ```
   无法生成筛选器代码
   ```
   **解决方案**: 运行更新脚本获取最新配置

4. **权限错误**
   ```
   Permission denied
   ```
   **解决方案**: 确保有写入权限

### 调试建议

1. **测试筛选器**: 使用 `auto_filter_test.py` 验证功能
2. **更新配置**: 使用 `update_filters.py` 获取最新筛选器
3. **检查网络**: 确保能访问 FinViz 网站
4. **查看日志**: 检查控制台输出的错误信息

## 文件结构

```
script/
├── auto_filter_test.py    # 筛选器测试脚本
├── update_filters.py      # 筛选器更新脚本
├── update_filters.sh      # 更新脚本的Shell版本
├── requirements.txt       # Python依赖
└── README.md             # 本说明文档
```

## 依赖要求

确保安装以下Python包：

```bash
pip install -r requirements.txt
```

主要依赖：
- `requests` - HTTP请求
- `beautifulsoup4` - HTML解析
- `user_agent` - 用户代理生成
- `tqdm` - 进度条显示

## 使用流程

### 日常使用
1. 运行测试脚本验证筛选器功能
2. 如有问题，运行更新脚本获取最新配置
3. 再次运行测试脚本确认修复

### 开发调试
1. 修改筛选器配置后运行测试脚本
2. 查看测试结果和错误信息
3. 根据结果调整配置或代码

## 注意事项

- 脚本会向 FinViz 网站发送请求，请确保网络连接正常
- 内置延迟机制避免请求过于频繁
- 测试结果会自动保存，便于后续分析
- 更新脚本会自动备份现有配置，确保数据安全

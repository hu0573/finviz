# FinViz 筛选器更新脚本

这个脚本用于从 FinViz 网站自动下载和更新筛选器选项，确保 `filters.json` 文件包含最新的筛选器数据。

## 功能特性

- 🔄 **自动下载**: 从 FinViz 筛选器页面下载最新源码
- 🔍 **智能解析**: 自动提取所有筛选器选项和值
- 📊 **差异报告**: 显示新增、删除和修改的筛选器
- 💾 **自动备份**: 更新前自动备份现有文件
- 🛡️ **错误处理**: 完善的错误处理和网络连接检查

## 安装依赖

```bash
# 安装脚本依赖项
pip install -r script/requirements.txt

# 或者单独安装
pip install requests beautifulsoup4 lxml
```

## 使用方法

### 基本使用

```bash
# 在项目根目录运行
python script/update_filters.py
```

### 脚本功能

1. **网络检查**: 首先检查与 FinViz 的连接
2. **下载源码**: 从 `https://finviz.com/screener.ashx?v=111&ft=4` 下载页面
3. **解析筛选器**: 提取所有筛选器选项和对应的值
4. **比较差异**: 与现有 `filters.json` 比较并显示变化
5. **备份文件**: 自动备份现有文件为 `.backup` 格式
6. **更新文件**: 保存新的筛选器数据到 `core/finviz/filters.json`

## 输出示例

```
FinViz 筛选器更新工具
==================================================
检查网络连接...
网络连接正常
正在下载页面源码: https://finviz.com/screener.ashx?v=111&ft=4
成功下载页面源码，大小: 258560 字符
正在解析HTML并提取筛选器...
提取筛选器: Market Cap. (25 个选项)
提取筛选器: Price/Earnings (25 个选项)
提取筛选器: Forward Price/Earnings (25 个选项)
...
总共提取了 45 个筛选器

=== 筛选器更新报告 ===
旧筛选器数量: 42
新筛选器数量: 45
变化: +3

新增筛选器 (3 个):
  + New Filter 1
  + New Filter 2
  + New Filter 3

修改筛选器 (2 个):
  ~ Market Cap. (选项数: 20 -> 25)
  ~ Price/Earnings (选项数: 22 -> 25)

备份现有文件到: core/finviz/filters.json.backup
正在保存筛选器数据到: core/finviz/filters.json
成功保存 45 个筛选器到文件

筛选器更新完成！
```

## 文件结构

```
script/
├── update_filters.py    # 主脚本文件
├── requirements.txt     # 依赖项列表
└── README.md           # 使用说明
```

## 技术实现

### 核心类: FinVizFilterUpdater

- `download_page_source()`: 下载网页源码
- `extract_filters_from_html()`: 从HTML提取筛选器
- `load_existing_filters()`: 加载现有筛选器文件
- `save_filters()`: 保存筛选器到JSON文件
- `compare_filters()`: 比较新旧筛选器差异
- `update_filters()`: 执行完整更新流程

### 筛选器提取逻辑

1. 使用 BeautifulSoup 解析HTML
2. 查找所有 `<select>` 元素
3. 提取每个select的name属性和选项
4. 智能匹配筛选器标签名称
5. 转换为符合现有格式的JSON结构

### 错误处理

- 网络连接检查
- 请求超时处理
- JSON解析错误处理
- 文件IO错误处理

## 注意事项

1. **网络要求**: 需要能够访问 `finviz.com`
2. **权限要求**: 需要对 `core/finviz/` 目录有写权限
3. **备份机制**: 更新前会自动备份现有文件
4. **数据格式**: 输出的JSON格式与现有 `filters.json` 完全兼容

## 故障排除

### 常见问题

1. **网络连接失败**
   ```
   错误: 无法连接到 FinViz 网站，请检查网络连接
   ```
   - 检查网络连接
   - 确认能够访问 finviz.com

2. **权限错误**
   ```
   保存筛选器文件失败: [Errno 13] Permission denied
   ```
   - 检查对 `core/finviz/` 目录的写权限
   - 确保文件没有被其他程序占用

3. **解析失败**
   ```
   警告: 未提取到任何筛选器数据
   ```
   - FinViz 网站结构可能发生变化
   - 检查网页源码是否正常下载

## 开发说明

如需修改脚本功能，主要关注以下方法：

- `_get_filter_label()`: 筛选器标签提取逻辑
- `extract_filters_from_html()`: HTML解析逻辑
- `compare_filters()`: 差异比较逻辑

## 版本历史

- **v1.0.0**: 初始版本，支持基本的筛选器更新功能

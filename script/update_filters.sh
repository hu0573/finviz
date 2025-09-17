#!/bin/bash
# FinViz 筛选器更新脚本
# 使用方法: ./script/update_filters.sh

echo "FinViz 筛选器更新工具"
echo "======================"

# 检查Python是否可用
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3，请确保已安装Python 3"
    exit 1
fi

# 检查依赖项
echo "检查依赖项..."
python3 -c "import requests, bs4" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误: 缺少必要的依赖项"
    echo "请运行: pip install requests beautifulsoup4 lxml"
    exit 1
fi

# 切换到项目根目录
cd "$(dirname "$0")/.."

# 运行更新脚本
echo "开始更新筛选器..."
python3 script/update_filters.py

echo "脚本执行完成"

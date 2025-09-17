#!/usr/bin/env python3
"""
FinViz 筛选器更新脚本使用示例

此脚本演示如何使用 update_filters.py 脚本更新筛选器。
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from script.update_filters import FinVizFilterUpdater


def main():
    """演示如何使用筛选器更新器"""
    print("FinViz 筛选器更新器使用示例")
    print("=" * 50)
    
    # 创建更新器实例
    updater = FinVizFilterUpdater()
    
    # 示例1: 只下载页面源码（不更新文件）
    print("\n示例1: 下载页面源码")
    try:
        html_content = updater.download_page_source()
        print(f"成功下载页面，大小: {len(html_content)} 字符")
    except Exception as e:
        print(f"下载失败: {e}")
        return
    
    # 示例2: 提取筛选器（不保存）
    print("\n示例2: 提取筛选器数据")
    try:
        filters_data = updater.extract_filters_from_html(html_content)
        print(f"提取了 {len(filters_data)} 个筛选器")
        
        # 显示前几个筛选器
        for i, (name, options) in enumerate(filters_data.items()):
            if i >= 3:  # 只显示前3个
                break
            print(f"  {name}: {len(options)} 个选项")
    except Exception as e:
        print(f"提取失败: {e}")
        return
    
    # 示例3: 比较现有筛选器
    print("\n示例3: 比较现有筛选器")
    try:
        old_filters = updater.load_existing_filters()
        updater.compare_filters(old_filters, filters_data)
    except Exception as e:
        print(f"比较失败: {e}")
    
    # 示例4: 完整更新流程（带备份）
    print("\n示例4: 执行完整更新流程")
    try:
        updater.update_filters(backup=True)
        print("更新完成！")
    except Exception as e:
        print(f"更新失败: {e}")


if __name__ == "__main__":
    main()

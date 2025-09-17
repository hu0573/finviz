#!/usr/bin/env python3
"""
FinViz 筛选器更新脚本

此脚本用于从 FinViz 网站下载最新的筛选器选项并更新 filters.json 文件。

功能：
1. 从 https://finviz.com/screener.ashx?v=111&ft=4 下载网页源码
2. 提取筛选器选项并转换为符合 filters.json 规范的格式
3. 更新 core/finviz/filters.json 文件

使用方法：
    python script/update_filters.py

作者：Alberto Rincones (code4road@gmail.com)
版本：1.0.0
"""

import json
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse


class FinVizFilterUpdater:
    """FinViz 筛选器更新器"""
    
    def __init__(self):
        self.base_url = "https://finviz.com"
        self.screener_url = "https://finviz.com/screener.ashx?v=111&ft=4"
        self.filters_file = Path(__file__).parent.parent / "core" / "finviz" / "filters.json"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def download_page_source(self) -> str:
        """
        下载 FinViz 筛选器页面的源码
        
        Returns:
            str: 网页源码
            
        Raises:
            requests.RequestException: 当请求失败时
        """
        print(f"正在下载页面源码: {self.screener_url}")
        
        try:
            # 添加重试机制
            for attempt in range(3):
                try:
                    print(f"尝试 {attempt + 1}/3...")
                    response = self.session.get(self.screener_url, timeout=30)
                    response.raise_for_status()
                    
                    print(f"成功下载页面源码，大小: {len(response.text)} 字符")
                    return response.text
                    
                except requests.RequestException as e:
                    print(f"尝试 {attempt + 1} 失败: {e}")
                    if attempt < 2:  # 不是最后一次尝试
                        print("等待 2 秒后重试...")
                        time.sleep(2)
                    else:
                        raise
            
        except requests.RequestException as e:
            print(f"下载页面源码失败: {e}")
            print(f"状态码: {getattr(e.response, 'status_code', 'N/A')}")
            print(f"响应内容: {getattr(e.response, 'text', 'N/A')[:200]}...")
            raise
    
    def extract_filters_from_html(self, html_content: str) -> Dict[str, Dict[str, str]]:
        """
        从HTML源码中提取筛选器选项
        
        Args:
            html_content: HTML源码
            
        Returns:
            Dict[str, Dict[str, str]]: 提取的筛选器数据
        """
        print("正在解析HTML并提取筛选器...")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        filters_data = {}
        
        # 查找所有FinViz筛选器下拉菜单 (id="fs_xxx"格式)
        filter_selects = soup.find_all('select', {'id': re.compile(r'^fs_')})
        
        for select in filter_selects:
            select_id = select.get('id', '')
            if not select_id:
                continue
            
            # 获取筛选器显示名称
            filter_label = self._get_filter_label(select, soup)
            if not filter_label:
                continue
            
            # 提取选项
            options = {}
            option_elements = select.find_all('option')
            
            for option in option_elements:
                option_value = option.get('value', '')
                option_text = option.get_text(strip=True)
                
                # 清理HTML实体
                option_text = self._clean_html_entities(option_text)
                
                if option_text:  # 只要有文本就添加，空值也保留
                    options[option_text] = option_value
            
            if options:
                # 使用筛选器显示名称作为键，与现有格式保持一致
                filters_data[filter_label] = options
                print(f"提取筛选器: {filter_label} ({len(options)} 个选项)")
        
        print(f"总共提取了 {len(filters_data)} 个筛选器")
        return filters_data
    
    def _get_filter_label(self, select_element, soup: BeautifulSoup) -> Optional[str]:
        """
        获取筛选器的显示标签
        
        Args:
            select_element: select元素
            soup: BeautifulSoup对象
            
        Returns:
            Optional[str]: 筛选器标签名称
        """
        # 方法1: 查找前面的span元素（FinViz使用span作为标签）
        label_span = select_element.find_previous('span', class_='screener-combo-title')
        if label_span:
            return label_span.get_text(strip=True)
        
        # 方法2: 查找同一行中的span元素
        parent_td = select_element.find_parent('td')
        if parent_td:
            # 查找同一行中的前一个td中的span
            prev_td = parent_td.find_previous_sibling('td')
            if prev_td:
                span = prev_td.find('span', class_='screener-combo-title')
                if span:
                    return span.get_text(strip=True)
        
        # 方法3: 使用select的id属性作为备选
        select_id = select_element.get('id', '')
        if select_id.startswith('fs_'):
            # 移除fs_前缀并转换为可读格式
            filter_name = select_id[3:]  # 移除'fs_'前缀
            # 将下划线转换为空格并首字母大写
            return filter_name.replace('_', ' ').title()
        
        return None
    
    def _clean_html_entities(self, text: str) -> str:
        """
        清理HTML实体
        
        Args:
            text: 原始文本
            
        Returns:
            str: 清理后的文本
        """
        # 常见的HTML实体替换
        replacements = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
            '&nbsp;': ' ',
        }
        
        for entity, replacement in replacements.items():
            text = text.replace(entity, replacement)
        
        return text
    
    def load_existing_filters(self) -> Dict[str, Dict[str, str]]:
        """
        加载现有的filters.json文件
        
        Returns:
            Dict[str, Dict[str, str]]: 现有的筛选器数据
        """
        if not self.filters_file.exists():
            print("filters.json 文件不存在，将创建新文件")
            return {}
        
        try:
            with open(self.filters_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"成功加载现有筛选器文件，包含 {len(data)} 个筛选器")
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"加载现有筛选器文件失败: {e}")
            return {}
    
    def save_filters(self, filters_data: Dict[str, Dict[str, str]]) -> None:
        """
        保存筛选器数据到JSON文件
        
        Args:
            filters_data: 筛选器数据
        """
        print(f"正在保存筛选器数据到: {self.filters_file}")
        
        try:
            # 确保目录存在
            self.filters_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存为格式化的JSON
            with open(self.filters_file, 'w', encoding='utf-8') as f:
                json.dump(filters_data, f, indent=2, ensure_ascii=False)
            
            print(f"成功保存 {len(filters_data)} 个筛选器到文件")
            
        except IOError as e:
            print(f"保存筛选器文件失败: {e}")
            raise
    
    def compare_filters(self, old_filters: Dict, new_filters: Dict) -> None:
        """
        比较新旧筛选器数据并显示差异
        
        Args:
            old_filters: 旧的筛选器数据
            new_filters: 新的筛选器数据
        """
        print("\n=== 筛选器更新报告 ===")
        
        # 统计信息
        old_count = len(old_filters)
        new_count = len(new_filters)
        
        print(f"旧筛选器数量: {old_count}")
        print(f"新筛选器数量: {new_count}")
        print(f"变化: {new_count - old_count:+d}")
        
        # 新增的筛选器
        new_keys = set(new_filters.keys()) - set(old_filters.keys())
        if new_keys:
            print(f"\n新增筛选器 ({len(new_keys)} 个):")
            for key in sorted(new_keys):
                print(f"  + {key}")
        
        # 删除的筛选器
        removed_keys = set(old_filters.keys()) - set(new_filters.keys())
        if removed_keys:
            print(f"\n删除筛选器 ({len(removed_keys)} 个):")
            for key in sorted(removed_keys):
                print(f"  - {key}")
        
        # 修改的筛选器
        modified_filters = []
        for key in set(old_filters.keys()) & set(new_filters.keys()):
            if old_filters[key] != new_filters[key]:
                modified_filters.append(key)
        
        if modified_filters:
            print(f"\n修改筛选器 ({len(modified_filters)} 个):")
            for key in sorted(modified_filters):
                old_options = len(old_filters[key])
                new_options = len(new_filters[key])
                print(f"  ~ {key} (选项数: {old_options} -> {new_options})")
        
        if not new_keys and not removed_keys and not modified_filters:
            print("\n筛选器数据无变化")
    
    def update_filters(self, backup: bool = True) -> None:
        """
        执行完整的筛选器更新流程
        
        Args:
            backup: 是否在更新前备份现有文件
        """
        print("开始更新 FinViz 筛选器...")
        
        try:
            # 1. 加载现有筛选器
            old_filters = self.load_existing_filters()
            
            # 2. 下载页面源码
            html_content = self.download_page_source()
            
            # 3. 提取筛选器
            new_filters = self.extract_filters_from_html(html_content)
            
            if not new_filters:
                print("警告: 未提取到任何筛选器数据")
                return
            
            # 4. 比较差异
            self.compare_filters(old_filters, new_filters)
            
            # 5. 备份现有文件
            if backup and old_filters and self.filters_file.exists():
                backup_file = self.filters_file.with_suffix('.json.backup')
                print(f"备份现有文件到: {backup_file}")
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(old_filters, f, indent=2, ensure_ascii=False)
            
            # 6. 保存新筛选器
            self.save_filters(new_filters)
            
            print("\n筛选器更新完成！")
            
        except Exception as e:
            print(f"更新筛选器时发生错误: {e}")
            sys.exit(1)


def main():
    """主函数"""
    print("FinViz 筛选器更新工具")
    print("=" * 50)
    
    updater = FinVizFilterUpdater()
    
    # 检查网络连接
    try:
        print("检查网络连接...")
        response = requests.get("https://finviz.com", timeout=10)
        print(f"FinViz 网站响应状态: {response.status_code}")
        if response.status_code == 200:
            print("网络连接正常")
        else:
            print(f"警告: FinViz 网站返回状态码 {response.status_code}")
    except requests.RequestException as e:
        print(f"错误: 无法连接到 FinViz 网站: {e}")
        print("请检查网络连接或稍后重试")
        sys.exit(1)
    
    # 执行更新
    updater.update_filters(backup=True)


if __name__ == "__main__":
    main()

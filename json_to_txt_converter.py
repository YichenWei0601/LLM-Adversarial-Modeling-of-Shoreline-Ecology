#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON游戏记录转换器
将游戏记录JSON文件转换为简洁的TXT表格格式
"""

import json
import sys
import os
from typing import Dict, Any

def convert_json_to_txt(json_file_path: str, output_file_path: str = None) -> str:
    """
    将JSON游戏记录转换为TXT表格格式
    
    Args:
        json_file_path: JSON文件路径
        output_file_path: 输出TXT文件路径（可选）
        
    Returns:
        生成的TXT文件路径
    """
    # 读取JSON文件
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 错误: 文件 {json_file_path} 不存在")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 错误: JSON文件格式错误 - {e}")
        return None
    
    # 确定输出文件名
    if output_file_path is None:
        base_name = os.path.splitext(json_file_path)[0]
        output_file_path = f"{base_name}_table.txt"
    
    # 提取游戏数据
    game_summary = data.get('game_summary', {})
    yearly_records = data.get('yearly_records', [])
    
    # 创建表格内容
    lines = []
    
    # 表头
    lines.append("=" * 50)
    lines.append("海岸线生态对抗建模系统 - 游戏记录表格")
    lines.append("=" * 50)
    lines.append("")
    
    # 游戏基本信息
    initial_country = game_summary.get('initial_scores', {}).get('country', 0)
    initial_shoreline = game_summary.get('initial_scores', {}).get('shoreline', 0)
    final_country = game_summary.get('final_scores', {}).get('country', 0)
    final_shoreline = game_summary.get('final_scores', {}).get('shoreline', 0)
    total_years = game_summary.get('total_years', 0)
    victory = game_summary.get('victory', False)
    game_over_reason = game_summary.get('game_over_reason', '未知')
    
    lines.append(f"初始分数: 国家={initial_country}, 海岸线={initial_shoreline}")
    lines.append(f"最终分数: 国家={final_country}, 海岸线={final_shoreline}")
    lines.append(f"游戏时长: {total_years}年")
    lines.append(f"游戏结果: {'胜利' if victory else '失败'}")
    lines.append(f"结束原因: {game_over_reason}")
    lines.append("")
    
    # 分数变化表格
    lines.append("年度分数变化表:")
    lines.append("-" * 50)
    lines.append(f"{'年份':<6} {'国家分数':<10} {'海岸线分数':<12}")
    lines.append("-" * 50)
    
    # 初始状态
    lines.append(f"{'初始':<6} {initial_country:<10} {initial_shoreline:<12}")
    
    # 每年数据
    for record in yearly_records:
        year = record.get('year', 0)
        country_score = record.get('country_score', 0)
        shoreline_score = record.get('shoreline_score', 0)
        lines.append(f"{year:<6} {country_score:<10} {shoreline_score:<12}")
    
    lines.append("-" * 50)
    lines.append(f"{'最终':<6} {final_country:<10} {final_shoreline:<12}")
    lines.append("")
    
    # 分数变化趋势
    if len(yearly_records) > 0:
        lines.append("分数变化趋势:")
        lines.append("-" * 50)
        
        country_change = final_country - initial_country
        shoreline_change = final_shoreline - initial_shoreline
        
        lines.append(f"国家发展分数变化: {initial_country} → {final_country} ({country_change:+d})")
        lines.append(f"海岸线状态分数变化: {initial_shoreline} → {final_shoreline} ({shoreline_change:+d})")
        
        if total_years > 0:
            avg_country_change = country_change / total_years
            avg_shoreline_change = shoreline_change / total_years
            lines.append(f"平均每年变化: 国家{avg_country_change:+.1f}, 海岸线{avg_shoreline_change:+.1f}")
    
    lines.append("")
    lines.append("=" * 50)
    
    # 写入文件
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ 转换成功!")
        print(f"📄 输入文件: {json_file_path}")
        print(f"📊 输出文件: {output_file_path}")
        return output_file_path
        
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")
        return None

def main():
    """主函数"""
    print("JSON游戏记录转TXT表格转换器")
    print("=" * 40)
    
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法: python json_to_txt_converter.py <JSON文件路径> [输出文件路径]")
        print()
        print("示例:")
        print("  python json_to_txt_converter.py game_record_20250709_013521.json")
        print("  python json_to_txt_converter.py game_record_20250709_013521.json output.txt")
        print()
        
        # 查找当前目录下的JSON文件
        json_files = [f for f in os.listdir('.') if f.endswith('.json') and 'game_record' in f]
        if json_files:
            print("📁 发现的游戏记录文件:")
            for i, file in enumerate(json_files, 1):
                print(f"  {i}. {file}")
            print()
            
            try:
                choice = input("请选择要转换的文件编号 (直接回车退出): ").strip()
                if choice:
                    file_index = int(choice) - 1
                    if 0 <= file_index < len(json_files):
                        selected_file = json_files[file_index]
                        print(f"选择文件: {selected_file}")
                        convert_json_to_txt(selected_file)
                    else:
                        print("❌ 无效的文件编号")
            except (ValueError, KeyboardInterrupt):
                print("退出程序")
        return
    
    # 从命令行参数获取文件路径
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 执行转换
    convert_json_to_txt(input_file, output_file)

if __name__ == "__main__":
    main()

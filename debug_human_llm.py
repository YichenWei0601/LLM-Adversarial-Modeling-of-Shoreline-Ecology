"""
调试人类LLM回复解析问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.llm_client import LLMClient
import json

def debug_human_llm():
    """调试人类LLM的回复内容"""
    
    # 读取配置
    with open("game_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    llm_client = LLMClient(
        api_key=config["api_key"],
        base_url=config["base_url"],
        model=config["model"]
    )
    
    # 读取提示模板和参考表
    with open("prompt/HumanLLM.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()
    
    with open("prompt/ref_scoring_table.txt", "r", encoding="utf-8") as f:
        ref_table = f.read()
    
    # 构建完整提示词
    prompt = prompt_template.format(
        country_score=60,
        shoreline_score=100,
        shoreline_opportunities="海岸线提供丰富的渔业资源和旅游潜力",
        shoreline_challenges="海岸侵蚀和海洋污染威胁生态平衡",
        ref_scoring_table=ref_table
    )
    
    print("=== 完整提示词 ===")
    print(prompt)
    print("\n" + "="*80 + "\n")
    
    # 直接调用LLM获取原始回复
    print("=== LLM原始回复 ===")
    raw_response = llm_client.call_llm(prompt)
    print(f"原始回复: '{raw_response}'")
    print(f"回复长度: {len(raw_response)}")
    print(f"回复字符: {repr(raw_response)}")
    print("\n" + "="*80 + "\n")
    
    # 测试解析逻辑
    print("=== 解析过程 ===")
    actions = {}
    lines = raw_response.split('\n')
    current_action = None
    
    print(f"总行数: {len(lines)}")
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        print(f"行{i}: '{line}' -> 去空格: '{line_stripped}'")
        
        # 跳过代码块标记和空行
        if line_stripped in ['```', ''] or not line_stripped:
            print(f"  -> 跳过空行或代码块标记")
            continue
            
        if line_stripped.startswith('ACTION_1:'):
            current_action = 'action_1'
            content = line_stripped.replace('ACTION_1:', '').strip()
            actions[current_action] = content
            print(f"  -> 发现ACTION_1: '{content}'")
        elif line_stripped.startswith('ACTION_2:'):
            current_action = 'action_2'
            content = line_stripped.replace('ACTION_2:', '').strip()
            actions[current_action] = content
            print(f"  -> 发现ACTION_2: '{content}'")
        elif current_action and line_stripped and not line_stripped.startswith('```'):
            # 只在不是代码块标记的情况下才添加内容
            if current_action in actions:
                actions[current_action] += ' ' + line_stripped
            else:
                actions[current_action] = line_stripped
            print(f"  -> 添加到{current_action}: '{line_stripped}'")
    
    # 确保两个行动都存在
    if 'action_1' not in actions:
        actions['action_1'] = ''
    if 'action_2' not in actions:
        actions['action_2'] = ''
    
    print(f"\n最终解析结果: {actions}")

if __name__ == "__main__":
    debug_human_llm()

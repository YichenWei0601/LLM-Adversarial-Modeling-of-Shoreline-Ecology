"""
测试LLM回复为空的问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.llm_client import LLMClient
from src.game_state import GameState

def test_llm_responses():
    """测试各种LLM调用是否返回空回复"""
    
    # 检查配置
    import json
    try:
        with open("game_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        api_key = config.get("api_key")
        base_url = config.get("base_url")
        model = config.get("model", "gpt-3.5-turbo")
    except:
        print("❌ 无法读取配置文件，请确保 game_config.json 存在")
        return
    
    if not api_key:
        print("❌ API Key 未配置")
        return
    
    print(f"🔑 使用API Key: {api_key[:10]}...")
    print(f"🌐 使用Base URL: {base_url}")
    print(f"🤖 使用模型: {model}")
    print()
    
    # 创建LLM客户端
    try:
        llm_client = LLMClient(api_key=api_key, base_url=base_url, model=model)
    except Exception as e:
        print(f"❌ LLM客户端初始化失败: {e}")
        return
    
    # 加载参考评分表
    try:
        with open("prompt/ref_scoring_table.txt", "r", encoding="utf-8") as f:
            ref_table = f.read()
    except:
        print("❌ 无法读取参考评分表")
        return
    
    print("=== 测试基础LLM调用 ===")
    try:
        basic_response = llm_client.call_llm("请说'你好'")
        print(f"基础调用结果: '{basic_response}'")
        print(f"结果长度: {len(basic_response)}")
        print(f"是否为空: {not basic_response.strip()}")
        print()
    except Exception as e:
        print(f"❌ 基础LLM调用失败: {e}")
        return
    
    print("=== 测试人类LLM调用 ===")
    try:
        human_response = llm_client.call_human_llm(
            country_score=60,
            shoreline_score=100,
            opportunities="海岸线提供丰富的渔业资源和旅游潜力",
            challenges="海岸侵蚀和海洋污染威胁生态平衡",
            ref_table=ref_table
        )
        print(f"人类LLM调用结果: {human_response}")
        print(f"action_1 是否为空: {not human_response.get('action_1', '').strip()}")
        print(f"action_2 是否为空: {not human_response.get('action_2', '').strip()}")
        print()
    except Exception as e:
        print(f"❌ 人类LLM调用失败: {e}")
        print()
    
    print("=== 测试海岸线LLM调用 ===")
    try:
        shore_response = llm_client.call_shore_llm(
            "ACTION_1: 发展可持续渔业\nACTION_2: 建设海岸防护设施"
        )
        print(f"海岸线LLM调用结果: {shore_response}")
        print(f"opportunities 是否为空: {not shore_response.get('opportunities', '').strip()}")
        print(f"challenges 是否为空: {not shore_response.get('challenges', '').strip()}")
        print()
    except Exception as e:
        print(f"❌ 海岸线LLM调用失败: {e}")
        print()
    
    print("=== 测试裁判LLM调用 ===")
    try:
        judge_response = llm_client.call_judge_llm(
            "ACTION_1: 发展可持续渔业\nACTION_2: 建设海岸防护设施",
            ref_table
        )
        print(f"裁判LLM调用结果: {judge_response}")
        required_keys = ['first_country', 'first_shoreline', 'second_country', 'second_shoreline']
        for key in required_keys:
            print(f"{key}: {judge_response.get(key, 'missing')}")
        print()
    except Exception as e:
        print(f"❌ 裁判LLM调用失败: {e}")
        print()

if __name__ == "__main__":
    test_llm_responses()

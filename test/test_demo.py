"""
测试和演示脚本
用于验证系统功能和演示使用方法
"""

import os
import sys
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.game_controller import ShorlineEcologyGame
from src.llm_client import LLMClient
from src.random_events import RandomEventSystem
from src.game_state import GameState

def test_llm_client():
    """测试LLM客户端基本功能"""
    print("=== 测试LLM客户端 ===")
    
    # 这里使用模拟的API调用，实际使用时需要真实的API
    client = LLMClient(api_key="test_key", model="gpt-3.5-turbo")
    
    # 测试基本功能
    print("✓ LLM客户端初始化成功")
    
    # 测试文件读取
    try:
        with open("prompt/HumanLLM.txt", "r", encoding="utf-8") as f:
            human_prompt = f.read()
        print("✓ 人类LLM提示词读取成功")
        
        with open("prompt/ShoreLLM.txt", "r", encoding="utf-8") as f:
            shore_prompt = f.read()
        print("✓ 海岸线LLM提示词读取成功")
        
        with open("prompt/JudgeLLM.txt", "r", encoding="utf-8") as f:
            judge_prompt = f.read()
        print("✓ 裁判LLM提示词读取成功")
        
        with open("prompt/ref_scoring_table.txt", "r", encoding="utf-8") as f:
            ref_table = f.read()
        print("✓ 参考评分表读取成功")
        
    except Exception as e:
        print(f"✗ 文件读取失败: {e}")
    
    print()

def test_random_events():
    """测试随机事件系统"""
    print("=== 测试随机事件系统 ===")
    
    event_system = RandomEventSystem()
    print(f"✓ 随机事件系统初始化成功，共{len(event_system.events)}个事件")
    
    # 测试事件触发
    triggered = event_system.trigger_random_events(1)
    print(f"✓ 随机事件触发测试完成，触发{len(triggered)}个事件")
    
    # 测试影响计算
    country_impact, shoreline_impact = event_system.calculate_total_impact(triggered)
    print(f"✓ 影响计算完成：国家{country_impact:+d}, 海岸线{shoreline_impact:+d}")
    
    # 测试灾害概率调整
    modifier = event_system.get_disaster_probability_modifier(60)
    print(f"✓ 灾害概率调整器测试完成，修正因子: {modifier}")
    
    print()

def test_game_state():
    """测试游戏状态管理"""
    print("=== 测试游戏状态管理 ===")
    
    game_state = GameState()
    print(f"✓ 游戏状态初始化：国家{game_state.country_score}, 海岸线{game_state.shoreline_score}")
    
    # 测试分数更新
    game_state.update_scores(5, -3, 2, -1)
    print(f"✓ 分数更新测试：国家{game_state.country_score}, 海岸线{game_state.shoreline_score}")
    
    # 测试游戏结束条件
    is_over = game_state.is_game_over()
    print(f"✓ 游戏结束检查：{is_over}")
    
    # 测试记录功能
    game_state.record_year(
        country_actions={"action_1": "测试行动1", "action_2": "测试行动2"},
        shore_response={"opportunities": "测试机遇", "challenges": "测试挑战"},
        judge_scores={"first_country": 2, "first_shoreline": -1, "second_country": 3, "second_shoreline": -2},
        random_events=[{"name": "测试事件", "occurred": True}],
        country_change=5,
        shoreline_change=-3,
        random_country_impact=2,
        random_shoreline_impact=-1
    )
    print(f"✓ 年度记录测试完成，记录数: {len(game_state.yearly_records)}")
    
    print()

def demo_game_flow():
    """演示游戏流程（不调用真实API）"""
    print("=== 游戏流程演示 ===")
    
    # 初始化组件
    game_state = GameState()
    event_system = RandomEventSystem()
    
    print(f"初始状态：国家{game_state.country_score}, 海岸线{game_state.shoreline_score}")
    
    # 模拟几年的游戏
    for year in range(1, 4):
        game_state.year = year
        print(f"\n--- 第{year}年 ---")
        
        # 模拟人类行动
        country_actions = {
            "action_1": f"第{year}年行动1：发展绿色技术",
            "action_2": f"第{year}年行动2：加强环保监管"
        }
        print(f"国家行动: {country_actions}")
        
        # 模拟裁判评分
        judge_scores = {
            "first_country": 2,
            "first_shoreline": 1,
            "second_country": -1,
            "second_shoreline": 3
        }
        print(f"裁判评分: {judge_scores}")
        
        # 计算分数变化
        country_change = judge_scores["first_country"] + judge_scores["second_country"]
        shoreline_change = judge_scores["first_shoreline"] + judge_scores["second_shoreline"]
        
        # 模拟随机事件
        triggered_events = event_system.trigger_random_events(year)
        random_country_impact, random_shoreline_impact = event_system.calculate_total_impact(triggered_events)
        
        if triggered_events:
            print(f"随机事件: {[event[0].name for event in triggered_events if event[1]]}")
        
        # 更新分数（包含年度奖励）
        annual_bonus = 1
        game_state.update_scores(country_change, shoreline_change, random_country_impact, random_shoreline_impact, annual_bonus)
        print(f"分数更新后：国家{game_state.country_score}, 海岸线{game_state.shoreline_score} (含年度奖励+{annual_bonus})")
        
        # 模拟海岸线响应
        shore_response = {
            "opportunities": f"第{year}年新机遇：海洋科技发展",
            "challenges": f"第{year}年新挑战：气候变化加剧"
        }
        print(f"海岸线响应: {shore_response}")
        
        # 记录年度数据
        random_events_data = [
            {
                "name": event.name,
                "description": event.description,
                "country_impact": event.country_impact,
                "shoreline_impact": event.shoreline_impact,
                "occurred": occurred
            }
            for event, occurred in triggered_events
        ]
        
        game_state.record_year(
            country_actions=country_actions,
            shore_response=shore_response,
            judge_scores=judge_scores,
            random_events=random_events_data,
            country_change=country_change,
            shoreline_change=shoreline_change,
            random_country_impact=random_country_impact,
            random_shoreline_impact=random_shoreline_impact
        )
        
        # 检查游戏是否结束
        if game_state.is_game_over():
            print(f"游戏结束: {game_state._get_game_over_reason()}")
            break
    
    # 显示游戏总结
    summary = game_state.get_game_summary()
    print(f"\n=== 游戏总结 ===")
    print(f"游戏时长: {summary['total_years']}年")
    print(f"最终分数: 国家{summary['final_scores']['country']}, 海岸线{summary['final_scores']['shoreline']}")
    print(f"游戏结果: {'胜利' if summary['victory'] else '失败'}")
    print(f"结束原因: {summary['game_over_reason']}")
    
    # 导出数据
    filename = game_state.export_to_json("demo_game.json")
    print(f"演示数据已导出到: {filename}")
    
    print()

def show_usage_examples():
    """显示使用示例"""
    print("=== 使用示例 ===")
    
    print("1. 基本使用:")
    print("   python run_game.py")
    print()
    
    print("2. 编程接口:")
    print("   from src import ShorlineEcologyGame")
    print("   game = ShorlineEcologyGame(api_key='your_key')")
    print("   statistics = game.run_multiple_games(10)")
    print()
    
    print("3. 环境变量配置:")
    print("   export OPENAI_API_KEY='your_key'")
    print("   export OPENAI_BASE_URL='https://api.openai.com/v1'")
    print("   export OPENAI_MODEL='gpt-3.5-turbo'")
    print()

def main():
    """主测试函数"""
    print("海岸线生态对抗建模系统 - 测试和演示")
    print("=" * 50)
    
    try:
        # 运行各项测试
        test_llm_client()
        test_random_events()
        test_game_state()
        demo_game_flow()
        show_usage_examples()
        
        print("✅ 所有测试和演示完成!")
        print("\n下一步：")
        print("1. 配置您的LLM API密钥")
        print("2. 运行 'python run_game.py' 开始真实游戏")
        print("3. 查看生成的JSON文件了解详细结果")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

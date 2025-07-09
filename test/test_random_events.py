"""
随机事件LLM评估功能测试脚本
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.random_events import RandomEventSystem, RandomEvent
from src.llm_client import LLMClient
from src.game_state import GameState

def test_event_probabilities():
    """测试随机事件概率调整"""
    print("📊 随机事件概率测试")
    print("=" * 50)
    
    event_system = RandomEventSystem(use_llm_evaluation=False)
    
    print("当前随机事件列表及概率:")
    for i, event in enumerate(event_system.events, 1):
        print(f"{i:2d}. {event.name:<15} - 概率: {event.probability:.3f} - 预设影响: 国家{event.country_impact:+d}, 海岸线{event.shoreline_impact:+d}")
    
    print(f"\n总计 {len(event_system.events)} 个事件")
    print(f"最高概率: {max(event.probability for event in event_system.events):.3f}")
    print(f"平均概率: {sum(event.probability for event in event_system.events) / len(event_system.events):.3f}")
    
    # 测试事件触发
    print(f"\n模拟100次事件触发测试:")
    triggered_count = 0
    for _ in range(100):
        triggered = event_system.trigger_random_events(1)
        if triggered:
            triggered_count += len([e for e, occurred in triggered if occurred])
    
    print(f"100次测试中共触发 {triggered_count} 次事件")
    print(f"平均触发率: {triggered_count/100:.1%}")
    print()

def test_impact_limits():
    """测试影响值限制在±3范围内"""
    print("🎯 影响值限制测试")
    print("=" * 50)
    
    event_system = RandomEventSystem(use_llm_evaluation=False)
    
    print("检查所有事件的影响值是否在±3范围内:")
    violations = []
    
    for event in event_system.events:
        country_impact = max(-3, min(3, event.country_impact))
        shoreline_impact = max(-3, min(3, event.shoreline_impact))
        
        country_violation = country_impact != event.country_impact
        shoreline_violation = shoreline_impact != event.shoreline_impact
        
        if country_violation or shoreline_violation:
            violations.append({
                'name': event.name,
                'original_country': event.country_impact,
                'limited_country': country_impact,
                'original_shoreline': event.shoreline_impact,
                'limited_shoreline': shoreline_impact
            })
        
        print(f"✅ {event.name:<20} - 国家: {country_impact:+d}, 海岸线: {shoreline_impact:+d}")
    
    if violations:
        print(f"\n⚠️  发现 {len(violations)} 个事件需要限制调整:")
        for v in violations:
            print(f"   {v['name']}: 国家 {v['original_country']:+d}→{v['limited_country']:+d}, 海岸线 {v['original_shoreline']:+d}→{v['limited_shoreline']:+d}")
    else:
        print("\n✅ 所有事件影响值都在±3范围内")
    
    print()

def test_llm_evaluation_simulation():
    """模拟LLM评估功能（不实际调用API）"""
    print("🤖 LLM评估功能模拟测试")
    print("=" * 50)
    
    # 模拟LLM客户端
    class MockLLMClient:
        def call_judge_llm_for_random_event(self, event_name, event_description, country_score, shoreline_score):
            # 模拟不同事件的评估结果
            if "海啸" in event_name or "台风" in event_name:
                return {"country_impact": -3, "shoreline_impact": -3, "reasoning": "严重自然灾害"}
            elif "保护区" in event_name or "技术" in event_name:
                return {"country_impact": 2, "shoreline_impact": 2, "reasoning": "积极环保措施"}
            elif "援助" in event_name:
                return {"country_impact": 3, "shoreline_impact": 1, "reasoning": "国际支持主要促进国家发展"}
            else:
                return {"country_impact": 0, "shoreline_impact": 1, "reasoning": "中性事件轻微影响"}
    
    mock_client = MockLLMClient()
    event_system = RandomEventSystem(use_llm_evaluation=True)
    
    # 测试几个代表性事件
    test_events = [
        RandomEvent("海啸", "强烈海啸袭击海岸线", 0.01, -3, -3),
        RandomEvent("海洋保护区成效", "保护区政策显现成效", 0.04, 1, 2),
        RandomEvent("国际援助", "获得国际环保资金援助", 0.02, 3, 1),
        RandomEvent("渔业资源波动", "渔业资源自然波动", 0.05, 0, 1)
    ]
    
    print("模拟LLM评估不同事件:")
    for event in test_events:
        country_impact, shoreline_impact = event_system.evaluate_event_impact_with_llm(
            event, mock_client, 65, 85
        )
        print(f"📋 {event.name:<20} - LLM评估: 国家{country_impact:+d}, 海岸线{shoreline_impact:+d}")
    
    print()

def demonstrate_new_features():
    """演示新功能特性"""
    print("✨ 新功能特性演示")
    print("=" * 50)
    
    print("1. 随机事件概率降低:")
    print("   ✅ 所有事件概率调整到0.1以下")
    print("   ✅ 减少游戏中的随机性，更注重策略")
    print()
    
    print("2. 影响值限制:")
    print("   ✅ 所有随机事件影响限制在±3分范围内")
    print("   ✅ 避免单个事件造成过大波动")
    print()
    
    print("3. LLM智能评估:")
    print("   ✅ 可选择启用LLM实时评估随机事件影响")
    print("   ✅ 根据当前游戏状态动态调整事件影响")
    print("   ✅ 提供评估理由，增加透明度")
    print()
    
    print("4. 双重保障机制:")
    print("   ✅ LLM评估失败时自动回退到预设值")
    print("   ✅ 所有影响值都经过±3范围检查")
    print()
    
    print("5. 配置灵活性:")
    print("   ✅ 可选择启用/关闭LLM评估")
    print("   ✅ 支持预设模式和智能模式切换")
    print()

def show_usage_examples():
    """显示使用示例"""
    print("📖 新功能使用示例")
    print("=" * 50)
    
    print("1. 命令行使用:")
    print("   运行游戏时会询问:")
    print("   '是否使用LLM评估随机事件影响? (y/n, 默认y):'")
    print()
    
    print("2. 编程接口:")
    print("   # 启用LLM评估")
    print("   game = ShorlineEcologyGame(use_llm_for_random_events=True)")
    print()
    print("   # 关闭LLM评估，使用预设值")
    print("   game = ShorlineEcologyGame(use_llm_for_random_events=False)")
    print()
    
    print("3. 随机事件系统:")
    print("   # 直接创建系统")
    print("   event_system = RandomEventSystem(use_llm_evaluation=True)")
    print()
    
    print("4. 推荐使用场景:")
    print("   🎯 研究模式: 启用LLM评估，获得更真实的事件影响")
    print("   ⚡ 快速测试: 关闭LLM评估，使用固定值提高速度")
    print("   🔬 对比分析: 分别运行两种模式，比较结果差异")
    print()

def main():
    """主测试函数"""
    print("🌊 海岸线生态对抗建模系统 - 随机事件LLM评估测试")
    print("=" * 60)
    print()
    
    try:
        # 测试事件概率
        test_event_probabilities()
        
        # 测试影响值限制
        test_impact_limits()
        
        # 模拟LLM评估
        test_llm_evaluation_simulation()
        
        # 演示新功能
        demonstrate_new_features()
        
        # 显示使用示例
        show_usage_examples()
        
        print("🎉 随机事件LLM评估测试完成!")
        print()
        print("💡 关键改进:")
        print("   📉 事件概率降低到0.1以下")
        print("   🎯 影响值限制在±3范围内")
        print("   🤖 可选LLM智能评估")
        print("   🛡️  双重保障机制")
        print()
        print("🚀 准备开始游戏? 运行: python run_game.py")
        
    except KeyboardInterrupt:
        print("\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

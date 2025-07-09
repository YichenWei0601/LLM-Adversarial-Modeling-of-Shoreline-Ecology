#!/usr/bin/env python3
"""
随机事件系统测试脚本
测试概率≤0.1，分数影响≤3，LLM评估功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.random_events import RandomEventSystem
from src.llm_client import LLMClient
import time

def test_event_probabilities():
    """测试事件概率是否都≤0.1"""
    print("🔍 测试随机事件概率...")
    
    event_system = RandomEventSystem(use_llm_evaluation=False)
    
    max_prob = 0
    over_limit_events = []
    
    for event in event_system.events:
        print(f"   {event.name}: {event.probability:.3f}")
        if event.probability > 0.1:
            over_limit_events.append((event.name, event.probability))
        max_prob = max(max_prob, event.probability)
    
    print(f"\n📊 概率统计:")
    print(f"   最大概率: {max_prob:.3f}")
    print(f"   超过0.1的事件: {len(over_limit_events)}")
    
    if over_limit_events:
        print("❌ 发现超过0.1概率的事件:")
        for name, prob in over_limit_events:
            print(f"     {name}: {prob:.3f}")
        return False
    else:
        print("✅ 所有事件概率都≤0.1")
        return True

def test_event_impacts():
    """测试事件分数影响是否都≤3"""
    print("\n🔍 测试随机事件分数影响...")
    
    event_system = RandomEventSystem(use_llm_evaluation=False)
    
    over_limit_events = []
    
    for event in event_system.events:
        country_abs = abs(event.country_impact)
        shoreline_abs = abs(event.shoreline_impact)
        print(f"   {event.name}: 国家{event.country_impact:+d}, 海岸线{event.shoreline_impact:+d}")
        
        if country_abs > 3 or shoreline_abs > 3:
            over_limit_events.append((event.name, event.country_impact, event.shoreline_impact))
    
    print(f"\n📊 影响统计:")
    print(f"   超过±3影响的事件: {len(over_limit_events)}")
    
    if over_limit_events:
        print("❌ 发现超过±3影响的事件:")
        for name, country, shoreline in over_limit_events:
            print(f"     {name}: 国家{country:+d}, 海岸线{shoreline:+d}")
        return False
    else:
        print("✅ 所有事件影响都≤±3")
        return True

def test_event_statistics():
    """测试事件统计功能"""
    print("\n🔍 测试事件统计功能...")
    
    event_system = RandomEventSystem(use_llm_evaluation=True)
    stats = event_system.get_event_statistics()
    
    print(f"📊 事件统计:")
    print(f"   总事件数: {stats['total_events']}")
    print(f"   灾难事件: {stats['disaster_events']}")
    print(f"   积极事件: {stats['positive_events']}")
    print(f"   中性事件: {stats['neutral_events']}")
    print(f"   最大概率: {stats['max_probability']:.3f}")
    print(f"   平均概率: {stats['avg_probability']:.3f}")
    print(f"   LLM评估: {'启用' if stats['use_llm_evaluation'] else '关闭'}")
    
    return True

def test_probability_modifier():
    """测试概率修正功能"""
    print("\n🔍 测试概率修正功能...")
    
    event_system = RandomEventSystem(use_llm_evaluation=False)
    
    # 测试不同海岸线分数的修正
    test_scores = [100, 90, 75, 60, 45, 30]
    
    for score in test_scores:
        modifier = event_system.get_disaster_probability_modifier(score)
        print(f"   海岸线分数{score}: 修正因子{modifier:.1f}")
        
        # 测试应用修正后的概率
        event_system.reset_probabilities()
        event_system.apply_disaster_modifier(score)
        
        max_prob = max(e.probability for e in event_system.events if e.shoreline_impact < 0 or e.country_impact < 0)
        print(f"     应用修正后最大灾难概率: {max_prob:.3f}")
        
        if max_prob > 0.1:
            print(f"     ⚠️  警告: 修正后概率超过0.1")
    
    return True

def test_random_event_triggering():
    """测试随机事件触发"""
    print("\n🔍 测试随机事件触发...")
    
    event_system = RandomEventSystem(use_llm_evaluation=False)
    
    # 模拟100年，统计事件发生情况
    total_events = 0
    event_counts = {}
    
    print("   模拟100年随机事件...")
    for year in range(1, 101):
        triggered = event_system.trigger_random_events(year)
        total_events += len(triggered)
        
        for event, occurred in triggered:
            if occurred:
                event_counts[event.name] = event_counts.get(event.name, 0) + 1
    
    print(f"\n📊 100年事件统计:")
    print(f"   总事件次数: {total_events}")
    print(f"   平均每年: {total_events/100:.2f}次")
    print(f"   发生过的事件类型: {len(event_counts)}")
    
    if event_counts:
        print("   各事件发生次数:")
        for name, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"     {name}: {count}次")
    
    return True

def test_llm_evaluation():
    """测试LLM评估功能（模拟）"""
    print("\n🔍 测试LLM评估功能...")
    
    event_system = RandomEventSystem(use_llm_evaluation=True)
    
    # 创建模拟LLM客户端
    class MockLLMClient:
        def call_judge_llm_for_random_event(self, event_name, event_description, current_country_score, current_shoreline_score):
            # 模拟LLM评估，返回在±3范围内的随机值
            import random
            return {
                'country_impact': random.randint(-3, 3),
                'shoreline_impact': random.randint(-3, 3),
                'reasoning': f'模拟评估: {event_name}'
            }
    
    mock_client = MockLLMClient()
    
    # 测试几个事件的LLM评估
    test_events = event_system.events[:3]  # 取前3个事件测试
    
    for event in test_events:
        country_impact, shoreline_impact = event_system.evaluate_event_impact_with_llm(
            event, mock_client, 50, 50
        )
        print(f"   {event.name}: LLM评估影响 国家{country_impact:+d}, 海岸线{shoreline_impact:+d}")
        
        # 验证LLM评估结果是否在±3范围内
        if abs(country_impact) > 3 or abs(shoreline_impact) > 3:
            print(f"     ❌ LLM评估结果超出±3范围")
            return False
    
    print("✅ LLM评估功能正常，结果在±3范围内")
    return True

def main():
    """主测试函数"""
    print("🎯 随机事件系统测试开始...\n")
    
    tests = [
        ("事件概率测试", test_event_probabilities),
        ("事件影响测试", test_event_impacts),
        ("事件统计测试", test_event_statistics),
        ("概率修正测试", test_probability_modifier),
        ("事件触发测试", test_random_event_triggering),
        ("LLM评估测试", test_llm_evaluation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 {test_name}")
        print('='*60)
        
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name} 通过")
            else:
                print(f"❌ {test_name} 失败")
        except Exception as e:
            print(f"❌ {test_name} 出错: {e}")
    
    print(f"\n{'='*60}")
    print(f"🎯 测试总结: {passed}/{total} 通过")
    print('='*60)
    
    if passed == total:
        print("🎉 所有测试通过！随机事件系统符合要求：")
        print("   ✅ 所有事件概率 ≤ 0.1")
        print("   ✅ 所有事件影响 ≤ ±3")
        print("   ✅ 支持LLM智能评估")
        print("   ✅ 支持概率修正机制")
        return True
    else:
        print("❌ 部分测试失败，请检查随机事件系统")
        return False

if __name__ == "__main__":
    main()

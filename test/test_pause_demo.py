"""
测试暂停功能的演示脚本
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.game_controller import ShorlineEcologyGame
from src.game_state import GameState
from src.random_events import RandomEventSystem

def test_pause_functionality():
    """测试暂停功能"""
    print("🧪 测试暂停功能演示")
    print("=" * 50)
    
    # 模拟游戏状态
    game_state = GameState()
    event_system = RandomEventSystem()
    
    print("模拟3年的游戏进程，每年暂停2秒观察...")
    print()
    
    for year in range(1, 4):
        game_state.year = year
        print(f"🗓️  === 第{year}年 ===")
        
        # 模拟游戏数据
        country_actions = {
            "action_1": f"第{year}年行动1：发展可再生能源",
            "action_2": f"第{year}年行动2：建立海洋保护区"
        }
        
        # 模拟分数变化
        country_change = 3
        shoreline_change = -1
        
        # 模拟随机事件
        triggered_events = event_system.trigger_random_events(year)
        random_country_impact = sum(event.country_impact for event, occurred in triggered_events if occurred)
        random_shoreline_impact = sum(event.shoreline_impact for event, occurred in triggered_events if occurred)
        
        # 更新分数
        game_state.update_scores(country_change, shoreline_change, random_country_impact, random_shoreline_impact)
        
        # 模拟海岸线响应
        shore_response = {
            "opportunities": f"第{year}年新机遇：海洋科技发展带来新商机",
            "challenges": f"第{year}年新挑战：气候变化加剧海岸侵蚀"
        }
        
        # 显示年度总结（模拟实际游戏的输出格式）
        print(f"📊 第{year}年总结:")
        print(f"   国家行动1: {country_actions['action_1']}")
        print(f"   国家行动2: {country_actions['action_2']}")
        print(f"   分数变化: 国家{country_change:+d}, 海岸线{shoreline_change:+d}")
        
        if random_country_impact != 0 or random_shoreline_impact != 0:
            print(f"   随机事件影响: 国家{random_country_impact:+d}, 海岸线{random_shoreline_impact:+d}")
        
        if triggered_events:
            event_names = [event.name for event, occurred in triggered_events if occurred]
            if event_names:
                print(f"   发生的随机事件: {', '.join(event_names)}")
        
        print(f"   当前分数: 国家={game_state.country_score}, 海岸线={game_state.shoreline_score}")
        print(f"   新的机遇: {shore_response['opportunities']}")
        print(f"   新的挑战: {shore_response['challenges']}")
        
        # 暂停观察
        print(f"\n⏳ 暂停2秒，观察年度变化...")
        time.sleep(2)
        print("-" * 80)
        print()
    
    print("✅ 暂停功能测试完成！")
    print()

def demo_different_pause_modes():
    """演示不同的暂停模式"""
    print("🎮 不同暂停模式演示")
    print("=" * 50)
    
    print("1. 快速模式演示（无暂停）:")
    print("   连续输出3年数据...")
    for year in range(1, 4):
        print(f"   第{year}年: 国家分数={60+year*5}, 海岸线分数={100-year*2}")
    print("   ✅ 快速模式完成\n")
    
    print("2. 观察模式演示（每年暂停1秒）:")
    for year in range(1, 4):
        print(f"   第{year}年: 国家分数={60+year*5}, 海岸线分数={100-year*2}")
        print("   ⏳ 暂停1秒...")
        time.sleep(1)
        if year < 3:
            print("   ───────────────")
    print("   ✅ 观察模式完成\n")

def show_usage_examples():
    """显示使用示例"""
    print("📖 暂停功能使用示例")
    print("=" * 50)
    
    print("1. 命令行使用:")
    print("   运行 python run_game.py")
    print("   选择 'y' 启用年度暂停")
    print("   输入暂停时长（如 5 秒）")
    print()
    
    print("2. 编程接口:")
    print("   # 启用暂停观察")
    print("   game = ShorlineEcologyGame(pause_between_years=True, pause_duration=5.0)")
    print("   summary = game.run_single_game()  # 每年暂停5秒")
    print()
    print("   # 快速模式")
    print("   game = ShorlineEcologyGame(pause_between_years=False)")
    print("   statistics = game.run_multiple_games(10)  # 连续运行")
    print()
    
    print("3. 推荐使用场景:")
    print("   📈 单次游戏观察: 启用暂停，设置3-5秒")
    print("   📊 多次游戏统计: 关闭暂停，快速收集数据")
    print("   🔍 详细分析: 启用暂停，设置更长时间")
    print()

def main():
    """主演示函数"""
    print("🌊 海岸线生态对抗建模系统 - 暂停功能演示")
    print("=" * 60)
    print()
    
    try:
        # 演示不同的暂停模式
        demo_different_pause_modes()
        
        # 测试暂停功能
        test_pause_functionality()
        
        # 显示使用示例
        show_usage_examples()
        
        print("🎉 演示完成！")
        print()
        print("💡 提示:")
        print("   - 单次游戏建议启用暂停，便于观察每年的详细变化")
        print("   - 多次游戏统计建议使用快速模式，提高效率")
        print("   - 可以根据需要自定义暂停时长（1-10秒）")
        print()
        print("🚀 准备开始真实游戏? 运行: python run_game.py")
        
    except KeyboardInterrupt:
        print("\n⏹️  演示被用户中断")
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")

if __name__ == "__main__":
    main()

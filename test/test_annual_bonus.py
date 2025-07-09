"""
年度奖励功能演示脚本
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.game_state import GameState
from src.random_events import RandomEventSystem

def demo_annual_bonus():
    """演示年度奖励功能"""
    print("🎁 年度奖励功能演示")
    print("=" * 50)
    
    # 创建游戏状态
    game_state = GameState()
    event_system = RandomEventSystem()
    
    print(f"初始状态: 国家={game_state.country_score}, 海岸线={game_state.shoreline_score}")
    print()
    
    print("模拟5年游戏，每年都有年度奖励+1分:")
    print("-" * 50)
    
    for year in range(1, 6):
        game_state.year = year
        print(f"🗓️  第{year}年:")
        
        # 模拟基础分数变化
        country_change = 2  # 基础变化
        shoreline_change = -1  # 基础变化
        
        # 模拟随机事件（简化）
        random_country_impact = 0
        random_shoreline_impact = 0
        
        # 年度奖励
        annual_bonus = 1
        
        print(f"   基础分数变化: 国家{country_change:+d}, 海岸线{shoreline_change:+d}")
        print(f"   年度自然增长: 国家+{annual_bonus}, 海岸线+{annual_bonus}")
        
        # 更新分数
        old_country = game_state.country_score
        old_shoreline = game_state.shoreline_score
        
        game_state.update_scores(
            country_change=country_change,
            shoreline_change=shoreline_change,
            random_country_impact=random_country_impact,
            random_shoreline_impact=random_shoreline_impact,
            annual_bonus=annual_bonus
        )
        
        # 计算实际变化
        actual_country_change = game_state.country_score - old_country
        actual_shoreline_change = game_state.shoreline_score - old_shoreline
        
        print(f"   实际总变化: 国家{actual_country_change:+d}, 海岸线{actual_shoreline_change:+d}")
        print(f"   当前分数: 国家={game_state.country_score}, 海岸线={game_state.shoreline_score}")
        print()
        
        time.sleep(1)  # 暂停1秒便于观察
    
    print("✅ 年度奖励演示完成!")
    print()

def compare_with_without_bonus():
    """对比有无年度奖励的差异"""
    print("📊 年度奖励影响对比")
    print("=" * 50)
    
    # 无奖励情况
    print("1. 无年度奖励模式:")
    game_state_no_bonus = GameState()
    for year in range(1, 4):
        game_state_no_bonus.year = year
        # 模拟相同的基础变化
        game_state_no_bonus.update_scores(
            country_change=2,
            shoreline_change=-1,
            annual_bonus=0  # 无奖励
        )
        print(f"   第{year}年: 国家={game_state_no_bonus.country_score}, 海岸线={game_state_no_bonus.shoreline_score}")
    
    print()
    
    # 有奖励情况
    print("2. 有年度奖励模式(+1):")
    game_state_with_bonus = GameState()
    for year in range(1, 4):
        game_state_with_bonus.year = year
        # 模拟相同的基础变化
        game_state_with_bonus.update_scores(
            country_change=2,
            shoreline_change=-1,
            annual_bonus=1  # 有奖励
        )
        print(f"   第{year}年: 国家={game_state_with_bonus.country_score}, 海岸线={game_state_with_bonus.shoreline_score}")
    
    print()
    
    # 分析差异
    country_diff = game_state_with_bonus.country_score - game_state_no_bonus.country_score
    shoreline_diff = game_state_with_bonus.shoreline_score - game_state_no_bonus.shoreline_score
    
    print("📈 3年后的差异:")
    print(f"   国家分数差异: +{country_diff}分")
    print(f"   海岸线分数差异: +{shoreline_diff}分")
    print(f"   年度奖励累计效果: 3年 × 1分/年 = 3分")
    print()

def demo_different_bonus_values():
    """演示不同年度奖励值的效果"""
    print("🎯 不同年度奖励值效果对比")
    print("=" * 50)
    
    bonus_values = [0, 1, 2, 3]
    results = {}
    
    for bonus in bonus_values:
        game_state = GameState()
        print(f"年度奖励 +{bonus}分:")
        
        for year in range(1, 4):
            game_state.year = year
            game_state.update_scores(
                country_change=1,  # 统一基础变化
                shoreline_change=-1,
                annual_bonus=bonus
            )
        
        results[bonus] = {
            'country': game_state.country_score,
            'shoreline': game_state.shoreline_score
        }
        
        print(f"   3年后: 国家={game_state.country_score}, 海岸线={game_state.shoreline_score}")
    
    print()
    print("📊 总结对比:")
    for bonus in bonus_values:
        country_total = results[bonus]['country'] - 60  # 减去初始分数
        shoreline_total = results[bonus]['shoreline'] - 100
        print(f"   奖励+{bonus}: 国家总增长{country_total:+d}, 海岸线总变化{shoreline_total:+d}")
    
    print()

def show_gameplay_implications():
    """展示年度奖励对游戏的影响"""
    print("🎮 年度奖励对游戏策略的影响")
    print("=" * 50)
    
    print("1. 游戏平衡性:")
    print("   ✅ 避免分数过度下降")
    print("   ✅ 确保长期游戏的可玩性")
    print("   ✅ 模拟自然的发展趋势")
    print()
    
    print("2. 策略意义:")
    print("   📈 国家发展: 每年基础+1分，减少达到100分的难度")
    print("   🌊 海岸线维护: 每年基础+1分，增加维持75分以上的可能性")
    print("   ⚖️  平衡考量: 玩家需要考虑长期累积效应")
    print()
    
    print("3. 推荐配置:")
    print("   🎯 标准模式: annual_bonus=1 (推荐新手)")
    print("   💪 挑战模式: annual_bonus=0 (纯策略博弈)")
    print("   🚀 快速模式: annual_bonus=2 (快节奏游戏)")
    print()
    
    print("4. 实际案例分析:")
    print("   假设每年基础变化: 国家+2, 海岸线-1")
    print("   无奖励模式: 25年后 国家=110, 海岸线=75 (刚好及格)")
    print("   +1奖励模式: 25年后 国家=135, 海岸线=100 (更安全)")
    print()

def main():
    """主演示函数"""
    print("🌊 海岸线生态对抗建模系统 - 年度奖励功能演示")
    print("=" * 60)
    print()
    
    try:
        # 基础演示
        demo_annual_bonus()
        
        # 对比演示
        compare_with_without_bonus()
        
        # 不同奖励值演示
        demo_different_bonus_values()
        
        # 游戏影响分析
        show_gameplay_implications()
        
        print("🎉 年度奖励功能演示完成!")
        print()
        print("💡 使用提示:")
        print("   - 运行游戏时可以自定义年度奖励值")
        print("   - 推荐新手使用+1分奖励")
        print("   - 高级玩家可以尝试0奖励挑战模式")
        print("   - 快速测试可以使用+2或+3分奖励")
        print()
        print("🚀 准备开始游戏? 运行: python run_game.py")
        
    except KeyboardInterrupt:
        print("\n⏹️  演示被用户中断")
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

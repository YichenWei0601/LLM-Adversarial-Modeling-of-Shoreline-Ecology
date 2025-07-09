"""
主游戏控制器
协调各个模块，运行对抗性建模游戏
"""

import logging
import os
import json
import time
from typing import Dict, List, Any
from .llm_client import LLMClient
from .random_events import RandomEventSystem
from .game_state import GameState

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ShorlineEcologyGame:
    """海岸线生态对抗建模游戏主控制器"""
    
    def __init__(self, api_key: str = None, base_url: str = None, model: str = "gpt-3.5-turbo", 
                 pause_between_years: bool = True, pause_duration: float = 5.0, annual_bonus: int = 1,
                 use_llm_for_random_events: bool = True):
        """
        初始化游戏
        
        Args:
            api_key: LLM API密钥
            base_url: LLM API基础URL
            model: 使用的模型名称
            pause_between_years: 是否在每年之间暂停
            pause_duration: 暂停时长（秒）
            annual_bonus: 每年自动增加的分数（默认1分）
            use_llm_for_random_events: 是否使用LLM评估随机事件
        """
        self.llm_client = LLMClient(api_key=api_key, base_url=base_url, model=model)
        self.random_event_system = RandomEventSystem(use_llm_evaluation=use_llm_for_random_events)
        self.game_state = GameState()
        self.ref_scoring_table = self._load_reference_table()
        self.pause_between_years = pause_between_years
        self.pause_duration = pause_duration
        self.annual_bonus = annual_bonus
        self.use_llm_for_random_events = use_llm_for_random_events
        
        logger.info(f"海岸线生态对抗建模游戏初始化完成 (年度奖励: +{annual_bonus}, 随机事件LLM评估: {'启用' if use_llm_for_random_events else '关闭'})")
    
    def _load_reference_table(self) -> str:
        """加载参考评分表"""
        try:
            with open("prompt/ref_scoring_table.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error("参考评分表文件未找到")
            return ""
    
    def run_single_game(self) -> Dict[str, Any]:
        """
        运行单次游戏
        
        Returns:
            游戏结果摘要
        """
        logger.info("开始新的游戏回合")
        self.game_state.reset_game()
        
        while not self.game_state.is_game_over():
            self.game_state.year += 1
            logger.info(f"=== 第{self.game_state.year}年 ===")
            
            try:
                # 1. 人类LLM决策
                logger.info("人类LLM进行决策...")
                country_actions = self.llm_client.call_human_llm(
                    country_score=self.game_state.country_score,
                    shoreline_score=self.game_state.shoreline_score,
                    opportunities=self.game_state.current_opportunities,
                    challenges=self.game_state.current_challenges,
                    ref_table=self.ref_scoring_table
                )
                
                # 2. 裁判LLM评分
                logger.info("裁判LLM进行评分...")
                actions_text = f"ACTION_1: {country_actions.get('action_1', '')}\nACTION_2: {country_actions.get('action_2', '')}"
                judge_scores = self.llm_client.call_judge_llm(
                    country_actions=actions_text,
                    ref_table=self.ref_scoring_table
                )
                
                # 3. 计算分数变化
                country_change = judge_scores.get('first_country', 0) + judge_scores.get('second_country', 0)
                shoreline_change = judge_scores.get('first_shoreline', 0) + judge_scores.get('second_shoreline', 0)
                
                # 4. 触发随机事件 (如果启用)
                random_country_impact = 0
                random_shoreline_impact = 0
                triggered_events = []
                
                if getattr(self, 'enable_random_events', True):
                    logger.info("检查随机事件...")
                    self.random_event_system.apply_disaster_modifier(self.game_state.shoreline_score)
                    triggered_events = self.random_event_system.trigger_random_events(self.game_state.year)
                    
                    if self.use_llm_for_random_events:
                        random_country_impact, random_shoreline_impact = self.random_event_system.calculate_total_impact_with_llm(
                            triggered_events, self.llm_client, self.game_state.country_score, self.game_state.shoreline_score
                        )
                    else:
                        random_country_impact, random_shoreline_impact = self.random_event_system.calculate_total_impact(triggered_events)
                else:
                    logger.info("随机事件已禁用")
                
                # 5. 更新分数
                self.game_state.update_scores(
                    country_change=country_change,
                    shoreline_change=shoreline_change,
                    random_country_impact=random_country_impact,
                    random_shoreline_impact=random_shoreline_impact,
                    annual_bonus=self.annual_bonus
                )
                
                # 6. 海岸线LLM响应
                logger.info("海岸线LLM生成响应...")
                shore_response = self.llm_client.call_shore_llm(actions_text)
                
                # 7. 更新当前机遇和挑战
                self.game_state.current_opportunities = shore_response.get('opportunities', self.game_state.current_opportunities)
                self.game_state.current_challenges = shore_response.get('challenges', self.game_state.current_challenges)
                
                # 8. 记录年度数据
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
                
                self.game_state.record_year(
                    country_actions=country_actions,
                    shore_response=shore_response,
                    judge_scores=judge_scores,
                    random_events=random_events_data,
                    country_change=country_change,
                    shoreline_change=shoreline_change,
                    random_country_impact=random_country_impact,
                    random_shoreline_impact=random_shoreline_impact,
                    annual_bonus=self.annual_bonus
                )
                
                # 9. 显示当前状态
                print(f"\n📊 第{self.game_state.year}年总结:")
                print(f"   国家行动1: {country_actions.get('action_1', 'N/A')}")
                print(f"   国家行动2: {country_actions.get('action_2', 'N/A')}")
                print(f"   分数变化: 国家{country_change:+d}, 海岸线{shoreline_change:+d}")
                if random_country_impact != 0 or random_shoreline_impact != 0:
                    print(f"   随机事件影响: 国家{random_country_impact:+d}, 海岸线{random_shoreline_impact:+d}")
                if self.annual_bonus > 0:
                    print(f"   年度自然增长: 国家+{self.annual_bonus}, 海岸线+{self.annual_bonus}")
                if triggered_events:
                    event_names = [event.name for event, occurred in triggered_events if occurred]
                    if event_names:
                        print(f"   发生的随机事件: {', '.join(event_names)}")
                print(f"   当前分数: 国家={self.game_state.country_score}, 海岸线={self.game_state.shoreline_score}")
                print(f"   新的机遇: {shore_response.get('opportunities', 'N/A')}")
                print(f"   新的挑战: {shore_response.get('challenges', 'N/A')}")
                
                logger.info(f"当前状态: 国家={self.game_state.country_score}, 海岸线={self.game_state.shoreline_score}")
                
                # 10. 暂停以便观察
                if self.pause_between_years:
                    print(f"\n⏳ 暂停{self.pause_duration}秒，观察年度变化...")
                    time.sleep(self.pause_duration)
                    print("-" * 80)
                
                # 11. 重置随机事件概率
                self.random_event_system.reset_probabilities()
                
            except Exception as e:
                logger.error(f"第{self.game_state.year}年处理出错: {str(e)}")
                break
        
        # 游戏结束
        summary = self.game_state.get_game_summary()
        logger.info(f"游戏结束: {summary['game_over_reason']}")
        
        return summary
    
    def run_multiple_games(self, num_games: int = 10, fast_mode: bool = True) -> Dict[str, Any]:
        """
        运行多次游戏并统计结果
        
        Args:
            num_games: 游戏次数
            fast_mode: 快速模式，禁用年度暂停
            
        Returns:
            多次游戏的统计结果
        """
        logger.info(f"开始运行{num_games}次游戏")
        
        # 临时保存原始设置
        original_pause = self.pause_between_years
        
        # 在多次游戏模式下，默认使用快速模式
        if fast_mode:
            self.pause_between_years = False
            print(f"🚀 多次游戏模式：已启用快速模式，将连续运行{num_games}次游戏")
        
        results = []
        victories = 0
        failures = 0
        
        for i in range(num_games):
            logger.info(f"运行第{i+1}次游戏...")
            
            try:
                summary = self.run_single_game()
                results.append(summary)
                
                if summary['victory']:
                    victories += 1
                else:
                    failures += 1
                
                # 保存单次游戏记录
                filename = f"game_{i+1:03d}.json"
                self.game_state.export_to_json(filename)
                
            except Exception as e:
                logger.error(f"第{i+1}次游戏运行失败: {str(e)}")
                failures += 1
        
        # 统计结果
        statistics = {
            "total_games": num_games,
            "victories": victories,
            "failures": failures,
            "victory_rate": victories / num_games if num_games > 0 else 0,
            "average_duration": sum(r['total_years'] for r in results) / len(results) if results else 0,
            "average_final_country_score": sum(r['final_scores']['country'] for r in results) / len(results) if results else 0,
            "average_final_shoreline_score": sum(r['final_scores']['shoreline'] for r in results) / len(results) if results else 0,
            "detailed_results": results
        }
        
        # 保存统计结果
        with open("game_statistics.json", "w", encoding="utf-8") as f:
            json.dump(statistics, f, ensure_ascii=False, indent=2)
        
        # 恢复原始设置
        self.pause_between_years = original_pause
        
        logger.info(f"多次游戏统计完成: 胜利率={statistics['victory_rate']:.2%}")
        
        return statistics
    
    def print_statistics(self, statistics: Dict[str, Any]):
        """
        打印游戏统计结果
        
        Args:
            statistics: 统计数据
        """
        print(f"\n=== 游戏统计结果 ===")
        print(f"总游戏次数: {statistics['total_games']}")
        print(f"胜利次数: {statistics['victories']}")
        print(f"失败次数: {statistics['failures']}")
        print(f"胜利率: {statistics['victory_rate']:.2%}")
        print(f"平均游戏时长: {statistics['average_duration']:.1f}年")
        print(f"平均最终国家分数: {statistics['average_final_country_score']:.1f}")
        print(f"平均最终海岸线分数: {statistics['average_final_shoreline_score']:.1f}")
        
        print(f"\n=== 详细结果 ===")
        for i, result in enumerate(statistics['detailed_results']):
            status = "胜利" if result['victory'] else "失败"
            print(f"游戏{i+1}: {status} ({result['total_years']}年) - 国家:{result['final_scores']['country']}, 海岸线:{result['final_scores']['shoreline']}")


def main():
    """主函数"""
    # 从环境变量或用户输入获取API配置
    api_key = os.getenv("OPENAI_API_KEY") or input("请输入OpenAI API Key: ")
    base_url = os.getenv("OPENAI_BASE_URL") or input("请输入API Base URL (可选，直接回车跳过): ") or None
    model = os.getenv("OPENAI_MODEL") or input("请输入模型名称 (默认gpt-3.5-turbo): ") or "gpt-3.5-turbo"
    
    # 暂停设置
    pause_input = input("是否在每年之间暂停观察? (y/n, 默认y): ").lower()
    pause_between_years = pause_input != "n"
    
    pause_duration = 5.0
    if pause_between_years:
        duration_input = input("请输入暂停时长(秒, 默认5): ")
        if duration_input:
            try:
                pause_duration = float(duration_input)
            except ValueError:
                print("输入格式错误，使用默认5秒")
                pause_duration = 5.0
    
    # 年度奖励设置
    annual_bonus = 1
    bonus_input = input("请输入每年自动增长分数 (默认1): ")
    if bonus_input:
        try:
            annual_bonus = int(bonus_input)
        except ValueError:
            print("输入格式错误，使用默认1分")
            annual_bonus = 1
    
    print(f"已设置每年自动增长: +{annual_bonus}分")
    
    # 随机事件评估设置
    llm_events_input = input("是否使用LLM评估随机事件影响? (y/n, 默认y): ").lower()
    use_llm_for_random_events = llm_events_input != "n"
    
    if use_llm_for_random_events:
        print("已启用LLM评估随机事件，事件影响将由AI实时判断")
    else:
        print("已关闭LLM评估随机事件，使用预设影响值")
    
    # 创建游戏实例
    game = ShorlineEcologyGame(
        api_key=api_key, 
        base_url=base_url, 
        model=model,
        pause_between_years=pause_between_years,
        pause_duration=pause_duration,
        annual_bonus=annual_bonus,
        use_llm_for_random_events=use_llm_for_random_events
    )
    
    # 运行多次游戏
    try:
        num_games = int(input("请输入要运行的游戏次数 (默认10): ") or "10")
        statistics = game.run_multiple_games(num_games)
        game.print_statistics(statistics)
    except KeyboardInterrupt:
        logger.info("用户中断游戏")
    except Exception as e:
        logger.error(f"游戏运行出错: {str(e)}")

if __name__ == "__main__":
    main()

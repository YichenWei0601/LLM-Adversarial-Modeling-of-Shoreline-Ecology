"""
游戏状态管理器
记录和管理游戏状态、分数变化等
"""

import json
import logging
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class YearlyRecord:
    """年度记录数据结构"""
    year: int
    country_score: int
    shoreline_score: int
    country_actions: Dict[str, str]
    shore_response: Dict[str, str]
    judge_scores: Dict[str, int]
    random_events: List[Dict[str, Any]]
    country_change: int
    shoreline_change: int
    random_country_impact: int
    random_shoreline_impact: int

class GameState:
    """游戏状态类"""
    
    def __init__(self, initial_country_score: int = 60, initial_shoreline_score: int = 100,
                 max_years: int = 25, victory_threshold: int = 100, failure_threshold: int = 75):
        self.initial_country_score = initial_country_score
        self.initial_shoreline_score = initial_shoreline_score
        self.max_years = max_years
        self.victory_threshold = victory_threshold
        self.failure_threshold = failure_threshold
        self.reset_game()
        logger.info(f"游戏状态初始化: 国家分数={initial_country_score}, 海岸线分数={initial_shoreline_score}, "
                   f"最大年数={max_years}, 胜利阈值={victory_threshold}, 失败阈值={failure_threshold}")
    
    def reset_game(self):
        """重置游戏状态"""
        self.country_score = self.initial_country_score
        self.shoreline_score = self.initial_shoreline_score
        self.year = 0
        self.game_over = False
        self.victory = False
        self.yearly_records = []
        self.current_opportunities = "海岸线提供丰富的渔业资源和旅游潜力"
        self.current_challenges = "海岸侵蚀和海洋污染威胁生态平衡"
    
    def is_game_over(self) -> bool:
        """检查游戏是否结束"""
        if self.country_score >= self.victory_threshold:
            self.victory = True
            self.game_over = True
            return True
        elif self.shoreline_score < self.failure_threshold:
            self.victory = False
            self.game_over = True
            return True
        elif self.year >= self.max_years:
            self.victory = False
            self.game_over = True
            return True
        return False
    
    def update_scores(self, country_change: int, shoreline_change: int, 
                     random_country_impact: int = 0, random_shoreline_impact: int = 0,
                     annual_bonus: int = 1):
        """
        更新分数
        
        Args:
            country_change: 国家分数变化
            shoreline_change: 海岸线分数变化
            random_country_impact: 随机事件对国家的影响
            random_shoreline_impact: 随机事件对海岸线的影响
            annual_bonus: 年度自然增长奖励（默认每年+1）
        """
        self.country_score += country_change + random_country_impact + annual_bonus
        self.shoreline_score += shoreline_change + random_shoreline_impact + annual_bonus
        
        # 确保分数在合理范围内
        self.country_score = max(0, min(100, self.country_score))
        self.shoreline_score = max(0, min(100, self.shoreline_score))
        
        logger.info(f"分数更新: 国家={self.country_score}, 海岸线={self.shoreline_score} (包含年度奖励+{annual_bonus})")
    
    
    def record_year(self, country_actions: Dict[str, str], shore_response: Dict[str, str],
                   judge_scores: Dict[str, int], random_events: List[Dict[str, Any]],
                   country_change: int, shoreline_change: int,
                   random_country_impact: int, random_shoreline_impact: int,
                   annual_bonus: int = 1):
        """
        记录年度数据
        
        Args:
            country_actions: 国家行动
            shore_response: 海岸线响应
            judge_scores: 裁判评分
            random_events: 随机事件
            country_change: 国家分数变化
            shoreline_change: 海岸线分数变化
            random_country_impact: 随机事件对国家的影响
            random_shoreline_impact: 随机事件对海岸线的影响
            annual_bonus: 年度自然增长奖励
        """
        record = YearlyRecord(
            year=self.year,
            country_score=self.country_score,
            shoreline_score=self.shoreline_score,
            country_actions=country_actions,
            shore_response=shore_response,
            judge_scores=judge_scores,
            random_events=random_events,
            country_change=country_change,
            shoreline_change=shoreline_change,
            random_country_impact=random_country_impact,
            random_shoreline_impact=random_shoreline_impact
        )
        
        self.yearly_records.append(record)
        logger.info(f"第{self.year}年记录已保存 (年度奖励: +{annual_bonus})")
    
    def get_game_summary(self) -> Dict[str, Any]:
        """获取游戏总结"""
        return {
            "initial_scores": {
                "country": self.initial_country_score,
                "shoreline": self.initial_shoreline_score
            },
            "final_scores": {
                "country": self.country_score,
                "shoreline": self.shoreline_score
            },
            "total_years": self.year,
            "victory": self.victory,
            "game_over_reason": self._get_game_over_reason(),
            "yearly_records": len(self.yearly_records)
        }
    
    def _get_game_over_reason(self) -> str:
        """获取游戏结束原因"""
        if self.victory:
            return f"国家发展达到{self.victory_threshold}分，获得胜利"
        elif self.shoreline_score < self.failure_threshold:
            return f"海岸线状态低于{self.failure_threshold}分，游戏失败"
        elif self.year >= self.max_years:
            return f"达到{self.max_years}年上限，游戏结束"
        else:
            return "游戏进行中"
    
    def export_to_json(self, filename: str = None) -> str:
        """
        导出游戏数据到JSON文件
        
        Args:
            filename: 文件名（可选）
            
        Returns:
            生成的文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"game_record_{timestamp}.json"
        
        # 准备导出数据
        export_data = {
            "game_summary": self.get_game_summary(),
            "yearly_records": []
        }
        
        # 转换年度记录
        for record in self.yearly_records:
            export_data["yearly_records"].append({
                "year": record.year,
                "country_score": record.country_score,
                "shoreline_score": record.shoreline_score,
                "country_actions": record.country_actions,
                "shore_response": record.shore_response,
                "judge_scores": record.judge_scores,
                "random_events": record.random_events,
                "score_changes": {
                    "country": record.country_change,
                    "shoreline": record.shoreline_change,
                    "random_country_impact": record.random_country_impact,
                    "random_shoreline_impact": record.random_shoreline_impact
                }
            })
        
        # 保存到文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"游戏数据已导出到: {filename}")
        return filename

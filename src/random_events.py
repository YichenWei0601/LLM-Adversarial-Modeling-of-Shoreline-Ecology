"""
随机事件系统
模拟自然灾害和其他随机事件对海岸线和国家发展的影响
概率≤0.1，分数影响绝对值≤3，支持LLM智能评估
"""

import random
import logging
from typing import Dict, Tuple, List

logger = logging.getLogger(__name__)

class RandomEvent:
    """随机事件类"""
    
    def __init__(self, name: str, description: str, probability: float, 
                 country_impact: int, shoreline_impact: int):
        self.name = name
        self.description = description
        self.probability = probability  # 发生概率 (0-1)
        self.country_impact = country_impact  # 对国家发展的影响
        self.shoreline_impact = shoreline_impact  # 对海岸线的影响

class RandomEventSystem:
    """随机事件系统"""
    
    def __init__(self, use_llm_evaluation: bool = True):
        self.events = self._initialize_events()
        self.use_llm_evaluation = use_llm_evaluation
        logger.info(f"随机事件系统初始化完成 (LLM评估: {'启用' if use_llm_evaluation else '关闭'})")
    
    def _initialize_events(self) -> List[RandomEvent]:
        """初始化随机事件列表 - 所有概率都≤0.1，分数影响绝对值≤3"""
        events = [
            # 自然灾害 - 概率≤0.1，影响≤3
            RandomEvent("海啸", "强烈海啸袭击海岸线，造成严重破坏", 0.001, -3, -3),
            RandomEvent("台风", "强台风登陆，对基础设施造成损害", 0.02, -1, -1),
            RandomEvent("海平面上升", "全球变暖导致海平面显著上升", 0.02, -1, -1),
            RandomEvent("风暴潮", "强风暴潮侵蚀海岸线", 0.04, -1, -1),
            RandomEvent("海洋酸化", "海洋酸化影响海洋生态系统", 0.002, -1, -2),
            RandomEvent("海岸侵蚀", "长期海岸侵蚀加剧", 0.008, -1, -2),
            RandomEvent("极端高温", "海洋极端高温事件", 0.003, -2, -3),
            
            # 积极事件 - 概率≤0.1，影响≤3
            RandomEvent("珊瑚礁复苏", "珊瑚礁生态系统自然恢复", 0.03, 1, 3),
            RandomEvent("海洋保护区成效", "海洋保护区政策显现成效", 0.06, 1, 2),
            RandomEvent("清洁技术突破", "新的清洁技术突破降低污染", 0.02, 2, 2),
            RandomEvent("国际援助", "获得国际环保资金援助", 0.08, 3, 1),
            RandomEvent("生态旅游兴起", "生态旅游带来经济效益", 0.1, 2, 1),
            RandomEvent("海洋生物多样性增加", "海洋生物多样性自然增加", 0.05, 1, 2),
            
            # 中性事件 - 概率≤0.1，影响≤3
            RandomEvent("渔业资源波动", "渔业资源因自然因素波动", 0.08, 0, random.randint(-2, 2)),
            RandomEvent("海洋生物迁移", "海洋生物迁移模式改变", 0.06, 0, random.randint(-1, 1)),
            RandomEvent("气候变化影响", "气候变化对海岸线造成缓慢影响", 0.09, random.randint(-1, 1), random.randint(-2, 1)),
            RandomEvent("洋流变化", "海洋洋流模式发生变化", 0.07, random.randint(-1, 1), random.randint(-1, 2)),
        ]
        
        # 确保所有随机影响都在±3范围内
        for event in events:
            event.country_impact = max(-3, min(3, event.country_impact))
            event.shoreline_impact = max(-3, min(3, event.shoreline_impact))
        
        return events
    
    def trigger_random_events(self, year: int) -> List[Tuple[RandomEvent, bool]]:
        """
        触发随机事件
        
        Args:
            year: 当前年份
            
        Returns:
            发生的事件列表及其是否发生
        """
        triggered_events = []
        
        for event in self.events:
            # 根据概率决定是否发生
            if random.random() < event.probability:
                triggered_events.append((event, True))
                logger.info(f"第{year}年发生随机事件: {event.name} - {event.description}")
        
        return triggered_events
    
    def calculate_total_impact(self, triggered_events: List[Tuple[RandomEvent, bool]]) -> Tuple[int, int]:
        """
        计算随机事件的总影响（使用预设值）
        
        Args:
            triggered_events: 触发的事件列表
            
        Returns:
            (国家发展影响, 海岸线影响)
        """
        total_country_impact = 0
        total_shoreline_impact = 0
        
        for event, occurred in triggered_events:
            if occurred:
                # 限制预设值在±3范围内
                country_impact = max(-3, min(3, event.country_impact))
                shoreline_impact = max(-3, min(3, event.shoreline_impact))
                
                total_country_impact += country_impact
                total_shoreline_impact += shoreline_impact
                
                logger.info(f"事件'{event.name}'影响: 国家{country_impact:+d}, 海岸线{shoreline_impact:+d}")
        
        return total_country_impact, total_shoreline_impact
    
    def calculate_total_impact_with_llm(self, triggered_events: List[Tuple[RandomEvent, bool]], 
                                       llm_client, current_country_score: int, current_shoreline_score: int) -> Tuple[int, int]:
        """
        使用LLM计算随机事件的总影响
        
        Args:
            triggered_events: 触发的事件列表
            llm_client: LLM客户端
            current_country_score: 当前国家分数
            current_shoreline_score: 当前海岸线分数
            
        Returns:
            (国家发展影响, 海岸线影响)
        """
        total_country_impact = 0
        total_shoreline_impact = 0
        
        for event, occurred in triggered_events:
            if occurred:
                if self.use_llm_evaluation:
                    country_impact, shoreline_impact = self.evaluate_event_impact_with_llm(
                        event, llm_client, current_country_score, current_shoreline_score
                    )
                else:
                    # 使用预设值但限制在±3范围内
                    country_impact = max(-3, min(3, event.country_impact))
                    shoreline_impact = max(-3, min(3, event.shoreline_impact))
                
                total_country_impact += country_impact
                total_shoreline_impact += shoreline_impact
                
                logger.info(f"事件'{event.name}'影响: 国家{country_impact:+d}, 海岸线{shoreline_impact:+d}")
        
        return total_country_impact, total_shoreline_impact
    
    def reset_probabilities(self):
        """重置所有事件的概率到初始值"""
        self.events = self._initialize_events()
    
    def get_disaster_probability_modifier(self, shoreline_score: int) -> float:
        """
        根据海岸线状态调整灾害概率
        海岸线状态越差，灾害概率越高
        
        Args:
            shoreline_score: 海岸线状态分数
            
        Returns:
            概率修正因子
        """
        if shoreline_score >= 90:
            return 0.5  # 状态良好，灾害概率降低
        elif shoreline_score >= 75:
            return 0.8  # 状态一般，灾害概率略降低
        elif shoreline_score >= 60:
            return 1.0  # 状态中等，概率不变
        elif shoreline_score >= 45:
            return 1.2  # 状态较差，灾害概率增加
        else:
            return 1.5  # 状态很差，灾害概率大幅增加
    
    def apply_disaster_modifier(self, shoreline_score: int):
        """
        应用灾害概率修正，但确保概率不超过0.1
        
        Args:
            shoreline_score: 海岸线状态分数
        """
        modifier = self.get_disaster_probability_modifier(shoreline_score)
        
        # 只对负面事件应用修正
        for event in self.events:
            if event.shoreline_impact < 0 or event.country_impact < 0:
                original_prob = event.probability
                event.probability = min(0.1, original_prob * modifier)  # 确保不超过0.1
    
    def evaluate_event_impact_with_llm(self, event: RandomEvent, llm_client, 
                                      current_country_score: int, current_shoreline_score: int) -> Tuple[int, int]:
        """
        使用LLM评估随机事件的影响
        
        Args:
            event: 随机事件
            llm_client: LLM客户端
            current_country_score: 当前国家分数
            current_shoreline_score: 当前海岸线分数
            
        Returns:
            (国家影响, 海岸线影响)
        """
        try:
            scores = llm_client.call_judge_llm_for_random_event(
                event_name=event.name,
                event_description=event.description,
                current_country_score=current_country_score,
                current_shoreline_score=current_shoreline_score
            )
            return scores['country_impact'], scores['shoreline_impact']
        except Exception as e:
            logger.warning(f"LLM评估随机事件失败，使用预设值: {e}")
            # 如果LLM评估失败，使用预设值但限制在±3范围内
            country_impact = max(-3, min(3, event.country_impact))
            shoreline_impact = max(-3, min(3, event.shoreline_impact))
            return country_impact, shoreline_impact
    
    def get_event_statistics(self) -> Dict[str, float]:
        """
        获取事件统计信息
        
        Returns:
            事件统计字典
        """
        total_events = len(self.events)
        disaster_events = sum(1 for e in self.events if e.country_impact < 0 or e.shoreline_impact < 0)
        positive_events = sum(1 for e in self.events if e.country_impact > 0 and e.shoreline_impact > 0)
        neutral_events = total_events - disaster_events - positive_events
        
        max_probability = max(e.probability for e in self.events)
        avg_probability = sum(e.probability for e in self.events) / total_events
        
        return {
            "total_events": total_events,
            "disaster_events": disaster_events,
            "positive_events": positive_events,
            "neutral_events": neutral_events,
            "max_probability": max_probability,
            "avg_probability": avg_probability,
            "use_llm_evaluation": self.use_llm_evaluation
        }

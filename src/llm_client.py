"""
LLM客户端模块
支持多种LLM API调用
"""

import openai
import os
import time
import logging
from typing import Dict, Any, Optional

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    """LLM客户端类，支持OpenAI API和其他兼容接口"""
    
    def __init__(self, api_key: str = None, base_url: str = None, model: str = "gpt-3.5-turbo"):
        """
        初始化LLM客户端
        
        Args:
            api_key: API密钥
            base_url: API基础URL (可选，用于自定义端点)
            model: 模型名称
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.model = model
        
        # 配置OpenAI客户端
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        logger.info(f"LLM客户端初始化完成，模型: {self.model}")
    
    def call_llm(self, prompt: str, system_prompt: str = None, max_retries: int = 5) -> str:
        """
        调用LLM生成回复
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            max_retries: 最大重试次数（默认5次，包含空回复重试）
            
        Returns:
            LLM生成的回复
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=10000  # 增加token限制，防止回复被截断
                )
                result = response.choices[0].message.content.strip() if response.choices and response.choices[0].message and response.choices[0].message.content else ""
                if result:
                    logger.info(f"LLM调用成功，尝试次数: {attempt + 1}")
                    return result
                else:
                    logger.warning(f"LLM回复为空 (尝试 {attempt + 1}/{max_retries})，1秒后自动重试...")
                    if attempt < max_retries - 1:  # 不是最后一次尝试才等待
                        time.sleep(1)  # 空回复重试间隔较短
            except Exception as e:
                logger.warning(f"LLM调用失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = min(2 ** attempt, 10)  # 最多等待10秒
                    logger.info(f"等待{wait_time}秒后重试...")
                    time.sleep(wait_time)  # 指数退避，但限制最大等待时间
                else:
                    raise Exception(f"LLM调用失败，已重试{max_retries}次: {str(e)}")
        
        # 5次都无回复
        logger.error(f"LLM连续{max_retries}次回复均为空，游戏无法继续！")
        raise Exception(f"LLM连续{max_retries}次回复均为空，游戏无法继续！")
    
    def call_human_llm(self, country_score: int, shoreline_score: int, 
                       opportunities: str, challenges: str, ref_table: str) -> Dict[str, str]:
        """
        调用人类LLM（国家决策者）
        
        Args:
            country_score: 当前国家发展分数
            shoreline_score: 当前海岸线状态分数
            opportunities: 海岸线机遇
            challenges: 海岸线挑战
            ref_table: 参考评分表
            
        Returns:
            包含两个行动的字典
        """
        with open("prompt/HumanLLM.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()

        if (opportunities is None or opportunities.strip() == "") and (challenges is None or challenges.strip() == ""):
            logger.warning("机遇和挑战信息为空，使用默认值")
            opportunities = "Coastline offers rich fisheries resources and tourism potential"
            challenges = "Coastal erosion and marine pollution threaten ecological balance"
        
        prompt = prompt_template.format(
            country_score=country_score,
            shoreline_score=shoreline_score,
            shoreline_opportunities=opportunities,
            shoreline_challenges=challenges,
            ref_scoring_table=ref_table
        )

        # print(f"=== 完整HumanLLM提示词 ===\n{prompt}\n{'='*80}\n")
        
        response = self.call_llm(prompt)

        # print(f"=== LLM原始回复 ===\n{response}\n{'='*80}\n")
        
        # 清理回复内容 - 移除think标签和其他不需要的内容
        cleaned_response = response
        
        # 移除<think>标签及其内容
        import re
        cleaned_response = re.sub(r'<think>.*?</think>', '', cleaned_response, flags=re.DOTALL)
        
        # 移除```代码块外的内容，只保留代码块内的ACTION
        code_block_match = re.search(r'```(.*?)```', cleaned_response, re.DOTALL)
        if code_block_match:
            cleaned_response = code_block_match.group(1).strip()
        
        print(f"=== 清理后的回复 ===\n{cleaned_response}\n{'='*80}\n")
        
        # 解析回复 - 改进版，过滤代码块标记
        actions = {}
        lines = cleaned_response.split('\n')
        current_action = None
        
        for line in lines:
            line = line.strip()
            
            # 跳过代码块标记和空行
            if line in ['```', ''] or not line:
                continue
                
            if line.startswith('ACTION_1:'):
                current_action = 'action_1'
                actions[current_action] = line.replace('ACTION_1:', '').strip()
            elif line.startswith('ACTION_2:'):
                current_action = 'action_2'
                actions[current_action] = line.replace('ACTION_2:', '').strip()
            elif current_action and line and not line.startswith('```'):
                # 只在不是代码块标记的情况下才添加内容
                if current_action in actions:
                    actions[current_action] += ' ' + line
                else:
                    actions[current_action] = line
        
        # 确保两个行动都存在
        if 'action_1' not in actions:
            actions['action_1'] = ''
        if 'action_2' not in actions:
            actions['action_2'] = ''
        
        logger.info(f"人类LLM生成行动: {actions}")
        return actions
    
    def call_shore_llm(self, country_actions: str) -> Dict[str, str]:
        """
        调用海岸线LLM（生态系统响应）
        
        Args:
            country_actions: 国家采取的行动
            
        Returns:
            包含机遇和挑战的字典
        """
        with open("prompt/ShoreLLM.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
        
        prompt = prompt_template.format(country_actions=country_actions)
        
        response = self.call_llm(prompt)
        
        # 解析回复 - 支持多种格式
        result = {}
        lines = response.split('\n')
        
        current_section = None
        for line in lines:
            line = line.strip()
            
            # 检测机遇部分
            if line.startswith('CHANCES:') or line.startswith('机遇:') or line.startswith('Opportunities:'):
                current_section = 'opportunities'
                # 如果同一行有内容，提取它
                for prefix in ['CHANCES:', '机遇:', 'Opportunities:']:
                    if line.startswith(prefix):
                        content = line.replace(prefix, '').strip()
                        if content:
                            result['opportunities'] = content
                        break
            
            # 检测挑战部分  
            elif line.startswith('CHALLENGES:') or line.startswith('挑战:') or line.startswith('Challenges:'):
                current_section = 'challenges'
                # 如果同一行有内容，提取它
                for prefix in ['CHALLENGES:', '挑战:', 'Challenges:']:
                    if line.startswith(prefix):
                        content = line.replace(prefix, '').strip()
                        if content:
                            result['challenges'] = content
                        break
            
            # 处理内容行
            elif current_section and line and not line.startswith('```') and line != '```':
                # 处理以 - 开头的项目列表
                if line.startswith('-'):
                    content = line.replace('-', '').strip()
                    if content and current_section not in result:
                        result[current_section] = content
                # 处理普通文本行
                elif not line.startswith('```') and current_section not in result:
                    result[current_section] = line
        
        # 确保返回的字典包含这两个键
        if 'opportunities' not in result:
            result['opportunities'] = ''
        if 'challenges' not in result:
            result['challenges'] = ''
        
        logger.info(f"海岸线LLM生成响应: {result}")
        return result
    
    def call_judge_llm(self, country_actions: str, ref_table: str) -> Dict[str, int]:
        """
        调用裁判LLM（评分系统）
        
        Args:
            country_actions: 国家采取的行动
            ref_table: 参考评分表
            
        Returns:
            包含分数变化的字典
        """
        with open("prompt/JudgeLLM.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
        
        prompt = prompt_template.format(
            country_actions=country_actions,
            ref_scoring_table=ref_table
        )
        
        response = self.call_llm(prompt)
        
        # 解析回复 - 支持多种格式
        scores = {}
        lines = response.split('\n')
        
        current_action = None
        for line in lines:
            line = line.strip()
            
            # 标准格式解析
            try:
                if line.startswith('first_country_rank:'):
                    scores['first_country'] = int(line.split(':')[1].strip())
                elif line.startswith('first_shoreline_rank:'):
                    scores['first_shoreline'] = int(line.split(':')[1].strip())
                elif line.startswith('second_country_rank:'):
                    scores['second_country'] = int(line.split(':')[1].strip())
                elif line.startswith('second_shoreline_rank:'):
                    scores['second_shoreline'] = int(line.split(':')[1].strip())
                
                # 备用格式解析 - 处理LLM可能的其他输出格式
                elif line.startswith('ACTION_1:'):
                    current_action = 'first'
                elif line.startswith('ACTION_2:'):
                    current_action = 'second'
                elif current_action and 'Country Score Change:' in line:
                    # 提取数值，处理 +4, -1 等格式
                    value_str = line.split('Country Score Change:')[1].strip()
                    value_str = value_str.replace('+', '').replace(' ', '')
                    scores[f'{current_action}_country'] = int(value_str)
                elif current_action and 'Shoreline Score Change:' in line:
                    # 提取数值，处理 +2, -4 等格式
                    value_str = line.split('Shoreline Score Change:')[1].strip()
                    value_str = value_str.replace('+', '').replace(' ', '')
                    scores[f'{current_action}_shoreline'] = int(value_str)
                    
            except (ValueError, IndexError) as e:
                # 解析失败时记录日志但继续处理
                logger.warning(f"解析裁判LLM响应时出错: {line} -> {e}")
                continue
        
        # 确保所有必需的键都存在，如果缺失则设为0
        required_keys = ['first_country', 'first_shoreline', 'second_country', 'second_shoreline']
        for key in required_keys:
            if key not in scores:
                scores[key] = 0
                logger.warning(f"裁判LLM响应中缺少 {key}，设为0")
        
        logger.info(f"裁判LLM评分结果: {scores}")
        return scores
    
    def call_judge_llm_for_random_event(self, event_name: str, event_description: str, 
                                       current_country_score: int, current_shoreline_score: int) -> Dict[str, int]:
        """
        调用裁判LLM评估随机事件的影响
        
        Args:
            event_name: 随机事件名称
            event_description: 随机事件描述
            current_country_score: 当前国家分数
            current_shoreline_score: 当前海岸线分数
            
        Returns:
            包含分数变化的字典
        """
        prompt = f"""You are the judge of a Shoreline Ecology Game.

A random event has occurred that will affect both the Country Development Score and Shoreline Status Score.

Current Status:
- Country Development Score: {current_country_score}
- Shoreline Status Score: {current_shoreline_score}

Random Event:
- Event Name: {event_name}
- Description: {event_description}

Please evaluate the impact of this random event and provide score changes for both the country and shoreline.
The score changes should be integers between -3 and +3 (inclusive).

Consider the following:
- Negative events (disasters, pollution) typically decrease both scores
- Positive events (recovery, technological breakthroughs) typically increase both scores
- Some events might have different impacts on country vs shoreline

Please respond in the following format:

```
country_impact: [integer between -3 and +3]
shoreline_impact: [integer between -3 and +3]
reasoning: [brief explanation of your scoring]
```"""
        
        response = self.call_llm(prompt)
        
        # 解析回复
        scores = {"country_impact": 0, "shoreline_impact": 0, "reasoning": ""}
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('country_impact:'):
                try:
                    impact = int(line.split(':')[1].strip())
                    # 限制在-3到+3范围内
                    scores['country_impact'] = max(-3, min(3, impact))
                except (ValueError, IndexError):
                    scores['country_impact'] = 0
            elif line.startswith('shoreline_impact:'):
                try:
                    impact = int(line.split(':')[1].strip())
                    # 限制在-3到+3范围内
                    scores['shoreline_impact'] = max(-3, min(3, impact))
                except (ValueError, IndexError):
                    scores['shoreline_impact'] = 0
            elif line.startswith('reasoning:'):
                scores['reasoning'] = line.replace('reasoning:', '').strip()
        
        logger.info(f"随机事件LLM评分结果: {event_name} -> 国家{scores['country_impact']:+d}, 海岸线{scores['shoreline_impact']:+d}")
        return scores

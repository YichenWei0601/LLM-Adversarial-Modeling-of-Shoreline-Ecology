# 海岸线生态对抗建模系统

这是一个基于大语言模型(LLM)的对抗性海岸线生态建模系统，模拟国家发展决策与海岸线生态系统之间的复杂交互。

## 系统概述

本系统通过三个LLM角色的对抗性交互，模拟真实世界中经济发展与环境保护之间的复杂关系：

- **人类LLM (HumanLLM)**: 代表国家决策者，制定发展策略
- **海岸线LLM (ShoreLLM)**: 代表海岸线生态系统的响应和变化
- **裁判LLM (JudgeLLM)**: 评估行动的影响，提供量化评分

## 游戏规则

- **初始状态**: 国家发展分数60分，海岸线状态分数100分
- **胜利条件**: 国家发展分数达到100分
- **失败条件**: 海岸线状态分数低于75分
- **时间限制**: 最多25年
- **随机事件**: 自然灾害、政策变化等随机事件影响游戏进程

## 安装和使用

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API

复制 `.env.example` 为 `.env` 并填入您的API配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

### 3. 运行游戏

```bash
python run_game.py
```

## 文件结构

```
├── README.md                 # 项目说明
├── requirements.txt          # Python依赖
├── .env.example             # 环境变量模板
├── run_game.py              # 游戏启动脚本
├── prompt/                  # LLM提示词
│   ├── HumanLLM.txt        # 人类决策者提示词
│   ├── ShoreLLM.txt        # 海岸线系统提示词
│   ├── JudgeLLM.txt        # 裁判评分提示词
│   └── ref_scoring_table.txt # 参考评分表
└── src/                     # 源代码
    ├── __init__.py
    ├── game_controller.py   # 主游戏控制器
    ├── llm_client.py        # LLM客户端
    ├── random_events.py     # 随机事件系统
    └── game_state.py        # 游戏状态管理
```

## 系统特性

### 1. 对抗性建模
- 三个LLM角色形成复杂的博弈关系
- 每个决策都会触发生态系统的响应
- 动态平衡经济发展与环境保护

### 2. 随机事件系统
- 自然灾害：海啸、台风、海平面上升等
- 积极事件：技术突破、国际援助等
- 事件概率根据海岸线状态动态调整

### 3. 量化评估
- 基于参考评分表的标准化评估
- 实时分数跟踪和记录
- 详细的年度记录和统计分析

### 4. 数据记录
- 每年的详细决策记录
- 分数变化追踪
- 随机事件影响分析
- JSON格式的结构化输出

## 输出文件

运行游戏后会生成以下文件：

- `game_statistics.json`: 多次游戏的统计结果
- `game_001.json` - `game_XXX.json`: 各次游戏的详细记录
- `game.log`: 游戏运行日志

## 使用示例

### 单次游戏
```python
from src import ShorlineEcologyGame

game = ShorlineEcologyGame(api_key="your_api_key")
summary = game.run_single_game()
print(summary)
```

### 多次游戏统计
```python
statistics = game.run_multiple_games(num_games=10)
game.print_statistics(statistics)
```

## 系统架构

### LLM角色分工

1. **HumanLLM**: 
   - 输入：当前分数、机遇、挑战
   - 输出：两个具体行动方案
   - 目标：平衡发展与保护

2. **ShoreLLM**:
   - 输入：人类的行动
   - 输出：新的机遇和挑战
   - 功能：模拟生态系统响应

3. **JudgeLLM**:
   - 输入：人类行动、参考评分表
   - 输出：量化分数变化
   - 功能：客观评估行动影响

### 游戏流程

1. 人类LLM基于当前状态制定策略
2. 裁判LLM评估策略的分数影响
3. 随机事件系统触发环境变化
4. 更新游戏状态和分数
5. 海岸线LLM生成新的生态响应
6. 记录年度数据，进入下一年

## 扩展功能

系统设计具有良好的扩展性，可以轻松添加：

- 新的随机事件类型
- 更复杂的评分机制
- 多区域海岸线建模
- 国际合作机制
- 实时可视化界面

## 技术特点

- **模块化设计**: 各组件独立，易于维护和扩展
- **异常处理**: 完善的错误处理和重试机制
- **日志记录**: 详细的运行日志便于调试
- **数据持久化**: 结构化数据存储，支持后续分析
- **多API支持**: 兼容多种LLM API接口

## 研究应用

本系统可用于：

- 环境政策影响研究
- 可持续发展策略评估
- 人工智能决策建模
- 复杂系统建模研究
- 教育和培训工具

## 贡献

欢迎提出改进建议和功能扩展！

## 许可证

MIT License
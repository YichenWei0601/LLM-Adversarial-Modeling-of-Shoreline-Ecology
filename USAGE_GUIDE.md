# 🌊 海岸线生态对抗建模系统 - 使用指南

## 🚀 快速开始

### 1. 系统要求
- Python 3.7+ 
- OpenAI API密钥或兼容的LLM API

### 2. 安装步骤

#### Windows用户:
```bash
# 双击运行安装脚本
install.bat

# 或手动安装
pip install -r requirements.txt
python setup_config.py
```

#### Linux/Mac用户:
```bash
# 运行安装脚本
chmod +x install.sh
./install.sh

# 或手动安装
pip3 install -r requirements.txt
python3 setup_config.py
```

### 3. 配置方式（三种选择）

#### 🎯 方式一：一键配置（推荐）
运行配置向导，一次性完成所有设置：
```bash
python setup_config.py
```
配置向导将：
- 设置API密钥和连接信息
- 配置游戏参数和偏好
- 创建完整的`game_config.json`配置文件
- 测试API连接

#### 🔧 方式二：手动配置文件
创建`game_config.json`文件：
```json
{
  "api_key": "your-openai-api-key",
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-3.5-turbo",
  "pause_between_years": true,
  "pause_duration": 5.0,
  "annual_bonus": 1,
  "use_llm_for_random_events": true,
  "default_mode": "2",
  "num_games": 10,
  "fast_mode": true
}
```

#### 🌍 方式三：环境变量
编辑`.env`文件（备选方案）：
```bash
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

### 4. 运行游戏

#### 🎮 标准运行（使用配置文件）
```bash
# Windows
python run_game.py

# Linux/Mac  
python3 run_game.py
```
**如果您已经配置了`game_config.json`，系统将：**
- ✅ 自动加载API和游戏设置
- ✅ 跳过重复的配置询问
- ✅ 根据您的偏好直接启动

#### 🎯 快速演示
```bash
# 运行预配置的演示
python test_demo.py

# 测试配置功能
python test_config_demo.py
```

### 5. 配置优先级
系统按以下优先级读取配置：
1. **🥇 game_config.json** - 完整配置文件（最高优先级）
2. **🥈 .env文件** - 环境变量
3. **🥉 用户输入** - 运行时询问（最后备选）

### 6. 游戏观察模式
系统支持两种观察模式：
- **详细观察模式**: 每年暂停5秒，可以仔细观察年度变化
- **快速模式**: 连续运行，适合多次游戏统计

运行时可以选择：
- 是否启用年度暂停
- 自定义暂停时长
- 多次游戏时自动启用快速模式

## 📋 详细说明

### 系统架构
```
人类LLM (决策者) ←→ 裁判LLM (评分) ←→ 海岸线LLM (生态响应)
                    ↓
                随机事件系统
                    ↓
                游戏状态管理
```

### 游戏规则
- **起始**: 国家60分，海岸线100分
- **目标**: 国家达到100分获胜
- **失败**: 海岸线低于75分
- **限制**: 最多25年
- **年度增长**: 每年国家和海岸线分数都自动+1分（可配置）

### 输出文件
- `game_statistics.json` - 多次游戏统计
- `game_001.json` - 单次游戏详细记录
- `game.log` - 运行日志

## 🔧 高级配置

### API配置选项
```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

### 支持的模型
- OpenAI: gpt-3.5-turbo, gpt-4, gpt-4-turbo
- 其他兼容OpenAI API的模型

### 游戏参数配置
编辑`game_config.json`文件自定义参数：
```json
{
  "initial_country_score": 60,
  "initial_shoreline_score": 100,
  "max_years": 25,
  "victory_threshold": 100,
  "failure_threshold": 75,
  "annual_bonus": 1
}
```

## 📊 使用示例

### 编程接口
```python
from src import ShorlineEcologyGame

# 创建游戏实例 - 启用年度暂停观察和年度奖励
game = ShorlineEcologyGame(
    api_key="your_api_key",
    model="gpt-3.5-turbo",
    pause_between_years=True,  # 启用年度暂停
    pause_duration=5.0,        # 暂停5秒
    annual_bonus=1             # 每年自动增长1分
)

# 运行单次游戏（带暂停观察）
summary = game.run_single_game()
print(f"结果: {'胜利' if summary['victory'] else '失败'}")

# 运行多次游戏统计（快速模式）
statistics = game.run_multiple_games(num_games=10, fast_mode=True)
print(f"胜利率: {statistics['victory_rate']:.2%}")
```

### 年度奖励配置
```python
# 标准模式 - 每年+1分
game = ShorlineEcologyGame(
    api_key="your_api_key",
    annual_bonus=1  # 国家和海岸线每年都+1分
)

# 快速发展模式 - 每年+2分
game = ShorlineEcologyGame(
    api_key="your_api_key", 
    annual_bonus=2  # 加速发展
)

# 无奖励模式 - 纯策略博弈
game = ShorlineEcologyGame(
    api_key="your_api_key",
    annual_bonus=0  # 不自动增长
)
```

### 观察模式配置
```python
# 详细观察模式 - 适合观察单次游戏
game = ShorlineEcologyGame(
    api_key="your_api_key",
    pause_between_years=True,   # 启用暂停
    pause_duration=3.0          # 每年暂停3秒
)

# 快速模式 - 适合批量统计
game = ShorlineEcologyGame(
    api_key="your_api_key", 
    pause_between_years=False   # 关闭暂停
)
```

### 批量分析
```python
# 分析不同策略的成功率
results = []
for i in range(100):
    summary = game.run_single_game()
    results.append(summary)

# 统计分析
success_rate = sum(1 for r in results if r['victory']) / len(results)
avg_duration = sum(r['total_years'] for r in results) / len(results)
```

## 🛠️ 故障排除

### 常见问题

1. **API调用失败**
   - 检查API密钥是否正确
   - 确认网络连接正常
   - 验证API端点URL

2. **模块导入错误**
   ```bash
   pip install -r requirements.txt
   ```

3. **编码问题**
   - 确保所有文件使用UTF-8编码
   - Windows用户可能需要设置环境变量

4. **权限问题**
   ```bash
   # Linux/Mac
   chmod +x *.sh
   ```

### 调试模式
设置环境变量启用详细日志：
```bash
export LOG_LEVEL=DEBUG
python run_game.py
```

## 🎯 测试验证

### 运行测试套件
```bash
python test_demo.py
```

### 验证组件
```bash
# 测试API连接
python setup_config.py

# 检查文件完整性
python -c "from src import *; print('All modules loaded successfully')"
```

## 📈 结果分析

### 数据结构
每次游戏生成的JSON文件包含：
- 游戏总结信息
- 年度详细记录
- 分数变化轨迹
- 随机事件记录
- LLM决策日志

### 可视化分析
可以使用以下工具分析结果：
```python
import json
import matplotlib.pyplot as plt

# 读取游戏数据
with open('game_001.json', 'r') as f:
    data = json.load(f)

# 绘制分数变化曲线
years = [r['year'] for r in data['yearly_records']]
country_scores = [r['country_score'] for r in data['yearly_records']]
shoreline_scores = [r['shoreline_score'] for r in data['yearly_records']]

plt.plot(years, country_scores, label='国家发展')
plt.plot(years, shoreline_scores, label='海岸线状态')
plt.legend()
plt.show()
```

## 🔄 更新和维护

### 检查更新
定期拉取最新代码：
```bash
git pull origin main
pip install -r requirements.txt
```

### 备份数据
重要的游戏记录建议备份：
```bash
mkdir backup
cp *.json backup/
```

## 🤝 贡献指南

### 扩展功能
系统支持以下扩展：
- 新增随机事件类型
- 自定义评分规则
- 多区域建模
- 实时可视化界面

### 提交代码
1. Fork项目
2. 创建功能分支
3. 提交代码
4. 发起Pull Request

## 📞 支持

遇到问题可以：
1. 查看日志文件`game.log`
2. 运行测试脚本诊断
3. 检查API配置
4. 提交Issue报告

---

**祝您使用愉快！🎉**

"""
简单的游戏运行脚本
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.game_controller import ShorlineEcologyGame
from src.game_state import GameState

def validate_input(value, value_type, min_val=None, max_val=None, default=None):
    """验证并转换用户输入"""
    try:
        if value_type == int:
            result = int(value)
        elif value_type == float:
            result = float(value)
        else:
            result = value
        
        if min_val is not None and result < min_val:
            print(f"⚠️ 值太小，最小值为 {min_val}，使用默认值 {default}")
            return default
        if max_val is not None and result > max_val:
            print(f"⚠️ 值太大，最大值为 {max_val}，使用默认值 {default}")
            return default
        
        return result
    except ValueError:
        print(f"⚠️ 输入格式错误，使用默认值 {default}")
        return default

def create_config():
    """创建新的配置文件"""
    print("🔧 创建游戏配置文件...")
    config = {}
    
    # API配置
    print("\n📡 API配置:")
    api_key = input("请输入OpenAI API Key: ").strip()
    if not api_key:
        print("⚠️ API Key不能为空")
        return None
    config["api_key"] = api_key
    config["base_url"] = input("请输入API Base URL (默认: https://api.openai.com/v1): ").strip() or "https://api.openai.com/v1"
    config["model"] = input("请输入模型名称 (默认: gpt-3.5-turbo): ").strip() or "gpt-3.5-turbo"
    
    # 游戏基础设置
    print("\n🎮 游戏基础设置:")
    country_score = input("初始国家发展分数 (默认60): ") or "60"
    config["initial_country_score"] = validate_input(country_score, int, 0, 100, 60)
    
    shoreline_score = input("初始海岸线状态分数 (默认100): ") or "100"
    config["initial_shoreline_score"] = validate_input(shoreline_score, int, 0, 100, 100)
    
    max_years = input("最大游戏年数 (默认25): ") or "25"
    config["max_years"] = validate_input(max_years, int, 1, 100, 25)
    
    victory_threshold = input("胜利阈值-国家分数 (默认100): ") or "100"
    config["victory_threshold"] = validate_input(victory_threshold, int, 1, 100, 100)
    
    failure_threshold = input("失败阈值-海岸线分数 (默认75): ") or "75"
    config["failure_threshold"] = validate_input(failure_threshold, int, 0, 100, 75)
    
    # 游戏体验设置
    print("\n⏱️ 游戏体验设置:")
    config["pause_between_years"] = input("是否在每年之间暂停? (y/n, 默认y): ").lower() != "n"
    if config["pause_between_years"]:
        pause_duration = input("每年暂停时长(秒, 默认5): ") or "5"
        config["pause_duration"] = validate_input(pause_duration, float, 0, 60, 5.0)
    else:
        config["pause_duration"] = 0
    
    annual_bonus = input("每年自动增长分数 (默认1): ") or "1"
    config["annual_bonus"] = validate_input(annual_bonus, int, 0, 10, 1)
    
    config["use_llm_for_random_events"] = input("使用LLM评估随机事件? (y/n, 默认y): ").lower() != "n"
    
    # 运行模式设置
    print("\n🎯 运行模式设置:")
    mode = input("默认运行模式 (1: 单次游戏, 2: 多次游戏, 默认2): ") or "2"
    config["default_mode"] = "1" if mode == "1" else "2"
    
    if config["default_mode"] == "2":
        num_games = input("默认游戏次数 (默认10): ") or "10"
        config["num_games"] = validate_input(num_games, int, 1, 1000, 10)
        config["fast_mode"] = input("多次游戏使用快速模式? (y/n, 默认y): ").lower() != "n"
    
    # 随机事件设置
    print("\n🎲 随机事件设置:")
    config["enable_random_events"] = input("启用随机事件? (y/n, 默认y): ").lower() != "n"
    if config["enable_random_events"]:
        disaster_prob = input("灾害概率修正因子 (默认1.0): ") or "1.0"
        config["disaster_probability_modifier"] = validate_input(disaster_prob, float, 0, 5.0, 1.0)
    
    # 保存配置
    try:
        with open("game_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print("\n✅ 配置文件已保存到 game_config.json")
        print("💡 下次运行将自动使用这些配置，无需重复输入")
        return config
    except Exception as e:
        print(f"\n❌ 保存配置文件失败: {e}")
        return None

def validate_config(config):
    """验证配置文件的完整性和正确性"""
    if not config:
        return False
    
    required_keys = ["api_key"]
    missing_keys = [key for key in required_keys if key not in config or not config[key]]
    
    if missing_keys:
        print(f"⚠️ 配置文件缺少必要项: {', '.join(missing_keys)}")
        return False
    
    # 验证数值范围
    validations = [
        ("initial_country_score", int, 0, 100),
        ("initial_shoreline_score", int, 0, 100),
        ("max_years", int, 1, 100),
        ("victory_threshold", int, 1, 100),
        ("failure_threshold", int, 0, 100),
        ("pause_duration", float, 0, 60),
        ("annual_bonus", int, 0, 10),
    ]
    
    for key, value_type, min_val, max_val in validations:
        if key in config:
            try:
                value = value_type(config[key])
                if not (min_val <= value <= max_val):
                    print(f"⚠️ 配置项 {key} 值 {value} 超出范围 [{min_val}, {max_val}]")
                    return False
            except (ValueError, TypeError):
                print(f"⚠️ 配置项 {key} 类型错误")
                return False
    
    return True

def load_config():
    """加载配置文件"""
    config = {}
    
    # 优先从game_config.json读取
    if os.path.exists("game_config.json"):
        try:
            with open("game_config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            print("✅ 已加载游戏配置文件 (game_config.json)")
            return config
        except Exception as e:
            print(f"⚠️  读取游戏配置文件失败: {e}")
    
    # 备选: 从.env文件读取API配置
    try:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                config.update({
                    "api_key": api_key,
                    "base_url": os.getenv("OPENAI_BASE_URL"),
                    "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
                })
                print("✅ 已从.env文件读取API配置")
        except ImportError:
            # python-dotenv 包未安装，跳过 .env 文件加载
            pass
    except Exception:
        # 其他错误，继续执行
        pass
    
    return config

def get_api_config(config):
    """获取API配置，优先使用配置文件"""
    api_key = config.get("api_key") or os.getenv("OPENAI_API_KEY")
    base_url = config.get("base_url") or os.getenv("OPENAI_BASE_URL")
    model = config.get("model") or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # 如果配置文件中没有API信息，才询问用户
    if not api_key:
        print("🔑 需要API配置信息:")
        api_key = input("请输入OpenAI API Key: ")
        if not api_key:
            raise ValueError("API Key不能为空")
    
    if not base_url:
        base_url_input = input("请输入API Base URL (可选，直接回车跳过): ")
        if base_url_input:
            base_url = base_url_input
    
    if not model or model == "gpt-3.5-turbo":
        model_input = input(f"请输入模型名称 (默认{model}): ")
        if model_input:
            model = model_input
    
    return api_key, base_url, model

def get_game_settings(config):
    """获取游戏设置，优先使用配置文件"""
    # 暂停设置
    if "pause_between_years" in config:
        pause_between_years = config["pause_between_years"]
        pause_duration = config.get("pause_duration", 5.0)
        print(f"✅ 使用配置: {'启用' if pause_between_years else '关闭'}年度暂停")
        if pause_between_years:
            print(f"   暂停时长: {pause_duration}秒")
    else:
        pause_input = input("是否在每年之间暂停观察游戏进程? (y/n, 默认y): ").lower()
        pause_between_years = pause_input != "n"
        
        pause_duration = 5.0
        if pause_between_years:
            duration_input = input("请输入每年暂停时长(秒, 默认5): ")
            if duration_input:
                try:
                    pause_duration = float(duration_input)
                except ValueError:
                    print("输入格式错误，使用默认5秒")
                    pause_duration = 5.0
            print(f"已设置每年暂停{pause_duration}秒")
        else:
            print("已关闭年度暂停，游戏将连续运行")
    
    # 年度奖励设置
    if "annual_bonus" in config:
        annual_bonus = config["annual_bonus"]
        print(f"✅ 使用配置: 每年自动增长 +{annual_bonus}分")
    else:
        annual_bonus = 1
        bonus_input = input("请输入每年自动增长分数 (默认1): ")
        if bonus_input:
            try:
                annual_bonus = int(bonus_input)
            except ValueError:
                print("输入格式错误，使用默认1分")
                annual_bonus = 1
        print(f"已设置每年自动增长: 国家+{annual_bonus}分, 海岸线+{annual_bonus}分")
    
    # 随机事件评估设置
    if "use_llm_for_random_events" in config:
        use_llm_for_random_events = config["use_llm_for_random_events"]
        print(f"✅ 使用配置: {'启用' if use_llm_for_random_events else '关闭'}LLM评估随机事件")
    else:
        llm_events_input = input("是否使用LLM评估随机事件影响? (y/n, 默认y): ").lower()
        use_llm_for_random_events = llm_events_input != "n"
        
        if use_llm_for_random_events:
            print("✅ 已启用LLM评估随机事件，事件影响将由AI实时判断（±3分范围内）")
        else:
            print("⚡ 已关闭LLM评估随机事件，使用预设影响值")
    
    return pause_between_years, pause_duration, annual_bonus, use_llm_for_random_events

def get_game_parameters(config):
    """获取游戏初始化参数"""
    return {
        'initial_country_score': config.get('initial_country_score', 60),
        'initial_shoreline_score': config.get('initial_shoreline_score', 100),
        'max_years': config.get('max_years', 25),
        'victory_threshold': config.get('victory_threshold', 100),
        'failure_threshold': config.get('failure_threshold', 75),
        'enable_random_events': config.get('enable_random_events', True),
        'disaster_probability_modifier': config.get('disaster_probability_modifier', 1.0)
    }

def show_config(config):
    """显示当前配置"""
    print("\n📋 当前配置:")
    print("-" * 40)
    
    # API配置
    print("📡 API设置:")
    print(f"   API Key: {'已设置' if config.get('api_key') else '未设置'}")
    print(f"   Base URL: {config.get('base_url', '未设置')}")
    print(f"   模型: {config.get('model', '未设置')}")
    
    # 游戏设置
    print("\n🎮 游戏设置:")
    print(f"   初始国家分数: {config.get('initial_country_score', '默认(60)')}")
    print(f"   初始海岸线分数: {config.get('initial_shoreline_score', '默认(100)')}")
    print(f"   最大年数: {config.get('max_years', '默认(25)')}")
    print(f"   胜利阈值: {config.get('victory_threshold', '默认(100)')}")
    print(f"   失败阈值: {config.get('failure_threshold', '默认(75)')}")
    
    # 体验设置
    print("\n⏱️ 体验设置:")
    print(f"   年度暂停: {'启用' if config.get('pause_between_years', True) else '关闭'}")
    if config.get('pause_between_years', True):
        print(f"   暂停时长: {config.get('pause_duration', 5)}秒")
    print(f"   年度奖励: +{config.get('annual_bonus', 1)}分")
    print(f"   LLM评估随机事件: {'启用' if config.get('use_llm_for_random_events', True) else '关闭'}")
    
    # 随机事件设置
    print("\n🎲 随机事件设置:")
    print(f"   启用随机事件: {'是' if config.get('enable_random_events', True) else '否'}")
    if config.get('enable_random_events', True):
        print(f"   灾害概率修正: {config.get('disaster_probability_modifier', 1.0)}")
    
    # 运行设置
    print("\n🎯 运行设置:")
    mode = config.get('default_mode', '2')
    print(f"   默认模式: {'单次游戏' if mode == '1' else '多次游戏统计'}")
    if mode == '2':
        print(f"   默认游戏次数: {config.get('num_games', 10)}")
        print(f"   快速模式: {'启用' if config.get('fast_mode', True) else '关闭'}")
    
    print("-" * 40)

def manage_config():
    """配置管理菜单"""
    while True:
        print("\n🔧 配置管理")
        print("1. 显示当前配置")
        print("2. 创建新配置")
        print("3. 编辑现有配置")
        print("4. 删除配置文件")
        print("5. 返回游戏")
        
        choice = input("请选择操作 (1-5): ").strip()
        
        if choice == "1":
            if os.path.exists("game_config.json"):
                config = load_config()
                show_config(config)
            else:
                print("❌ 配置文件不存在")
        
        elif choice == "2":
            create_config()
        
        elif choice == "3":
            if os.path.exists("game_config.json"):
                print("📝 编辑配置 (将重新创建配置文件)")
                # 先显示当前配置
                config = load_config()
                show_config(config)
                confirm = input("\n确认重新配置? (y/n): ").lower()
                if confirm == "y":
                    create_config()
            else:
                print("❌ 配置文件不存在，请先创建")
        
        elif choice == "4":
            if os.path.exists("game_config.json"):
                confirm = input("确认删除配置文件? (y/n): ").lower()
                if confirm == "y":
                    os.remove("game_config.json")
                    print("✅ 配置文件已删除")
            else:
                print("❌ 配置文件不存在")
        
        elif choice == "5":
            break
        
        else:
            print("❌ 无效选择，请重试")

def main():
    """主函数"""
    print("=== 海岸线生态对抗建模系统 ===")
    print("本系统模拟国家与海岸线生态系统的对抗性交互")
    print("目标: 将国家发展从60分提升到100分，同时保持海岸线状态在75分以上")
    print()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--config":
            manage_config()
            return
        elif sys.argv[1] == "--help":
            print("🎮 使用说明:")
            print("   python run_game.py        - 正常运行游戏")
            print("   python run_game.py --config  - 配置管理")
            print("   python run_game.py --help    - 显示帮助")
            return
    
    # 检查是否需要创建配置文件
    if not os.path.exists("game_config.json"):
        print("🔍 未找到配置文件 (game_config.json)")
        print("选项:")
        print("  1. 创建新配置文件")
        print("  2. 进入配置管理")
        print("  3. 使用默认设置继续")
        
        choice = input("请选择 (1-3, 默认3): ").strip() or "3"
        
        if choice == "1":
            config = create_config()
            if config is None:
                print("❌ 配置创建失败，继续使用默认设置")
                config = {}
        elif choice == "2":
            manage_config()
            return
        else:
            print("⚠️  将使用默认设置，部分功能可能需要手动输入")
            config = {}
    else:
        # 加载现有配置并提供管理选项
        config = load_config()
        if config:
            print("💡 提示: 使用 'python run_game.py --config' 可以管理配置")
    
    # 验证配置
    config_valid = validate_config(config)
    if not config_valid:
        print("⚠️  配置文件存在问题，建议重新配置")
        fix_choice = input("是否现在修复配置? (y/n): ").lower()
        if fix_choice == "y":
            manage_config()
            return
    
    # 获取API配置
    try:
        api_key, base_url, model = get_api_config(config)
        print(f"使用模型: {model}")
        print()
    except Exception as e:
        print(f"❌ API配置错误: {e}")
        print("💡 建议:")
        print("   1. 运行 'python run_game.py --config' 进行配置")
        print("   2. 重新运行本程序并选择创建配置文件")
        return
    
    # 获取游戏设置
    pause_between_years, pause_duration, annual_bonus, use_llm_for_random_events = get_game_settings(config)
    
    # 获取游戏初始化参数
    game_params = get_game_parameters(config)
    
    try:
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
        
        # 设置游戏状态参数
        game.game_state = GameState(
            initial_country_score=game_params['initial_country_score'],
            initial_shoreline_score=game_params['initial_shoreline_score'],
            max_years=game_params['max_years'],
            victory_threshold=game_params['victory_threshold'],
            failure_threshold=game_params['failure_threshold']
        )
        
        # 设置游戏控制器的其他参数
        game.enable_random_events = game_params['enable_random_events']
        
        # 设置随机事件系统参数
        if hasattr(game.random_event_system, 'disaster_probability_modifier'):
            game.random_event_system.disaster_probability_modifier = game_params['disaster_probability_modifier']
        
        # 选择运行模式
        if "default_mode" in config:
            mode = str(config["default_mode"])
            print(f"✅ 使用配置的默认模式: {'单次游戏' if mode == '1' else '多次游戏统计'}")
        else:
            mode = input("选择运行模式 (1: 单次游戏, 2: 多次游戏统计, 默认2): ") or "2"
        
        if mode == "1":
            # 单次游戏
            print("开始单次游戏...")
            summary = game.run_single_game()
            
            print(f"\n=== 游戏结果 ===")
            print(f"游戏时长: {summary['total_years']}年")
            print(f"最终国家分数: {summary['final_scores']['country']}")
            print(f"最终海岸线分数: {summary['final_scores']['shoreline']}")
            print(f"结果: {'胜利' if summary['victory'] else '失败'}")
            print(f"结束原因: {summary['game_over_reason']}")
            
            # 导出详细记录
            filename = game.game_state.export_to_json()
            print(f"详细记录已保存到: {filename}")
            
        else:
            # 多次游戏统计
            if "num_games" in config:
                num_games = config["num_games"]
                print(f"✅ 使用配置的游戏次数: {num_games}")
            else:
                num_games_input = input("请输入要运行的游戏次数 (默认10): ") or "10"
                num_games = validate_input(num_games_input, int, 1, 1000, 10)
            
            # 快速模式选项
            if "fast_mode" in config:
                fast_mode = config["fast_mode"]
                print(f"✅ 使用配置: {'启用' if fast_mode else '关闭'}快速模式")
            else:
                if pause_between_years:
                    fast_mode_input = input(f"多次游戏建议使用快速模式(无暂停)，是否启用? (y/n, 默认y): ").lower()
                    fast_mode = fast_mode_input != "n"
                else:
                    fast_mode = True
            
            print(f"开始运行{num_games}次游戏...")
            
            statistics = game.run_multiple_games(num_games, fast_mode=fast_mode)
            game.print_statistics(statistics)
            
            print(f"\n统计结果已保存到: game_statistics.json")
            print(f"各次游戏详细记录已保存到: game_001.json - game_{num_games:03d}.json")
    
    except KeyboardInterrupt:
        print("\n用户中断游戏")
    except Exception as e:
        print(f"游戏运行出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
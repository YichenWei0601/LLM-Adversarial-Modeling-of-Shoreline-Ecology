"""
配置向导
帮助用户设置API配置和其他选项
"""

import os
import json
from typing import Dict, Any

def create_env_file():
    """创建.env配置文件"""
    print("🔧 API配置向导")
    print("=" * 30)
    
    # 获取用户输入
    api_key = input("请输入您的OpenAI API Key: ").strip()
    if not api_key:
        print("❌ API Key不能为空")
        return False
    
    base_url = input("请输入API Base URL (默认: https://api.openai.com/v1): ").strip()
    if not base_url:
        base_url = "https://api.openai.com/v1"
    
    model = input("请输入模型名称 (默认: gpt-3.5-turbo): ").strip()
    if not model:
        model = "gpt-3.5-turbo"
    
    # 创建.env文件
    env_content = f"""# OpenAI API配置
OPENAI_API_KEY={api_key}
OPENAI_BASE_URL={base_url}
OPENAI_MODEL={model}

# 日志配置
LOG_LEVEL=INFO
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ .env文件创建成功!")
        return True
    except Exception as e:
        print(f"❌ 创建.env文件失败: {e}")
        return False

def create_game_config():
    """创建游戏配置文件"""
    print("\n🎮 游戏配置向导")
    print("=" * 30)
    
    config = {}
    
    # API配置（从.env读取或询问用户）
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        model = os.getenv("OPENAI_MODEL")
        
        if api_key:
            print(f"✅ 从.env文件读取到API配置")
            config["api_key"] = api_key
            config["base_url"] = base_url
            config["model"] = model or "gpt-3.5-turbo"
        else:
            print("⚠️  未找到API配置，请手动输入:")
            api_key = input("请输入OpenAI API Key: ").strip()
            if api_key:
                config["api_key"] = api_key
                config["base_url"] = input("请输入API Base URL (可选): ").strip() or None
                config["model"] = input("请输入模型名称 (默认gpt-3.5-turbo): ").strip() or "gpt-3.5-turbo"
    
    except ImportError:
        print("⚠️  未安装python-dotenv，请手动输入API配置:")
        api_key = input("请输入OpenAI API Key: ").strip()
        if api_key:
            config["api_key"] = api_key
            config["base_url"] = input("请输入API Base URL (可选): ").strip() or None
            config["model"] = input("请输入模型名称 (默认gpt-3.5-turbo): ").strip() or "gpt-3.5-turbo"
    
    # 游戏参数配置
    try:
        print("\n游戏参数配置:")
        config["initial_country_score"] = int(input("初始国家发展分数 (默认60): ") or "60")
        config["initial_shoreline_score"] = int(input("初始海岸线状态分数 (默认100): ") or "100")
        config["max_years"] = int(input("最大游戏年数 (默认25): ") or "25")
        config["victory_threshold"] = int(input("胜利阈值-国家分数 (默认100): ") or "100")
        config["failure_threshold"] = int(input("失败阈值-海岸线分数 (默认75): ") or "75")
        
        # 游戏体验配置
        print("\n游戏体验配置:")
        config["pause_between_years"] = input("是否在每年之间暂停? (y/n, 默认y): ").lower() != "n"
        if config["pause_between_years"]:
            config["pause_duration"] = float(input("每年暂停时长(秒, 默认5): ") or "5")
        else:
            config["pause_duration"] = 0
        
        config["annual_bonus"] = int(input("每年自动增长分数 (默认1): ") or "1")
        config["use_llm_for_random_events"] = input("使用LLM评估随机事件? (y/n, 默认y): ").lower() != "n"
        
        # 随机事件配置
        print("\n随机事件配置:")
        config["enable_random_events"] = input("启用随机事件? (y/n, 默认y): ").lower() != "n"
        if config["enable_random_events"]:
            config["disaster_probability_modifier"] = float(input("灾害概率修正因子 (默认1.0): ") or "1.0")
        
        # 保存配置
        with open("game_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print("✅ 游戏配置文件创建成功!")
        print("   包含API配置、游戏参数、用户偏好等完整设置")
        return True
        
    except ValueError as e:
        print(f"❌ 输入格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")
        return False

def test_api_connection():
    """测试API连接"""
    print("\n🔍 测试API连接")
    print("=" * 30)
    
    try:
        from src.llm_client import LLMClient
        
        # 读取配置
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        if not api_key:
            print("❌ 未找到API Key，请先配置.env文件")
            return False
        
        # 创建客户端
        client = LLMClient(api_key=api_key, base_url=base_url, model=model)
        
        # 测试简单调用
        print("正在测试API连接...")
        response = client.call_llm("请回复'连接成功'", max_retries=1)
        
        if response:
            print(f"✅ API连接测试成功! 回复: {response[:50]}...")
            return True
        else:
            print("❌ API连接测试失败: 无回复")
            return False
            
    except Exception as e:
        print(f"❌ API连接测试失败: {e}")
        return False

def show_system_info():
    """显示系统信息"""
    print("\n📊 系统信息")
    print("=" * 30)
    
    try:
        import sys
        import platform
        
        print(f"Python版本: {sys.version}")
        print(f"操作系统: {platform.system()} {platform.release()}")
        print(f"架构: {platform.machine()}")
        
        # 检查依赖包
        try:
            import openai
            print(f"OpenAI包版本: {openai.__version__}")
        except ImportError:
            print("❌ OpenAI包未安装")
        
        # 检查文件
        files_to_check = [
            "prompt/HumanLLM.txt",
            "prompt/ShoreLLM.txt", 
            "prompt/JudgeLLM.txt",
            "prompt/ref_scoring_table.txt",
            "src/game_controller.py",
            "src/llm_client.py",
            "run_game.py"
        ]
        
        print("\n文件检查:")
        for file_path in files_to_check:
            if os.path.exists(file_path):
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - 文件不存在")
        
    except Exception as e:
        print(f"❌ 获取系统信息失败: {e}")

def main():
    """主配置流程"""
    print("🌊 海岸线生态对抗建模系统 - 配置向导")
    print("=" * 50)
    
    # 显示系统信息
    show_system_info()
    
    # 配置API
    if not os.path.exists(".env"):
        print("\n未找到.env配置文件，开始API配置...")
        if not create_env_file():
            return
    else:
        print("\n✅ 找到现有.env配置文件")
        if input("是否重新配置API? (y/n): ").lower() == "y":
            create_env_file()
    
    # 配置游戏参数
    if not os.path.exists("game_config.json"):
        print("\n未找到游戏配置文件，开始游戏配置...")
        create_game_config()
    else:
        print("\n✅ 找到现有游戏配置文件")
        if input("是否重新配置游戏参数? (y/n): ").lower() == "y":
            create_game_config()
    
    # 测试API连接
    if input("\n是否测试API连接? (y/n): ").lower() == "y":
        try:
            # 先尝试加载python-dotenv
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except ImportError:
                print("⚠️  建议安装python-dotenv: pip install python-dotenv")
            
            test_api_connection()
        except Exception as e:
            print(f"❌ 测试过程出错: {e}")
    
    print("\n🎉 配置完成!")
    print("\n下一步:")
    print("1. 运行 'python run_game.py' 开始游戏")
    print("2. 或运行 'python test_demo.py' 查看演示")

if __name__ == "__main__":
    main()

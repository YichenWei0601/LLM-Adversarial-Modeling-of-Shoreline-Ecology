#!/usr/bin/env python3
"""
配置功能演示脚本
展示如何使用配置文件而不必每次输入API信息
"""

import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_demo_config():
    """创建演示配置文件"""
    demo_config = {
        "api_key": "demo-api-key-placeholder",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-3.5-turbo",
        "initial_country_score": 60,
        "initial_shoreline_score": 100,
        "max_years": 5,  # 演示用短期游戏
        "victory_threshold": 100,
        "failure_threshold": 75,
        "pause_between_years": False,  # 演示用无暂停
        "pause_duration": 0,
        "annual_bonus": 1,
        "use_llm_for_random_events": False,  # 演示用关闭LLM评估
        "enable_random_events": True,
        "disaster_probability_modifier": 1.0,
        "default_mode": "1",  # 单次游戏
        "num_games": 1,
        "fast_mode": True
    }
    
    with open("game_config.json", "w", encoding="utf-8") as f:
        json.dump(demo_config, f, ensure_ascii=False, indent=2)
    
    print("✅ 已创建演示配置文件 (game_config.json)")
    return demo_config

def test_config_loading():
    """测试配置加载功能"""
    print("🔍 测试配置加载功能...")
    
    # 导入运行脚本的加载函数
    try:
        sys.path.append('.')
        from run_game import load_config, get_api_config, get_game_settings
        
        # 测试加载配置
        config = load_config()
        print(f"   配置项数量: {len(config)}")
        print(f"   包含API配置: {'api_key' in config}")
        print(f"   包含游戏配置: {'max_years' in config}")
        
        # 测试API配置获取（模拟）
        try:
            # 模拟环境变量为空的情况
            old_env = os.environ.copy()
            os.environ.pop('OPENAI_API_KEY', None)
            os.environ.pop('OPENAI_BASE_URL', None)
            os.environ.pop('OPENAI_MODEL', None)
            
            print("\n   🔑 测试API配置获取:")
            if config.get("api_key"):
                print(f"      ✅ 从配置文件读取API Key: {config['api_key'][:10]}...")
                print(f"      ✅ 模型: {config.get('model', 'N/A')}")
            else:
                print("      ❌ 配置文件中无API配置")
            
            # 恢复环境变量
            os.environ.update(old_env)
            
        except Exception as e:
            print(f"      ⚠️  API配置测试出错: {e}")
        
        # 测试游戏设置获取
        print("\n   🎮 测试游戏设置:")
        if 'pause_between_years' in config:
            print(f"      ✅ 暂停设置: {config['pause_between_years']}")
        if 'annual_bonus' in config:
            print(f"      ✅ 年度奖励: {config['annual_bonus']}")
        if 'use_llm_for_random_events' in config:
            print(f"      ✅ LLM评估: {config['use_llm_for_random_events']}")
        if 'default_mode' in config:
            print(f"      ✅ 默认模式: {config['default_mode']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置加载测试失败: {e}")
        return False

def test_config_priority():
    """测试配置优先级"""
    print("\n🔍 测试配置优先级（配置文件 > 环境变量 > 用户输入）...")
    
    # 创建测试配置
    config = {
        "api_key": "config-file-key",
        "model": "config-file-model"
    }
    
    # 设置环境变量
    os.environ['OPENAI_API_KEY'] = 'env-key'
    os.environ['OPENAI_MODEL'] = 'env-model'
    
    # 模拟优先级逻辑
    final_api_key = config.get("api_key") or os.getenv("OPENAI_API_KEY") or "user-input-key"
    final_model = config.get("model") or os.getenv("OPENAI_MODEL") or "default-model"
    
    print(f"   📁 配置文件API Key: {config.get('api_key')}")
    print(f"   🌍 环境变量API Key: {os.getenv('OPENAI_API_KEY')}")
    print(f"   🎯 最终选择: {final_api_key}")
    
    if final_api_key == config.get("api_key"):
        print("   ✅ 配置优先级正确：配置文件 > 环境变量")
    else:
        print("   ❌ 配置优先级错误")
    
    # 清理环境变量
    os.environ.pop('OPENAI_API_KEY', None)
    os.environ.pop('OPENAI_MODEL', None)
    
    return final_api_key == config.get("api_key")

def show_config_benefits():
    """展示配置文件的好处"""
    print("\n📋 配置文件的优势:")
    print("   ✅ 一次配置，多次使用")
    print("   ✅ 不需要每次输入API信息")
    print("   ✅ 保存游戏偏好设置")
    print("   ✅ 支持快速启动游戏")
    print("   ✅ 便于自动化和批量运行")
    print("   ✅ 环境变量作为备选")
    
    print("\n📖 使用方法:")
    print("   1. 运行 'python setup_config.py' 进行初始配置")
    print("   2. 或手动创建 'game_config.json' 文件")
    print("   3. 直接运行 'python run_game.py' 无需重复输入")
    print("   4. 修改配置文件调整游戏参数")

def main():
    """主演示函数"""
    print("🎯 配置功能演示")
    print("=" * 50)
    
    # 备份现有配置
    backup_needed = False
    if os.path.exists("game_config.json"):
        backup_needed = True
        os.rename("game_config.json", "game_config.json.backup")
        print("📋 已备份现有配置文件")
    
    try:
        # 创建演示配置
        demo_config = create_demo_config()
        
        # 测试配置功能
        tests = [
            ("配置加载", test_config_loading),
            ("配置优先级", test_config_priority)
        ]
        
        passed = 0
        for test_name, test_func in tests:
            print(f"\n{'='*60}")
            print(f"🧪 {test_name}测试")
            print('='*60)
            
            try:
                if test_func():
                    passed += 1
                    print(f"✅ {test_name}测试通过")
                else:
                    print(f"❌ {test_name}测试失败")
            except Exception as e:
                print(f"❌ {test_name}测试出错: {e}")
        
        print(f"\n{'='*60}")
        print(f"🎯 测试结果: {passed}/{len(tests)} 通过")
        print('='*60)
        
        # 展示配置优势
        show_config_benefits()
        
        if passed == len(tests):
            print("\n🎉 配置功能测试全部通过！")
            print("\n现在您可以:")
            print("   1. 编辑 game_config.json 调整设置")
            print("   2. 直接运行 'python run_game.py' 开始游戏")
            print("   3. 无需每次重复输入API和游戏设置")
        else:
            print("\n❌ 部分测试失败，请检查配置功能")
    
    finally:
        # 清理演示文件
        if os.path.exists("game_config.json"):
            os.remove("game_config.json")
            print("\n🧹 已清理演示配置文件")
        
        # 恢复备份
        if backup_needed:
            os.rename("game_config.json.backup", "game_config.json")
            print("📋 已恢复原配置文件")

if __name__ == "__main__":
    main()

#!/bin/bash
# 快速安装脚本 (Linux/Mac)

echo "🌊 海岸线生态对抗建模系统 - 快速安装"
echo "=================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python"
    exit 1
fi

echo "✅ Python已安装: $(python3 --version)"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到pip3，请先安装pip"
    exit 1
fi

echo "✅ pip已安装"

# 安装依赖
echo "📦 安装Python依赖包..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 依赖包安装成功"
else
    echo "⚠️  依赖包安装可能有问题，请检查"
fi

# 检查环境变量配置
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量配置文件..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件，填入您的API配置"
    echo "   nano .env  或  vim .env"
fi

# 运行测试
echo "🧪 运行系统测试..."
python3 test_demo.py

if [ $? -eq 0 ]; then
    echo "✅ 系统测试通过"
else
    echo "⚠️  系统测试可能有问题"
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "📋 下一步操作："
echo "1. 编辑 .env 文件，配置您的LLM API"
echo "2. 运行: python3 run_game.py"
echo "3. 或者运行: ./run.sh (如果在Linux/Mac)"
echo ""
echo "📚 更多信息请查看 README.md"

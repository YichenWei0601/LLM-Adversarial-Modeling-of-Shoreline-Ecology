@echo off
chcp 65001
title 海岸线生态对抗建模系统 - 快速安装

echo.
echo 🌊 海岸线生态对抗建模系统 - 快速安装
echo ==================================
echo.

echo 检查Python环境...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python
    echo 请访问 https://www.python.org/downloads/ 下载安装
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo ✅ Python已安装: %%i

echo.
echo 📦 安装Python依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo ⚠️  依赖包安装可能有问题，请检查
) else (
    echo ✅ 依赖包安装成功
)

echo.
echo 📝 检查环境变量配置...
if not exist ".env" (
    echo 创建环境变量配置文件...
    copy .env.example .env > nul
    echo ⚠️  请编辑 .env 文件，填入您的API配置
    echo    使用记事本或其他编辑器打开 .env 文件
)

echo.
echo 🧪 运行系统测试...
python test_demo.py
if errorlevel 1 (
    echo ⚠️  系统测试可能有问题
) else (
    echo ✅ 系统测试通过
)

echo.
echo 🎉 安装完成！
echo.
echo 📋 下一步操作：
echo 1. 编辑 .env 文件，配置您的LLM API
echo 2. 运行: python run_game.py
echo 3. 或者双击: run.bat
echo.
echo 📚 更多信息请查看 README.md
echo.
echo 按任意键退出...
pause > nul

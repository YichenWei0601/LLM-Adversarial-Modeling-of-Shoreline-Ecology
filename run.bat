@echo off
chcp 65001
title 海岸线生态对抗建模系统

echo.
echo ====================================
echo 海岸线生态对抗建模系统
echo ====================================
echo.

echo 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo.
echo 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告: 依赖包安装可能有问题
)

echo.
echo 运行系统测试...
python test_demo.py
if errorlevel 1 (
    echo 警告: 测试可能有问题
)

echo.
echo 启动游戏...
python run_game.py

echo.
echo 游戏结束，按任意键退出...
pause > nul

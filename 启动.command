#!/bin/bash
# 双击启动 MoodTracker Web 界面
# Mac 用户：双击此文件即可

cd "$(dirname "$0")"

echo "正在启动 MoodTracker..."
python3 server.py &
SERVER_PID=$!

# 等待服务器启动
sleep 2

# 自动打开浏览器
open "http://127.0.0.1:7777"

echo ""
echo "浏览器已打开，如果没有自动跳转请手动访问："
echo "http://127.0.0.1:7777"
echo ""
echo "用完后回到这个窗口按 Ctrl+C 停止服务"
echo ""

# 等待用户退出
wait $SERVER_PID

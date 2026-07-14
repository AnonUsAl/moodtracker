# MoodTracker

个人情绪追踪工具。支持命令行、Web 可视化界面和 Android 手机 App 三种方式记录每天的心情和状态。

## 为什么

持续记录情绪波动有助于识别规律，对自己和医生都有参考价值。这个工具把数据存在本地 JSON 文件里，不依赖任何第三方服务，隐私完全自己掌控。

## 安装

不需要安装任何依赖（手机端除外），只需要 Python 3。

```bash
git clone https://github.com/AnonUsAl/moodtracker.git
cd moodtracker
```

## 使用

### Mac / Windows

双击 `启动.command`（Mac）自动打开浏览器，或手动运行：

```bash
python server.py
```

浏览器访问 http://127.0.0.1:7777 ，即可使用可视化界面：

- 点击表情按钮选择心情分数（1-5）
- 输入可选备注
- 查看情绪趋势折线图、统计概览、历史记录列表

### Android 手机

在电脑上打包 APK，然后安装到手机：

```bash
cd mobile
buildozer android debug
```

打包完成后，APK 文件在 `mobile/bin/` 目录下。传到手机安装即可。

> **首次打包**需要安装 Java JDK 17+ 和 Android SDK，buildozer 会自动下载。整个过程约 20-30 分钟，后续打包会快很多。

详细步骤见下方 [打包 APK](#打包-apk) 章节。

### 命令行

```bash
python moodtracker.py log       # 记录心情
python moodtracker.py history   # 查看最近 7 条记录
python moodtracker.py stats     # 查看统计
```

## 打包 APK

### 环境准备

1. 安装 Java JDK 17 或更高版本

   ```bash
   # Mac
   brew install openjdk@17
   ```

2. 安装 Python 依赖

   ```bash
   pip install buildozer kivy
   ```

3. 安装系统依赖（仅 Linux/macOS 需要）

   ```bash
   # Mac
   brew install autoconf automake libtool pkg-config
   ```

### 打包步骤

```bash
cd moodtracker/mobile
buildozer android debug
```

首次运行会自动下载 Android SDK 和 NDK（约 3GB），请耐心等待。完成后 APK 在：

```
mobile/bin/moodtracker-1.0-debug.apk
```

### 安装到手机

1. 把 APK 传到手机（微信/数据线/U盘都行）
2. 手机设置里允许「安装未知来源应用」
3. 点击安装

## 数据

所有记录存储在 `data/records.json`（桌面端）或 App 数据目录（手机端），格式如下：

```json
[
  {
    "date": "2026-07-14",
    "time": "17:57",
    "mood": 4,
    "note": "今天开始了一个新项目，感觉不错"
  }
]
```

桌面端 Web 界面和命令行共享同一份数据。手机端数据独立存储在手机本地。所有数据不上传任何地方。

## 情绪分数参考

| 分数 | 含义 |
|------|------|
| 1 | 很低 |
| 2 | 低 |
| 3 | 一般 |
| 4 | 好 |
| 5 | 很好 |

## 项目结构

```
moodtracker/
├── moodtracker.py          # CLI 主入口
├── server.py               # Web 服务器
├── storage.py              # 数据读写（CLI 和 Web 共用）
├── 启动.command            # Mac 双击启动脚本
├── static/
│   └── index.html          # Web 可视化界面
├── mobile/
│   ├── app.py              # Kivy 手机端界面
│   ├── storage.py          # 手机端数据存储
│   └── buildozer.spec      # APK 打包配置
└── data/
    └── records.json        # 数据文件
```

## License

MIT

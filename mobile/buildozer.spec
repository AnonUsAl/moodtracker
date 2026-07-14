[app]

# 应用信息
title = MoodTracker
package.name = moodtracker
package.domain = org.moodtracker

# 源码配置
source.dir = .
source.include_exts = py

# 版本
version = 1.0

# 依赖
requirements = python3,kivy

# 权限
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# 构建配置
fullscreen = 0
orientation = portrait

# Android 配置
android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a

# 日志
log_level = 2

[buildozer]

# 构建目录
build_dir = .buildozer

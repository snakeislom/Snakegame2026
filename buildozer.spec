[app]
title = Snake Pro 2026
package.name = snakepro
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,wav,kv,atlas
version = 0.1

# Pydroid 3 da ishlatilgan kutubxonalar:
requirements = python3,pygame,kivy

orientation = landscape
fullscreen = 1
android.api = 31
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

# Pygame o'yinlari uchun p4a sozlamasi (source_dir-siz!)
p4a.branch = master
entrypoint = main.py

[buildozer]
log_level = 2
warn_on_root = 1
android.accept_sdk_license = True

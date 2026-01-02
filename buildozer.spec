[app]
title = Snake Pro 2026
package.name = snakepro
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,wav,kv,atlas
version = 0.1

# MUHIM: Agar o'yiningiz Pygame bo'lsa, shunday qoldiring. 
# Agar Kivy bo'lsa, pygame o'rniga kivy deb yozing.
requirements = python3,pygame

orientation = landscape
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a

# Pygame uchun maxsus sozlamalar
p4a.branch = master
p4a.source_dir = 
entrypoint = new.py

[buildozer]
log_level = 2
warn_on_root = 1

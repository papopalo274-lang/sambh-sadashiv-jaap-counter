[app]
title = Naam Jaap Counter
package.name = naamjaap
package.domain = org.naamjaap
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,ttf
version = 2.0
requirements = python3==3.11.6,kivy==2.3.0,android
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,VIBRATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = "@android:style/Theme.NoTitleBar"
orientation = portrait
fullscreen = 0
android.presplash_color = #0A0514
android.enable_androidx = True
android.archs = arm64-v8a, armeabi-v7a
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 0
build_dir = ./.buildozer
bin_dir = ./bin

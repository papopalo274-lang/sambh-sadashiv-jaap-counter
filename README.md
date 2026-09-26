# 🕉️ Naam Jaap Counter — v2 World-Class Edition

Beautiful Hindu mantra counter app built with Python & Kivy.

## ✨ Features
- 🌸 **8 Mantras** — Sambh Sadashiv, Om Namah Shivay, Hare Krishna, Jai Shri Ram, and more
- 🎨 **5 Themes** — Shiv Ratri, Sunrise Saffron, Ocean Blue, Forest Green, Rose Gold
- 🌀 **Animated Mandala** — spinning sacred geometry tap button
- 📿 **108-Bead Mala Ring** — visual mala progress tracker
- 🌺 **Particle Shower** — flower petals burst on every tap
- 📊 **Stats Panel** — lifetime count per mantra
- 💾 **SQLite storage** — data persists forever

## 📱 Build APK via GitHub Actions (Easiest)

1. Create a GitHub repository
2. Upload all files
3. Go to **Actions** tab → build runs automatically
4. Download APK from **Actions → Artifacts** after ~20 min

## 💻 Build Locally (Ubuntu / WSL2)

```bash
sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool cmake libffi-dev libssl-dev
pip install buildozer==1.5.0 cython==0.29.33
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
buildozer android debug
# APK → bin/naamjaap-2.0-debug.apk
```

## 🕉️ ॐ नमः शिवाय — साम्ब सदाशिव

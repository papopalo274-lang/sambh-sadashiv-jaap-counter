"""
Sambh Sadashiv Jaap Counter — World-Class Edition
Full-featured spiritual mantra counter with:
- Beautiful mandala tap button
- Multiple mantras (Sambh Sadashiv, Om Namah Shivay, etc.)
- Theme/wallpaper switcher (5 sacred themes)
- Mala progress ring (108 bead tracker)
- Particle shower animations
- Lifetime + daily stats
- Reset with confirmation
"""

import os
import sqlite3
import random
import math
from datetime import datetime

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
from kivy.graphics import (Color, Ellipse, Line, Rectangle, RoundedRectangle,
                            PushMatrix, PopMatrix, Rotate, Scale, Translate)
from kivy.graphics.instructions import InstructionGroup
from kivy.utils import platform
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.properties import (NumericProperty, StringProperty,
                              ListProperty, BooleanProperty)

# ─── Android Sound ────────────────────────────────────────────────────────────
if platform == 'android':
    try:
        from jnius import autoclass
        ToneGenerator = autoclass('android.media.ToneGenerator')
        AudioManager  = autoclass('android.media.AudioManager')
        tone_gen = ToneGenerator(AudioManager.STREAM_MUSIC, 85)
    except Exception:
        tone_gen = None
else:
    tone_gen = None

# ─── Themes ───────────────────────────────────────────────────────────────────
THEMES = {
    "Shiv Ratri": {
        "bg":        (0.04, 0.02, 0.10, 1),
        "bg2":       (0.10, 0.04, 0.18, 1),
        "gold":      (0.78, 0.58, 0.16, 1),
        "accent":    (0.55, 0.18, 0.75, 1),
        "flame":     (1.00, 0.42, 0.21, 1),
        "text":      (0.95, 0.90, 0.80, 1),
        "counter":   (0.00, 0.95, 0.80, 1),
        "mandala":   [(0.78,0.58,0.16,1),(0.55,0.18,0.75,1),(1.00,0.42,0.21,1)],
        "glow":      (0.55, 0.18, 0.75, 0.25),
    },
    "Sunrise Saffron": {
        "bg":        (0.10, 0.04, 0.00, 1),
        "bg2":       (0.20, 0.08, 0.00, 1),
        "gold":      (1.00, 0.75, 0.10, 1),
        "accent":    (0.95, 0.35, 0.00, 1),
        "flame":     (1.00, 0.60, 0.00, 1),
        "text":      (1.00, 0.95, 0.85, 1),
        "counter":   (1.00, 0.85, 0.20, 1),
        "mandala":   [(1.00,0.75,0.10,1),(0.95,0.35,0.00,1),(1.00,0.55,0.00,1)],
        "glow":      (1.00, 0.50, 0.00, 0.20),
    },
    "Ocean Blue": {
        "bg":        (0.00, 0.04, 0.14, 1),
        "bg2":       (0.00, 0.10, 0.25, 1),
        "gold":      (0.20, 0.80, 1.00, 1),
        "accent":    (0.00, 0.55, 0.85, 1),
        "flame":     (0.10, 0.90, 0.85, 1),
        "text":      (0.85, 0.95, 1.00, 1),
        "counter":   (0.10, 0.95, 0.90, 1),
        "mandala":   [(0.20,0.80,1.00,1),(0.00,0.55,0.85,1),(0.10,0.90,0.85,1)],
        "glow":      (0.00, 0.55, 0.85, 0.20),
    },
    "Forest Green": {
        "bg":        (0.02, 0.08, 0.02, 1),
        "bg2":       (0.04, 0.14, 0.04, 1),
        "gold":      (0.55, 0.90, 0.20, 1),
        "accent":    (0.20, 0.70, 0.20, 1),
        "flame":     (0.80, 1.00, 0.10, 1),
        "text":      (0.88, 0.98, 0.85, 1),
        "counter":   (0.55, 1.00, 0.45, 1),
        "mandala":   [(0.55,0.90,0.20,1),(0.20,0.70,0.20,1),(0.80,1.00,0.10,1)],
        "glow":      (0.20, 0.70, 0.20, 0.20),
    },
    "Rose Gold": {
        "bg":        (0.12, 0.04, 0.06, 1),
        "bg2":       (0.20, 0.06, 0.10, 1),
        "gold":      (0.95, 0.70, 0.55, 1),
        "accent":    (0.85, 0.35, 0.50, 1),
        "flame":     (1.00, 0.60, 0.40, 1),
        "text":      (1.00, 0.92, 0.90, 1),
        "counter":   (1.00, 0.80, 0.70, 1),
        "mandala":   [(0.95,0.70,0.55,1),(0.85,0.35,0.50,1),(1.00,0.60,0.40,1)],
        "glow":      (0.85, 0.35, 0.50, 0.20),
    },
}
THEME_NAMES = list(THEMES.keys())

# ─── Mantras ──────────────────────────────────────────────────────────────────
MANTRAS = [
    {"name": "साम्ब सदाशिव",   "sanskrit": "🕉 साम्ब सदाशिव 🕉",   "flash": "🌸 साम्ब सदाशिव 🌸"},
    {"name": "ॐ नमः शिवाय",    "sanskrit": "🕉 ॐ नमः शिवाय 🕉",    "flash": "🌿 ॐ नमः शिवाय 🌿"},
    {"name": "हरे कृष्ण",       "sanskrit": "🌺 हरे कृष्ण हरे राम 🌺","flash": "🌺 हरे कृष्ण 🌺"},
    {"name": "जय श्री राम",    "sanskrit": "🙏 जय श्री राम 🙏",    "flash": "🙏 जय श्री राम 🙏"},
    {"name": "ॐ नमो नारायण",   "sanskrit": "✨ ॐ नमो नारायण ✨",   "flash": "✨ नारायण ✨"},
    {"name": "ॐ गं गणपतये",    "sanskrit": "🐘 ॐ गं गणपतये नमः 🐘","flash": "🐘 गणपति बप्पा 🐘"},
    {"name": "जय माता दी",     "sanskrit": "🌸 जय माता दी 🌸",     "flash": "🌸 माता रानी 🌸"},
    {"name": "ॐ",               "sanskrit": "🕉 ॐ 🕉",               "flash": "🕉 ॐ 🕉"},
]

# ─── Database ─────────────────────────────────────────────────────────────────
def get_db_path():
    if platform == 'android':
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), "jaap_v2.db")
    return "jaap_v2.db"

DB = get_db_path()

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records (
        date TEXT, mantra TEXT, count INTEGER, last_updated TEXT,
        PRIMARY KEY(date, mantra))''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY, value TEXT)''')
    conn.commit(); conn.close()

def get_count(mantra_name):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT count FROM records WHERE date=? AND mantra=?", (today, mantra_name))
    row = c.fetchone(); conn.close()
    return row[0] if row else 0

def save_count(mantra_name, count):
    today = datetime.now().strftime("%Y-%m-%d")
    now_t = datetime.now().strftime("%H:%M:%S")
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute('''INSERT INTO records VALUES(?,?,?,?)
        ON CONFLICT(date,mantra) DO UPDATE SET count=?,last_updated=?''',
        (today, mantra_name, count, now_t, count, now_t))
    conn.commit(); conn.close()

def get_lifetime(mantra_name):
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT SUM(count) FROM records WHERE mantra=?", (mantra_name,))
    r = c.fetchone()[0]; conn.close()
    return r or 0

def get_setting(key, default=""):
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (key,))
    r = c.fetchone(); conn.close()
    return r[0] if r else default

def save_setting(key, value):
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("INSERT INTO settings VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=?",
              (key, value, value))
    conn.commit(); conn.close()

def reset_mantra(mantra_name):
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("DELETE FROM records WHERE mantra=?", (mantra_name,))
    conn.commit(); conn.close()

# ─── Particle Widget ──────────────────────────────────────────────────────────
class ParticleWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.particles = []

    def burst(self, theme):
        colors = theme["mandala"]
        for _ in range(40):
            cx = self.width / 2
            cy = self.height / 2
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 9)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.uniform(8, 20)
            life = random.uniform(0.6, 1.4)
            color = random.choice(colors)
            shape = random.choice(['ellipse', 'petal'])
            self.particles.append({
                'x': cx, 'y': cy, 'vx': vx, 'vy': vy,
                'size': size, 'life': life, 'max_life': life,
                'color': color, 'shape': shape
            })
        Clock.unschedule(self._step)
        Clock.schedule_interval(self._step, 1/45)

    def _step(self, dt):
        self.canvas.clear()
        alive = []
        with self.canvas:
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] -= 0.25  # gravity
                p['life'] -= dt
                if p['life'] > 0:
                    alpha = p['life'] / p['max_life']
                    r, g, b, _ = p['color']
                    Color(r, g, b, alpha)
                    s = p['size'] * alpha
                    if p['shape'] == 'petal':
                        Ellipse(pos=(p['x']-s/2, p['y']-s), size=(s, s*1.6))
                    else:
                        Ellipse(pos=(p['x']-s/2, p['y']-s/2), size=(s, s))
                    alive.append(p)
        self.particles = alive
        if not self.particles:
            Clock.unschedule(self._step)
            self.canvas.clear()

# ─── Mandala Button ───────────────────────────────────────────────────────────
class MandalaButton(Widget):
    angle    = NumericProperty(0)
    scale    = NumericProperty(1.0)
    glow_alpha = NumericProperty(0.0)

    def __init__(self, theme, **kw):
        super().__init__(**kw)
        self.theme = theme
        self._anim_event = None
        self.bind(pos=self._draw, size=self._draw, angle=self._draw,
                  scale=self._draw, glow_alpha=self._draw)
        Clock.schedule_interval(self._spin, 1/30)

    def set_theme(self, theme):
        self.theme = theme
        self._draw()

    def _spin(self, dt):
        self.angle = (self.angle + 0.4) % 360
        self._draw()

    def _draw(self, *_):
        self.canvas.clear()
        if self.width <= 0:
            return
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        r  = min(self.width, self.height) / 2 * 0.88 * self.scale
        t  = self.theme

        with self.canvas:
            # ── glow aura ──
            for i in range(5, 0, -1):
                a = self.glow_alpha * (i / 5) * 0.5
                gr, gg, gb, _ = t["glow"]
                Color(gr, gg, gb, a)
                gr_r = r + dp(i * 10)
                Ellipse(pos=(cx-gr_r, cy-gr_r), size=(gr_r*2, gr_r*2))

            # ── outer ring ──
            Color(*t["gold"][:3], 0.7)
            Line(circle=(cx, cy, r), width=dp(2))

            # ── petal mandala (2 layers, counter-rotating) ──
            petals   = 12
            colors   = t["mandala"]
            petal_r  = r * 0.30
            for layer in range(2):
                ang_off = self.angle if layer == 0 else -self.angle * 1.5
                for i in range(petals):
                    theta = math.radians(i * 360 / petals + ang_off)
                    dist  = r * 0.60
                    px = cx + math.cos(theta) * dist
                    py = cy + math.sin(theta) * dist
                    col = colors[i % len(colors)]
                    Color(*col[:3], 0.75 - layer * 0.2)
                    Ellipse(pos=(px - petal_r/2, py - petal_r*0.85),
                            size=(petal_r, petal_r * 1.7))

            # ── inner star ──
            Color(*t["gold"][:3], 0.9)
            pts = []
            for i in range(8):
                a1 = math.radians(i * 45 + self.angle * 0.5)
                a2 = math.radians(i * 45 + 22.5 + self.angle * 0.5)
                pts += [cx + math.cos(a1)*r*0.38, cy + math.sin(a1)*r*0.38,
                        cx + math.cos(a2)*r*0.22, cy + math.sin(a2)*r*0.22]
            pts += [pts[0], pts[1]]
            Line(points=pts, width=dp(1.5))

            # ── center circle ──
            cr = r * 0.28
            Color(*t["accent"][:3], 0.92)
            Ellipse(pos=(cx-cr, cy-cr), size=(cr*2, cr*2))

            # ── OM symbol ──
            Color(*t["gold"])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.glow_alpha = 1.0
            Animation(scale=0.93, duration=0.08).start(self)
            return True

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            Animation(scale=1.0, duration=0.12).start(self)
            Animation(glow_alpha=0.0, duration=0.5).start(self)
            if self.parent:
                self.parent.dispatch('on_mandala_tap')
            return True

# ─── Main Screen ─────────────────────────────────────────────────────────────
class JaapScreen(Screen):
    def __init__(self, app_ref, **kw):
        super().__init__(**kw)
        self.app = app_ref
        self.register_event_type('on_mandala_tap')
        self._build_ui()

    def on_mandala_tap(self, *_):
        pass  # overridden below

    def _build_ui(self):
        self.root_layout = FloatLayout()

        # Background
        self.bg_widget = Widget(size_hint=(1,1))
        self._draw_bg()
        self.root_layout.add_widget(self.bg_widget)

        # Particles layer
        self.particles = ParticleWidget(size_hint=(1,1))
        self.root_layout.add_widget(self.particles)

        # Main vertical layout
        main = BoxLayout(orientation='vertical', padding=[dp(16), dp(10), dp(16), dp(8)],
                         spacing=dp(4), size_hint=(1,1))

        # ── Top bar ──
        top = BoxLayout(orientation='horizontal', size_hint=(1, 0.07), spacing=dp(8))

        self.clock_lbl = Label(text="", font_size=sp(12),
                               color=self.app.theme["gold"],
                               size_hint=(0.65, 1), halign='left', valign='middle')
        self.clock_lbl.bind(size=self.clock_lbl.setter('text_size'))

        btn_theme = self._icon_btn("🎨", self._show_theme_picker)
        btn_mantra = self._icon_btn("📿", self._show_mantra_picker)
        btn_info = self._icon_btn("📊", self._show_stats)

        top.add_widget(self.clock_lbl)
        top.add_widget(btn_theme)
        top.add_widget(btn_mantra)
        top.add_widget(btn_info)
        main.add_widget(top)

        # ── Mantra name ──
        self.mantra_name_lbl = Label(
            text=self.app.current_mantra["name"],
            font_size=sp(18), bold=True,
            color=self.app.theme["gold"],
            size_hint=(1, 0.06), halign='center', valign='middle')
        self.mantra_name_lbl.bind(size=self.mantra_name_lbl.setter('text_size'))
        main.add_widget(self.mantra_name_lbl)

        # ── Mala progress ring label ──
        self.mala_progress_lbl = Label(text="", font_size=sp(11),
            color=self.app.theme["text"],
            size_hint=(1, 0.04), halign='center', valign='middle')
        self.mala_progress_lbl.bind(size=self.mala_progress_lbl.setter('text_size'))
        main.add_widget(self.mala_progress_lbl)

        # ── Mala ring widget ──
        self.mala_ring = MalaRingWidget(size_hint=(1, 0.06))
        main.add_widget(self.mala_ring)

        # ── Mandala button ──
        mandala_wrap = FloatLayout(size_hint=(1, 0.38))
        self.mandala = MandalaButton(theme=self.app.theme, size_hint=(0.78, 0.78),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.mandala.bind(on_touch_up=self._mandala_touch)
        mandala_wrap.add_widget(self.mandala)

        # OM label in center of mandala
        self.om_lbl = Label(text="🕉", font_size=sp(52),
                            size_hint=(0.4, 0.4),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            halign='center', valign='middle')
        mandala_wrap.add_widget(self.om_lbl)
        main.add_widget(mandala_wrap)

        # ── Flash mantra label ──
        self.flash_lbl = Label(text="", font_size=sp(20), bold=True,
                               color=self.app.theme["accent"],
                               size_hint=(1, 0.06), halign='center', valign='middle')
        self.flash_lbl.bind(size=self.flash_lbl.setter('text_size'))
        main.add_widget(self.flash_lbl)

        # ── Count display ──
        self.count_lbl = Label(
            text=str(self.app.count),
            font_size=sp(64), bold=True,
            color=self.app.theme["counter"],
            size_hint=(1, 0.14), halign='center', valign='middle')
        self.count_lbl.bind(size=self.count_lbl.setter('text_size'))
        main.add_widget(self.count_lbl)

        # ── Stats row ──
        stats = BoxLayout(orientation='horizontal', size_hint=(1, 0.06), spacing=dp(8))
        self.mala_lbl = Label(
            text="", font_size=sp(13), color=self.app.theme["gold"],
            size_hint=(0.5, 1), halign='center', valign='middle')
        self.mala_lbl.bind(size=self.mala_lbl.setter('text_size'))
        self.total_lbl = Label(
            text="", font_size=sp(13), color=self.app.theme["gold"],
            size_hint=(0.5, 1), halign='center', valign='middle')
        self.total_lbl.bind(size=self.total_lbl.setter('text_size'))
        stats.add_widget(self.mala_lbl)
        stats.add_widget(self.total_lbl)
        main.add_widget(stats)

        # ── Bottom buttons ──
        btns = BoxLayout(orientation='horizontal', size_hint=(1, 0.09),
                         spacing=dp(10))
        self.tap_btn = Button(
            text="✨ जाप करें ✨",
            font_size=sp(16), bold=True,
            background_color=self.app.theme["accent"],
            background_normal='',
            size_hint=(0.65, 1))
        self.tap_btn.bind(on_press=self._on_tap)

        reset_btn = Button(
            text="🔄 रीसेट",
            font_size=sp(13),
            background_color=(0.7, 0.1, 0.1, 1),
            background_normal='',
            size_hint=(0.35, 1))
        reset_btn.bind(on_press=self._confirm_reset)
        btns.add_widget(self.tap_btn)
        btns.add_widget(reset_btn)
        main.add_widget(btns)

        self.root_layout.add_widget(main)
        self.add_widget(self.root_layout)

        self._refresh_ui()
        Clock.schedule_interval(self._tick, 1)

    def _icon_btn(self, text, cb):
        b = Button(text=text, font_size=sp(20),
                   background_color=(0,0,0,0),
                   background_normal='',
                   size_hint=(None, 1), width=dp(42))
        b.bind(on_press=cb)
        return b

    def _draw_bg(self):
        self.bg_widget.canvas.clear()
        with self.bg_widget.canvas:
            Color(*self.app.theme["bg"])
            Rectangle(pos=self.bg_widget.pos, size=Window.size)
            # gradient overlay circle
            Color(*self.app.theme["bg2"][:3], 0.6)
            Ellipse(pos=(-Window.width*0.2, Window.height*0.2),
                    size=(Window.width*1.4, Window.width*1.4))

    def _tick(self, dt):
        now = datetime.now()
        self.clock_lbl.text = now.strftime("⏰ %I:%M %p  📅 %d %b")

    def _refresh_ui(self):
        c = self.app.count
        mala = c // 108
        bead = c % 108
        life = get_lifetime(self.app.current_mantra["name"])
        self.count_lbl.text   = str(c)
        self.mala_lbl.text    = f"माला: {mala}"
        self.total_lbl.text   = f"कुल: {life:,}"
        self.mala_progress_lbl.text = f"● {bead}/108 मनके"
        self.mala_ring.update(bead, self.app.theme)
        self.mantra_name_lbl.text = self.app.current_mantra["name"]

    def _mandala_touch(self, widget, touch):
        if widget.collide_point(*touch.pos) and touch.phase == 'end':
            self._on_tap(None)

    def _on_tap(self, *_):
        self.app.count += 1
        save_count(self.app.current_mantra["name"], self.app.count)
        self._refresh_ui()

        # Flash mantra
        self.flash_lbl.text = self.app.current_mantra["flash"]
        Clock.unschedule(self._clear_flash)
        Clock.schedule_once(self._clear_flash, 0.8)

        # Particles
        self.particles.burst(self.app.theme)

        # Sound
        if platform == 'android' and tone_gen:
            try: tone_gen.startTone(ToneGenerator.TONE_PROP_BEEP, 80)
            except: pass

    def _clear_flash(self, *_):
        self.flash_lbl.text = ""

    def _confirm_reset(self, *_):
        content = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        lbl = Label(text=f"क्या आप '{self.app.current_mantra['name']}'\nका सारा जाप रीसेट करना चाहते हैं?",
                    halign='center', font_size=sp(15))
        btns = BoxLayout(spacing=dp(10), size_hint=(1, None), height=dp(44))
        yes = Button(text="✅ हाँ, रीसेट करें", background_color=(0.8,0.1,0.1,1), background_normal='')
        no  = Button(text="❌ नहीं", background_color=(0.1,0.5,0.1,1), background_normal='')
        btns.add_widget(yes); btns.add_widget(no)
        content.add_widget(lbl); content.add_widget(btns)
        pop = Popup(title="⚠️ रीसेट करें?", content=content,
                    size_hint=(0.85, 0.32), auto_dismiss=True)
        yes.bind(on_press=lambda *_: (reset_mantra(self.app.current_mantra["name"]),
                                      setattr(self.app, 'count', 0),
                                      self._refresh_ui(), pop.dismiss()))
        no.bind(on_press=pop.dismiss)
        pop.open()

    def _show_theme_picker(self, *_):
        content = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(10))
        lbl = Label(text="थीम चुनें  — Choose Theme",
                    font_size=sp(15), size_hint=(1, None), height=dp(36))
        content.add_widget(lbl)
        grid = GridLayout(cols=1, spacing=dp(8), size_hint=(1, None))
        grid.bind(minimum_height=grid.setter('height'))
        pop = Popup(title="🎨 Theme", content=content,
                    size_hint=(0.88, 0.72), auto_dismiss=True)
        for name in THEME_NAMES:
            th = THEMES[name]
            btn = Button(text=f"  {name}",
                         font_size=sp(15), bold=True,
                         background_color=th["accent"],
                         background_normal='',
                         size_hint=(1, None), height=dp(46))
            def _pick(_, n=name):
                self.app.apply_theme(n)
                self._apply_theme_visuals()
                pop.dismiss()
            btn.bind(on_press=_pick)
            grid.add_widget(btn)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        content.add_widget(scroll)
        pop.open()

    def _show_mantra_picker(self, *_):
        content = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(10))
        lbl = Label(text="मन्त्र चुनें  — Choose Mantra",
                    font_size=sp(15), size_hint=(1, None), height=dp(36))
        content.add_widget(lbl)
        grid = GridLayout(cols=1, spacing=dp(8), size_hint=(1, None))
        grid.bind(minimum_height=grid.setter('height'))
        pop = Popup(title="📿 Mantra", content=content,
                    size_hint=(0.88, 0.80), auto_dismiss=True)
        for m in MANTRAS:
            th = self.app.theme
            btn = Button(text=m["name"],
                         font_size=sp(16), bold=True,
                         background_color=th["accent"],
                         background_normal='',
                         size_hint=(1, None), height=dp(48))
            def _pick(_, mantra=m):
                self.app.current_mantra = mantra
                self.app.count = get_count(mantra["name"])
                save_setting("mantra", mantra["name"])
                self._refresh_ui()
                pop.dismiss()
            btn.bind(on_press=_pick)
            grid.add_widget(btn)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        content.add_widget(scroll)
        pop.open()

    def _show_stats(self, *_):
        content = BoxLayout(orientation='vertical', padding=dp(14), spacing=dp(8))
        rows = []
        for m in MANTRAS:
            life = get_lifetime(m["name"])
            if life > 0:
                rows.append((m["name"], life))
        if not rows:
            rows = [(self.app.current_mantra["name"], 0)]
        grid = GridLayout(cols=2, spacing=dp(6), size_hint=(1, None))
        grid.bind(minimum_height=grid.setter('height'))
        for name, cnt in sorted(rows, key=lambda x: -x[1]):
            grid.add_widget(Label(text=name, font_size=sp(13),
                                   size_hint=(1, None), height=dp(34)))
            grid.add_widget(Label(text=f"{cnt:,}", font_size=sp(13), bold=True,
                                   color=self.app.theme["counter"],
                                   size_hint=(1, None), height=dp(34)))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        content.add_widget(Label(text="📊 सभी मन्त्रों का जाप", font_size=sp(15),
                                  size_hint=(1, None), height=dp(36)))
        content.add_widget(scroll)
        Popup(title="Statistics", content=content,
              size_hint=(0.88, 0.72), auto_dismiss=True).open()

    def _apply_theme_visuals(self):
        t = self.app.theme
        self._draw_bg()
        self.mandala.set_theme(t)
        self.clock_lbl.color      = t["gold"]
        self.mantra_name_lbl.color = t["gold"]
        self.count_lbl.color      = t["counter"]
        self.mala_lbl.color       = t["gold"]
        self.total_lbl.color      = t["gold"]
        self.flash_lbl.color      = t["accent"]
        self.tap_btn.background_color = t["accent"]
        self.mala_progress_lbl.color  = t["text"]
        self.mala_ring.update(self.app.count % 108, t)

# ─── Mala Bead Ring Widget ────────────────────────────────────────────────────
class MalaRingWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._beads = 0
        self._theme = list(THEMES.values())[0]
        self.bind(size=self._draw, pos=self._draw)

    def update(self, beads, theme):
        self._beads = beads
        self._theme = theme
        self._draw()

    def _draw(self, *_):
        self.canvas.clear()
        if self.width <= 0: return
        with self.canvas:
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            ring_r = min(self.width / 2 - dp(6), self.height / 2 - dp(4))
            bead_r = dp(4)
            total = 108
            for i in range(total):
                ang = math.radians(i * 360 / total - 90)
                bx = cx + math.cos(ang) * ring_r
                by = cy + math.sin(ang) * ring_r
                if i < self._beads:
                    Color(*self._theme["gold"])
                    Ellipse(pos=(bx-bead_r, by-bead_r), size=(bead_r*2, bead_r*2))
                else:
                    Color(*self._theme["text"][:3], 0.20)
                    Ellipse(pos=(bx-bead_r*0.7, by-bead_r*0.7),
                            size=(bead_r*1.4, bead_r*1.4))

# ─── App ──────────────────────────────────────────────────────────────────────
class JaapApp(App):
    def build(self):
        init_db()
        Window.clearcolor = (0.04, 0.02, 0.10, 1)

        # Load saved settings
        saved_theme  = get_setting("theme", THEME_NAMES[0])
        saved_mantra = get_setting("mantra", MANTRAS[0]["name"])
        self.theme   = THEMES.get(saved_theme, THEMES[THEME_NAMES[0]])
        self.current_mantra = next(
            (m for m in MANTRAS if m["name"] == saved_mantra), MANTRAS[0])
        self.count = get_count(self.current_mantra["name"])

        self.sm = ScreenManager(transition=FadeTransition(duration=0.2))
        self.jaap_screen = JaapScreen(app_ref=self, name='jaap')
        self.sm.add_widget(self.jaap_screen)
        self.sm.current = 'jaap'
        return self.sm

    def apply_theme(self, name):
        self.theme = THEMES.get(name, self.theme)
        save_setting("theme", name)

if __name__ == '__main__':
    JaapApp().run()

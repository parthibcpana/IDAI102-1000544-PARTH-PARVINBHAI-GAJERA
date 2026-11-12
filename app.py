import html
import math
import random
from datetime import date, datetime
import pandas as pd
from PIL import Image, ImageDraw
import streamlit as st

# ------------------------------------------------------------------------------
# WaterBuddy — Your Daily Hydration Companion
# Formative Assessment 2 (FA-2) | WellNest Technologies Pvt. Ltd.
# Candidate: Parth Pravinbhai Gajera (ID: 1000544) • CRS: Artificial Intelligence
# ------------------------------------------------------------------------------

st.set_page_config(
    page_title="WaterBuddy — Daily Hydration Companion",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_html(html_str: str):
    """Render cleaned multi-line HTML safely without markdown indentation issues."""
    clean = "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# DOMAIN DATA: CLINICAL AGE COHORTS, VESSELS & COMPANION MASCOTS
# ------------------------------------------------------------------------------

AGE_GOALS = {
    "6–12 years (Kids)": {
        "goal": 1600,
        "cups": 6.4,
        "tier": "🧒 Children",
        "fact": "Children turn over fluids rapidly due to high surface-to-mass ratios. Regular hydration prevents playground fatigue."
    },
    "13–18 years (Teens)": {
        "goal": 2000,
        "cups": 8.0,
        "tier": "🎒 Teens",
        "fact": "Rapid adolescent physical growth and athletic activity demand steady water intake for cognitive school focus."
    },
    "19–50 years (Adults)": {
        "goal": 2500,
        "cups": 10.0,
        "tier": "💼 Adults",
        "fact": "Combats air-conditioned office screen fatigue. Mild 1-2% dehydration triggers tension headaches and brain fog."
    },
    "65+ years (Seniors)": {
        "goal": 1800,
        "cups": 7.2,
        "tier": "👵 Seniors",
        "fact": "Age-related hypodipsia blunts natural thirst receptors. Scheduled routine sipping protects kidney and cardiovascular health."
    },
}

VESSELS = [
    {"name": "Coffee / Tea Mug", "amount": 250, "icon": "☕"},
    {"name": "Standard Glass", "amount": 250, "icon": "🥛"},
    {"name": "Travel Tumbler", "amount": 350, "icon": "🧋"},
    {"name": "Sports Gym Bottle", "amount": 500, "icon": "🍶"},
    {"name": "Hydro Flask", "amount": 750, "icon": "🚰"},
]

COMPANIONS = {
    "HydroBuddy the Sea Turtle 🐢": "Wise ocean navigator, patient habit builder & calm companion.",
    "Bubbles the Playful Dolphin 🐬": "Agile, joyful swimmer celebrating fast logging and energetic hydration.",
    "Splash the River Otter 🦦": "Energetic river explorer who loves regular sips and steady flow.",
    "Misty the Friendly Raindrop 💧": "Calm atmospheric spirit reminding you of cellular vitality.",
    "Pippin the Polar Penguin 🐧": "Crisp Antarctic friend who loves refreshing cold water drinks.",
}

HYDRATION_TIPS = [
    "Drink a full glass of room-temperature water right after waking up to activate your metabolism.",
    "Keep a reusable water bottle within arm's reach of your desk to eliminate screen-bound thirst inertia.",
    "Thirst is a delayed biological signal—by the time you feel thirsty, you're already 1-2% dehydrated.",
    "Having a glass of water 20 minutes before meals aids digestion and supports nutrient absorption.",
    "Fatigue at 3:00 PM is frequently a silent symptom of dehydration rather than lack of sleep or sugar.",
    "Every cup of dehydrating coffee or tea is best balanced with an equal glass of pure water.",
    "Mild dehydration reduces working memory, concentration, and psychomotor speed by up to 20%.",
    "Proper hydration maintains natural skin elasticity, cellular turgor, and joint lubrication.",
    "Sip steadily across the day rather than chugging massive volumes all at once for optimal kidney absorption.",
    "Track your water throughout the day so you can comfortably finish your goal well before bedtime.",
]

# ------------------------------------------------------------------------------
# PROCEDURAL IN-MEMORY HEADLESS TURTLE VECTOR ENGINE
# ------------------------------------------------------------------------------

class HeadlessTurtle:
    """Pure Python Turtle geometry engine executing on Pillow canvases without Tkinter dependencies."""
    def __init__(self, w=240, h=240):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)
        self.x, self.y = w / 2, h / 2
        self.heading = 90
        self.down = True
        self.color = (56, 189, 248, 255)
        self.width = 3

    def forward(self, d):
        rad = math.radians(self.heading)
        nx = self.x + d * math.cos(rad)
        ny = self.y - d * math.sin(rad)
        if self.down:
            self.draw.line([(self.x, self.y), (nx, ny)], fill=self.color, width=self.width)
        self.x, self.y = nx, ny

    def left(self, a): self.heading = (self.heading + a) % 360
    def right(self, a): self.heading = (self.heading - a) % 360
    def penup(self): self.down = False
    def pendown(self): self.down = True
    def goto(self, x, y):
        if self.down:
            self.draw.line([(self.x, self.y), (x, y)], fill=self.color, width=self.width)
        self.x, self.y = x, y

    def arc(self, r, ext, steps=14):
        step_len = (2 * math.pi * r * (abs(ext) / 360.0)) / steps
        for _ in range(steps):
            self.forward(step_len)
            self.left(ext / steps)

def draw_vector_art(art_type="drop"):
    """Procedurally renders professional vector artworks for hydration milestone rewards."""
    t = HeadlessTurtle(240, 240)
    cx, cy = 120, 100
    if art_type in ("drop", "water"):
        drop_pts = []
        for s in range(21):
            frac = s / 20.0
            y = 50 + frac * 125
            w = math.sin(frac * math.pi) * 40
            drop_pts.append((cx + w, y))
        for s in range(20, -1, -1):
            frac = s / 20.0
            y = 50 + frac * 125
            w = math.sin(frac * math.pi) * 40
            drop_pts.append((cx - w, y))
        t.draw.polygon(drop_pts, fill=(14, 165, 233, 240), outline=(2, 132, 199, 255))
        t.draw.ellipse([(cx + 10, cy - 10), (cx + 24, cy + 22)], fill=(224, 242, 254, 230))
        t.penup(); t.goto(cx, 160); t.heading = 270; t.color = (255, 255, 255, 200); t.width = 3; t.pendown()
        t.arc(28, 90)
    elif art_type in ("leaf", "plant"):
        t.penup(); t.goto(120, 215); t.heading = 90; t.color = (74, 122, 92, 255); t.width = 5; t.pendown(); t.forward(45)
        leaf_pts = []
        for step in range(21):
            frac = step / 20.0
            y = 175 - frac * 140
            x = 120 + math.sin(frac * math.pi) * 48
            leaf_pts.append((x, y))
        for step in range(20, -1, -1):
            frac = step / 20.0
            y = 175 - frac * 140
            x = 120 - math.sin(frac * math.pi) * 48
            leaf_pts.append((x, y))
        t.draw.polygon(leaf_pts, fill=(16, 185, 129, 240), outline=(5, 150, 105, 255))
        t.penup(); t.goto(120, 175); t.heading = 90; t.color = (5, 150, 105, 255); t.width = 3; t.pendown(); t.forward(140)
        for y_pos in [145, 120, 95, 70]:
            t.penup(); t.goto(120, y_pos); t.heading = 40; t.width = 2; t.pendown(); t.forward(30)
            t.penup(); t.goto(120, y_pos); t.heading = 140; t.pendown(); t.forward(30)
    else:  # badge rosette
        r_pts_l = [(cx - 24, cy + 26), (cx - 52, cy + 126), (cx - 32, cy + 112), (cx - 12, cy + 120), (cx - 6, cy + 28)]
        t.draw.polygon(r_pts_l, fill=(2, 132, 199, 255), outline=(3, 105, 161, 255))
        t.draw.line([(cx - 24, cy + 26), (cx - 32, cy + 112)], fill=(56, 189, 248, 200), width=2)
        r_pts_r = [(cx + 6, cy + 28), (cx + 12, cy + 120), (cx + 32, cy + 112), (cx + 52, cy + 126), (cx + 24, cy + 26)]
        t.draw.polygon(r_pts_r, fill=(3, 105, 161, 255), outline=(7, 89, 133, 255))
        t.draw.line([(cx + 24, cy + 26), (cx + 32, cy + 112)], fill=(56, 189, 248, 200), width=2)
        rosette_pts = []
        for i in range(64):
            ang = i * (math.pi / 32)
            r = 58 if i % 2 == 0 else 50
            rosette_pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        t.draw.polygon(rosette_pts, fill=(245, 158, 11, 255), outline=(180, 83, 9, 255))
        t.draw.ellipse([(cx - 48, cy - 48), (cx + 48, cy + 48)], fill=(251, 191, 36, 255), outline=(217, 119, 6, 255), width=2)
        t.draw.ellipse([(cx - 41, cy - 41), (cx + 41, cy + 41)], fill=(2, 132, 199, 255), outline=(3, 105, 161, 255), width=2)
        for j in range(12):
            s_ang = j * (2 * math.pi / 12)
            sx = cx + 37 * math.cos(s_ang)
            sy = cy + 37 * math.sin(s_ang)
            t.draw.ellipse([(sx - 2, sy - 2), (sx + 2, sy + 2)], fill=(254, 240, 138, 255))
        t.draw.ellipse([(cx - 30, cy - 30), (cx + 30, cy + 30)], fill=(254, 243, 199, 255), outline=(217, 119, 6, 255), width=2)
        star_pts = []
        for k in range(10):
            ang = -math.pi / 2 + k * (math.pi / 5)
            sr = 19 if k % 2 == 0 else 8.0
            star_pts.append((cx + sr * math.cos(ang), cy + sr * math.sin(ang)))
        t.draw.polygon(star_pts, fill=(217, 119, 6, 255), outline=(146, 64, 14, 255))
        star_inner = []
        for k in range(10):
            ang = -math.pi / 2 + k * (math.pi / 5)
            sr = 15 if k % 2 == 0 else 6.0
            star_inner.append((cx + sr * math.cos(ang), cy + sr * math.sin(ang)))
        t.draw.polygon(star_inner, fill=(245, 158, 11, 255))
    return t.img

# ------------------------------------------------------------------------------
# 60 FPS ANIMATED SVG WATER BOTTLE ENGINE
# ------------------------------------------------------------------------------

def render_animated_bottle_svg(progress_pct, total_ml, goal_ml, width=190, height=310):
    """Renders a glass water bottle with dynamic SVG fluid wave levels and rising bubbles."""
    display_pct = max(0.0, float(progress_pct))
    fill_pct = min(100.0, display_pct)
    fill_h = (fill_pct / 100.0) * 220
    water_y = 270 - fill_h

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 320" width="{width}" height="{height}" style="display: block; margin: 0 auto; filter: drop-shadow(0 8px 24px rgba(2, 132, 199, 0.25));">
    <defs>
        <linearGradient id="wb-glass" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.25"/>
            <stop offset="25%" stop-color="#ffffff" stop-opacity="0.12"/>
            <stop offset="70%" stop-color="#bae6fd" stop-opacity="0.08"/>
            <stop offset="100%" stop-color="#0284c7" stop-opacity="0.3"/>
        </linearGradient>
        <linearGradient id="wb-water" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#38bdf8"/>
            <stop offset="50%" stop-color="#0284c7"/>
            <stop offset="100%" stop-color="#0369a1"/>
        </linearGradient>
        <clipPath id="wb-clip">
            <path d="M 74 48 L 126 48 C 128 58, 144 70, 154 88 L 154 252 C 154 270, 142 276, 122 276 L 78 276 C 58 276, 46 270, 46 252 L 46 88 C 56 70, 72 58, 74 48 Z"/>
        </clipPath>
    </defs>
    <style>
        @keyframes wave-flow {{
            0% {{ transform: translateX(0px); }}
            50% {{ transform: translateX(-35px); }}
            100% {{ transform: translateX(0px); }}
        }}
        @keyframes bubble-rise {{
            0% {{ transform: translateY(0px); opacity: 0.8; }}
            100% {{ transform: translateY(-70px); opacity: 0; }}
        }}
        .wb-wave {{ animation: wave-flow 4s ease-in-out infinite; }}
        .wb-b1 {{ animation: bubble-rise 3s ease-in infinite; }}
        .wb-b2 {{ animation: bubble-rise 2.4s ease-in infinite 1s; }}
    </style>
    <!-- Bottle Cap & Neck -->
    <rect x="76" y="14" width="48" height="16" rx="4" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
    <line x1="84" y1="18" x2="84" y2="26" stroke="#38bdf8" stroke-width="2"/>
    <line x1="100" y1="18" x2="100" y2="26" stroke="#38bdf8" stroke-width="2"/>
    <line x1="116" y1="18" x2="116" y2="26" stroke="#38bdf8" stroke-width="2"/>
    <rect x="70" y="30" width="60" height="18" fill="#e0f2fe" opacity="0.6" stroke="#38bdf8" stroke-width="2"/>
    <!-- Water Chamber (Clipped) -->
    <g clip-path="url(#wb-clip)">
        <rect x="35" y="{water_y}" width="130" height="{fill_h + 30}" fill="url(#wb-water)"/>
        <path class="wb-wave" d="M -20 {water_y} Q 30 {water_y - 6} 80 {water_y} T 180 {water_y} T 280 {water_y} L 280 290 L -20 290 Z" fill="#38bdf8" opacity="0.65"/>
        <circle class="wb-b1" cx="80" cy="{water_y + 40}" r="3.5" fill="#ffffff" opacity="0.75"/>
        <circle class="wb-b2" cx="120" cy="{water_y + 65}" r="4.5" fill="#ffffff" opacity="0.65"/>
    </g>
    <!-- Outer Glass Bottle Silhouette -->
    <path d="M 74 48 L 126 48 C 128 58, 144 70, 154 88 L 154 252 C 154 270, 142 276, 122 276 L 78 276 C 58 276, 46 270, 46 252 L 46 88 C 56 70, 72 58, 74 48 Z" fill="url(#wb-glass)" stroke="#38bdf8" stroke-width="3"/>
    <!-- Specular Highlight Sheen -->
    <path d="M 54 95 L 54 245" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round" opacity="0.45"/>
    <!-- Measurement Ticks -->
    <line x1="144" y1="105" x2="154" y2="105" stroke="#38bdf8" stroke-width="2"/>
    <line x1="140" y1="160" x2="154" y2="160" stroke="#38bdf8" stroke-width="2"/>
    <line x1="144" y1="215" x2="154" y2="215" stroke="#38bdf8" stroke-width="2"/>
    <!-- Percentage & Volume Text Inside Bottle -->
    <text x="100" y="195" text-anchor="middle" fill="#ffffff" font-size="26" font-weight="900" font-family="sans-serif" style="text-shadow: 0 2px 6px rgba(0,0,0,0.5);">{display_pct:.0f}%</text>
    <text x="100" y="218" text-anchor="middle" fill="#e0f2fe" font-size="11" font-weight="700" font-family="sans-serif" style="text-shadow: 0 2px 4px rgba(0,0,0,0.5);">{total_ml:,} / {goal_ml:,} ml</text>
    </svg>
    """

# ------------------------------------------------------------------------------
# 5-CHARACTER ANIMATED SVG MASCOT ENGINE
# ------------------------------------------------------------------------------

def render_animated_avatar_svg(companion_str, mood="start", width=140, height=140):
    """Renders 5 unique animal spirit companions across 5 reactive emotional states."""
    c_lower = companion_str.lower()
    if "dolphin" in c_lower:
        c_type = "dolphin"
    elif "otter" in c_lower:
        c_type = "otter"
    elif "raindrop" in c_lower or "cloud" in c_lower:
        c_type = "raindrop"
    elif "penguin" in c_lower:
        c_type = "penguin"
    else:
        c_type = "turtle"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="{width}" height="{height}">
    <defs>
        <radialGradient id="gl-sh" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="#0284c7" stop-opacity="0"/>
        </radialGradient>
    </defs>
    <style>
        @keyframes float-c {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-6px); }} }}
        @keyframes wave-f {{ 0%, 100% {{ transform: rotate(0deg); }} 50% {{ transform: rotate(18deg); }} }}
        @keyframes blink-e {{ 0%, 90%, 100% {{ transform: scaleY(1); }} 95% {{ transform: scaleY(0.1); }} }}
        .fl-g {{ animation: float-c 3.5s ease-in-out infinite; }}
        .wv-g {{ transform-origin: 150px 100px; animation: wave-f 1.8s ease-in-out infinite; }}
        .bk-g {{ transform-origin: 100px 70px; animation: blink-e 4s infinite; }}
    </style>
    <circle cx="100" cy="100" r="95" fill="url(#gl-sh)"/>
    <g class="fl-g">
    """

    if c_type == "dolphin":
        svg += """
        <path d="M 40 130 C 60 70, 120 50, 165 95 C 175 105, 185 110, 190 100 C 180 125, 150 145, 110 145 C 75 145, 50 140, 40 130 Z" fill="#0284c7" stroke="#0369a1" stroke-width="2.5"/>
        <path d="M 60 135 C 90 142, 125 140, 150 115 C 130 135, 95 140, 60 135 Z" fill="#e0f2fe"/>
        <polygon points="105,62 120,40 128,64" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
        <g class="wv-g">
        <polygon points="175,100 195,85 190,105 195,120" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
        </g>
        <ellipse cx="85" cy="115" rx="18" ry="8" fill="#38bdf8" transform="rotate(20 85 115)"/>
        """
    elif c_type == "otter":
        svg += """
        <ellipse cx="100" cy="130" rx="46" ry="48" fill="#78350f" stroke="#451a03" stroke-width="2.5"/>
        <ellipse cx="100" cy="138" rx="30" ry="34" fill="#fef3c7"/>
        <circle cx="70" cy="46" r="10" fill="#78350f"/>
        <circle cx="130" cy="46" r="10" fill="#78350f"/>
        <ellipse cx="100" cy="68" rx="36" ry="30" fill="#92400e" stroke="#451a03" stroke-width="2.5"/>
        <ellipse cx="100" cy="74" rx="20" ry="14" fill="#fef3c7"/>
        <polygon points="96,68 104,68 100,74" fill="#1e293b"/>
        <ellipse cx="78" cy="118" rx="10" ry="16" fill="#78350f" transform="rotate(20 78 118)"/>
        <g class="wv-g">
        <ellipse cx="122" cy="118" rx="10" ry="16" fill="#78350f" transform="rotate(-20 122 118)"/>
        </g>
        <circle cx="100" cy="120" r="12" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
        """
    elif c_type == "raindrop":
        svg += """
        <path d="M 100 25 C 100 25, 45 95, 45 135 C 45 165, 70 185, 100 185 C 130 185, 155 165, 155 135 C 155 95, 100 25, 100 25 Z" fill="#0ea5e9" stroke="#0284c7" stroke-width="3"/>
        <path d="M 68 110 C 62 130, 70 160, 92 170 C 76 160, 68 135, 74 115 Z" fill="#e0f2fe" opacity="0.6"/>
        <ellipse cx="126" cy="112" rx="12" ry="7" fill="#38bdf8" transform="rotate(25 126 112)"/>
        <ellipse cx="74" cy="112" rx="12" ry="7" fill="#38bdf8" transform="rotate(-25 74 112)"/>
        """
    elif c_type == "penguin":
        svg += """
        <ellipse cx="100" cy="125" rx="46" ry="54" fill="#0f172a" stroke="#020617" stroke-width="2.5"/>
        <ellipse cx="100" cy="132" rx="32" ry="42" fill="#ffffff"/>
        <circle cx="100" cy="62" r="32" fill="#0f172a"/>
        <polygon points="94,64 106,64 100,76" fill="#f97316"/>
        <ellipse cx="78" cy="172" rx="14" ry="7" fill="#f97316"/>
        <ellipse cx="122" cy="172" rx="14" ry="7" fill="#f97316"/>
        <ellipse cx="58" cy="115" rx="10" ry="26" fill="#0f172a" transform="rotate(25 58 115)"/>
        <g class="wv-g">
        <ellipse cx="142" cy="115" rx="10" ry="26" fill="#0f172a" transform="rotate(-25 142 115)"/>
        </g>
        """
    else:  # turtle
        svg += """
        <ellipse cx="60" cy="155" rx="14" ry="20" fill="#40916c" stroke="#1b4332" stroke-width="2" transform="rotate(-25 60 155)"/>
        <ellipse cx="140" cy="155" rx="14" ry="20" fill="#40916c" stroke="#1b4332" stroke-width="2" transform="rotate(25 140 155)"/>
        <ellipse cx="48" cy="95" rx="15" ry="25" fill="#52b788" stroke="#1b4332" stroke-width="2" transform="rotate(-30 48 95)"/>
        <g class="wv-g">
        <ellipse cx="152" cy="95" rx="15" ry="25" fill="#52b788" stroke="#1b4332" stroke-width="2" transform="rotate(30 152 95)"/>
        </g>
        <ellipse cx="100" cy="125" rx="52" ry="46" fill="#2d6a4f" stroke="#1b4332" stroke-width="3"/>
        <ellipse cx="100" cy="125" rx="40" ry="34" fill="#40916c" stroke="#1b4332" stroke-width="2"/>
        <ellipse cx="100" cy="125" rx="24" ry="20" fill="#74c69d" stroke="#2d6a4f" stroke-width="2"/>
        <ellipse cx="100" cy="62" rx="26" ry="24" fill="#74c69d" stroke="#1b4332" stroke-width="2"/>
        """

    # Face Expressions & Mood Overlay
    if mood == "ecstatic":
        svg += """
        <!-- Sunglasses & Gold Crown -->
        <rect x="74" y="52" width="22" height="13" rx="3" fill="#1e293b"/>
        <rect x="104" y="52" width="22" height="13" rx="3" fill="#1e293b"/>
        <line x1="96" y1="58" x2="104" y2="58" stroke="#f59e0b" stroke-width="3"/>
        <polygon points="85,32 92,20 100,28 108,20 115,32" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
        <ellipse cx="78" cy="72" rx="5" ry="3" fill="#f43f5e" opacity="0.6"/>
        <ellipse cx="122" cy="72" rx="5" ry="3" fill="#f43f5e" opacity="0.6"/>
        <path d="M 88 72 Q 100 84 112 72" fill="#f43f5e" stroke="#1e293b" stroke-width="2.5" stroke-linecap="round"/>
        """
    elif mood in ("happy", "energized"):
        svg += """
        <g class="bk-g">
        <circle cx="88" cy="58" r="5" fill="#1e293b"/>
        <circle cx="86" cy="56" r="1.8" fill="#ffffff"/>
        <circle cx="112" cy="58" r="5" fill="#1e293b"/>
        <circle cx="110" cy="56" r="1.8" fill="#ffffff"/>
        </g>
        <ellipse cx="78" cy="68" rx="5" ry="3" fill="#fb7185" opacity="0.65"/>
        <ellipse cx="122" cy="68" rx="5" ry="3" fill="#fb7185" opacity="0.65"/>
        <path d="M 88 68 Q 100 80 112 68" fill="none" stroke="#1e293b" stroke-width="3" stroke-linecap="round"/>
        """
    else:  # start / attentive
        svg += """
        <circle cx="88" cy="58" r="4.5" fill="#1e293b"/>
        <circle cx="86" cy="56" r="1.6" fill="#ffffff"/>
        <circle cx="112" cy="58" r="4.5" fill="#1e293b"/>
        <circle cx="110" cy="56" r="1.6" fill="#ffffff"/>
        <path d="M 91 68 Q 100 74 109 68" fill="none" stroke="#1e293b" stroke-width="2.5" stroke-linecap="round"/>
        """

    svg += "</g></svg>"
    return svg

# ------------------------------------------------------------------------------
# MATHEMATICAL PROGRESS, BADGES & DYNAMIC SPEECH
# ------------------------------------------------------------------------------

def calculate_progress(total_ml: int, goal_ml: int):
    """Pure mathematical progress calculation with bounds clamping."""
    goal = max(1, int(goal_ml))
    total = max(0, int(total_ml))
    remaining = max(0, goal - total)
    pct = round((total / goal) * 100.0, 1)
    bar_val = min(1.0, max(0.0, total / goal))
    return remaining, pct, bar_val

def get_user_hydration_rank(intake_history):
    """Computes an honorific hydration rank based on active drink consistency."""
    count = len(intake_history)
    if count == 0:
        return "🌱 Seedling Sipper"
    elif count <= 2:
        return "💧 Morning Dew"
    elif count <= 4:
        return "🌊 Flowing Stream"
    else:
        return "👑 Ocean Master"

def evaluate_badges(intake_history, total_intake, daily_goal, standard_goal):
    """Evaluates 5 dynamic hydration milestone achievements live from active transactions."""
    count = len(intake_history)
    badges = [
        {
            "id": "first_sip",
            "name": "First Sip",
            "icon": "🌱",
            "desc": "Log your first water intake of the day",
            "unlocked": count >= 1,
            "progress": f"{min(count, 1)}/1 drink logged"
        },
        {
            "id": "steady_pacer",
            "name": "Steady Pacer",
            "icon": "⏱️",
            "desc": "Build habit rhythm with 3+ logged drinks today",
            "unlocked": count >= 3,
            "progress": f"{min(count, 3)}/3 drinks logged"
        },
        {
            "id": "halfway_hydrated",
            "name": "Halfway Hydrated",
            "icon": "🌊",
            "desc": "Reach 50% of your daily water target",
            "unlocked": total_intake >= (daily_goal * 0.5),
            "progress": f"{total_intake}/{int(daily_goal * 0.5)} ml"
        },
        {
            "id": "hydro_champion",
            "name": "Hydro Champion",
            "icon": "👑",
            "desc": "Achieve 100% of your daily hydration goal",
            "unlocked": total_intake >= daily_goal and daily_goal > 0,
            "progress": f"{total_intake}/{daily_goal} ml"
        },
        {
            "id": "calibration_master",
            "name": "Calibration Master",
            "icon": "🎯",
            "desc": "Personalize your daily goal from standard baseline",
            "unlocked": daily_goal != standard_goal,
            "progress": f"Target: {daily_goal} ml"
        },
    ]
    return badges

def get_mascot_speech(companion_str, user_name, total_ml, goal_ml, pct, mood):
    """Generates personalized, character-driven speech based on emotional milestones."""
    c_name = companion_str.split()[0]
    first_name = user_name.strip() if user_name.strip() else "Friend"

    if mood == "ecstatic":
        return f"🎉 GOAL CRUSHED, {first_name}! You reached {total_ml:,} ml (100%+)! {c_name} put on gold sunglasses to celebrate your vibrant cellular energy!"
    elif mood == "energized":
        return f"⚡ Almost at the finish line, {first_name}! You're at {pct:.0f}% ({total_ml:,} ml). Just one more refreshing glass to hit your target!"
    elif mood == "happy":
        return f"🌟 Halfway milestone achieved! Fantastic rhythm, {first_name}. You've logged {total_ml:,} ml. Your brain focus and energy are powered up!"
    elif mood == "attentive":
        return f"💧 Wonderful start, {first_name}! {total_ml:,} ml logged ({pct:.0f}%). Keep your bottle nearby and take calm, steady sips!"
    else:  # start
        return f"Good day, {first_name}! I am {c_name}. Every sip is an investment in your energy and focus. Log your first drink below!"

# ------------------------------------------------------------------------------
# SESSION STATE INITIALIZATION (Clean Defaults, 100% Local Volatile Memory)
# ------------------------------------------------------------------------------

if "onboarded" not in st.session_state: st.session_state.onboarded = False
if "user_name" not in st.session_state: st.session_state.user_name = "Parth Gajera"
if "user_avatar" not in st.session_state: st.session_state.user_avatar = list(COMPANIONS.keys())[0]
if "age_cohort" not in st.session_state: st.session_state.age_cohort = list(AGE_GOALS.keys())[2]  # Adults default
if "daily_goal" not in st.session_state: st.session_state.daily_goal = AGE_GOALS[st.session_state.age_cohort]["goal"]
if "total_intake" not in st.session_state: st.session_state.total_intake = 0
if "intake_history" not in st.session_state: st.session_state.intake_history = []
if "dark_theme" not in st.session_state: st.session_state.dark_theme = True
if "recent_art" not in st.session_state: st.session_state.recent_art = None
if "mascot_mood" not in st.session_state: st.session_state.mascot_mood = "start"
if "show_reset_confirm" not in st.session_state: st.session_state.show_reset_confirm = False
if "nav_view" not in st.session_state: st.session_state.nav_view = "📊 Dashboard"

# ------------------------------------------------------------------------------
# COMPREHENSIVE DUAL-PALETTE HIGH-CONTRAST CSS THEME ENGINE
# ------------------------------------------------------------------------------

if st.session_state.dark_theme:
    render_html("""
    <style>
    .stApp { background-color: #07131b !important; color: #f8fafc !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    h1, h2, h3, h4, h5, p, span, label { color: #f8fafc !important; }
    [data-testid="stSidebar"] { background-color: #050e14 !important; border-right: 1.5px solid #0e2a3c !important; }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    .hero-banner { background: linear-gradient(135deg, #0c2738, #0e3a53) !important; border: 1.5px solid #0284c7 !important; border-radius: 18px; padding: 1.4rem 1.6rem; color: #f8fafc !important; margin-bottom: 1.2rem; box-shadow: 0 8px 24px rgba(0,0,0,0.4); }
    .metric-card { background: #0c1e2a !important; border: 1.5px solid #164e63 !important; border-radius: 14px; padding: 1.1rem; text-align: center; box-shadow: 0 4px 14px rgba(0,0,0,0.3); }
    .metric-val { font-size: 2rem; font-weight: 900; color: #38bdf8 !important; margin-top: 0.2rem; }
    .metric-lbl { font-size: 0.85rem; font-weight: 700; color: #94a3b8 !important; text-transform: uppercase; letter-spacing: 0.5px; }
    .vessel-chip { background: #0e2637 !important; border: 1.5px solid #0369a1 !important; border-radius: 12px; padding: 0.8rem; text-align: center; color: #f8fafc !important; }
    .mascot-bubble { background: #0c2536 !important; border: 1.5px solid #38bdf8 !important; border-radius: 16px; padding: 1.1rem 1.3rem; color: #f8fafc !important; box-shadow: 0 4px 16px rgba(56, 189, 248, 0.15); }
    .badge-on { background: linear-gradient(135deg, #0369a1, #0284c7) !important; border: 2px solid #38bdf8 !important; border-radius: 14px; padding: 1rem; color: #ffffff !important; box-shadow: 0 4px 16px rgba(56, 189, 248, 0.25); margin-bottom: 0.8rem; }
    .badge-off { background: #0c1822 !important; border: 2px dashed #334155 !important; border-radius: 14px; padding: 1rem; color: #64748b !important; filter: grayscale(100%); opacity: 0.55; margin-bottom: 0.8rem; }
    .avatar-card { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 1.2rem; }
    .avatar-circle { width: 96px; height: 96px; border-radius: 50%; border: 3px solid #38bdf8; overflow: hidden; background: #0c2536; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 18px rgba(56, 189, 248, 0.3); margin: 0 auto; }
    .rank-pill { font-size: 0.8rem; background: #0c4a6e; color: #38bdf8; border: 1px solid #0284c7; padding: 0.2rem 0.7rem; border-radius: 99px; font-weight: 800; display: inline-block; margin-top: 0.35rem; }
    </style>
    """)
else:
    render_html("""
    <style>
    .stApp { background-color: #f0f9ff !important; color: #0f172a !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    h1, h2, h3, h4, h5, p, span, label { color: #0f172a !important; }
    [data-testid="stSidebar"] { background-color: #e0f2fe !important; border-right: 1.5px solid #bae6fd !important; }
    [data-testid="stSidebar"] * { color: #0f172a !important; }
    .hero-banner { background: linear-gradient(135deg, #e0f2fe, #bae6fd) !important; border: 1.5px solid #38bdf8 !important; border-radius: 18px; padding: 1.4rem 1.6rem; color: #0369a1 !important; margin-bottom: 1.2rem; box-shadow: 0 4px 16px rgba(2, 132, 199, 0.1); }
    .metric-card { background: #ffffff !important; border: 1.5px solid #bae6fd !important; border-radius: 14px; padding: 1.1rem; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .metric-val { font-size: 2rem; font-weight: 900; color: #0284c7 !important; margin-top: 0.2rem; }
    .metric-lbl { font-size: 0.85rem; font-weight: 700; color: #64748b !important; text-transform: uppercase; letter-spacing: 0.5px; }
    .vessel-chip { background: #ffffff !important; border: 1.5px solid #bae6fd !important; border-radius: 12px; padding: 0.8rem; text-align: center; color: #0f172a !important; }
    .mascot-bubble { background: #ffffff !important; border: 1.5px solid #38bdf8 !important; border-radius: 16px; padding: 1.1rem 1.3rem; color: #0f172a !important; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.12); }
    .badge-on { background: linear-gradient(135deg, #0284c7, #0369a1) !important; border: 2px solid #38bdf8 !important; border-radius: 14px; padding: 1rem; color: #ffffff !important; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.2); margin-bottom: 0.8rem; }
    .badge-off { background: #f8fafc !important; border: 2px dashed #cbd5e1 !important; border-radius: 14px; padding: 1rem; color: #64748b !important; filter: grayscale(100%); opacity: 0.55; margin-bottom: 0.8rem; }
    .avatar-card { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 1.2rem; }
    .avatar-circle { width: 96px; height: 96px; border-radius: 50%; border: 3px solid #0284c7; overflow: hidden; background: #ffffff; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 16px rgba(2, 132, 199, 0.18); margin: 0 auto; }
    .rank-pill { font-size: 0.8rem; background: #e0f2fe; color: #0369a1; border: 1px solid #38bdf8; padding: 0.2rem 0.7rem; border-radius: 99px; font-weight: 800; display: inline-block; margin-top: 0.35rem; }
    </style>
    """)

# ------------------------------------------------------------------------------
# SCREEN 1: WELCOME & ONBOARDING (First-Run Standalone Experience)
# ------------------------------------------------------------------------------

if not st.session_state.onboarded:
    render_html("""
    <div style="text-align: center; margin-top: 1rem; margin-bottom: 1.5rem;">
        <h1 style="color: #38bdf8; font-size: 2.6rem; font-weight: 900; margin: 0;">💧 Meet WaterBuddy</h1>
        <p style="color: #94a3b8; font-size: 1.2rem; margin-top: 0.4rem;">Your intelligent, age-aware daily hydration companion.</p>
    </div>
    """)

    col_ob1, col_ob2 = st.columns([1.15, 0.85], gap="large")
    with col_ob1:
        st.subheader("⚙️ Configure Your Hydration Profile")
        in_name = st.text_input("Your Name:", value=st.session_state.user_name)
        in_avatar = st.selectbox("Choose Your Companion Spirit Mascot:", options=list(COMPANIONS.keys()))
        in_cohort = st.selectbox("Select Your Clinical Age Cohort:", options=list(AGE_GOALS.keys()), index=list(AGE_GOALS.keys()).index(st.session_state.age_cohort))

        std_goal = AGE_GOALS[in_cohort]["goal"]
        st.caption(f"💡 **Clinical Recommendation**: ~{std_goal:,} ml/day ({AGE_GOALS[in_cohort]['cups']} cups). {AGE_GOALS[in_cohort]['fact']}")

        in_goal = st.number_input(
            "Fine-Tune Your Daily Target (ml):",
            min_value=500,
            max_value=6000,
            value=int(std_goal),
            step=100,
            help="You can adjust the suggested clinical baseline to match your climate or physical activity."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Enter WaterBuddy Dashboard →", type="primary", width="stretch"):
            st.session_state.user_name = in_name.strip() if in_name.strip() else "Friend"
            st.session_state.user_avatar = in_avatar
            st.session_state.age_cohort = in_cohort
            st.session_state.daily_goal = in_goal
            st.session_state.onboarded = True
            c_name = in_avatar.split()[0]
            st.toast(f"Welcome, {st.session_state.user_name}! {c_name} is ready!", icon="💧")
            st.rerun()

    with col_ob2:
        st.subheader("🐾 Companion Preview")
        preview_svg = render_animated_avatar_svg(in_avatar, "happy", 180, 180)
        render_html(f"""
        <div style="background: #0c2536; border: 1.5px solid #38bdf8; border-radius: 18px; padding: 1.4rem; text-align: center; margin-bottom: 1rem;">
            {preview_svg}
            <div style="font-size: 1.25rem; font-weight: 800; color: #38bdf8; margin-top: 0.6rem;">{in_avatar.split('—')[0]}</div>
            <p style="font-size: 0.88rem; color: #e0f2fe; margin-top: 0.3rem;">{COMPANIONS[in_avatar]}</p>
        </div>
        <div style="background: #081a26; border: 1.5px solid #0284c7; border-radius: 14px; padding: 1.1rem; color: #e0f2fe; font-size: 0.85rem; line-height: 1.6;">
            <strong style="color: #38bdf8;">The Calm Technology Promise:</strong>
            <ul style="margin: 0.4rem 0 0 1.2rem; padding: 0;">
                <li>🔒 <strong>100% Local Privacy:</strong> 0 KB cloud telemetry; runs locally in your session.</li>
                <li>🎯 <strong>Age-Aware Goals:</strong> Clinically benchmarked against WHO / EFSA standards.</li>
                <li>🌊 <strong>Dynamic Dual Visuals:</strong> 60 FPS animated fluid wave bottle & mascot rewards.</li>
            </ul>
        </div>
        """)

# ------------------------------------------------------------------------------
# SCREEN 2: MAIN DASHBOARD & TABS
# ------------------------------------------------------------------------------
else:
    # Calculations
    total = int(st.session_state.total_intake)
    goal = int(st.session_state.daily_goal)
    std_baseline = AGE_GOALS[st.session_state.age_cohort]["goal"]
    remaining, percentage, bar_value = calculate_progress(total, goal)

    # Determine Mascot Emotional State
    if percentage >= 100:
        st.session_state.mascot_mood = "ecstatic"
    elif percentage >= 75:
        st.session_state.mascot_mood = "energized"
    elif percentage >= 50:
        st.session_state.mascot_mood = "happy"
    elif percentage >= 25:
        st.session_state.mascot_mood = "attentive"
    else:
        st.session_state.mascot_mood = "start"

    # Sidebar: Profile Card, Navigation, Settings & Guarded Reset
    with st.sidebar:
        user_rank = get_user_hydration_rank(st.session_state.intake_history)
        avatar_svg_mini = render_animated_avatar_svg(st.session_state.user_avatar, st.session_state.mascot_mood, 90, 90)
        c_short = st.session_state.user_avatar.split()[0]

        render_html(f"""
        <div class="avatar-card">
            <div class="avatar-circle">
                {avatar_svg_mini}
            </div>
            <div style="font-size: 1.25rem; font-weight: 800; margin-top: 0.6rem;">{html.escape(st.session_state.user_name)}</div>
            <div class="rank-pill">{user_rank}</div>
            <div style="font-size: 0.84rem; margin-top: 0.35rem; opacity: 0.9;">{st.session_state.user_avatar.split('—')[0]}</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Target: {goal:,} ml/day</div>
        </div>
        """)

        if st.button("⚙️ Edit Profile / Avatar", width="stretch"):
            st.session_state.onboarded = False
            st.rerun()

        st.markdown("---")
        st.session_state.nav_view = st.radio("Navigation:", ["📊 Dashboard", "🏆 Wall of Badges", "🥤 Vessel & Cup Studio"])

        dark_toggle = st.toggle("🌙 High-Contrast Dark Mode", value=st.session_state.dark_theme)
        if dark_toggle != st.session_state.dark_theme:
            st.session_state.dark_theme = dark_toggle
            st.rerun()

        st.markdown("---")
        st.caption(f"💡 *{random.choice(HYDRATION_TIPS)}*")

        if not st.session_state.show_reset_confirm:
            if st.button("🔄 Start a New Day (Reset)", width="stretch"):
                st.session_state.show_reset_confirm = True
                st.rerun()
        else:
            st.warning("Clear today's logged water intake?")
            rc1, rc2 = st.columns(2)
            with rc1:
                if st.button("Yes, Reset", type="primary", width="stretch"):
                    st.session_state.total_intake = 0
                    st.session_state.intake_history = []
                    st.session_state.recent_art = None
                    st.session_state.show_reset_confirm = False
                    st.session_state.mascot_mood = "start"
                    st.toast("Started fresh for a new day!", icon="🔄")
                    st.rerun()
            with rc2:
                if st.button("Cancel", width="stretch"):
                    st.session_state.show_reset_confirm = False
                    st.rerun()

    # --------------------------------------------------------------------------
    # VIEW 1: 📊 DASHBOARD
    # --------------------------------------------------------------------------
    if st.session_state.nav_view == "📊 Dashboard":
        # Hero Mascot Canvas with Dynamic Speech & Procedural Vector Reward
        speech_msg = get_mascot_speech(st.session_state.user_avatar, st.session_state.user_name, total, goal, percentage, st.session_state.mascot_mood)

        if st.session_state.recent_art:
            col_m1, col_m2, col_m3 = st.columns([0.65, 2.35, 1.0])
            with col_m1:
                render_html(render_animated_avatar_svg(st.session_state.user_avatar, st.session_state.mascot_mood, 140, 140))
            with col_m2:
                render_html(f"""
                <div class="mascot-bubble">
                    <div style="font-size: 1.15rem; font-weight: 800; color: #38bdf8;">{c_short}'s Live Reaction:</div>
                    <div style="font-size: 0.98rem; margin-top: 0.3rem; line-height: 1.5;">"{html.escape(speech_msg)}"</div>
                </div>
                """)
            with col_m3:
                art_img = draw_vector_art(st.session_state.recent_art)
                art_label = {"drop": "Water Droplet 💧", "leaf": "Hydration Sprout 🌿", "badge": "Achievement Rosette 🏆"}.get(st.session_state.recent_art, "Hydration Milestone")
                st.image(art_img, width=130, caption=f"{c_short} drew: {art_label}")
        else:
            col_m1, col_m2 = st.columns([0.65, 3.35])
            with col_m1:
                render_html(render_animated_avatar_svg(st.session_state.user_avatar, st.session_state.mascot_mood, 140, 140))
            with col_m2:
                render_html(f"""
                <div class="mascot-bubble">
                    <div style="font-size: 1.15rem; font-weight: 800; color: #38bdf8;">{c_short}'s Live Reaction:</div>
                    <div style="font-size: 0.98rem; margin-top: 0.3rem; line-height: 1.5;">"{html.escape(speech_msg)}"</div>
                </div>
                """)

        st.markdown("<br>", unsafe_allow_html=True)

        # Top Metric Row: Total Logged, Daily Goal, Remaining, and Clinical Comparison
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            render_html(f"""
            <div class="metric-card">
                <div class="metric-lbl">Total Water Logged</div>
                <div class="metric-val">{total:,} <span style="font-size: 1.1rem;">ml</span></div>
                <div style="font-size: 0.82rem; color: #38bdf8; font-weight: 700; margin-top: 0.2rem;">{percentage:.1f}% of goal</div>
            </div>
            """)
        with kpi2:
            render_html(f"""
            <div class="metric-card">
                <div class="metric-lbl">Daily Target</div>
                <div class="metric-val">{goal:,} <span style="font-size: 1.1rem;">ml</span></div>
                <div style="font-size: 0.82rem; color: #94a3b8; margin-top: 0.2rem;">~{goal / 250:.1f} standard cups</div>
            </div>
            """)
        with kpi3:
            render_html(f"""
            <div class="metric-card">
                <div class="metric-lbl">Remaining to Go</div>
                <div class="metric-val">{remaining:,} <span style="font-size: 1.1rem;">ml</span></div>
                <div style="font-size: 0.82rem; color: {'#34d399' if remaining == 0 else '#94a3b8'}; font-weight: 700; margin-top: 0.2rem;">
                    {'✨ Target Achieved!' if remaining == 0 else f'~{remaining / 250:.1f} cups left'}
                </div>
            </div>
            """)
        with kpi4:
            delta_val = goal - std_baseline
            render_html(f"""
            <div class="metric-card">
                <div class="metric-lbl">Standard Comparison</div>
                <div class="metric-val">{std_baseline:,} <span style="font-size: 1.1rem;">ml</span></div>
                <div style="font-size: 0.82rem; color: #38bdf8; font-weight: 700; margin-top: 0.2rem;">
                    {f'+{delta_val} ml vs baseline' if delta_val > 0 else (f'{delta_val} ml vs baseline' if delta_val < 0 else 'Exactly at baseline')}
                </div>
            </div>
            """)

        st.markdown("<br>", unsafe_allow_html=True)

        # Dual Feedback Section: Animated Bottle on Left, Logging & Vessel Chips on Right
        col_feed1, col_feed2 = st.columns([1.1, 1.9], gap="large")
        with col_feed1:
            st.subheader("🍶 Your Water Bottle")
            render_html(render_animated_bottle_svg(percentage, total, goal, 200, 310))
            st.progress(bar_value)
            st.caption(f"Progress: **{percentage:.1f}%** ({total:,} of {goal:,} ml)")

        with col_feed2:
            st.subheader("➕ Log Your Drink")
            st.caption("One-click rapid logging from real-world calibrated vessels:")

            # 5 Tactile Vessel Container Chips
            v_cols = st.columns(len(VESSELS))
            for idx, v in enumerate(VESSELS):
                with v_cols[idx]:
                    render_html(f"""
                    <div class="vessel-chip">
                        <div style="font-size: 1.8rem; line-height: 1;">{v['icon']}</div>
                        <div style="font-weight: 700; font-size: 0.82rem; margin-top: 0.3rem;">{v['name'].split()[0]}</div>
                        <div style="font-size: 0.78rem; color: #38bdf8; font-weight: 800;">+{v['amount']} ml</div>
                    </div>
                    """)
                    if st.button(f"+{v['amount']}", key=f"vessel_btn_{idx}", width="stretch"):
                        st.session_state.total_intake += v['amount']
                        st.session_state.intake_history.append({
                            "id": len(st.session_state.intake_history) + 1,
                            "time": datetime.now().strftime("%I:%M %p"),
                            "vessel": f"{v['icon']} {v['name']}",
                            "amount": v['amount'],
                            "running_total": st.session_state.total_intake
                        })
                        new_pct = (st.session_state.total_intake / goal) * 100
                        if new_pct >= 100:
                            st.session_state.recent_art = "badge"
                            st.balloons()
                        elif new_pct >= 50:
                            st.session_state.recent_art = "leaf"
                        else:
                            st.session_state.recent_art = "drop"
                        st.toast(f"+{v['amount']} ml added from {v['name']}!", icon="💧")
                        st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            # Custom Numeric Stepper
            with st.form("custom_drink_form", clear_on_submit=True):
                cf1, cf2 = st.columns([2, 1])
                with cf1:
                    custom_amt = st.number_input("Or Enter Custom Amount (ml):", min_value=10, max_value=2500, value=250, step=50)
                with cf2:
                    st.write("")
                    st.write("")
                    submit_custom = st.form_submit_button("💧 Log Drink", width="stretch")

                if submit_custom:
                    st.session_state.total_intake += int(custom_amt)
                    st.session_state.intake_history.append({
                        "id": len(st.session_state.intake_history) + 1,
                        "time": datetime.now().strftime("%I:%M %p"),
                        "vessel": "🏷️ Custom Entry",
                        "amount": int(custom_amt),
                        "running_total": st.session_state.total_intake
                    })
                    new_pct = (st.session_state.total_intake / goal) * 100
                    if new_pct >= 100:
                        st.session_state.recent_art = "badge"
                        st.balloons()
                    elif new_pct >= 50:
                        st.session_state.recent_art = "leaf"
                    else:
                        st.session_state.recent_art = "drop"
                    st.toast(f"{int(custom_amt)} ml logged successfully!", icon="💧")
                    st.rerun()

            # Interactive Cup Converter with 1-Click Direct Addition
            st.markdown("<br>", unsafe_allow_html=True)
            render_html("""
            <div style="font-size: 0.95rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.4rem;">🥤 Interactive Cup Converter (1 Cup = 250 ml)</div>
            """)
            cup_c1, cup_c2, cup_c3 = st.columns([1.2, 1.2, 1.4])
            with cup_c1:
                cups_input = st.number_input("Cups Count:", min_value=0.5, max_value=15.0, value=1.0, step=0.5, label_visibility="collapsed")
            with cup_c2:
                converted_ml = int(cups_input * 250)
                st.markdown(f"<div style='font-size: 1.2rem; font-weight: 800; padding-top: 0.2rem; color: #38bdf8;'>= {converted_ml:,} ml</div>", unsafe_allow_html=True)
            with cup_c3:
                if st.button(f"+ Add {converted_ml} ml to Tracker", width="stretch"):
                    st.session_state.total_intake += converted_ml
                    st.session_state.intake_history.append({
                        "id": len(st.session_state.intake_history) + 1,
                        "time": datetime.now().strftime("%I:%M %p"),
                        "vessel": f"🥤 {cups_input} Cup(s)",
                        "amount": converted_ml,
                        "running_total": st.session_state.total_intake
                    })
                    st.toast(f"Logged {converted_ml} ml from Cup Converter!", icon="🥤")
                    st.rerun()

        # Intake Activity Feed & History Ledger
        st.markdown("---")
        st.subheader("📋 Today's Hydration Ledger")
        if st.session_state.intake_history:
            df_hist = pd.DataFrame(st.session_state.intake_history)
            df_hist = df_hist[["id", "time", "vessel", "amount", "running_total"]]
            df_hist.columns = ["#", "Time", "Vessel / Source", "Amount (ml)", "Running Total (ml)"]

            lh1, lh2 = st.columns([3, 1])
            with lh1:
                st.dataframe(df_hist, width="stretch", hide_index=True)
            with lh2:
                if st.button("↩️ Undo Last Drink", width="stretch"):
                    last_item = st.session_state.intake_history.pop()
                    st.session_state.total_intake = max(0, st.session_state.total_intake - last_item["amount"])
                    st.toast(f"Undid {last_item['amount']} ml log.", icon="↩️")
                    st.rerun()
                st.download_button(
                    "📥 Export Intake CSV",
                    df_hist.to_csv(index=False).encode("utf-8"),
                    f"waterbuddy_log_{date.today().isoformat()}.csv",
                    "text/csv",
                    width="stretch"
                )
        else:
            st.caption("No drinks logged yet today. Click any vessel chip above to record your first sip!")

    # --------------------------------------------------------------------------
    # VIEW 2: 🏆 WALL OF BADGES
    # --------------------------------------------------------------------------
    elif st.session_state.nav_view == "🏆 Wall of Badges":
        st.title("🏆 Wall of Badges & Hydration Milestones")
        st.caption("Unlocked achievements glow in vibrant radiant aqua. Locked badges remain in monochrome grayscale B&W until earned!")

        badges = evaluate_badges(st.session_state.intake_history, total, goal, std_baseline)
        unlocked_count = sum(1 for b in badges if b["unlocked"])

        st.metric("Milestones Unlocked", f"{unlocked_count} of {len(badges)}", f"{int((unlocked_count / len(badges)) * 100)}% Complete")
        st.markdown("<br>", unsafe_allow_html=True)

        wb1, wb2 = st.columns(2, gap="large")
        for i, b in enumerate(badges):
            target_col = wb1 if i % 2 == 0 else wb2
            with target_col:
                if b["unlocked"]:
                    render_html(f"""
                    <div class="badge-on">
                        <div style="display: flex; gap: 1rem; align-items: center;">
                            <div style="font-size: 3.2rem;">{b['icon']}</div>
                            <div>
                                <h3 style="margin: 0; color: #ffffff;">{b['name']}</h3>
                                <p style="margin: 0.2rem 0; font-size: 0.9rem; color: #e0f2fe;">{b['desc']}</p>
                                <span style="background: #38bdf8; color: #082f49; font-weight: 800; font-size: 0.75rem; padding: 0.2rem 0.65rem; border-radius: 99px;">
                                    ✨ UNLOCKED ({b['progress']})
                                </span>
                            </div>
                        </div>
                    </div>
                    """)
                else:
                    render_html(f"""
                    <div class="badge-off">
                        <div style="display: flex; gap: 1rem; align-items: center;">
                            <div style="font-size: 3.2rem;">🔒</div>
                            <div>
                                <h3 style="margin: 0; color: #64748b;">{b['name']}</h3>
                                <p style="margin: 0.2rem 0; font-size: 0.9rem; color: #94a3b8;">{b['desc']}</p>
                                <span style="background: #334155; color: #ffffff; font-weight: 700; font-size: 0.75rem; padding: 0.2rem 0.65rem; border-radius: 99px;">
                                    🔒 LOCKED ({b['progress']})
                                </span>
                            </div>
                        </div>
                    </div>
                    """)

    # --------------------------------------------------------------------------
    # VIEW 3: 🥤 VESSEL & CUP STUDIO
    # --------------------------------------------------------------------------
    elif st.session_state.nav_view == "🥤 Vessel & Cup Studio":
        st.title("🥤 Vessel & Hydration Calibration Studio")
        st.caption("Deep clinical research into beverage containers, demographic needs, and daily habits.")

        vc1, vc2 = st.columns(2, gap="large")
        with vc1:
            st.subheader("🍶 Common Beverage Vessels & Milliliter Ratios")
            for v in VESSELS:
                render_html(f"""
                <div style="background: #0c2536; border: 1.5px solid #0284c7; border-radius: 12px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; gap: 0.8rem; align-items: center;">
                        <span style="font-size: 1.8rem;">{v['icon']}</span>
                        <strong>{v['name']}</strong>
                    </div>
                    <span style="font-weight: 800; color: #38bdf8;">{v['amount']} ml (~{v['amount'] / 250:.1f} cups)</span>
                </div>
                """)

        with vc2:
            st.subheader("📚 Clinical Hydration Baselines (WHO / EFSA)")
            for cohort_name, cohort_info in AGE_GOALS.items():
                render_html(f"""
                <div style="background: #0c2536; border: 1.5px solid #164e63; border-radius: 12px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>{cohort_info['tier']} ({cohort_name})</strong>
                        <span style="color: #38bdf8; font-weight: 800;">{cohort_info['goal']:,} ml/day</span>
                    </div>
                    <p style="font-size: 0.85rem; color: #cbd5e1; margin: 0.3rem 0 0 0;">{cohort_info['fact']}</p>
                </div>
                """)

# ------------------------------------------------------------------------------
# FOOTER: ACADEMIC CREDENTIALS & METADATA
# ------------------------------------------------------------------------------
st.divider()
render_html("""
<div style="text-align: center; color: #64748b; font-size: 0.82rem; padding: 0.8rem 0;">
    <strong>WaterBuddy — Your Daily Hydration Companion</strong> • IDAI 102: Python Programming<br>
    Candidate: <strong>Parth Pravinbhai Gajera</strong> (ID: <code>1000544</code>) • CRS: Artificial Intelligence • WellNest Technologies Pvt. Ltd.
</div>
""")

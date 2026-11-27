import base64
import html
import io
import math
import os
import random
from datetime import date, datetime, timedelta
import pandas as pd
from PIL import Image, ImageDraw
import streamlit as st

try:
    import altair as alt
    HAS_ALTAIR = True
except Exception:
    HAS_ALTAIR = False

ASSET_3D_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "3d")

@st.cache_data(show_spinner=False)
def load_asset_b64(rel_path: str) -> str:
    full = os.path.join(ASSET_3D_DIR, rel_path.replace("/", os.sep))
    if not os.path.isfile(full):
        return ""
    with open(full, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

st.set_page_config(
    page_title="WaterBuddy — Daily Hydration Companion",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="auto",
)

def render_html(html_str: str):
    clean = "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)

def render_section_header(kicker: str, title: str, subtitle: str = ""):
    sub_html = f'<p class="sec-sub">{html.escape(subtitle)}</p>' if subtitle else ""
    droplet_svg = (
        '<svg width="14" height="16" viewBox="0 0 14 16" xmlns="http://www.w3.org/2000/svg" style="display:block;">'
        '<path d="M7 1 C7 1, 13 7.5, 13 10.8 C13 13.8, 10.3 15.5, 7 15.5 C3.7 15.5, 1 13.8, 1 10.8 C1 7.5, 7 1, 7 1 Z" fill="currentColor" opacity="0.88"/>'
        '</svg>'
    )
    render_html(f"""
    <div class="sec-wrap">
      <div class="sec-divider">
        <span class="sec-line"></span>
        <span class="sec-ornament">{droplet_svg}</span>
        <span class="sec-line"></span>
      </div>
      <div class="eyebrow" style="margin-top:0.65rem;">{html.escape(kicker)}</div>
      <h3 class="sec-title">{html.escape(title)}</h3>
      {sub_html}
    </div>
    """)

# ------------------------------------------------------------------------------
# DOMAIN DATA: CLINICAL AGE COHORTS, VESSELS & COMPANION MASCOTS
# ------------------------------------------------------------------------------

AGE_GOALS = {
    "6–12 years (Kids)": {"goal": 1600, "cups": 6.4, "tier": "Children", "img": "cohorts/child.png", "fact": "Children turn over fluids rapidly due to high surface-to-mass ratios. Regular hydration prevents playground fatigue."},
    "13–18 years (Teens)": {"goal": 2000, "cups": 8.0, "tier": "Teens", "img": "cohorts/teen.png", "fact": "Rapid adolescent physical growth and athletic activity demand steady water intake for cognitive school focus."},
    "19–50 years (Adults)": {"goal": 2500, "cups": 10.0, "tier": "Adults", "img": "cohorts/adult.png", "fact": "Combats air-conditioned office screen fatigue. Mild 1-2% dehydration triggers tension headaches and brain fog."},
    "65+ years (Seniors)": {"goal": 1800, "cups": 7.2, "tier": "Seniors", "img": "cohorts/senior.png", "fact": "Age-related hypodipsia blunts natural thirst receptors. Scheduled routine sipping protects kidney and cardiovascular health."},
}

VESSELS = [
    {"id": "mug", "name": "Coffee Mug", "amount": 250, "desc": "Morning brew or herbal tea mug"},
    {"id": "glass", "name": "Water Glass", "amount": 250, "desc": "Dining table clear sparkling glass"},
    {"id": "tumbler", "name": "Travel Tumbler", "amount": 350, "desc": "Insulated desk & commute tumbler"},
    {"id": "bottle", "name": "Sports Bottle", "amount": 500, "desc": "Active workout squeeze bottle"},
    {"id": "flask", "name": "Hydro Flask", "amount": 750, "desc": "All-day brushed steel vacuum flask"},
]

def render_vessel_svg(v_id: str, size: int = 56, dark: bool = False) -> str:
    uri = load_asset_b64(f"vessels/{v_id}_3d.png")
    if uri:
        img_tag = f'<img src="{uri}" class="asset-3d" alt="{html.escape(v_id)}" style="width:{size}px; height:{size}px; object-fit:contain; display:block; filter:drop-shadow(0 5px 8px rgba(15,41,51,0.14));"/>'
        if dark:
            return f'<span style="display:inline-flex; align-items:center; justify-content:center; width:{size + 10}px; height:{size + 10}px; border-radius:14px; background:rgba(232,244,247,0.92); padding:4px; flex-shrink:0;">{img_tag}</span>'
        return f'<span style="display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;">{img_tag}</span>'
    shapes = {
        "mug": '<path d="M5 7h11v10a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V7zm11 2h2.5a2.5 2.5 0 0 1 0 5H16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "glass": '<path d="M6.5 4h11l-1.4 16H7.9L6.5 4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
        "tumbler": '<path d="M8 7h8l-1.1 13H9.1L8 7z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M12 7l2.2-4.5" stroke="currentColor" stroke-width="2"/>',
        "bottle": '<path d="M9.5 3h5v2.8l2 2.4V19a2 2 0 0 1-2 2h-5a2 2 0 0 1-2-2V8.2l2-2.4V3z" fill="none" stroke="currentColor" stroke-width="2"/>',
        "flask": '<rect x="7" y="6" width="10" height="15" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/>',
    }
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="display:inline-block; color:#1A7887;">{shapes.get(v_id, shapes["glass"])}</svg>'

def render_badge_svg(b_id: str, unlocked: bool) -> str:
    uri = load_asset_b64(f"badges/{b_id}.png" if unlocked else "badges/locked.png")
    if uri:
        return f'<img src="{uri}" class="asset-3d" alt="{html.escape(b_id)}" style="width:52px; height:52px; object-fit:contain; display:block; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.22));"/>'
    return '<svg width="36" height="36" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/></svg>'

COMPANIONS = {
    "HydroBuddy the Sea Turtle": "Wise ocean navigator, patient habit builder & calm companion.",
    "Bubbles the Playful Dolphin": "Agile, joyful swimmer celebrating fast logging and energetic hydration.",
    "Splash the River Otter": "Energetic river explorer who loves regular sips and steady flow.",
    "Misty the Friendly Raindrop": "Calm atmospheric spirit reminding you of cellular vitality.",
    "Pippin the Polar Penguin": "Crisp Antarctic friend who loves refreshing cold water drinks.",
}

HYDRATION_TIPS = [
    "Drink a full glass of room-temperature water right after waking up to activate your metabolism.",
    "Keep a reusable water bottle within arm's reach of your desk to eliminate screen-bound thirst inertia.",
    "Thirst is a delayed biological signal; sipping regularly keeps focus steady before fatigue sets in.",
    "Having a glass of water 20 minutes before meals aids digestion and supports nutrient absorption.",
    "Afternoon tiredness at 3:00 PM is frequently a mild hydration dip rather than lack of caffeine.",
    "Pair every cup of coffee or tea with an equal glass of pure water for steady balance.",
    "Sip steadily across the day rather than chugging massive volumes all at once for clean absorption.",
    "Proper hydration supports healthy thermoregulation, clear thinking, and steady athletic endurance.",
]

# ------------------------------------------------------------------------------
# UNIQUE COASTAL SPRING WATERFALL SVG HERO (Welcome Screen Artwork + Man & Turtle)
# ------------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def render_coastal_spring_svg(dark=False):
    """Coastal waterfall, alpine lagoon, lighthouse, reeds & hiker man with turtle companion."""
    sky_top = "#132229" if dark else "#FBFDF9"
    sky_bot = "#1B333D" if dark else "#DCF0F4"
    beam = "#264653" if dark else "#F8F0C4"
    ridge1 = "#23434E" if dark else "#C2E2E8"
    ridge2 = "#1B3742" if dark else "#88C3CE"
    ridge3 = "#152E38" if dark else "#4992A3"
    water = "#265D6D" if dark else "#7AC0CE"
    lake = "#1A4552" if dark else "#58A6B6"
    shore = "#12262C" if dark else "#2A606A"
    win_fill = "rgba(16, 27, 33, 0.62)" if dark else "rgba(255, 255, 255, 0.66)"
    win_stroke = "#355360" if dark else "#FFFFFF"
    win_kicker = "#63BAC9" if dark else "#1A7887"
    win_title = "#EAF4F7" if dark else "#0F2933"
    win_sub = "#AEC8CF" if dark else "#426169"

    svg_str = f"""
    <svg viewBox="0 0 1120 330" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="wb-sky" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="{sky_top}"/><stop offset="100%" stop-color="{sky_bot}"/>
        </linearGradient>
      </defs>
      <style>
        @keyframes ripple-flow {{ 0%, 100% {{ transform: translateX(0px); }} 50% {{ transform: translateX(12px); }} }}
        @keyframes fall-shimmer {{ 0%, 100% {{ opacity: 0.45; }} 50% {{ opacity: 0.85; }} }}
        .rp {{ animation: ripple-flow 5s ease-in-out infinite; }}
        .wf {{ animation: fall-shimmer 2.8s ease-in-out infinite; }}
      </style>

      <!-- Coastal Dawn Sky & Warm Rising Rays -->
      <rect width="1120" height="330" fill="url(#wb-sky)"/>
      <polygon points="880,0 1120,0 1120,210 560,330" fill="{beam}" opacity="0.4"/>
      <circle cx="998" cy="64" r="32" fill="#F2DC82" opacity="0.72"/>
      <path d="M 190 54 Q 196 48 202 54 Q 208 48 214 54 M 238 72 Q 243 67 248 72 Q 253 67 258 72" fill="none" stroke="#5D828C" stroke-width="1.6" stroke-linecap="round"/>

      <!-- Terraced Alpine Ridges -->
      <path d="M 0 198 Q 160 142 360 185 T 760 165 T 1120 192 L 1120 330 L 0 330 Z" fill="{ridge1}"/>
      <path d="M 0 222 Q 240 176 470 218 T 940 192 T 1120 212 L 1120 330 L 0 330 Z" fill="{ridge2}"/>
      <path d="M 0 248 Q 210 216 420 240 T 860 220 T 1120 246 L 1120 330 L 0 330 Z" fill="{ridge3}"/>

      <!-- Cascading Mountain Waterfall into Lagoon -->
      <path d="M 852 195 L 878 195 L 894 264 L 842 264 Z" fill="#BCE3EB" opacity="0.9"/>
      <g class="wf">
        <line x1="858" y1="198" x2="853" y2="259" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="870" y1="198" x2="876" y2="259" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
      </g>
      <ellipse cx="868" cy="264" rx="44" ry="8" fill="#E8F6F8" opacity="0.75"/>

      <!-- Crystal Oasis Lagoon & Ripples -->
      <path d="M 0 264 Q 380 250 760 256 T 1120 248 L 1120 330 L 0 330 Z" fill="{water}"/>
      <path d="M 140 278 Q 520 264 960 282 L 1120 286 L 1120 330 L 0 330 L 0 284 Z" fill="{lake}"/>
      <g class="rp" opacity="0.55">
        <line x1="250" y1="286" x2="340" y2="286" stroke="#DCF2F5" stroke-width="2" stroke-linecap="round"/>
        <line x1="590" y1="292" x2="710" y2="292" stroke="#DCF2F5" stroke-width="2" stroke-linecap="round"/>
        <line x1="825" y1="274" x2="905" y2="274" stroke="#DCF2F5" stroke-width="2" stroke-linecap="round"/>
      </g>

      <!-- Coastal White & Coral Lighthouse Unobstructed on Left Headland -->
      <g transform="translate(26, 174)">
        <polygon points="10,72 16,18 28,18 34,72" fill="#FFFDF8" stroke="#1E4D59" stroke-width="1.4"/>
        <polygon points="13,44 31,44 33,56 11,56" fill="#C8604E"/>
        <rect x="15" y="10" width="14" height="8" rx="1.5" fill="#1F3E47"/>
        <rect x="17" y="11" width="10" height="6" fill="#F4D371"/>
        <polygon points="13,10 22,2 31,10" fill="#C8604E"/>
      </g>

      <!-- Foreground Lagoon Stone Banks & Shoreline Reeds -->
      <path d="M 0 296 Q 280 280 460 306 L 460 330 L 0 330 Z" fill="{shore}"/>
      <path d="M 760 304 Q 950 284 1120 292 L 1120 330 L 760 330 Z" fill="{shore}"/>
      <g stroke="#214E4E" stroke-width="2.4" stroke-linecap="round">
        <line x1="948" y1="312" x2="942" y2="256"/><line x1="960" y1="314" x2="964" y2="262"/>
        <line x1="974" y1="316" x2="982" y2="268"/><line x1="120" y1="314" x2="115" y2="274"/>
      </g>
      <ellipse cx="942" cy="264" rx="3" ry="8" fill="#7D5333"/><ellipse cx="980" cy="274" rx="3" ry="7" fill="#7D5333"/>

      <!-- Hydrated Trail Walker Man with Hydro Flask + HydroBuddy Sea Turtle -->
      <g transform="translate(345, 224)">
        <ellipse cx="22" cy="70" rx="18" ry="4.5" fill="#0F2933" opacity="0.28"/>
        <line x1="17" y1="45" x2="12" y2="68" stroke="#1F3E48" stroke-width="5" stroke-linecap="round"/>
        <line x1="25" y1="45" x2="31" y2="68" stroke="#28505C" stroke-width="5" stroke-linecap="round"/>
        <path d="M 10 22 Q 21 17 32 22 L 34 48 L 10 48 Z" fill="#1A7887"/>
        <circle cx="21" cy="11" r="7.5" fill="#E8B892"/>
        <path d="M 14 9 Q 21 1 28 9 Z" fill="#2A2623"/>
        <line x1="28" y1="25" x2="36" y2="36" stroke="#1A7887" stroke-width="4" stroke-linecap="round"/>
        <!-- Reusable Insulated Teal Water Bottle in Hand -->
        <rect x="33" y="32" width="8" height="16" rx="2.5" fill="#BFE7EE" stroke="#135D69" stroke-width="1.3"/>
        <rect x="35" y="29" width="4" height="3" fill="#0F2933"/>
        <!-- Sea Turtle Companion -->
        <g transform="translate(50, 50)">
          <ellipse cx="14" cy="20" rx="14" ry="3.5" fill="#0F2933" opacity="0.24"/>
          <ellipse cx="6" cy="18" rx="3" ry="4" fill="#4E96A3"/><ellipse cx="21" cy="18" rx="3" ry="4" fill="#4E96A3"/>
          <path d="M 2 15 Q 14 0 26 15 Z" fill="#1F6673" stroke="#0F2933" stroke-width="1.4"/>
          <ellipse cx="14" cy="15" rx="12" ry="3.5" fill="#DFC378"/>
          <circle cx="29" cy="12" r="5" fill="#5FAAB8" stroke="#0F2933" stroke-width="1.3"/>
          <circle cx="31" cy="11" r="1.2" fill="#0F2933"/>
        </g>
      </g>

      <!-- Editorial Frosted Glass Showcase Banner -->
      <rect x="98" y="20" width="924" height="184" rx="18" fill="{win_fill}" stroke="{win_stroke}" stroke-width="1.6"/>
      <text x="560" y="60" text-anchor="middle" fill="{win_kicker}" font-size="13" font-weight="800" letter-spacing="1.4" font-family="sans-serif">DAILY HYDRATION COMPANION • WATERBUDDY</text>
      <text x="560" y="102" text-anchor="middle" fill="{win_title}" font-size="34" font-weight="900" font-family="sans-serif">Turning Simple Sips into</text>
      <text x="560" y="142" text-anchor="middle" fill="{win_title}" font-size="34" font-weight="900" font-family="sans-serif">Vibrant Daily Clarity</text>
      <text x="560" y="176" text-anchor="middle" fill="{win_sub}" font-size="15" font-weight="600" font-family="sans-serif">WHO &amp; EFSA calibrated daily water goals, tactile vessel logging, and serene hydro companion milestones.</text>
    </svg>
    """.strip()
    b64 = base64.b64encode(svg_str.encode("utf-8")).decode("ascii")
    return f'<img src="data:image/svg+xml;base64,{b64}" alt="WaterBuddy Coastal Spring Oasis" style="width:100%; height:auto; display:block; border-radius:22px; border:1px solid rgba(26,120,135,0.14); box-shadow:0 12px 36px rgba(15,41,51,0.07);"/>'

# ------------------------------------------------------------------------------
# CLOUD-SAFE PURE PYTHON HEADLESS TURTLE ENGINE (Drives Vector Mascot & Vault)
# ------------------------------------------------------------------------------

class HeadlessTurtle:
    """Pure Python Turtle geometry engine rendering Pillow PNGs and SVG vector paths."""
    def __init__(self, w=280, h=280):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)
        self.x, self.y, self.heading = w / 2, h / 2, 90
        self.down, self.color, self.width = True, (26, 120, 135, 255), 3
        self.svg_paths = []
        self._cur_pts = []

    def _flush_svg_stroke(self):
        if len(self._cur_pts) >= 2:
            d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in self._cur_pts)
            r, g, b, a = self.color
            op = round(a / 255.0, 2)
            self.svg_paths.append(
                f'<path d="{d}" fill="none" stroke="rgb({r},{g},{b})" stroke-opacity="{op}" '
                f'stroke-width="{self.width}" stroke-linecap="round" stroke-linejoin="round"/>'
            )
        self._cur_pts = []

    def forward(self, d):
        rad = math.radians(self.heading)
        nx, ny = self.x + d * math.cos(rad), self.y - d * math.sin(rad)
        if self.down:
            self.draw.line([(self.x, self.y), (nx, ny)], fill=self.color, width=self.width)
            if not self._cur_pts:
                self._cur_pts.append((self.x, self.y))
            self._cur_pts.append((nx, ny))
        self.x, self.y = nx, ny

    def left(self, a): self.heading = (self.heading + a) % 360
    def right(self, a): self.heading = (self.heading - a) % 360

    def penup(self):
        self._flush_svg_stroke()
        self.down = False

    def pendown(self):
        self.down = True
        self._cur_pts = [(self.x, self.y)]

    def goto(self, x, y):
        if self.down:
            self.draw.line([(self.x, self.y), (x, y)], fill=self.color, width=self.width)
            if not self._cur_pts:
                self._cur_pts.append((self.x, self.y))
            self._cur_pts.append((x, y))
        else:
            self._flush_svg_stroke()
        self.x, self.y = x, y

    def arc(self, r, ext, steps=14):
        sl = (2 * math.pi * r * (abs(ext) / 360.0)) / steps
        for _ in range(steps):
            self.forward(sl)
            self.left(ext / steps)

    def trace_oval_svg_pts(self, cx, cy, rx, ry, rot_deg=0, steps=28):
        """Uses turtle polar heading stepping to generate rotated oval polygon points."""
        rad_rot = math.radians(rot_deg)
        ca, sa = math.cos(rad_rot), math.sin(rad_rot)
        pts = []
        for i in range(steps):
            ang = math.radians((i / float(steps)) * 360.0)
            lx, ly = rx * math.cos(ang), ry * math.sin(ang)
            px = cx + lx * ca - ly * sa
            py = cy + lx * sa + ly * ca
            pts.append(f"{px:.1f},{py:.1f}")
        return " ".join(pts)

    def trace_star_svg_pts(self, cx, cy, r_outer, r_inner, points=5):
        """Uses turtle heading rotation to trace a crisp geometric star polygon."""
        pts = []
        self.heading = 90
        step_deg = 180.0 / points
        for k in range(points * 2):
            r = r_outer if k % 2 == 0 else r_inner
            rad = math.radians(self.heading)
            pts.append(f"{cx + r * math.cos(rad):.1f},{cy - r * math.sin(rad):.1f}")
            self.right(step_deg)
        return " ".join(pts)

    def trace_turtle_shell_scutes(self, cx, cy, hex_rx=23, hex_ry=20, outer_rx=44, outer_ry=38):
        """Moves the Python turtle across the carapace to trace the center hexagon & 6 scute ribs."""
        hex_pts = []
        self.color = (16, 74, 84, 185)
        self.width = 2
        for k in range(6):
            ang = math.radians(k * 60 + 30)
            hx, hy = cx + hex_rx * math.cos(ang), cy + hex_ry * math.sin(ang)
            ox, oy = cx + outer_rx * math.cos(ang), cy + outer_ry * math.sin(ang)
            hex_pts.append(f"{hx:.1f},{hy:.1f}")
            self.penup()
            self.goto(hx, hy)
            self.pendown()
            self.goto(ox, oy)
        self.penup()
        ribs_svg = "\n".join(self.svg_paths)
        return " ".join(hex_pts), ribs_svg


# ------------------------------------------------------------------------------
# 3D PHOTOREALISTIC ANIMATED WATER BOTTLE & 5 ANIMATED MASCOTS (6 SITUATIONS)
# ------------------------------------------------------------------------------

MOOD_META = {
    "start":     ("Morning Calm",         "0% — First Sip Awaits"),
    "attentive": ("Attentive Sip",        "1–49% — Initial Spark"),
    "happy":     ("Halfway Happy",        "50–74% — Steady Stride"),
    "energized": ("Homestretch Cheer",    "75–99% — Almost There"),
    "ecstatic":  ("Goal Triumph",         "100–124% — Target Met"),
    "paced":     ("Mindful Surplus",      "125–149% — Ease Pace"),
    "caution":   ("Over-Hydration Alert", ">=150% / >4.5L — Pause"),
}

def render_animated_bottle_svg(progress_pct, total_ml, goal_ml, width=192, height=276, dark=False):
    """3D cylindrical glass bottle with dual counter waves, 3D meniscus, bubbles, etched scale & reflections."""
    display_pct = max(0.0, float(progress_pct))
    fill_pct = min(100.0, display_pct)
    bottom_y = 272.0
    top_y = 74.0
    chamber_h = bottom_y - top_y
    fill_h = (fill_pct / 100.0) * chamber_h
    water_y = bottom_y - fill_h
    is_over_caution = (total_ml > 4500 or display_pct >= 150.0)
    is_surplus = (display_pct >= 125.0 and not is_over_caution)
    is_goal_hit = (display_pct >= 100.0 and not is_over_caution)

    bid = f"wb3_{width}_{int(display_pct * 10)}_{1 if dark else 0}"
    glass_stroke = "#5CC3D2" if dark else "#1A7887"
    glass_inner = "rgba(180, 236, 245, 0.28)" if dark else "rgba(255, 255, 255, 0.72)"
    glass_bg_l = "rgba(38, 86, 102, 0.34)" if dark else "rgba(218, 243, 248, 0.56)"
    glass_bg_m = "rgba(19, 43, 54, 0.14)" if dark else "rgba(255, 255, 255, 0.36)"
    glass_bg_r = "rgba(26, 78, 92, 0.38)" if dark else "rgba(176, 224, 234, 0.48)"
    tick_off = "#6A949E" if dark else "#5A848E"
    tick_on = "#B6F3FA" if dark else "#FFFFFF"
    aura_col = "#D69838" if (is_goal_hit or is_over_caution) else "#38B6C7"
    aura_op = "0.26" if is_goal_hit else ("0.20" if fill_pct >= 50 else "0.10")

    if is_over_caution:
        w_top, w_mid, w_bot, men_col = "#E7B45E", "#C88424", "#8A5310", "#F8DAA0"
        wave_b, wave_f = "#A66A1A", "#E6AF4C"
    elif is_surplus:
        w_top, w_mid, w_bot, men_col = "#7CE3D8", "#2B9A93", "#135D5B", "#CCF8F2"
        wave_b, wave_f = "#1C7672", "#65CFC4"
    elif is_goal_hit:
        w_top, w_mid, w_bot, men_col = "#84EEFA", "#239EB1", "#0D5D6B", "#D8FAFF"
        wave_b, wave_f = "#147A8C", "#6BE5F3"
    else:
        w_top, w_mid, w_bot, men_col = "#73E3F0", "#2297AA", "#0F5A67", "#BAEFF6"
        wave_b, wave_f = "#157485", "#5AD2E2"

    # Outer cylindrical glass contour centered at x=110 (viewBox 0 0 220 322)
    outer_path = (
        "M 84 48 L 136 48 "
        "C 138 60, 158 70, 168 88 "
        "L 168 258 C 168 274, 154 282, 132 282 "
        "L 88 282 C 66 282, 52 274, 52 258 "
        "L 52 88 C 62 70, 82 60, 84 48 Z"
    )
    inner_clip_path = (
        "M 87 52 L 133 52 "
        "C 135 63, 153 73, 163 90 "
        "L 163 257 C 163 270, 150 276, 130 276 "
        "L 90 276 C 70 276, 57 270, 57 257 "
        "L 57 90 C 67 73, 85 63, 87 52 Z"
    )

    water_layer = ""
    if fill_pct > 0:
        w_top_clamp = max(56.0, water_y)
        men_rx = 52.5 if w_top_clamp >= 92 else max(24.0, 52.5 * (0.45 + 0.55 * ((w_top_clamp - 52.0) / 40.0)))
        bubbles_svg = ""
        if fill_h > 22:
            b_y1 = min(264.0, w_top_clamp + fill_h * 0.72)
            b_y2 = min(266.0, w_top_clamp + fill_h * 0.85)
            b_y3 = min(260.0, w_top_clamp + fill_h * 0.56)
            b_y4 = min(268.0, w_top_clamp + fill_h * 0.90)
            bubbles_svg = (
                f'<circle class="wb-b1" cx="76" cy="{b_y1:.1f}" r="3.4" fill="#FFFFFF" opacity="0.65"/>'
                f'<circle class="wb-b2" cx="142" cy="{b_y2:.1f}" r="2.6" fill="#E3FBFF" opacity="0.72"/>'
                f'<circle class="wb-b3" cx="98" cy="{b_y3:.1f}" r="2.1" fill="#FFFFFF" opacity="0.58"/>'
                f'<circle class="wb-b4" cx="126" cy="{b_y4:.1f}" r="4.0" fill="#D5FAFF" opacity="0.52"/>'
                f'<circle class="wb-b5" cx="112" cy="{b_y2:.1f}" r="1.8" fill="#FFFFFF" opacity="0.68"/>'
            )
        water_layer = (
            f'<g clip-path="url(#{bid}_clip)">'
            f'<rect x="46" y="{w_top_clamp + 3.0:.1f}" width="128" height="{max(16.0, 286.0 - w_top_clamp):.1f}" fill="url(#{bid}_liq)"/>'
            f'<path class="wb-wb" d="M -30 {w_top_clamp:.1f} Q 15 {w_top_clamp - 5.5:.1f} 60 {w_top_clamp:.1f} T 150 {w_top_clamp:.1f} T 240 {w_top_clamp:.1f} T 330 {w_top_clamp:.1f} L 330 290 L -30 290 Z" fill="{wave_b}" opacity="0.55"/>'
            f'<path class="wb-wf" d="M -30 {w_top_clamp + 0.5:.1f} Q 20 {w_top_clamp - 4:.1f} 70 {w_top_clamp + 0.5:.1f} T 170 {w_top_clamp + 0.5:.1f} T 270 {w_top_clamp + 0.5:.1f} L 270 290 L -30 290 Z" fill="{wave_f}" opacity="0.74"/>'
            f'<ellipse class="wb-men" cx="110" cy="{w_top_clamp:.1f}" rx="{men_rx:.1f}" ry="5.5" fill="{men_col}" opacity="0.82"/>'
            f'<ellipse class="wb-men" cx="110" cy="{w_top_clamp:.1f}" rx="{men_rx - 2:.1f}" ry="4.4" fill="none" stroke="#FFFFFF" stroke-width="1.3" opacity="0.62"/>'
            f'<rect x="46" y="{w_top_clamp:.1f}" width="128" height="{max(16.0, 286.0 - w_top_clamp):.1f}" fill="url(#{bid}_cyl)"/>'
            f'<ellipse cx="110" cy="268" rx="44" ry="8" fill="#A6F3FC" opacity="0.22"/>'
            f'{bubbles_svg}'
            f'</g>'
        )

    # Volumetric laser-etched graduation ticks at 25%, 50%, 75%, 100% (unobstructed outside-wall labels)
    ticks_svg = ""
    for pct_mark, y_mark, lbl_mark in [(100, 74, "100%"), (75, 123, "75%"), (50, 173, "50%"), (25, 223, "25%")]:
        hit = fill_pct >= pct_mark - 0.5
        t_col = tick_on if hit else tick_off
        lbl_col = ("#8FE6F2" if dark else "#1A7887") if hit else tick_off
        t_op = "0.95" if hit else "0.65"
        ticks_svg += (
            f'<line x1="156" y1="{y_mark}" x2="168" y2="{y_mark}" stroke="{t_col}" stroke-width="2.0" stroke-linecap="round" opacity="{t_op}"/>'
            f'<text x="172" y="{y_mark + 3}" text-anchor="start" fill="{lbl_col}" font-size="8.4" font-weight="700" font-family="sans-serif" opacity="{t_op}">{lbl_mark}</text>'
        )

    spark_svg = ""
    if is_goal_hit:
        spark_svg = (
            '<g class="wb-sp">'
            '<polygon points="44,64 46,70 52,72 46,74 44,80 42,74 36,72 42,70" fill="#E8B948" opacity="0.9"/>'
            '<polygon points="176,56 178,61 183,63 178,65 176,70 174,65 169,63 174,61" fill="#E8B948" opacity="0.88"/>'
            '</g>'
        )

    bot_caption = (
        "Caution: Over-Hydration Alert" if is_over_caution else
        ("Surplus Zone: Ease Pace" if is_surplus else
         ("Goal Reached: Hydrated" if is_goal_hit else "3D Fluid Hydration Chamber"))
    )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 322" width="{width}" height="{height}" style="display:block; margin:0 auto;">',
        '<defs>',
        f'<clipPath id="{bid}_clip"><path d="{inner_clip_path}"/></clipPath>',
        f'<radialGradient id="{bid}_aura" cx="50%" cy="54%" r="50%"><stop offset="0%" stop-color="{aura_col}" stop-opacity="{aura_op}"/><stop offset="100%" stop-color="{aura_col}" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="{bid}_glass" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{glass_bg_l}"/><stop offset="28%" stop-color="{glass_bg_m}"/><stop offset="72%" stop-color="{glass_bg_m}"/><stop offset="100%" stop-color="{glass_bg_r}"/></linearGradient>',
        f'<linearGradient id="{bid}_liq" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{w_top}"/><stop offset="48%" stop-color="{w_mid}"/><stop offset="100%" stop-color="{w_bot}"/></linearGradient>',
        f'<linearGradient id="{bid}_cyl" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#051E24" stop-opacity="0.30"/><stop offset="22%" stop-color="#FFFFFF" stop-opacity="0.22"/><stop offset="52%" stop-color="#FFFFFF" stop-opacity="0.0"/><stop offset="84%" stop-color="#082830" stop-opacity="0.06"/><stop offset="100%" stop-color="#04191F" stop-opacity="0.30"/></linearGradient>',
        f'<linearGradient id="{bid}_cap" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#0F4D58"/><stop offset="32%" stop-color="#48A6B5"/><stop offset="68%" stop-color="#1A7887"/><stop offset="100%" stop-color="#0B3B44"/></linearGradient>',
        f'<linearGradient id="{bid}_col" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#86BAC4"/><stop offset="35%" stop-color="#EAF7FA"/><stop offset="70%" stop-color="#AAD2DB"/><stop offset="100%" stop-color="#6A9AA4"/></linearGradient>',
        f'<linearGradient id="{bid}_sheen" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.68"/><stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.24"/><stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.48"/></linearGradient>',
        '</defs>',
        '<style>',
        '@keyframes wbW1 { 0%, 100% { transform: translateX(0px); } 50% { transform: translateX(-34px); } }',
        '@keyframes wbW2 { 0%, 100% { transform: translateX(-28px); } 50% { transform: translateX(8px); } }',
        '@keyframes wbMn { 0%, 100% { transform: scaleY(1); } 50% { transform: scaleY(1.25); } }',
        '@keyframes wbBb { 0% { transform: translate(0px, 0px); opacity: 0.78; } 50% { transform: translate(3px, -24px); opacity: 0.55; } 100% { transform: translate(-2px, -50px); opacity: 0; } }',
        '@keyframes wbSp { 0%, 100% { opacity: 0.45; transform: scale(0.94); } 50% { opacity: 1; transform: scale(1.08); } }',
        '.wb-wb { animation: wbW1 5.2s ease-in-out infinite; }',
        '.wb-wf { animation: wbW2 3.6s ease-in-out infinite; }',
        '.wb-men { transform-origin: 110px center; animation: wbMn 3.6s ease-in-out infinite; }',
        '.wb-b1 { animation: wbBb 2.9s ease-in infinite; }',
        '.wb-b2 { animation: wbBb 2.4s ease-in infinite 0.9s; }',
        '.wb-b3 { animation: wbBb 3.3s ease-in infinite 1.5s; }',
        '.wb-b4 { animation: wbBb 3.6s ease-in infinite 0.4s; }',
        '.wb-b5 { animation: wbBb 2.2s ease-in infinite 1.9s; }',
        '.wb-sp { animation: wbSp 2.4s ease-in-out infinite; transform-origin: 110px 68px; }',
        '</style>',
        f'<circle cx="110" cy="170" r="102" fill="url(#{bid}_aura)"/>',
        '<ellipse cx="110" cy="292" rx="58" ry="10" fill="rgba(10,32,40,0.22)"/>',
        f'<path d="{outer_path}" fill="url(#{bid}_glass)"/>',
        water_layer,
        '<path d="M 59 258 C 59 272, 72 278, 90 278 L 130 278 C 148 278, 161 272, 161 258 C 154 268, 140 271, 110 271 C 80 271, 66 268, 59 258 Z" fill="#FFFFFF" opacity="0.34"/>',
        f'<path d="M 63 92 L 63 252" stroke="url(#{bid}_sheen)" stroke-width="8" stroke-linecap="round" opacity="0.38"/>',
        '<path d="M 58 92 L 58 250" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" opacity="0.72"/>',
        '<path d="M 61 84 Q 72 64 85 52" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" opacity="0.62"/>',
        '<path d="M 162 96 L 162 246" stroke="#C7F4FA" stroke-width="1.5" stroke-linecap="round" opacity="0.46"/>',
        ticks_svg,
        f'<path d="{outer_path}" fill="none" stroke="{glass_stroke}" stroke-width="2.5"/>',
        f'<path d="{inner_clip_path}" fill="none" stroke="{glass_inner}" stroke-width="1.1"/>',
        f'<rect x="78" y="34" width="64" height="14" rx="4" fill="url(#{bid}_col)" stroke="{glass_stroke}" stroke-width="1.6"/>',
        '<line x1="80" y1="39" x2="140" y2="39" stroke="#FFFFFF" stroke-width="1.2" opacity="0.65"/>',
        '<line x1="80" y1="43" x2="140" y2="43" stroke="#165C68" stroke-width="1.1" opacity="0.45"/>',
        f'<rect x="81" y="10" width="58" height="24" rx="6" fill="url(#{bid}_cap)" stroke="{glass_stroke}" stroke-width="1.6"/>',
        '<ellipse cx="110" cy="12" rx="28" ry="3.5" fill="#6CC5D3" opacity="0.48"/>',
        '<line x1="91" y1="15" x2="91" y2="30" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity="0.45"/>',
        '<line x1="101" y1="15" x2="101" y2="30" stroke="#99E3EE" stroke-width="1.4" stroke-linecap="round" opacity="0.38"/>',
        '<line x1="119" y1="15" x2="119" y2="30" stroke="#083038" stroke-width="1.6" stroke-linecap="round" opacity="0.45"/>',
        '<line x1="129" y1="15" x2="129" y2="30" stroke="#083038" stroke-width="1.6" stroke-linecap="round" opacity="0.45"/>',
        spark_svg,
        f'<rect x="65" y="152" width="90" height="48" rx="14" fill="rgba(10,30,38,0.82)" stroke="{"rgba(232,185,72,0.75)" if is_goal_hit else "rgba(155,232,242,0.45)"}" stroke-width="1.4"/>',
        f'<text x="110" y="176" text-anchor="middle" fill="{"#F7D473" if is_goal_hit else "#FFFFFF"}" font-size="21" font-weight="900" font-family="sans-serif">{display_pct:.0f}%</text>',
        f'<text x="110" y="191" text-anchor="middle" fill="#CBEFF5" font-size="9.4" font-weight="700" font-family="sans-serif">{total_ml:,} / {goal_ml:,} ml</text>',
        f'<text x="110" y="311" text-anchor="middle" fill="{"#9EC1CB" if dark else "#4D6B73"}" font-size="10.2" font-weight="700" font-family="sans-serif">{bot_caption}</text>',
        '</svg>',
    ]
    return "".join(parts)


def _svg_face_expressions(hx, hy, eye_dx, mouth_dy, mood, uid, skin_dark="#0F2933", mouth_light="#FFFFFF", accent="#D69838", cheek_op="0.58", accessory_anchor_y=28, cup_offset=(54, 42)):
    """Unified crisp vector facial expression & prop generator across all 5 animated mascots."""
    elx, erx = hx - eye_dx, hx + eye_dx
    ey = hy - 2
    my = hy + mouth_dy
    if mood == "start":
        return (
            f'<path d="M {elx - 6} {ey} Q {elx} {ey + 5} {elx + 6} {ey}" fill="none" stroke="{skin_dark}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<path d="M {erx - 6} {ey} Q {erx} {ey + 5} {erx + 6} {ey}" fill="none" stroke="{skin_dark}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<path d="M {hx - 7} {my} Q {hx} {my + 5} {hx + 7} {my}" fill="none" stroke="{skin_dark}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<g class="m-fx"><circle cx="{hx + 28}" cy="{hy - 22}" r="4.5" fill="none" stroke="#85D7E4" stroke-width="1.6"/>'
            f'<circle cx="{hx + 34}" cy="{hy - 32}" r="2.8" fill="none" stroke="#85D7E4" stroke-width="1.3"/></g>'
        )
    if mood == "attentive":
        cx_off, cy_off = cup_offset
        return (
            f'<g class="m-bk">'
            f'<circle cx="{elx}" cy="{ey}" r="5.6" fill="{skin_dark}"/><circle cx="{elx - 1.8}" cy="{ey - 2}" r="2" fill="#FFF"/>'
            f'<circle cx="{erx}" cy="{ey}" r="5.6" fill="{skin_dark}"/><circle cx="{erx - 1.8}" cy="{ey - 2}" r="2" fill="#FFF"/>'
            f'</g>'
            f'<path d="M {hx - 7} {my} Q {hx} {my + 6} {hx + 7} {my}" fill="none" stroke="{skin_dark}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<g transform="translate({hx + cx_off}, {hy + cy_off}) rotate(-10)"><g class="m-cup">'
            f'<polygon points="-9,-11 9,-11 7,12 -7,12" fill="#E6F8FB" stroke="#1A7887" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<polygon points="-7.2,-1 7.2,-1 5.6,10.2 -5.6,10.2" fill="#3AB3C5"/>'
            f'<line x1="3" y1="-17" x2="-1" y2="5" stroke="#D69838" stroke-width="2" stroke-linecap="round"/>'
            f'</g></g>'
        )
    if mood == "happy":
        return (
            f'<g class="m-bk">'
            f'<circle cx="{elx}" cy="{ey}" r="5.5" fill="{skin_dark}"/><circle cx="{elx - 1.8}" cy="{ey - 2}" r="2.1" fill="#FFF"/>'
            f'<circle cx="{erx}" cy="{ey}" r="5.5" fill="{skin_dark}"/><circle cx="{erx - 1.8}" cy="{ey - 2}" r="2.1" fill="#FFF"/>'
            f'</g>'
            f'<ellipse cx="{elx - 5}" cy="{ey + 10}" rx="5.2" ry="3" fill="#F27289" opacity="{cheek_op}"/>'
            f'<ellipse cx="{erx + 5}" cy="{ey + 10}" rx="5.2" ry="3" fill="#F27289" opacity="{cheek_op}"/>'
            f'<path d="M {hx - 10} {my - 1} Q {hx} {my + 11} {hx + 10} {my - 1}" fill="none" stroke="{skin_dark}" stroke-width="2.8" stroke-linecap="round"/>'
            f'<g class="m-fx"><circle cx="{hx - 36}" cy="{hy - 18}" r="3.4" fill="#6CD5E4" opacity="0.85"/>'
            f'<circle cx="{hx + 38}" cy="{hy - 22}" r="2.6" fill="#6CD5E4" opacity="0.85"/></g>'
        )
    if mood == "energized":
        return (
            f'<path d="M {elx - 6} {ey - 8} Q {elx} {ey - 12} {elx + 5} {ey - 7}" fill="none" stroke="{skin_dark}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<path d="M {erx - 5} {ey - 7} Q {erx} {ey - 12} {erx + 6} {ey - 8}" fill="none" stroke="{skin_dark}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<circle cx="{elx}" cy="{ey}" r="6" fill="{skin_dark}"/><circle cx="{elx - 2}" cy="{ey - 2}" r="2.3" fill="#FFF"/><circle cx="{elx + 1.5}" cy="{ey + 1.5}" r="1.2" fill="#F4CF67"/>'
            f'<circle cx="{erx}" cy="{ey}" r="6" fill="{skin_dark}"/><circle cx="{erx - 2}" cy="{ey - 2}" r="2.3" fill="#FFF"/><circle cx="{erx + 1.5}" cy="{ey + 1.5}" r="1.2" fill="#F4CF67"/>'
            f'<ellipse cx="{elx - 5}" cy="{ey + 10}" rx="5.5" ry="3.2" fill="#F27289" opacity="{cheek_op}"/>'
            f'<ellipse cx="{erx + 5}" cy="{ey + 10}" rx="5.5" ry="3.2" fill="#F27289" opacity="{cheek_op}"/>'
            f'<path d="M {hx - 11} {my - 1} Q {hx} {my + 13} {hx + 11} {my - 1} Z" fill="#E26378" stroke="{skin_dark}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<g class="m-fx">'
            f'<polygon points="{hx - 42},{hy - 18} {hx - 39},{hy - 12} {hx - 33},{hy - 10} {hx - 39},{hy - 8} {hx - 42},{hy - 2} {hx - 45},{hy - 8} {hx - 51},{hy - 10} {hx - 45},{hy - 12}" fill="{accent}"/>'
            f'<polygon points="{hx + 42},{hy - 22} {hx + 44},{hy - 17} {hx + 49},{hy - 15} {hx + 44},{hy - 13} {hx + 42},{hy - 8} {hx + 40},{hy - 13} {hx + 35},{hy - 15} {hx + 40},{hy - 17}" fill="#5BC8D8"/>'
            f'</g>'
        )
    if mood == "paced":
        # Balanced serene eyes (^ ^ calm arches), gentle reassuring smile & warm golden leaf/balance aura
        return (
            f'<path d="M {elx - 6} {ey + 1} Q {elx} {ey - 5} {elx + 6} {ey + 1}" fill="none" stroke="{skin_dark}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<path d="M {erx - 6} {ey + 1} Q {erx} {ey - 5} {erx + 6} {ey + 1}" fill="none" stroke="{skin_dark}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<ellipse cx="{elx - 5}" cy="{ey + 9}" rx="4.5" ry="2.6" fill="#E8B948" opacity="0.48"/>'
            f'<ellipse cx="{erx + 5}" cy="{ey + 9}" rx="4.5" ry="2.6" fill="#E8B948" opacity="0.48"/>'
            f'<path d="M {hx - 8} {my} Q {hx} {my + 7} {hx + 8} {my}" fill="none" stroke="{skin_dark}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<g class="m-fx">'
            f'<circle cx="{hx + 34}" cy="{accessory_anchor_y + 4}" r="7.5" fill="#E8B948" opacity="0.9"/>'
            f'<line x1="{hx + 30}" y1="{accessory_anchor_y + 4}" x2="{hx + 38}" y2="{accessory_anchor_y + 4}" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>'
            f'</g>'
        )
    if mood == "caution":
        bx, by = hx + 34, accessory_anchor_y + 4
        return (
            f'<line x1="{elx - 6}" y1="{ey - 7}" x2="{elx + 5}" y2="{ey - 10}" stroke="{skin_dark}" stroke-width="2.3" stroke-linecap="round"/>'
            f'<line x1="{erx - 5}" y1="{ey - 10}" x2="{erx + 6}" y2="{ey - 7}" stroke="{skin_dark}" stroke-width="2.3" stroke-linecap="round"/>'
            f'<circle cx="{elx}" cy="{ey}" r="6" fill="#FFFFFF" stroke="{skin_dark}" stroke-width="2"/><circle cx="{elx}" cy="{ey}" r="2.5" fill="{skin_dark}"/>'
            f'<circle cx="{erx}" cy="{ey}" r="6" fill="#FFFFFF" stroke="{skin_dark}" stroke-width="2"/><circle cx="{erx}" cy="{ey}" r="2.5" fill="{skin_dark}"/>'
            f'<ellipse cx="{hx}" cy="{my + 4}" rx="5" ry="6.2" fill="{skin_dark}"/>'
            f'<g class="m-sw"><path d="M {erx + 12} {ey - 8} C {erx + 12} {ey - 8}, {erx + 17} {ey - 1}, {erx + 17} {ey + 3} A 5 5 0 1 1 {erx + 7} {ey + 3} C {erx + 7} {ey - 1}, {erx + 12} {ey - 8}, {erx + 12} {ey - 8} Z" fill="#5BC8D8" stroke="#135D69" stroke-width="1.3"/></g>'
            f'<g class="m-fx">'
            f'<polygon points="{bx},{by - 12} {bx + 11},{by + 7} {bx - 11},{by + 7}" fill="#E69B35" stroke="#8F560E" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<line x1="{bx}" y1="{by - 6}" x2="{bx}" y2="{by + 1}" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>'
            f'<circle cx="{bx}" cy="{by + 4.3}" r="1.2" fill="#FFFFFF"/>'
            f'</g>'
        )
    return (
        f'<g class="m-crown">'
        f'<polygon points="{hx - 14},{accessory_anchor_y + 2} {hx - 16},{accessory_anchor_y - 11} {hx - 7},{accessory_anchor_y - 4} {hx},{accessory_anchor_y - 14} {hx + 7},{accessory_anchor_y - 4} {hx + 16},{accessory_anchor_y - 11} {hx + 14},{accessory_anchor_y + 2}" fill="#E9B842" stroke="#9C6A12" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<circle cx="{hx}" cy="{accessory_anchor_y - 14}" r="2.2" fill="#FFF3C4"/>'
        f'</g>'
        f'<rect x="{elx - 10}" y="{ey - 6}" width="20" height="12" rx="4" fill="#13252C" stroke="{accent}" stroke-width="2"/>'
        f'<rect x="{erx - 10}" y="{ey - 6}" width="20" height="12" rx="4" fill="#13252C" stroke="{accent}" stroke-width="2"/>'
        f'<line x1="{elx + 10}" y1="{ey - 1}" x2="{erx - 10}" y2="{ey - 1}" stroke="{accent}" stroke-width="2.4"/>'
        f'<line x1="{elx - 6}" y1="{ey - 3}" x2="{elx - 1}" y2="{ey + 2}" stroke="#FFFFFF" stroke-width="1.5" opacity="0.55" stroke-linecap="round"/>'
        f'<line x1="{erx - 6}" y1="{ey - 3}" x2="{erx - 1}" y2="{ey + 2}" stroke="#FFFFFF" stroke-width="1.5" opacity="0.55" stroke-linecap="round"/>'
        f'<ellipse cx="{elx - 5}" cy="{ey + 11}" rx="5" ry="2.8" fill="#F27289" opacity="0.55"/>'
        f'<ellipse cx="{erx + 5}" cy="{ey + 11}" rx="5" ry="2.8" fill="#F27289" opacity="0.55"/>'
        f'<path d="M {hx - 11} {my - 1} Q {hx} {my + 13} {hx + 11} {my - 1} Z" fill="#D95D6E" stroke="{skin_dark}" stroke-width="2" stroke-linejoin="round"/>'
        f'<g class="m-fx">'
        f'<polygon points="{hx - 40},{hy - 18} {hx - 38},{hy - 12} {hx - 32},{hy - 10} {hx - 38},{hy - 8} {hx - 40},{hy - 2} {hx - 42},{hy - 8} {hx - 48},{hy - 10} {hx - 42},{hy - 12}" fill="#E9B842"/>'
        f'<polygon points="{hx + 40},{hy - 14} {hx + 42},{hy - 9} {hx + 47},{hy - 7} {hx + 42},{hy - 5} {hx + 40},{hy} {hx + 38},{hy - 5} {hx + 33},{hy - 7} {hx + 38},{hy - 9}" fill="#E9B842"/>'
        f'</g>'
    )


def render_animated_avatar_svg(companion_str, mood="start", width=135, height=135, uid="m"):
    """Renders all 5 animated companions across 7 reactive situations; HydroBuddy Turtle is driven by HeadlessTurtle."""
    c_lower = companion_str.lower()
    c_type = (
        "dolphin" if "dolphin" in c_lower else
        "otter" if "otter" in c_lower else
        "raindrop" if ("raindrop" in c_lower or "cloud" in c_lower or "misty" in c_lower) else
        "penguin" if "penguin" in c_lower else
        "turtle"
    )
    svg_id = f"{uid}_{c_type}_{mood}_{width}"

    body_cls = (
        "m-dance" if mood == "ecstatic" else
        "m-hop" if mood == "energized" else
        "m-bob" if mood in ("happy", "paced") else
        "m-tilt" if mood == "attentive" else
        "m-shiver" if mood == "caution" else
        "m-rest"
    )
    wave_l_cls = "m-cheer-l" if mood in ("energized", "ecstatic") else ("m-sway-l" if mood in ("happy", "paced") else "")
    wave_r_cls = "m-cheer-r" if mood in ("energized", "ecstatic") else ("m-wave-r" if mood in ("happy", "attentive", "paced") else "")

    aura_color = "#E69B35" if mood in ("caution", "paced") else ("#E9B842" if mood == "ecstatic" else "#3EB6C6")
    aura_opacity = "0.28" if mood in ("ecstatic", "caution") else ("0.22" if mood in ("happy", "energized", "paced") else "0.14")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="{width}" height="{height}" style="max-width:100%; height:auto; display:block; margin:0 auto;">',
        '<defs>',
        f'<radialGradient id="{svg_id}_aura" cx="50%" cy="52%" r="50%"><stop offset="0%" stop-color="{aura_color}" stop-opacity="{aura_opacity}"/><stop offset="100%" stop-color="{aura_color}" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="{svg_id}_sh" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#3798A6"/><stop offset="55%" stop-color="#1E6F7D"/><stop offset="100%" stop-color="#124B54"/></linearGradient>',
        f'<linearGradient id="{svg_id}_drop" x1="20%" y1="0%" x2="80%" y2="100%"><stop offset="0%" stop-color="#7EE2EE"/><stop offset="52%" stop-color="#2494A6"/><stop offset="100%" stop-color="#125C68"/></linearGradient>',
        '</defs>',
        '<style>',
        '@keyframes mRest { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-4px); } }',
        '@keyframes mTilt { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-5px) rotate(-2.5deg); } }',
        '@keyframes mBob { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-7px); } }',
        '@keyframes mHop { 0%, 100% { transform: translateY(0px) scale(1); } 45% { transform: translateY(-9px) scale(1.03); } }',
        '@keyframes mDance { 0%, 100% { transform: translateY(0px) rotate(-2deg); } 50% { transform: translateY(-10px) rotate(2deg); } }',
        '@keyframes mShv { 0%, 100% { transform: translate(0px, 0px); } 25% { transform: translate(-2px, 1px); } 75% { transform: translate(2px, -1px); } }',
        '@keyframes mWaveR { 0%, 100% { transform: rotate(0deg); } 50% { transform: rotate(-22deg); } }',
        '@keyframes mSwayL { 0%, 100% { transform: rotate(0deg); } 50% { transform: rotate(10deg); } }',
        '@keyframes mCheerL { 0%, 100% { transform: rotate(24deg); } 50% { transform: rotate(42deg); } }',
        '@keyframes mCheerR { 0%, 100% { transform: rotate(-24deg); } 50% { transform: rotate(-42deg); } }',
        '@keyframes mBlink { 0%, 88%, 100% { transform: scaleY(1); } 94% { transform: scaleY(0.1); } }',
        '@keyframes mFx { 0%, 100% { opacity: 0.55; transform: translateY(0px); } 50% { opacity: 1; transform: translateY(-4px); } }',
        '@keyframes mCrown { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-3px); } }',
        '@keyframes mSw { 0%, 100% { transform: translateY(0px); opacity: 0.9; } 50% { transform: translateY(5px); opacity: 0.45; } }',
        '.m-rest { animation: mRest 4.0s ease-in-out infinite; }',
        '.m-tilt { transform-origin: 100px 125px; animation: mTilt 3.2s ease-in-out infinite; }',
        '.m-bob { animation: mBob 2.2s ease-in-out infinite; }',
        '.m-hop { transform-origin: 100px 140px; animation: mHop 1.3s ease-in-out infinite; }',
        '.m-dance { transform-origin: 100px 140px; animation: mDance 1.05s ease-in-out infinite; }',
        '.m-shiver { animation: mShv 0.24s infinite; }',
        '.m-wave-r { transform-origin: 142px 104px; animation: mWaveR 1.35s ease-in-out infinite; }',
        '.m-sway-l { transform-origin: 58px 104px; animation: mSwayL 2.2s ease-in-out infinite; }',
        '.m-cheer-l { transform-origin: 58px 104px; animation: mCheerL 0.85s ease-in-out infinite; }',
        '.m-cheer-r { transform-origin: 142px 104px; animation: mCheerR 0.85s ease-in-out infinite; }',
        '.m-bk { transform-box: fill-box; transform-origin: center; animation: mBlink 4.2s infinite; }',
        '.m-fx { animation: mFx 2.2s ease-in-out infinite; }',
        '.m-crown { animation: mCrown 1.8s ease-in-out infinite; }',
        '.m-sw { animation: mSw 1.5s ease-in-out infinite; }',
        '.m-cup { transform-box: fill-box; transform-origin: center; animation: mRest 2.2s ease-in-out infinite; }',
        '</style>',
        f'<circle cx="100" cy="102" r="92" fill="url(#{svg_id}_aura)"/>',
        '<ellipse cx="100" cy="176" rx="46" ry="8" fill="rgba(15,41,51,0.12)"/>',
        f'<g class="{body_cls}">',
    ]

    if c_type == "turtle":
        # Pure Python Turtle geometry engine computes flippers, layered shell rings & hexagonal scutes!
        t = HeadlessTurtle(200, 200)
        hl_pts = t.trace_oval_svg_pts(64, 152, 13, 19, rot_deg=-24)
        hr_pts = t.trace_oval_svg_pts(136, 152, 13, 19, rot_deg=24)
        fl_pts = t.trace_oval_svg_pts(48, 102, 15, 26, rot_deg=-34)
        fr_pts = t.trace_oval_svg_pts(152, 102, 15, 26, rot_deg=34)
        sh_outer = t.trace_oval_svg_pts(100, 124, 52, 46)
        sh_mid = t.trace_oval_svg_pts(100, 124, 41, 35)
        hex_pts, ribs_svg = t.trace_turtle_shell_scutes(100, 124, hex_rx=22, hex_ry=18, outer_rx=43, outer_ry=36)
        head_pts = t.trace_oval_svg_pts(100, 59, 26, 23)
        shell_stroke = "#E9B842" if mood == "ecstatic" else "#165C66"

        parts += [
            # Hind flippers & tail
            f'<polygon points="{hl_pts}" fill="#2E8B98" stroke="#134C54" stroke-width="2" stroke-linejoin="round"/>',
            f'<polygon points="{hr_pts}" fill="#2E8B98" stroke="#134C54" stroke-width="2" stroke-linejoin="round"/>',
            '<polygon points="94,164 106,164 100,179" fill="#2E8B98" stroke="#134C54" stroke-width="1.8" stroke-linejoin="round"/>',
            # Articulated waving front flippers
            f'<g class="{wave_l_cls}"><polygon points="{fl_pts}" fill="#4FB3C2" stroke="#134C54" stroke-width="2" stroke-linejoin="round"/></g>',
            f'<g class="{wave_r_cls}"><polygon points="{fr_pts}" fill="#4FB3C2" stroke="#134C54" stroke-width="2" stroke-linejoin="round"/></g>',
            # Layered carapace shell with Python Turtle scute hexagon & ribs
            f'<polygon points="{sh_outer}" fill="url(#{svg_id}_sh)" stroke="#11444D" stroke-width="2.8" stroke-linejoin="round"/>',
            f'<polygon points="{sh_mid}" fill="#2D8B99" stroke="#165C66" stroke-width="1.8" stroke-linejoin="round"/>',
            ribs_svg,
            f'<polygon points="{hex_pts}" fill="#76C5D1" stroke="{shell_stroke}" stroke-width="2.2" stroke-linejoin="round"/>',
            '<path d="M 68 96 Q 82 86 104 86" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" opacity="0.42"/>',
            # Head & facial expression overlay
            f'<polygon points="{head_pts}" fill="#74BEC9" stroke="#134C54" stroke-width="2.2" stroke-linejoin="round"/>',
            _svg_face_expressions(100, 59, 12, 9, mood, svg_id, skin_dark="#0F2933", accessory_anchor_y=30, cup_offset=(62, 46)),
        ]

    elif c_type == "dolphin":
        parts += [
            # Curved ocean wave splash beneath dolphin
            '<path d="M 38 158 Q 70 144 100 156 T 162 152 Q 130 172 100 168 T 38 158 Z" fill="#9CE1EC" opacity="0.58"/>',
            # Swept tail fluke peeking cleanly on right side
            f'<g class="{wave_l_cls}" style="transform-origin:144px 134px;"><path d="M 134 128 Q 162 124 174 108 Q 168 130 152 138 Q 168 148 164 162 Q 148 148 134 140 Z" fill="#1A7887" stroke="#114F59" stroke-width="2.2" stroke-linejoin="round"/></g>',
            # Sleek swept ocean dorsal fin
            '<path d="M 92 56 Q 108 22 128 36 Q 118 49 114 60 Z" fill="#1A7887" stroke="#114F59" stroke-width="2.2" stroke-linejoin="round"/>',
            # Left pectoral fin + right waving pectoral fin
            f'<g class="{wave_l_cls}"><ellipse cx="52" cy="116" rx="18" ry="9" fill="#46A6B6" stroke="#114F59" stroke-width="2" transform="rotate(-28 52 116)"/></g>',
            f'<g class="{wave_r_cls}"><ellipse cx="148" cy="116" rx="18" ry="9" fill="#46A6B6" stroke="#114F59" stroke-width="2" transform="rotate(28 148 116)"/></g>',
            # Smooth dolphin forehead & torso dome
            f'<ellipse cx="100" cy="108" rx="46" ry="50" fill="url(#{svg_id}_sh)" stroke="#114F59" stroke-width="2.5"/>',
            # Soft pearl-aqua belly & face highlight patch + gentle rostrum smile ridge
            '<path d="M 65 98 C 65 72, 135 72, 135 98 C 135 138, 122 154, 100 154 C 78 154, 65 138, 65 98 Z" fill="#E3F4F7" opacity="0.92"/>',
            '<path d="M 88 92 Q 100 87 112 92" fill="none" stroke="#6AC0CE" stroke-width="2" stroke-linecap="round"/>',
            '<path d="M 70 72 Q 84 62 100 62" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" opacity="0.45"/>',
            _svg_face_expressions(100, 82, 15, 16, mood, svg_id, skin_dark="#0F2933", accessory_anchor_y=28, cup_offset=(62, 34)),
        ]

    elif c_type == "otter":
        parts += [
            # Tail + body + cream belly
            f'<g class="{wave_l_cls}" style="transform-origin:132px 150px;"><path d="M 130 146 Q 172 152 168 122 Q 152 126 132 138 Z" fill="#6F4423" stroke="#4D2F18" stroke-width="2.2"/></g>',
            '<ellipse cx="100" cy="128" rx="46" ry="44" fill="#86552F" stroke="#4D2F18" stroke-width="2.5"/>',
            '<ellipse cx="100" cy="133" rx="30" ry="31" fill="#FAF0D2"/>',
            '<ellipse cx="72" cy="166" rx="12" ry="7" fill="#5D371A" stroke="#4D2F18" stroke-width="1.8"/>',
            '<ellipse cx="128" cy="166" rx="12" ry="7" fill="#5D371A" stroke="#4D2F18" stroke-width="1.8"/>',
            # Animated front paws + aqua/gold gem held on tummy
            f'<g class="{wave_l_cls}"><ellipse cx="62" cy="116" rx="11" ry="18" fill="#86552F" stroke="#4D2F18" stroke-width="2" transform="rotate(22 62 116)"/></g>',
            f'<g class="{wave_r_cls}"><ellipse cx="138" cy="116" rx="11" ry="18" fill="#86552F" stroke="#4D2F18" stroke-width="2" transform="rotate(-22 138 116)"/></g>',
            f'<circle cx="100" cy="128" r="12" fill="{"#E9B842" if mood == "ecstatic" else "#4CB7C7"}" stroke="{"#9C6A12" if mood == "ecstatic" else "#165C66"}" stroke-width="2"/>',
            '<ellipse cx="96" cy="124" rx="4" ry="2.5" fill="#FFFFFF" opacity="0.65"/>',
            # Ears + Head + cream muzzle + whiskers + button nose
            '<circle cx="67" cy="46" r="10" fill="#7D502D" stroke="#4D2F18" stroke-width="2"/><circle cx="67" cy="46" r="5" fill="#E8B8AF"/>',
            '<circle cx="133" cy="46" r="10" fill="#7D502D" stroke="#4D2F18" stroke-width="2"/><circle cx="133" cy="46" r="5" fill="#E8B8AF"/>',
            '<ellipse cx="100" cy="67" rx="36" ry="29" fill="#9A673F" stroke="#4D2F18" stroke-width="2.4"/>',
            '<ellipse cx="100" cy="75" rx="20" ry="13" fill="#FAF0D2"/>',
            '<polygon points="95,69 105,69 100,75" fill="#1F2933"/>',
            '<line x1="72" y1="73" x2="84" y2="75" stroke="#4D2F18" stroke-width="1.3"/><line x1="71" y1="79" x2="84" y2="79" stroke="#4D2F18" stroke-width="1.3"/>',
            '<line x1="128" y1="73" x2="116" y2="75" stroke="#4D2F18" stroke-width="1.3"/><line x1="129" y1="79" x2="116" y2="79" stroke="#4D2F18" stroke-width="1.3"/>',
            _svg_face_expressions(100, 58, 13, 18, mood, svg_id, skin_dark="#17242A", accessory_anchor_y=32, cup_offset=(58, 52)),
        ]

    elif c_type == "raindrop":
        parts += [
            # Animated droplet hands on left/right sides
            f'<g class="{wave_l_cls}"><ellipse cx="44" cy="128" rx="12" ry="7.5" fill="#5EC4D3" stroke="#135D69" stroke-width="1.8" transform="rotate(-24 44 128)"/></g>',
            f'<g class="{wave_r_cls}"><ellipse cx="156" cy="128" rx="12" ry="7.5" fill="#5EC4D3" stroke="#135D69" stroke-width="1.8" transform="rotate(24 156 128)"/></g>',
            # Plump 3D glossy teardrop contour
            f'<path d="M 100 24 C 100 24, 48 92, 48 134 C 48 164, 71 184, 100 184 C 129 184, 152 164, 152 134 C 152 92, 100 24, 100 24 Z" fill="url(#{svg_id}_drop)" stroke="#114C56" stroke-width="2.6"/>',
            '<path d="M 70 108 C 63 128, 69 156, 90 168 C 75 156, 70 132, 76 112 Z" fill="#E3F9FC" opacity="0.68"/>',
            '<ellipse cx="83" cy="86" rx="5" ry="12" fill="#FFFFFF" opacity="0.42" transform="rotate(18 83 86)"/>',
            _svg_face_expressions(100, 124, 13, 12, mood, svg_id, skin_dark="#0E2A33", accessory_anchor_y=21, cup_offset=(62, 6)),
        ]

    else:  # penguin
        parts += [
            # Webbed orange feet + animated flapping wings + torso
            '<ellipse cx="78" cy="170" rx="15" ry="7" fill="#E09A34" stroke="#9B6418" stroke-width="1.8"/><ellipse cx="122" cy="170" rx="15" ry="7" fill="#E09A34" stroke="#9B6418" stroke-width="1.8"/>',
            f'<g class="{wave_l_cls}"><ellipse cx="56" cy="118" rx="11" ry="28" fill="#182B36" stroke="#0C171E" stroke-width="2" transform="rotate(26 56 118)"/></g>',
            f'<g class="{wave_r_cls}"><ellipse cx="144" cy="118" rx="11" ry="28" fill="#182B36" stroke="#0C171E" stroke-width="2" transform="rotate(-26 144 118)"/></g>',
            '<ellipse cx="100" cy="126" rx="44" ry="50" fill="#182B36" stroke="#0C171E" stroke-width="2.4"/>',
            '<ellipse cx="100" cy="133" rx="30" ry="39" fill="#FFFFFF"/>',
            # Teal cozy scarf
            '<path d="M 68 88 Q 100 98 132 88 L 128 98 Q 100 107 72 98 Z" fill="#1A7887" stroke="#114F59" stroke-width="1.6"/>',
            '<polygon points="116,94 128,96 124,116 114,112" fill="#5EB3C2" stroke="#114F59" stroke-width="1.4"/>',
            # Snowy heart-contoured penguin face + golden beak
            '<circle cx="100" cy="62" r="32" fill="#182B36" stroke="#0C171E" stroke-width="2.2"/>',
            '<path d="M 74 58 C 74 44, 96 42, 100 54 C 104 42, 126 44, 126 58 C 126 74, 114 82, 100 82 C 86 82, 74 74, 74 58 Z" fill="#FFFFFF"/>',
            '<polygon points="94,65 106,65 100,74" fill="#E09A34" stroke="#9B6418" stroke-width="1.4" stroke-linejoin="round"/>',
            _svg_face_expressions(100, 58, 12, 19, mood, svg_id, skin_dark="#0F2933", accessory_anchor_y=28),
        ]

    parts.append('</g></svg>')
    return "".join(parts)


def draw_vector_art(art_type="drop"):
    t = HeadlessTurtle(280, 280)
    cx, cy = 140, 134

    if art_type == "preview":
        t.draw.ellipse([(cx - 88, cy - 88), (cx + 88, cy + 88)], fill=(214, 237, 241, 180), outline=(77, 163, 178, 170), width=2)
        t.draw.polygon([(cx, cy - 36), (cx + 22, cy + 4), (cx + 16, cy + 28), (cx, cy + 36), (cx - 16, cy + 28), (cx - 22, cy + 4)], fill=(77, 163, 178, 195), outline=(26, 120, 135, 210))
        return t.img

    if art_type in ("drop", "water"):
        t.draw.ellipse([(cx - 102, cy - 102), (cx + 102, cy + 102)], fill=(224, 242, 246, 245), outline=(26, 120, 135, 220), width=3)
        drop = [(cx + math.sin((s / 24.0) * math.pi) * 44, 54 + (s / 24.0) * 144) for s in range(25)]
        drop += [(cx - math.sin((s / 24.0) * math.pi) * 44, 54 + (s / 24.0) * 144) for s in range(24, -1, -1)]
        t.draw.polygon(drop, fill=(26, 120, 135, 245), outline=(15, 76, 86, 255))
        t.draw.ellipse([(cx + 12, cy - 18), (cx + 26, cy + 20)], fill=(214, 239, 244, 235))
        t.penup(); t.goto(cx, 182); t.heading = 270; t.color = (240, 250, 252, 220); t.width = 3; t.pendown(); t.arc(30, 90)

    elif art_type in ("leaf", "plant"):
        t.draw.ellipse([(cx - 102, cy - 102), (cx + 102, cy + 102)], fill=(230, 243, 236, 245), outline=(44, 130, 114, 220), width=3)
        t.penup(); t.goto(cx, 228); t.heading = 90; t.color = (44, 130, 114, 255); t.width = 5; t.pendown(); t.forward(44)
        leaf = [(cx + math.sin((s / 24.0) * math.pi) * 48, 190 - (s / 24.0) * 142) for s in range(25)]
        leaf += [(cx - math.sin((s / 24.0) * math.pi) * 48, 190 - (s / 24.0) * 142) for s in range(24, -1, -1)]
        t.draw.polygon(leaf, fill=(64, 152, 134, 240), outline=(28, 96, 84, 255))
        t.penup(); t.goto(cx, 190); t.heading = 90; t.width = 3; t.pendown(); t.forward(140)
        for yp in [162, 134, 106, 80]:
            t.penup(); t.goto(cx, yp); t.heading = 40; t.width = 2; t.pendown(); t.forward(28)
            t.penup(); t.goto(cx, yp); t.heading = 140; t.pendown(); t.forward(28)

    elif art_type == "traveler":
        t.draw.ellipse([(cx - 102, cy - 102), (cx + 102, cy + 102)], fill=(228, 244, 247, 245), outline=(26, 120, 135, 220), width=3)
        t.draw.pieslice([(cx - 98, cy + 18), (cx + 98, cy + 108)], 0, 180, fill=(136, 195, 206, 220))
        t.draw.ellipse([(cx + 22, cy - 70), (cx + 62, cy - 30)], fill=(242, 220, 130, 180))
        t.draw.line([(cx - 18, cy + 20), (cx - 28, cy + 62)], fill=(20, 48, 58, 255), width=7)
        t.draw.line([(cx - 6, cy + 20), (cx + 6, cy + 62)], fill=(31, 66, 78, 255), width=7)
        t.draw.polygon([(cx - 30, cy - 24), (cx + 4, cy - 24), (cx + 8, cy + 22), (cx - 32, cy + 22)], fill=(26, 120, 135, 255))
        t.draw.ellipse([(cx - 25, cy - 54), (cx - 1, cy - 30)], fill=(232, 184, 146, 255))
        t.draw.pieslice([(cx - 26, cy - 56), (cx, cy - 38)], 180, 360, fill=(42, 38, 35, 255))
        t.draw.rectangle([(cx + 6, cy - 4), (cx + 20, cy + 20)], fill=(191, 231, 238, 255), outline=(19, 93, 105, 255), width=2)
        t.draw.pieslice([(cx + 28, cy + 36), (cx + 70, cy + 72)], 180, 360, fill=(31, 102, 115, 255))
        t.draw.ellipse([(cx + 66, cy + 44), (cx + 80, cy + 58)], fill=(95, 170, 184, 255))

    else:
        cm = 114
        t.draw.polygon([(cx - 24, cm + 26), (cx - 52, cm + 136), (cx - 30, cm + 118), (cx - 10, cm + 128), (cx - 4, cm + 28)], fill=(26, 120, 135, 255))
        t.draw.polygon([(cx + 4, cm + 28), (cx + 10, cm + 128), (cx + 30, cm + 118), (cx + 52, cm + 136), (cx + 24, cm + 26)], fill=(19, 93, 105, 255))
        r_pts = [(cx + (64 if i % 2 == 0 else 54) * math.cos(i * math.pi / 32), cm + (64 if i % 2 == 0 else 54) * math.sin(i * math.pi / 32)) for i in range(64)]
        t.draw.polygon(r_pts, fill=(214, 152, 56, 255), outline=(235, 194, 96, 255))
        t.draw.ellipse([(cx - 50, cm - 50), (cx + 50, cm + 50)], fill=(228, 172, 72, 255), outline=(168, 110, 30, 255), width=2)
        t.draw.ellipse([(cx - 41, cm - 41), (cx + 41, cm + 41)], fill=(26, 120, 135, 255), outline=(191, 231, 238, 240), width=2)
        t.draw.ellipse([(cx - 29, cm - 29), (cx + 29, cm + 29)], fill=(250, 244, 212, 255), outline=(196, 136, 40, 255), width=2)
        sp = [(cx + (19 if k % 2 == 0 else 8) * math.cos(-math.pi / 2 + k * math.pi / 5), cm + (19 if k % 2 == 0 else 8) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
        t.draw.polygon(sp, fill=(200, 140, 40, 255), outline=(138, 86, 20, 255))

    return t.img

def image_to_png_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def image_to_data_uri(img):
    return "data:image/png;base64," + base64.b64encode(image_to_png_bytes(img)).decode("ascii")

# ------------------------------------------------------------------------------
# DOMAIN LOGIC, BADGES & LOGGING HELPERS
# ------------------------------------------------------------------------------

def calculate_progress(total_ml: int, goal_ml: int):
    goal = max(1, int(goal_ml))
    total = max(0, int(total_ml))
    remaining = max(0, goal - total)
    pct = round((total / goal) * 100.0, 1)
    bar_val = min(1.0, max(0.0, total / goal))
    return remaining, pct, bar_val

def get_user_hydration_rank(intake_history):
    c = len(intake_history)
    if c == 0: return "Seedling Sipper"
    if c <= 2: return "Morning Dew"
    if c <= 4: return "Flowing Stream"
    return "Ocean Master"

def get_collected_hydro_arts(intake_history, total_ml, goal_ml):
    earned = set()
    if len(intake_history) >= 1: earned.add("drop")
    if len(intake_history) >= 2: earned.add("traveler")
    pct = (total_ml / max(1, goal_ml)) * 100.0
    if pct >= 50: earned.add("leaf")
    if pct >= 100: earned.add("badge")
    return earned

def evaluate_badges(intake_history, total_intake, daily_goal, standard_goal):
    count = len(intake_history)
    return [
        {"id": "first_sip", "name": "First Sip", "desc": "Log your first water intake of the day", "unlocked": count >= 1, "progress": f"{min(count, 1)}/1 drink logged", "pct": 100 if count >= 1 else 0},
        {"id": "steady_pacer", "name": "Steady Pacer", "desc": "Build rhythm with 3+ logged drinks today", "unlocked": count >= 3, "progress": f"{min(count, 3)}/3 drinks logged", "pct": min(100, int((count / 3.0) * 100))},
        {"id": "halfway_hydrated", "name": "Halfway Hydrated", "desc": "Reach 50% of your daily water target", "unlocked": total_intake >= (daily_goal * 0.5), "progress": f"{total_intake}/{int(daily_goal * 0.5)} ml", "pct": min(100, int((total_intake / max(1, daily_goal * 0.5)) * 100))},
        {"id": "hydro_champion", "name": "Hydro Champion", "desc": "Achieve 100% of your daily hydration goal", "unlocked": total_intake >= daily_goal and daily_goal > 0, "progress": f"{total_intake}/{daily_goal} ml", "pct": min(100, int((total_intake / max(1, daily_goal)) * 100))},
        {"id": "calibration_master", "name": "Calibration Master", "desc": "Personalize your daily target from baseline", "unlocked": daily_goal != standard_goal, "progress": f"Target: {daily_goal} ml", "pct": 100 if daily_goal != standard_goal else 0},
    ]

def evaluate_mascot_mood(total_ml: int, pct: float) -> str:
    if total_ml > 4500 or pct >= 150.0:
        return "caution"
    if pct >= 125.0:
        return "paced"
    if pct >= 100.0:
        return "ecstatic"
    if pct >= 75.0:
        return "energized"
    if pct >= 50.0:
        return "happy"
    if total_ml > 0:
        return "attentive"
    return "start"

def get_coach_progress(total_ml: int, goal_ml: int, pct: float, accent_color: str):
    """Monotonic Hydration Journey progress for Companion Coach (never resets to 0% after reaching 100%)."""
    if total_ml <= 0:
        return "Stage 1/5 • Log your very first sip to awaken clarity", 0, accent_color
    if total_ml > 4500 or pct >= 150.0:
        return f"Over-Hydration Guard • {pct:.0f}% ({total_ml:,} ml — Pause fluids)", 100, "#D96B38"
    if pct >= 125.0:
        return f"Mindful Surplus • {pct:.0f}% of goal (Hydration tank full)", 100, "#D69838"
    if pct >= 100.0:
        return f"Stage 5/5 • Daily Target Complete ({total_ml:,} / {goal_ml:,} ml)", 100, accent_color
    if pct >= 75.0:
        return f"Stage 4/5 • Final Stretch ({max(0, goal_ml - total_ml):,} ml left)", int(pct), accent_color
    if pct >= 50.0:
        return f"Stage 3/5 • Halfway Cleared -> 75% Push ({total_ml:,}/{goal_ml:,} ml)", int(pct), accent_color
    half_ml = int(goal_ml * 0.5)
    return f"Stage 2/5 • Building Rhythm -> Halfway ({total_ml:,}/{half_ml:,} ml)", int(pct), accent_color

def get_mascot_speech(companion_str, user_name, total_ml, goal_ml, pct, mood, sip_count=0, last_action="init", last_desc=""):
    c_name = companion_str.split()[0]
    fn = user_name.strip() if user_name.strip() else "Friend"
    rem = max(0, goal_ml - total_ml)
    if mood == "caution":
        return f"Over-hydration caution, {fn}! {total_ml:,} ml ({pct:.0f}% of goal) pushes beyond safe balance — pause drinking for a while to protect electrolytes."
    if last_action == "undo":
        return f"Stepped back one entry cleanly, {fn}. Adjusted balance is {total_ml:,} ml ({pct:.0f}%)."
    if last_action == "goal_change":
        return f"Daily target calibrated to {goal_ml:,} ml, {fn}. Current progress recalibrated to {pct:.0f}%."
    if mood == "paced":
        return f"You're well ahead at {pct:.0f}% ({total_ml:,} ml), {fn}! Your body is fully hydrated right now — space out any extra sips gently."
    if mood == "ecstatic":
        return f"Goal conquered, {fn}! {total_ml:,} ml logged ({pct:.0f}%). {c_name} put on gold shades & crown — just light maintenance sips from here!"
    if mood == "energized":
        return f"Final push at {pct:.0f}% ({total_ml:,} ml), {fn}! Only {rem:,} ml (~{rem / 250:.1f} glasses) left — {c_name} is cheering both fins up!"
    if mood == "happy":
        return f"Halfway cleared at {pct:.0f}%, {fn}! Afternoon focus stays crisp when sipping steadily — {rem:,} ml remaining to reach your goal."
    if mood == "attentive":
        if sip_count == 1:
            note = f" ({last_desc})" if last_desc else ""
            return f"Awesome first sip{note}, {fn}! That initial {total_ml:,} ml kickstarts metabolism and alertness. Keep your bottle within arm's reach!"
        to_half = max(0, int(goal_ml * 0.5) - total_ml)
        return f"Steady momentum across {sip_count} sips ({total_ml:,} ml • {pct:.0f}%), {fn}! Only {to_half:,} ml more brings you to the halfway milestone."
    if last_action == "reset":
        return f"Fresh morning slate, {fn}! {c_name} is rested and ready whenever you take your first glass."
    return f"Good day, {fn}! I am {c_name}. Kick off with sip #1 below or click + Log Drink at the top to wake up your daily flow."

def analyze_hydration_timeline(intake_history, goal_ml: int):
    """Computes real timeline timestamps, inter-drink intervals, periods, and consistency metrics."""
    rows = []
    base_day = date.today()
    prev_dt = None
    gap_mins = []
    for idx, entry in enumerate(intake_history):
        t_str = entry.get("time", "12:00 PM")
        try:
            t_obj = datetime.strptime(t_str.strip(), "%I:%M %p").time()
        except Exception:
            t_obj = datetime.now().time()
        dt = datetime.combine(base_day, t_obj)
        if prev_dt is not None and dt <= prev_dt:
            plot_dt = prev_dt + timedelta(minutes=1)
        else:
            plot_dt = dt
        if prev_dt is None:
            gap_str, gap_h = "First Sip", 0.0
        else:
            diff_m = max(1.0, (plot_dt - prev_dt).total_seconds() / 60.0)
            gap_mins.append(diff_m)
            hrs, mins = int(diff_m // 60), int(diff_m % 60)
            gap_str = f"{hrs}h {mins}m" if hrs > 0 else f"{mins}m"
            gap_h = round(diff_m / 60.0, 2)
        prev_dt = plot_dt

        hr = dt.hour
        period = "Morning" if hr < 12 else ("Afternoon" if hr < 17 else "Evening")
        rows.append({
            "#": entry["id"],
            "Time": t_str,
            "Timestamp": plot_dt,
            "Vessel / Source": entry["vessel"],
            "Sip Interval": gap_str,
            "GapHours": gap_h,
            "Period": period,
            "Amount (ml)": int(entry["amount"]),
            "Running Total (ml)": int(entry["running_total"]),
        })

    df = pd.DataFrame(rows)
    if len(gap_mins) >= 1:
        avg_m = sum(gap_mins) / len(gap_mins)
        ah, am = int(avg_m // 60), int(avg_m % 60)
        avg_gap_str = f"Every {ah}h {am}m" if ah > 0 else f"Every {am}m"
        # Consistency score favors moderate intervals (30–210 min) with low variance
        mean_diff = sum(abs(g - avg_m) for g in gap_mins) / len(gap_mins)
        spread_pen = min(45, (mean_diff / max(30.0, avg_m)) * 45.0)
        cadence_bonus = 95 if 30 <= avg_m <= 210 else (82 if avg_m > 210 else 72)
        score = max(35, min(100, int(cadence_bonus - spread_pen)))
        rhythm_lbl = "Steady Rhythm" if score >= 80 else ("Moderate Gaps" if score >= 60 else "Clustered Sips")
    else:
        avg_gap_str = "Awaiting 2nd sip"
        score = 100 if len(rows) == 1 else 0
        rhythm_lbl = "Strong Start" if len(rows) == 1 else "No Drinks Yet"

    peak_row = df.loc[df["Amount (ml)"].idxmax()] if not df.empty else None
    peak_str = f"{int(peak_row['Amount (ml)'])} ml ({peak_row['Vessel / Source']})" if peak_row is not None else "—"
    return df, avg_gap_str, score, rhythm_lbl, peak_str

def log_drink(amount_ml: int, source_label: str, goal_ml: int, time_lbl: str = None, notify: bool = True):
    amt = int(amount_ml)
    st.session_state.total_intake += amt
    st.session_state.intake_history.append({
        "id": len(st.session_state.intake_history) + 1,
        "time": time_lbl or datetime.now().strftime("%I:%M %p"),
        "vessel": source_label,
        "amount": amt,
        "running_total": int(st.session_state.total_intake),
    })
    st.session_state.last_action = "log"
    st.session_state.last_drink_desc = f"+{amt} ml {source_label}"
    npct = (st.session_state.total_intake / max(1, goal_ml)) * 100.0
    if notify:
        if st.session_state.total_intake > 4500 or npct >= 150.0:
            st.session_state.pending_toast = (f"Logged +{amt} ml ({source_label}) — Caution: Over-hydration zone ({npct:.0f}%).", "⚠️")
        elif npct >= 125.0:
            st.session_state.pending_toast = (f"Logged +{amt} ml ({source_label}) — Ahead of goal ({npct:.0f}%), ease pace gently.", "💧")
        elif npct >= 100.0:
            st.session_state.pending_toast = (f"Goal Achieved! +{amt} ml ({source_label}) pushed you to {npct:.0f}%!", "🎉")
        else:
            st.session_state.pending_toast = (f"Logged +{amt} ml ({source_label}) • {npct:.0f}% of goal", "💧")
    if npct >= 100:
        st.session_state.recent_art = "badge"
        return True
    elif npct >= 50:
        st.session_state.recent_art = "leaf"
    else:
        st.session_state.recent_art = "drop"
    return False

# ------------------------------------------------------------------------------
# SESSION STATE INITIALIZATION (Zero External DB, 100% Local Memory)
# ------------------------------------------------------------------------------

if "dark_theme" not in st.session_state:
    st.session_state.dark_theme = st.query_params.get("theme") == "dark"
if "onboarded" not in st.session_state:
    st.session_state.onboarded = st.query_params.get("onboarded") in ["true", "1"]
if "user_name" not in st.session_state: st.session_state.user_name = "Parth Gajera"
if "user_avatar" not in st.session_state: st.session_state.user_avatar = list(COMPANIONS.keys())[0]
if "age_cohort" not in st.session_state: st.session_state.age_cohort = list(AGE_GOALS.keys())[2]
if "daily_goal" not in st.session_state: st.session_state.daily_goal = AGE_GOALS[st.session_state.age_cohort]["goal"]
if "recent_art" not in st.session_state: st.session_state.recent_art = None
if "mascot_mood" not in st.session_state: st.session_state.mascot_mood = "start"
if "last_action" not in st.session_state: st.session_state.last_action = "init"
if "last_drink_desc" not in st.session_state: st.session_state.last_drink_desc = ""
if "show_reset_confirm" not in st.session_state: st.session_state.show_reset_confirm = False
if "pending_toast" not in st.session_state: st.session_state.pending_toast = None
if "nav_view" not in st.session_state:
    qv = st.query_params.get("view")
    st.session_state.nav_view = "Wall of Badges" if qv == "badges" else ("Vessel Studio" if qv == "studio" else "Dashboard")

if "intake_history" not in st.session_state:
    st.session_state.intake_history = []
    st.session_state.total_intake = 0
    dm = st.query_params.get("demo")
    if dm in ["true", "1"]:
        for amt, lbl, tm in [(250, "Coffee Mug", "08:30 AM"), (350, "Travel Tumbler", "11:15 AM"), (500, "Sports Bottle", "02:40 PM")]:
            log_drink(amt, lbl, st.session_state.daily_goal, tm, notify=False)
    elif dm == "full":
        st.session_state.daily_goal = 2000
        for amt, lbl, tm in [(250, "Water Glass", "08:00 AM"), (350, "Travel Tumbler", "10:15 AM"), (500, "Sports Bottle", "01:30 PM"), (750, "Hydro Flask", "04:45 PM"), (250, "1.0 Cup", "07:20 PM")]:
            log_drink(amt, lbl, st.session_state.daily_goal, tm, notify=False)

# ------------------------------------------------------------------------------
# UNIFIED TOKENIZED CSS (Coastal Aqua Oasis Light Default + Deep Tide Dark Toggle)
# ------------------------------------------------------------------------------

is_dark = st.session_state.dark_theme
T = {
    "bg": "#101B21" if is_dark else "#F3F9FA",
    "side": "#15232B" if is_dark else "#E6F1F3",
    "surface": "#1A2B34" if is_dark else "#FFFFFF",
    "soft": "#20343E" if is_dark else "#E9F4F6",
    "ink": "#EAF4F7" if is_dark else "#0F2933",
    "muted": "#9DB7BF" if is_dark else "#4B6B73",
    "accent": "#4EA5B4" if is_dark else "#1A7887",
    "accent_hv": "#3D8D9B" if is_dark else "#135D69",
    "accent_soft": "#21434F" if is_dark else "#D6EDF1",
    "border": "rgba(180, 222, 230, 0.14)" if is_dark else "rgba(26, 120, 135, 0.12)",
    "shadow": "0 8px 28px rgba(0, 0, 0, 0.25)" if is_dark else "0 8px 28px rgba(15, 41, 51, 0.055)",
    "gold_bg": "rgba(214, 152, 56, 0.16)" if is_dark else "#FAF2D8",
    "gold_ink": "#F2CA6B" if is_dark else "#8A5E14",
    "alert_info_bg": "#19313A" if is_dark else "#E5F4F6",
    "alert_warn_bg": "#2E2615" if is_dark else "#FDF4E1",
    "alert_err_bg": "#361C20" if is_dark else "#FBECEB",
}

render_html(f"""
<style>
  :root {{
    --bg: {T['bg']}; --side: {T['side']}; --surface: {T['surface']}; --soft: {T['soft']};
    --ink: {T['ink']}; --muted: {T['muted']}; --accent: {T['accent']}; --accent-hv: {T['accent_hv']};
    --accent-soft: {T['accent_soft']}; --border: {T['border']}; --shadow: {T['shadow']};
  }}
  .stApp {{ background: var(--bg) !important; color: var(--ink) !important; }}
  [data-testid="stHeader"] {{ background: transparent !important; }}
  h1, h2, h3, h4, h5, p, span, label, [data-testid="stSidebar"] * {{ color: var(--ink) !important; }}
  [data-testid="stSidebar"] {{ background: var(--side) !important; border-right: 1px solid var(--border) !important; }}
  [data-testid="stSidebarCollapseButton"] button, [data-testid="collapsedControl"] button {{
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: 12px !important; color: var(--ink) !important; box-shadow: var(--shadow) !important;
  }}
  [data-testid="stBaseButton-primary"], button[kind="primary"] {{
    background: #1A7887 !important; border: none !important; border-radius: 99px !important;
    color: #FFFFFF !important; font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(26, 120, 135, 0.24) !important;
  }}
  [data-testid="stBaseButton-primary"]:hover, button[kind="primary"]:hover {{ background: #135D69 !important; }}
  [data-testid="stBaseButton-primary"] *, button[kind="primary"] * {{ color: #FFFFFF !important; }}

  [role="dialog"],
  div:has(> [role="dialog"]),
  [data-testid="stDialog"] [role="dialog"],
  [data-testid="stDialog"] [role="dialog"] > div,
  [data-testid="stModal"] [role="dialog"],
  [data-testid="stModal"] [role="dialog"] > div,
  div[data-baseweb="modal"] [role="dialog"] {{
    background: {T['surface']} !important; background-color: {T['surface']} !important;
    color: {T['ink']} !important; border: 1px solid {T['border']} !important; border-radius: 22px !important;
  }}
  [role="dialog"] *, div:has(> [role="dialog"]) *, [data-testid="stDialog"] *, [data-testid="stModal"] * {{ color: {T['ink']} !important; }}
  [role="dialog"] [data-testid="stBaseButton-primary"] *, [role="dialog"] button[kind="primary"] * {{ color: #FFFFFF !important; }}
  [role="dialog"] button[aria-label="Close"] svg,
  [data-testid="stDialog"] button[aria-label="Close"] svg,
  [data-testid="stModal"] button[aria-label="Close"] svg {{
    color: {T['ink']} !important; fill: currentColor !important;
  }}
  div[data-baseweb="popover"],
  div[data-baseweb="popover"] > div,
  div[data-baseweb="popover"] > div > div,
  [data-testid="stVirtualDropdown"],
  [data-testid="stVirtualDropdown"] > div,
  [data-testid="stSelectboxVirtualDropdown"],
  [data-testid="stSelectboxVirtualDropdown"] > div,
  [data-testid="stSelectboxVirtualDropdown"] [role="listbox"],
  div[data-baseweb="menu"],
  ul[data-baseweb="menu"],
  [role="listbox"],
  [role="listbox"] > div,
  [role="option"] {{
    background: {T['surface']} !important; background-color: {T['surface']} !important;
    color: {T['ink']} !important; border-color: {T['border']} !important;
  }}
  [data-testid="stSelectboxVirtualDropdown"] {{
    border: 1px solid {T['border']} !important; border-radius: 12px !important; box-shadow: {T['shadow']} !important;
  }}
  div[data-baseweb="popover"] *, [data-testid="stSelectboxVirtualDropdown"] *,
  [role="listbox"] *, [role="option"] *, div[data-baseweb="menu"] * {{
    color: {T['ink']} !important;
  }}
  [role="option"]:hover, [role="option"][aria-selected="true"],
  [role="option"][data-focused="true"], [role="option"][data-selected="true"],
  [role="option"]:hover *, [role="option"][aria-selected="true"] *,
  [role="option"][data-focused="true"] *, [role="option"][data-selected="true"] * {{
    background: {T['accent_soft']} !important; background-color: {T['accent_soft']} !important; color: {T['ink']} !important;
  }}

  /* Theme-Safe Alerts (Info, Warning, Over-Hydration Guardrail & Reset) */
  [data-testid="stAlert"], [data-testid="stAlertContainer"], div[role="alert"], .stAlert {{
    background: {T['alert_info_bg']} !important; background-color: {T['alert_info_bg']} !important;
    color: var(--ink) !important; border: 1px solid var(--border) !important;
    border-left: 4px solid var(--accent) !important; border-radius: 14px !important;
  }}
  [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]),
  [data-testid="stAlertContainer"]:has([data-testid="stAlertContentWarning"]) {{
    background: {T['alert_warn_bg']} !important; background-color: {T['alert_warn_bg']} !important;
    border-left-color: #D69838 !important;
  }}
  [data-testid="stAlert"]:has([data-testid="stAlertContentError"]),
  [data-testid="stAlertContainer"]:has([data-testid="stAlertContentError"]) {{
    background: {T['alert_err_bg']} !important; background-color: {T['alert_err_bg']} !important;
    border-left-color: #C45B4D !important;
  }}
  [data-testid="stAlert"] *, [data-testid="stAlertContainer"] *, div[role="alert"] *, .stAlert * {{
    color: var(--ink) !important;
  }}
  [data-testid="stAlert"] svg, div[role="alert"] svg {{
    fill: var(--accent) !important; color: var(--accent) !important;
  }}
  [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) svg {{
    fill: #D69838 !important; color: #D69838 !important;
  }}

  /* High-Contrast Toast Pop-ups (Light & Dark Modes) */
  [data-testid="stToastContainer"] {{ z-index: 999999 !important; }}
  [data-testid="stToast"] {{
    background: {T['surface']} !important; background-color: {T['surface']} !important;
    color: {T['ink']} !important; border: 1.5px solid {T['accent']} !important;
    border-radius: 16px !important; box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28) !important;
  }}
  [data-testid="stToast"] > div, [data-testid="stToast"] [data-testid="stMarkdownContainer"],
  [data-testid="stToast"] p, [data-testid="stToast"] span, [data-testid="stToast"] div {{
    background: transparent !important; color: {T['ink']} !important; font-weight: 600 !important;
  }}
  [data-testid="stToast"] button svg {{ color: {T['muted']} !important; fill: {T['muted']} !important; }}

  [data-testid="stForm"], .st-key-cup_conv_card {{
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: 20px !important;
  }}

  [data-testid="stBaseButton-secondary"], button[kind="secondary"],
  [data-testid="stDownloadButton"] button, [data-testid="stFormSubmitButton"] button {{
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: 99px !important; color: var(--ink) !important; font-weight: 600 !important;
  }}
  [data-testid="stBaseButton-secondary"]:hover, button[kind="secondary"]:hover,
  [data-testid="stDownloadButton"] button:hover, [data-testid="stFormSubmitButton"] button:hover {{
    background: var(--accent-soft) !important; border-color: var(--accent) !important;
  }}
  [data-testid="stBaseButton-secondary"] *, button[kind="secondary"] *,
  [data-testid="stDownloadButton"] button *, [data-testid="stFormSubmitButton"] button * {{ color: var(--ink) !important; }}

  [data-testid="stSelectbox"] .react-aria-ComboBox [role="group"],
  [data-testid="stTextInputRootElement"],
  [data-testid="stDateInputField"],
  [data-testid="stSelectbox"] [data-baseweb="select"] > div,
  [data-testid="stDateInput"] [data-baseweb="input"],
  [data-testid="stDateInput"] [data-baseweb="base-input"],
  [data-testid="stTextInput"] [data-baseweb="input"],
  [data-testid="stTextInput"] [data-baseweb="base-input"],
  [data-testid="stNumberInput"] [data-baseweb="input"],
  [data-testid="stNumberInput"] [data-baseweb="base-input"],
  [data-baseweb="select"] > div,
  [data-baseweb="input"],
  [data-baseweb="base-input"] {{
    background: {T['surface']} !important; background-color: {T['surface']} !important;
    color: {T['ink']} !important; border: 1px solid {T['border']} !important; border-radius: 12px !important;
  }}
  [data-testid="stSelectbox"] .react-aria-ComboBox [role="group"] *,
  [data-testid="stTextInputRootElement"] *,
  [data-testid="stDateInputField"] *,
  [data-testid="stNumberInputContainer"] *,
  [data-testid="stNumberInputContainer"] input,
  [data-baseweb="select"] > div *,
  [data-baseweb="input"] input,
  [data-baseweb="base-input"] input {{
    background: transparent !important; background-color: transparent !important;
    color: {T['ink']} !important; -webkit-text-fill-color: {T['ink']} !important; caret-color: {T['ink']} !important;
  }}
  [data-testid="stTextInputRootElement"] input::placeholder,
  [data-testid="stSelectbox"] input::placeholder {{
    color: {T['muted']} !important; -webkit-text-fill-color: {T['muted']} !important; opacity: 0.78 !important;
  }}
  [data-testid="stSelectbox"] svg, [data-testid="stDateInput"] svg,
  [data-baseweb="select"] svg, .stDateInput svg {{
    color: {T['ink']} !important; fill: {T['ink']} !important;
  }}
  [data-testid="stNumberInputContainer"], .stNumberInput div[data-baseweb="input"] {{
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: 12px !important;
  }}
  [data-testid="stNumberInputStepDown"], [data-testid="stNumberInputStepUp"], .stNumberInput button {{
    background: var(--soft) !important; color: var(--ink) !important; border-color: var(--border) !important;
  }}
  [data-testid="stNumberInputStepDown"] svg, [data-testid="stNumberInputStepUp"] svg, .stNumberInput button svg {{
    fill: var(--ink) !important; color: var(--ink) !important;
  }}

  @keyframes mascotBob {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-5px); }} }}
  .mascot-3d-bob {{ animation: mascotBob 3.4s ease-in-out infinite; }}
  .asset-3d {{ transition: transform 0.25s cubic-bezier(.22,1,.36,1), filter 0.25s ease; }}

  .studio-grid {{
    display: grid; grid-template-columns: 1fr 1.38fr 1fr; gap: 18px;
    align-items: stretch; margin: 0.4rem 0 1.1rem 0;
  }}
  .studio-panel {{
    background: var(--surface); border: 1px solid var(--border); border-radius: 22px;
    padding: 1.25rem 1.35rem; box-shadow: var(--shadow);
    display: flex; flex-direction: column; justify-content: space-between;
    transition: transform 0.22s ease, box-shadow 0.22s ease;
  }}
  .studio-panel:hover {{ transform: translateY(-3px); }}
  .eyebrow {{
    font-size: 0.72rem; font-weight: 800; letter-spacing: 0.9px; text-transform: uppercase;
    color: var(--accent) !important; margin-bottom: 0.25rem;
  }}
  .soft-bar {{ width: 100%; height: 7px; background: var(--soft); border-radius: 99px; overflow: hidden; margin-top: 0.4rem; }}
  .soft-fill {{ height: 100%; background: var(--accent); border-radius: 99px; transition: width 0.35s ease; }}

  .nav-head {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 0.35rem; }}
  .rank-pill {{
    background: {T['gold_bg']}; color: {T['gold_ink']} !important; font-size: 0.78rem;
    font-weight: 800; padding: 0.26rem 0.78rem; border-radius: 99px; white-space: nowrap;
  }}
  [data-testid="stMetric"] {{
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: 20px !important; padding: 0.9rem 0.95rem !important; box-shadow: var(--shadow) !important;
  }}
  [data-testid="stMetricValue"] * {{ color: var(--ink) !important; font-size: clamp(1.3rem, 1.8vw, 1.8rem) !important; }}
  [data-testid="stMetricLabel"] * {{ color: var(--muted) !important; font-weight: 700 !important; font-size: 0.76rem !important; }}
  [data-testid="stMetricDelta"] {{
    background: var(--accent-soft) !important; border-radius: 99px !important;
    padding: 0.12rem 0.48rem !important; width: fit-content !important; font-size: 0.72rem !important;
  }}
  [data-testid="stMetricDelta"] div, [data-testid="stMetricDelta"] span, [data-testid="stMetricDelta"] svg {{
    color: var(--accent) !important;
  }}
  .vessel-chip {{
    background: var(--surface); border: 1px solid var(--border); border-radius: 18px;
    padding: 0.8rem 0.4rem; text-align: center; height: 156px; margin-bottom: 0.5rem;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    box-shadow: var(--shadow); transition: transform 0.22s ease, border-color 0.22s ease;
  }}
  .vessel-chip:hover {{ transform: translateY(-4px); border-color: var(--accent); }}
  .vessel-chip:hover .asset-3d {{ transform: scale(1.1) rotate(-4deg); }}
  .interactive-card {{
    background: var(--surface); border: 1px solid var(--border); border-radius: 18px;
    padding: 0.9rem 1.1rem; margin-bottom: 0.45rem; box-shadow: var(--shadow);
    display: flex; align-items: center; gap: 0.95rem;
    transition: transform 0.22s ease, border-color 0.22s ease;
  }}
  .interactive-card:hover {{ transform: translateY(-3px); border-color: var(--accent); }}
  .interactive-card:hover .asset-3d {{ transform: scale(1.08); }}
  .badge-on {{
    background: #1A7887 !important; border-radius: 20px; padding: 1.15rem;
    color: #FFFFFF !important; margin-bottom: 0.85rem; box-shadow: 0 8px 24px rgba(26, 120, 135, 0.24);
    transition: transform 0.22s ease;
  }}
  .badge-on:hover {{ transform: translateY(-3px); }}
  .badge-on *, .badge-on h3, .badge-on p {{ color: #FFFFFF !important; }}
  .badge-off {{
    background: var(--soft) !important; border: 1px dashed var(--border) !important;
    border-radius: 20px; padding: 1.15rem; opacity: 0.72; margin-bottom: 0.85rem;
  }}
  .avatar-circle {{
    width: 88px; height: 88px; border-radius: 50%; border: 2.5px solid var(--accent);
    background: var(--surface); display: flex; align-items: center; justify-content: center;
    margin: 0 auto; overflow: hidden; box-shadow: var(--shadow);
  }}

  /* Ornamental Hydro Section Dividers */
  .sec-wrap {{ margin: 1.5rem 0 0.75rem 0; }}
  .sec-divider {{ display: flex; align-items: center; gap: 12px; opacity: 0.78; }}
  .sec-line {{ flex: 1; height: 1px; background: linear-gradient(90deg, transparent, var(--accent), transparent); opacity: 0.45; }}
  .sec-ornament {{
    color: var(--accent) !important; background: var(--soft); border: 1px solid var(--border);
    padding: 5px 10px; border-radius: 99px; display: inline-flex; align-items: center; justify-content: center;
  }}
  .sec-title {{ margin: 0.12rem 0 0 0 !important; font-size: 1.4rem !important; font-weight: 800 !important; letter-spacing: -0.35px; color: var(--ink) !important; }}
  .sec-sub {{ margin: 0.18rem 0 0 0 !important; font-size: 0.86rem; color: var(--muted) !important; }}

  .wb-ledger-wrap {{
    background: var(--surface); border: 1px solid var(--border); border-radius: 18px;
    overflow-x: auto; box-shadow: var(--shadow); margin-bottom: 0.75rem;
  }}
  .wb-ledger {{ width: 100%; border-collapse: collapse; font-size: 0.84rem; }}
  .wb-ledger th {{
    background: var(--soft); color: var(--muted) !important; text-align: left;
    padding: 0.65rem 0.85rem; font-size: 0.74rem; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.04em; border-bottom: 1px solid var(--border); white-space: nowrap;
  }}
  .wb-ledger td {{
    padding: 0.58rem 0.85rem; border-bottom: 1px solid var(--border); color: var(--ink) !important;
    vertical-align: middle; white-space: nowrap;
  }}
  .wb-ledger tr:last-child td {{ border-bottom: none; }}
  .wb-ledger tr:hover td {{ background: rgba(78, 165, 180, 0.08); }}
  .wb-pbar {{ width: 92px; height: 7px; background: var(--soft); border-radius: 99px; overflow: hidden; display: inline-block; vertical-align: middle; margin-right: 7px; }}
  .wb-pfill {{ display: block; height: 100%; background: var(--accent); border-radius: 99px; }}
  .st-key-top_log_drink_btn button, .st-key-nav_dash button, .st-key-nav_badges button, .st-key-nav_vessels button {{
    padding: 0.42rem 0.65rem !important; font-size: 0.84rem !important; white-space: nowrap !important;
  }}

  @media (max-width: 920px) {{
    .studio-grid {{ grid-template-columns: 1fr !important; }}
    .nav-head {{ flex-direction: column; align-items: flex-start; }}
  }}
</style>
""")

@st.dialog("Log Custom Water Intake")
def open_custom_drink_dialog(goal_ml: int):
    st.caption("Record a custom glass or refill right away without scrolling.")
    d_amt = st.number_input("Amount (ml)", min_value=10, max_value=2500, value=300, step=50, key="modal_drink_ml")
    d_src = st.text_input("Beverage or Bottle Name", value="Refill Bottle", key="modal_drink_src")
    if st.button("Record Water Intake", type="primary", width="stretch", key="modal_drink_submit"):
        hit_goal = log_drink(int(d_amt), d_src.strip() or "Custom Drink", goal_ml)
        if hit_goal: st.balloons()
        st.rerun()

# ------------------------------------------------------------------------------
# SCREEN 1: WELCOME & ONBOARDING (Alpine Spring Oasis Landscape)
# ------------------------------------------------------------------------------

if st.session_state.get("pending_toast"):
    _t_msg, _t_ico = st.session_state.pending_toast
    st.session_state.pending_toast = None
    st.toast(_t_msg, icon=_t_ico)

if not st.session_state.onboarded:
    render_html(render_coastal_spring_svg(dark=is_dark))
    st.markdown("<div style='height:0.65rem;'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 0.85], gap="large")
    with c1:
        st.subheader("Configure Your Hydration Profile")
        in_name = st.text_input("Your Name:", value=st.session_state.user_name)
        in_avatar = st.selectbox("Choose Your Companion Spirit Mascot:", options=list(COMPANIONS.keys()))
        in_cohort = st.selectbox("Select Your Clinical Age Cohort:", options=list(AGE_GOALS.keys()), index=list(AGE_GOALS.keys()).index(st.session_state.age_cohort))
        std_goal = AGE_GOALS[in_cohort]["goal"]
        st.caption(f"Clinical baseline: ~{std_goal:,} ml/day ({AGE_GOALS[in_cohort]['cups']} cups). {AGE_GOALS[in_cohort]['fact']}")
        in_goal = st.number_input("Fine-Tune Your Daily Target (ml):", min_value=500, max_value=6000, value=int(std_goal), step=100)
        if st.button("Enter WaterBuddy Dashboard ->", type="primary", width="stretch"):
            st.session_state.user_name = in_name.strip() if in_name.strip() else "Friend"
            st.session_state.user_avatar = in_avatar
            st.session_state.age_cohort = in_cohort
            st.session_state.daily_goal = in_goal
            st.session_state.onboarded = True
            st.rerun()

    with c2:
        preview_mood_map = {
            "Cheerful Glow (50%)": "happy",
            "Morning Calm (0%)": "start",
            "Attentive Sip (1–49%)": "attentive",
            "Final Stretch (75%)": "energized",
            "Goal Triumph (100%)": "ecstatic",
            "Mindful Surplus (125–149%)": "paced",
            "Over-Hydration Alert (150%+)": "caution",
        }
        sel_preview_lbl = st.selectbox(
            "Preview Companion Behavior by Situation:",
            options=list(preview_mood_map.keys()),
            key="onb_mood_preview"
        )
        sel_preview_mood = preview_mood_map[sel_preview_lbl]
        p_title, p_sub = MOOD_META[sel_preview_mood]
        render_html(f"""
        <div class="studio-panel" style="align-items:center; text-align:center;">
          <div style="display:flex; justify-content:space-between; width:100%; align-items:center; margin-bottom:0.2rem;">
            <span class="eyebrow">Live Mascot Preview</span>
            <span class="rank-pill">{p_title}</span>
          </div>
          {render_animated_avatar_svg(in_avatar, sel_preview_mood, 162, 162, uid="onb")}
          <div style="font-size:0.78rem; color:{T['muted']}; margin-bottom:0.55rem;">{html.escape(in_avatar)} • {p_sub}</div>
          <div style="text-align:left; width:100%; font-size:0.86rem; line-height:1.58; color:{T['muted']}; border-top:1px solid {T['border']}; padding-top:0.65rem;">
            <div class="eyebrow">Calm Hydration Suite</div>
            <div>• <strong>Python Turtle Mascot:</strong> animated expression &amp; flipper behaviors per milestone</div>
            <div>• <strong>100% Session Memory:</strong> private local tracking with CSV &amp; report export</div>
            <div>• <strong>WHO / EFSA Baselines:</strong> calibrated across Kids, Teens, Adults &amp; Seniors</div>
          </div>
        </div>
        """)

# ------------------------------------------------------------------------------
# SCREEN 2: MAIN HYDRATION STUDIO & GALLERY VIEWS
# ------------------------------------------------------------------------------

else:
    total = int(st.session_state.total_intake)
    goal = int(st.session_state.daily_goal)
    std_baseline = AGE_GOALS[st.session_state.age_cohort]["goal"]
    remaining, percentage, _ = calculate_progress(total, goal)
    badges = evaluate_badges(st.session_state.intake_history, total, goal, std_baseline)
    unlocked_cnt = sum(1 for b in badges if b["unlocked"])
    earned_arts = get_collected_hydro_arts(st.session_state.intake_history, total, goal)
    user_rank = get_user_hydration_rank(st.session_state.intake_history)

    st.session_state.mascot_mood = evaluate_mascot_mood(total, percentage)
    cur_mood = st.session_state.mascot_mood
    cur_mood_label, _ = MOOD_META.get(cur_mood, ("Morning Calm", ""))

    with st.sidebar:
        render_html(f"""
        <div style="text-align:center; margin-bottom:0.8rem;">
          <div class="avatar-circle">{render_animated_avatar_svg(st.session_state.user_avatar, cur_mood, 74, 74, uid="side")}</div>
          <div style="font-size:1.12rem; font-weight:800; margin-top:0.5rem;">{html.escape(st.session_state.user_name)}</div>
          <div style="font-size:0.78rem; font-weight:700; color:{T['accent']};">{user_rank} • {cur_mood_label}</div>
          <div style="font-size:0.76rem; opacity:0.78;">Target: {goal:,} ml/day</div>
        </div>
        <div style="background:{T['surface']}; border:1px solid {T['border']}; border-radius:14px; padding:0.65rem 0.8rem; margin-bottom:0.8rem; font-size:0.78rem;">
          <div style="display:flex; justify-content:space-between; font-weight:700;">
            <span>{unlocked_cnt}/{len(badges)} Badges</span><span>{percentage:.0f}% Goal</span>
          </div>
          <div class="soft-bar"><div class="soft-fill" style="width:{min(100, int(percentage))}%;"></div></div>
          <div style="margin-top:0.35rem; color:{T['muted']};">Hydro Art: {len(earned_arts)}/4 unlocked</div>
        </div>
        """)
        if st.button("Edit Profile", width="stretch"):
            st.session_state.onboarded = False
            st.rerun()

        st.markdown("---")
        nav_opts = ["Dashboard", "Wall of Badges", "Vessel Studio"]
        if st.session_state.get("sidebar_nav_radio") not in nav_opts:
            st.session_state.sidebar_nav_radio = st.session_state.nav_view
        def _sync_sidebar_nav():
            st.session_state.nav_view = st.session_state.sidebar_nav_radio
        def _switch_view(target: str):
            st.session_state.nav_view = target
            st.session_state.sidebar_nav_radio = target
        st.radio("Navigation", nav_opts, key="sidebar_nav_radio", on_change=_sync_sidebar_nav)
        dark_toggle = st.toggle("Deep Tide Dark Mode", value=st.session_state.dark_theme)
        if dark_toggle != st.session_state.dark_theme:
            st.session_state.dark_theme = dark_toggle
            st.rerun()

        st.markdown("---")
        tip_idx = len(st.session_state.intake_history) % len(HYDRATION_TIPS)
        st.caption(f"*{HYDRATION_TIPS[tip_idx]}*")
        if not st.session_state.show_reset_confirm:
            if st.button("Start a New Day (Reset)", width="stretch"):
                st.session_state.show_reset_confirm = True
                st.rerun()
        else:
            st.warning("Clear today's logged intake?")
            rc1, rc2 = st.columns(2)
            if rc1.button("Yes, Reset", type="primary", width="stretch"):
                st.session_state.total_intake, st.session_state.intake_history, st.session_state.recent_art = 0, [], None
                st.session_state.show_reset_confirm, st.session_state.mascot_mood = False, "start"
                st.session_state.last_action, st.session_state.last_drink_desc = "reset", ""
                st.rerun()
            if rc2.button("Cancel", width="stretch"):
                st.session_state.show_reset_confirm = False
                st.rerun()

    # CLEAN TOP ACTION BAR WITH FIRST-VIEW "+ Log Drink" BUTTON
    h1, h2 = st.columns([1.18, 2.02])
    with h1:
        render_html(f"""
        <div class="nav-head">
          <div>
            <span style="font-size:1.45rem; font-weight:900; letter-spacing:-0.4px; color:{T['ink']};">WaterBuddy</span>
            <span style="font-size:0.86rem; color:{T['muted']}; margin-left:0.6rem; white-space:nowrap;"><strong>{html.escape(st.session_state.user_name)}</strong> • {total:,} / {goal:,} ml</span>
          </div>
          <span class="rank-pill">{user_rank}</span>
        </div>
        """)
    with h2:
        b_log, b1, b2, b3 = st.columns([1.15, 1.05, 1.1, 0.9])
        if b_log.button("+ Log Drink", type="primary", width="stretch", key="top_log_drink_btn"):
            open_custom_drink_dialog(goal)
        if b1.button("● Dashboard" if st.session_state.nav_view == "Dashboard" else "Dashboard", type="secondary", width="stretch", key="nav_dash", on_click=_switch_view, args=("Dashboard",)):
            pass
        if b2.button(f"{'● ' if st.session_state.nav_view == 'Wall of Badges' else ''}Badges ({unlocked_cnt}/{len(badges)})", type="secondary", width="stretch", key="nav_badges", on_click=_switch_view, args=("Wall of Badges",)):
            pass
        if b3.button("● Vessels" if st.session_state.nav_view == "Vessel Studio" else "Vessels", type="secondary", width="stretch", key="nav_vessels", on_click=_switch_view, args=("Vessel Studio",)):
            pass

    if total > 4500 or percentage >= 150.0:
        st.warning(
            f"WellNest Over-Hydration Guardrail ({percentage:.0f}% of goal, {total:,} ml): "
            "Today's intake is well above your physiological target. Pause further drinking and spread recovery fluids slowly."
        )

    # --------------------------------------------------------------------------
    # VIEW 1: DASHBOARD
    # --------------------------------------------------------------------------
    if st.session_state.nav_view == "Dashboard":
        c_short = st.session_state.user_avatar.split()[0]
        speech_msg = get_mascot_speech(
            st.session_state.user_avatar,
            st.session_state.user_name,
            total,
            goal,
            percentage,
            cur_mood,
            sip_count=len(st.session_state.intake_history),
            last_action=st.session_state.last_action,
            last_desc=st.session_state.last_drink_desc,
        )
        active_art = st.session_state.recent_art or "preview"
        art_img = draw_vector_art(active_art)
        art_uri = image_to_data_uri(art_img)
        art_labels = {"preview": "Spring Seed (Log sip to unlock)", "drop": "Crystal Water Droplet", "leaf": "Hydration Sprout", "traveler": "Walker Man & Turtle", "badge": "Ocean Championship Rosette"}
        coach_lbl, coach_pct, coach_col = get_coach_progress(total, goal, percentage, T["accent"])

        render_html(f"""
        <div class="studio-grid">
          <div class="studio-panel">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span class="eyebrow">Fluid Chamber</span>
              <span style="font-size:0.78rem; font-weight:700; color:{T['muted']};">{percentage:.0f}% filled</span>
            </div>
            {render_animated_bottle_svg(percentage, total, goal, 192, 276, dark=is_dark)}
            <div class="soft-bar"><div class="soft-fill" style="width:{min(100, int(percentage))}%;"></div></div>
          </div>

          <div class="studio-panel">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
              <span class="eyebrow">Companion Coach</span>
              <span style="display:flex; align-items:center; gap:6px;">
                <span style="background:{T['accent_soft']}; color:{T['accent']}; font-size:0.7rem; font-weight:800; padding:2px 8px; border-radius:99px;">{cur_mood_label}</span>
                <span style="font-size:0.75rem; font-weight:700; color:{T['muted']};">{len(st.session_state.intake_history)} sips</span>
              </span>
            </div>
            <div style="display:flex; align-items:center; gap:1rem; margin:0.4rem 0;">
              <div style="flex:0 0 132px; text-align:center;">{render_animated_avatar_svg(st.session_state.user_avatar, cur_mood, 132, 132, uid="hero")}</div>
              <div style="background:{T['soft']}; border-radius:16px; padding:0.9rem 1rem; font-size:0.86rem; line-height:1.45; flex:1;">
                <div style="font-weight:800; color:{T['accent']}; margin-bottom:0.2rem;">{c_short} says:</div>
                "{html.escape(speech_msg)}"
              </div>
            </div>
            <div style="border-top:1px solid {T['border']}; padding-top:0.55rem;">
              <div style="display:flex; justify-content:space-between; font-size:0.78rem; font-weight:700;">
                <span>{html.escape(coach_lbl)}</span><span style="color:{coach_col};">{coach_pct}%</span>
              </div>
              <div class="soft-bar"><div class="soft-fill" style="width:{coach_pct}%; background:{coach_col};"></div></div>
            </div>
          </div>

          <div class="studio-panel" style="align-items:center; text-align:center;">
            <div style="display:flex; justify-content:space-between; width:100%; align-items:center;">
              <span class="eyebrow">Hydro Art Vault</span>
              <span style="font-size:0.78rem; font-weight:700; color:{T['muted']};">{len(earned_arts)}/4 unlocked</span>
            </div>
            <img src="{art_uri}" alt="Hydro Art" style="width:150px; height:150px; object-fit:contain; margin:0.2rem auto;"/>
            <div style="width:100%;">
              <div style="font-size:0.8rem; font-weight:700; color:{T['ink']}; margin-bottom:0.35rem;">{art_labels.get(active_art, 'Milestone Art')}</div>
              <div style="display:flex; justify-content:center; flex-wrap:wrap; gap:4px; font-size:0.7rem; font-weight:700; color:{T['muted']};">
                <span style="padding:2px 7px; border-radius:99px; background:{T['accent_soft'] if 'drop' in earned_arts else T['soft']};">Drop</span>
                <span style="padding:2px 7px; border-radius:99px; background:{T['accent_soft'] if 'traveler' in earned_arts else T['soft']};">Hiker</span>
                <span style="padding:2px 7px; border-radius:99px; background:{T['accent_soft'] if 'leaf' in earned_arts else T['soft']};">Leaf</span>
                <span style="padding:2px 7px; border-radius:99px; background:{T['accent_soft'] if 'badge' in earned_arts else T['soft']};">Rosette</span>
              </div>
            </div>
          </div>
        </div>
        """)

        if st.session_state.recent_art:
            _, dlc = st.columns([1.85, 1.15])
            dlc.download_button("Download Artwork (.png)", image_to_png_bytes(art_img), f"waterbuddy_{active_art}.png", "image/png", width="stretch")

        # 4 KPI METRICS
        delta_std = goal - std_baseline
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Water Logged", f"{total:,} ml", f"{percentage:.1f}% of goal")
        k2.metric("Daily Target", f"{goal:,} ml", f"~{goal / 250:.1f} standard cups")
        k3.metric("Remaining to Go", f"{remaining:,} ml", "Target Achieved" if remaining == 0 else f"~{remaining / 250:.1f} cups left")
        k4.metric("WHO Baseline", f"{std_baseline:,} ml", f"{delta_std:+} ml vs cohort" if delta_std != 0 else "Matched baseline")

        # RAPID VESSELS (3D Assets)
        render_section_header("Rapid Vessels", "Log by Everyday Container", "One-tap logging calibrated to real-world glass and bottle capacities.")
        v_cols = st.columns(len(VESSELS))
        for idx, v in enumerate(VESSELS):
            with v_cols[idx]:
                render_html(f"<div class='vessel-chip'><div>{render_vessel_svg(v['id'], 48, dark=is_dark)}</div><div style='font-weight:700; font-size:0.81rem; line-height:1.2; margin-top:0.3rem;'>{v['name']}</div><div style='font-size:0.76rem; color:{T['accent']}; font-weight:800; margin-top:0.12rem;'>+{v['amount']} ml</div></div>")
                if st.button(f"+{v['amount']} ml", key=f"vessel_btn_{idx}", width="stretch"):
                    if log_drink(v["amount"], v["name"], goal): st.balloons()
                    st.rerun()

        # CUSTOM VOLUME STEPPER & CUP CONVERTER
        render_section_header("Precision Volume", "Custom Amount & Cup Converter", "Enter an exact milliliter value or convert servings automatically (1 cup = 250 ml).")
        f_col1, f_col2 = st.columns([1.0, 1.1], gap="large")
        with f_col1:
            with st.form("custom_drink_form", clear_on_submit=True):
                cf1, cf2 = st.columns([1.85, 1.15], vertical_alignment="bottom")
                custom_amt = cf1.number_input("Custom Amount (ml)", min_value=10, max_value=2500, value=250, step=50)
                if cf2.form_submit_button("Log Drink", width="stretch"):
                    if log_drink(int(custom_amt), "Custom Entry", goal): st.balloons()
                    st.rerun()
        with f_col2:
            with st.container(border=True, key="cup_conv_card"):
                cc1, cc2, cc3 = st.columns([1.15, 0.9, 1.3], vertical_alignment="bottom")
                cups_in = cc1.number_input("Cups (250 ml)", min_value=0.5, max_value=15.0, value=1.0, step=0.5)
                conv_ml = int(cups_in * 250)
                cc2.markdown(f"<div style='font-size:1.05rem; font-weight:800; color:{T['accent']}; text-align:center; padding-bottom:0.55rem;'>= {conv_ml:,} ml</div>", unsafe_allow_html=True)
                if cc3.button(f"+ Add {conv_ml} ml", width="stretch"):
                    if log_drink(conv_ml, f"{cups_in} Cup(s)", goal): st.balloons()
                    st.rerun()

        # CHRONOLOGICAL LEDGER + TIMELINE & CONSISTENCY ANALYTICS
        render_section_header(
            "History & Analytics",
            "Hydration Timeline, Consistency & Full Ledger",
            "Track clock-time sip trajectory, day-period balance, inter-sip cadence, and your full intake dataset.",
        )
        if st.session_state.intake_history:
            df_h, avg_gap_str, score, rhythm_lbl, peak_str = analyze_hydration_timeline(st.session_state.intake_history, goal)
            render_html(f"""
            <div style="display:flex; flex-wrap:wrap; gap:0.65rem; margin:0.2rem 0 0.85rem;">
              <div style="flex:1; min-width:175px; background:{T['soft']}; border:1px solid {T['border']}; border-radius:14px; padding:0.55rem 0.85rem;">
                <div style="font-size:0.7rem; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:{T['muted']};">Sip Frequency</div>
                <div style="font-size:1.0rem; font-weight:800; color:{T['ink']}; margin-top:2px;">{html.escape(avg_gap_str)}</div>
              </div>
              <div style="flex:1; min-width:175px; background:{T['soft']}; border:1px solid {T['border']}; border-radius:14px; padding:0.55rem 0.85rem;">
                <div style="font-size:0.7rem; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:{T['muted']};">Rhythm Consistency</div>
                <div style="font-size:1.0rem; font-weight:800; color:{T['accent']}; margin-top:2px;">{score}% ({html.escape(rhythm_lbl)})</div>
              </div>
              <div style="flex:1; min-width:175px; background:{T['soft']}; border:1px solid {T['border']}; border-radius:14px; padding:0.55rem 0.85rem;">
                <div style="font-size:0.7rem; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:{T['muted']};">Peak Single Intake</div>
                <div style="font-size:1.0rem; font-weight:800; color:{T['ink']}; margin-top:2px;">{html.escape(peak_str)}</div>
              </div>
            </div>
            """)

            c_ch1, c_ch2 = st.columns([1.15, 1.0], gap="large")
            with c_ch1:
                st.markdown("**Intake Timeline (Volume by Clock Time)**")
                st.caption("Timed line trajectory of each logged drink with drop stems and dashed mean sip volume.")
                if HAS_ALTAIR:
                    avg_sip_val = round(float(df_h["Amount (ml)"].mean()), 1)
                    mean_df = pd.DataFrame({"MeanSip": [avg_sip_val], "Label": [f"Avg {avg_sip_val:.0f} ml"]})
                    base_tl = alt.Chart(df_h).encode(
                        x=alt.X("Timestamp:T", title="Clock Time", axis=alt.Axis(format="%I:%M %p", tickCount=min(6, max(2, len(df_h))), labelAngle=-15)),
                        y=alt.Y("Amount (ml):Q", title="Drink Volume (ml)", scale=alt.Scale(zero=True)),
                        tooltip=[
                            alt.Tooltip("#:O", title="Sip #"),
                            alt.Tooltip("Time:N", title="Logged Time"),
                            alt.Tooltip("Period:N", title="Day Period"),
                            alt.Tooltip("Vessel / Source:N", title="Source"),
                            alt.Tooltip("Amount (ml):Q", title="Volume (ml)"),
                            alt.Tooltip("Sip Interval:N", title="Gap Since Prev"),
                            alt.Tooltip("Running Total (ml):Q", title="Running Total (ml)"),
                        ],
                    )
                    area_tl = base_tl.mark_area(opacity=0.14, color=T["accent"], interpolate="monotone")
                    stem_tl = base_tl.mark_rule(opacity=0.35, strokeWidth=2, color=T["accent"]).encode(y2=alt.datum(0))
                    line_tl = base_tl.mark_line(strokeWidth=3, color=T["accent"], interpolate="monotone")
                    pts_tl = base_tl.mark_circle(size=95, opacity=1.0, stroke=T["ink"], strokeWidth=1.5).encode(
                        color=alt.Color(
                            "Period:N",
                            title="Period",
                            scale=alt.Scale(
                                domain=["Morning", "Afternoon", "Evening"],
                                range=["#0284C7", T["accent"], "#D97706"],
                            ),
                        )
                    )
                    mean_rule = alt.Chart(mean_df).mark_rule(strokeDash=[5, 4], strokeWidth=1.6, color=T["muted"]).encode(
                        y="MeanSip:Q",
                        tooltip=[alt.Tooltip("Label:N", title="Average Sip")],
                    )
                    tl_chart = (
                        (area_tl + stem_tl + line_tl + pts_tl + mean_rule)
                        .properties(height=255)
                        .configure(background="transparent")
                        .configure_view(strokeWidth=0)
                        .configure_axis(labelColor=T["ink"], titleColor=T["muted"], gridColor=T["border"])
                        .configure_legend(orient="top", labelColor=T["ink"], titleColor=T["muted"])
                    )
                    st.altair_chart(tl_chart, width="stretch")
                else:
                    st.line_chart(df_h.set_index("Time")["Amount (ml)"], color=T["accent"])

            with c_ch2:
                tab_pace, tab_cum = st.tabs(["Pacing & Consistency", "Cumulative vs Goal"])
                with tab_pace:
                    st.caption(f"Day-period split vs balanced ~{goal // 3:,} ml/period pace ({score}% {rhythm_lbl}).")
                    per_order = ["Morning", "Afternoon", "Evening"]
                    p_rows = []
                    for p_name in per_order:
                        sub = df_h[df_h["Period"] == p_name]
                        p_rows.append({
                            "Period": p_name,
                            "Total (ml)": int(sub["Amount (ml)"].sum()) if not sub.empty else 0,
                            "Sips": int(len(sub)),
                            "SipsLbl": f"{int(sub['Amount (ml)'].sum()) if not sub.empty else 0} ml ({len(sub)}x)",
                        })
                    df_p = pd.DataFrame(p_rows)
                    if HAS_ALTAIR:
                        pace_target = round(goal / 3.0)
                        pace_df = pd.DataFrame({"PaceTarget": [pace_target], "PaceLabel": [f"Balanced Pace ({pace_target:,} ml/period)"]})
                        max_p = max(pace_target * 1.15, int(df_p["Total (ml)"].max() * 1.18), 300)
                        p_base = alt.Chart(df_p).encode(
                            x=alt.X("Period:N", sort=per_order, title="Day Period", axis=alt.Axis(labelAngle=0)),
                            y=alt.Y("Total (ml):Q", title="Period Volume (ml)", scale=alt.Scale(domain=[0, max_p])),
                            tooltip=[
                                alt.Tooltip("Period:N", title="Period"),
                                alt.Tooltip("Total (ml):Q", title="Volume (ml)"),
                                alt.Tooltip("Sips:Q", title="Drink Count"),
                            ],
                        )
                        p_bars = p_base.mark_bar(cornerRadiusTopLeft=7, cornerRadiusTopRight=7, width=42).encode(
                            color=alt.Color(
                                "Period:N",
                                legend=None,
                                scale=alt.Scale(domain=per_order, range=["#0284C7", T["accent"], "#D97706"]),
                            )
                        )
                        p_lbls = p_base.mark_text(dy=-8, fontSize=11, fontWeight="bold", color=T["ink"]).encode(text="SipsLbl:N")
                        p_rule = alt.Chart(pace_df).mark_rule(strokeDash=[5, 4], strokeWidth=1.8, color=T["muted"]).encode(
                            y="PaceTarget:Q",
                            tooltip=[alt.Tooltip("PaceLabel:N", title="Reference")],
                        )
                        p_chart = (
                            (p_bars + p_lbls + p_rule)
                            .properties(height=215)
                            .configure(background="transparent")
                            .configure_view(strokeWidth=0)
                            .configure_axis(labelColor=T["ink"], titleColor=T["muted"], gridColor=T["border"])
                        )
                        st.altair_chart(p_chart, width="stretch")
                    else:
                        st.bar_chart(df_p.set_index("Period")["Total (ml)"], color=T["accent"])

                with tab_cum:
                    st.caption(f"Cumulative build across clock time vs {goal:,} ml daily target.")
                    if HAS_ALTAIR:
                        goal_df = pd.DataFrame({"GoalTarget": [int(goal)], "GoalLabel": [f"Daily Goal ({goal:,} ml)"]})
                        cum_base = alt.Chart(df_h).encode(
                            x=alt.X("Timestamp:T", title="Clock Time", axis=alt.Axis(format="%I:%M %p", tickCount=min(6, max(2, len(df_h))), labelAngle=-15)),
                            y=alt.Y(
                                "Running Total (ml):Q",
                                title="Cumulative Volume (ml)",
                                scale=alt.Scale(domain=[0, max(int(goal * 1.12), int(df_h["Running Total (ml)"].max() * 1.08))]),
                            ),
                            tooltip=[
                                alt.Tooltip("#:O", title="Sip #"),
                                alt.Tooltip("Time:N", title="Logged Time"),
                                alt.Tooltip("Amount (ml):Q", title="Added (ml)"),
                                alt.Tooltip("Running Total (ml):Q", title="Running Total (ml)"),
                            ],
                        )
                        cum_area = cum_base.mark_area(opacity=0.16, color=T["accent"], interpolate="monotone")
                        cum_line = cum_base.mark_line(strokeWidth=3, color=T["accent"], interpolate="monotone")
                        cum_pts = cum_base.mark_circle(size=80, color=T["accent"], stroke=T["ink"], strokeWidth=1.5)
                        goal_rule = alt.Chart(goal_df).mark_rule(strokeDash=[6, 4], strokeWidth=2, color="#D97706").encode(
                            y="GoalTarget:Q",
                            tooltip=[alt.Tooltip("GoalLabel:N", title="Cohort Goal")],
                        )
                        cum_chart = (
                            (cum_area + cum_line + cum_pts + goal_rule)
                            .properties(height=225, padding={"top": 16, "left": 6, "right": 8, "bottom": 4})
                            .configure(background="transparent")
                            .configure_view(strokeWidth=0)
                            .configure_axis(labelColor=T["ink"], titleColor=T["muted"], gridColor=T["border"])
                        )
                        st.altair_chart(cum_chart, width="stretch")
                    else:
                        st.bar_chart(df_h.set_index("#")["Running Total (ml)"], color=T["accent"])

            st.markdown("**Chronological Hydration Dataset**")
            disp_cols = ["#", "Time", "Vessel / Source", "Sip Interval", "Period", "Amount (ml)", "Running Total (ml)"]
            if is_dark:
                max_run = max(goal, int(df_h["Running Total (ml)"].max()))
                rows_html = []
                for _, r in df_h[disp_cols].iterrows():
                    pct_w = min(100, int(round((int(r["Running Total (ml)"]) / max(1, max_run)) * 100)))
                    rows_html.append(
                        f"<tr><td>{int(r['#'])}</td><td>{html.escape(str(r['Time']))}</td>"
                        f"<td><strong>{html.escape(str(r['Vessel / Source']))}</strong></td>"
                        f"<td style='color:{T['muted']};'>{html.escape(str(r['Sip Interval']))}</td>"
                        f"<td><span style='background:{T['accent_soft']}; color:{T['accent']}; padding:2px 8px; border-radius:99px; font-size:0.75rem; font-weight:700;'>{html.escape(str(r['Period']))}</span></td>"
                        f"<td>+{int(r['Amount (ml)']):,} ml</td>"
                        f"<td><span class='wb-pbar'><span class='wb-pfill' style='width:{pct_w}%;'></span></span><strong>{int(r['Running Total (ml)']):,} ml</strong></td></tr>"
                    )
                render_html(
                    "<div class='wb-ledger-wrap'><table class='wb-ledger'>"
                    "<thead><tr><th>#</th><th>Time</th><th>Vessel / Source</th><th>Sip Interval</th><th>Period</th><th>Amount (ml)</th><th>Running Total (ml)</th></tr></thead>"
                    f"<tbody>{''.join(rows_html)}</tbody></table></div>"
                )
            else:
                st.dataframe(
                    df_h[disp_cols],
                    width="stretch",
                    hide_index=True,
                    column_config={
                        "Running Total (ml)": st.column_config.ProgressColumn(
                            "Running Total (ml)",
                            format="%d ml",
                            min_value=0,
                            max_value=max(goal, int(df_h["Running Total (ml)"].max())),
                        )
                    },
                )
            u1, u2 = st.columns(2)
            if u1.button("Undo Last Drink", width="stretch"):
                removed = st.session_state.intake_history.pop()
                st.session_state.total_intake = max(0, st.session_state.total_intake - removed["amount"])
                st.session_state.last_action = "undo"
                np = (st.session_state.total_intake / max(1, goal)) * 100
                st.session_state.recent_art = ("badge" if np >= 100 else "leaf" if np >= 50 else "drop") if st.session_state.intake_history else None
                st.rerun()
            u2.download_button("Export Intake CSV", df_h[disp_cols].to_csv(index=False).encode("utf-8"), f"waterbuddy_log_{date.today().isoformat()}.csv", "text/csv", width="stretch")
        else:
            st.caption("No drinks logged yet today. Use + Log Drink above or tap any vessel card.")

    # --------------------------------------------------------------------------
    # VIEW 2: WALL OF BADGES & HYDRO ART VAULT
    # --------------------------------------------------------------------------
    elif st.session_state.nav_view == "Wall of Badges":
        st.title("Wall of Badges & Hydration Milestones")
        st.caption("Unlocked milestones light up in coastal teal with 3D trophy emblems while pending goals await completion.")
        st.metric("Milestones Unlocked", f"{unlocked_cnt} of {len(badges)}", f"{int((unlocked_cnt / len(badges)) * 100)}% Complete")

        wb1, wb2 = st.columns(2, gap="large")
        for i, b in enumerate(badges):
            b_icon = render_badge_svg(b["id"], b["unlocked"])
            with (wb1 if i % 2 == 0 else wb2):
                if b["unlocked"]:
                    render_html(f"<div class='badge-on'><div style='display:flex; gap:1rem; align-items:center;'><div style='width:62px; height:62px; border-radius:16px; background:rgba(255,255,255,0.18); display:flex; align-items:center; justify-content:center; flex-shrink:0;'>{b_icon}</div><div><h3 style='margin:0;'>{b['name']}</h3><p style='margin:0.2rem 0; font-size:0.9rem;'>{b['desc']}</p><span style='background:rgba(255,255,255,0.22); font-weight:800; font-size:0.75rem; padding:0.2rem 0.65rem; border-radius:99px;'>UNLOCKED ({b['progress']})</span></div></div></div>")
                else:
                    render_html(f"<div class='badge-off'><div style='display:flex; gap:1rem; align-items:center;'><div style='width:62px; height:62px; border-radius:16px; background:{T['surface']}; border:1px solid {T['border']}; display:flex; align-items:center; justify-content:center; flex-shrink:0; color:{T['muted']};'>{b_icon}</div><div><h3 style='margin:0;'>{b['name']}</h3><p style='margin:0.2rem 0; font-size:0.9rem;'>{b['desc']}</p><span style='font-weight:700; font-size:0.75rem;'>LOCKED ({b['progress']})</span></div></div></div>")

        render_section_header("Procedural Vector Vault", "Hydro Art Collector Vault", f"Collect all 4 coastal emblems drawn in-memory by HeadlessTurtle + Pillow ({len(earned_arts)}/4 unlocked).")
        art_cols = st.columns(4, gap="medium")
        specs = [
            ("drop", "Crystal Droplet", "1st logged drink"),
            ("traveler", "Spring Hiker & Turtle", "Any 2+ logged drinks"),
            ("leaf", "Hydration Sprout", "Reach 50% daily goal"),
            ("badge", "Ocean Rosette", "Achieve 100% daily goal"),
        ]
        for col_a, (ak, ttl, dsc) in zip(art_cols, specs):
            unl = ak in earned_arts
            col_a.markdown(f"<div class='studio-panel' style='align-items:center; text-align:center; padding:1rem;'><img src='{image_to_data_uri(draw_vector_art(ak if unl else 'preview'))}' style='width:140px; height:140px;'/><div style='font-weight:800; font-size:0.86rem; margin-top:0.3rem;'>{ttl}</div><div style='font-size:0.76rem; color:{T['muted']};'>{'Unlocked • ' if unl else 'Locked • '}{dsc}</div></div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # VIEW 3: VESSEL & HYDRATION CALIBRATION STUDIO (Interactive 3D Edition)
    # --------------------------------------------------------------------------
    elif st.session_state.nav_view == "Vessel Studio":
        st.title("Vessel & Hydration Calibration Studio")
        st.caption("Interactive 3D beverage vessel studio and WHO / EFSA cohort personas calibrated to real daily routines.")

        banner_uri = load_asset_b64("vessels/vessels_banner_3d.png")
        if banner_uri:
            render_html(f"""
            <div style="background:{T['surface']}; border:1px solid {T['border']}; border-radius:22px; padding:1.1rem 1.5rem; margin-bottom:0.85rem; box-shadow:{T['shadow']}; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem;">
              <div style="flex:1 1 280px;">
                <div class="eyebrow">3D Fluid Reference Lineup</div>
                <div style="font-size:1.22rem; font-weight:800; color:{T['ink']}; margin-bottom:0.25rem;">Interactive Vessels &amp; Age Personas</div>
                <div style="font-size:0.86rem; color:{T['muted']}; line-height:1.5;">Tap any 3D container below to log water directly from this studio, or switch your active clinical age target on the right.</div>
              </div>
              <div style="flex:1 1 420px; text-align:center; {'background:rgba(235,246,249,0.94); border-radius:18px; padding:0.75rem 1rem;' if is_dark else ''}">
                <img src="{banner_uri}" alt="3D Hydration Vessels Lineup" style="width:100%; max-width:520px; height:auto; display:block; margin:0 auto; filter:drop-shadow(0 8px 16px rgba(15,41,51,0.12));"/>
              </div>
            </div>
            """)

        vc1, vc2 = st.columns(2, gap="large")
        with vc1:
            render_section_header("Capacities", "Beverage Vessel Ratios", "Real-world 3D containers with instant one-tap logging.")
            for v in VESSELS:
                r1, r2 = st.columns([1.85, 1.15], vertical_alignment="center")
                with r1:
                    render_html(f"<div class='interactive-card'>{render_vessel_svg(v['id'], 54, dark=is_dark)}<div style='flex:1;'><div style='display:flex; justify-content:space-between; align-items:baseline; gap:8px;'><strong>{v['name']}</strong><span style='font-weight:800; color:{T['accent']}; white-space:nowrap;'>{v['amount']} ml</span></div><div style='font-size:0.8rem; color:{T['muted']}; margin-top:0.15rem;'>{v['desc']} (~{v['amount'] / 250:.1f} cups)</div></div></div>")
                with r2:
                    if st.button(f"+{v['amount']} ml", key=f"studio_log_{v['id']}", width="stretch"):
                        if log_drink(v["amount"], v["name"], goal): st.balloons()
                        st.rerun()
        with vc2:
            render_section_header("Age Baselines", "Clinical Baselines (WHO / EFSA)", "Choose any 3D age cohort persona to apply its daily hydration goal.")
            for idx_c, (cn, ci) in enumerate(AGE_GOALS.items()):
                c_img_uri = load_asset_b64(ci["img"])
                avatar_block = f"<img src='{c_img_uri}' class='asset-3d' alt='{ci['tier']}' style='width:64px; height:64px; object-fit:contain; flex-shrink:0; filter:drop-shadow(0 6px 10px rgba(15,41,51,0.16));'/>" if c_img_uri else ""
                is_cur = (st.session_state.age_cohort == cn and goal == ci["goal"])
                b1, b2 = st.columns([2.05, 0.95], vertical_alignment="center")
                with b1:
                    render_html(f"<div class='interactive-card' style='border-color:{T['accent'] if is_cur else T['border']};'>{avatar_block}<div style='flex:1;'><div style='display:flex; justify-content:space-between; gap:8px;'><strong>{ci['tier']} • {cn.split(' (')[0]}</strong><span style='color:{T['accent']}; font-weight:800; white-space:nowrap;'>{ci['goal']:,} ml</span></div><p style='font-size:0.8rem; color:{T['muted']}; margin:0.2rem 0 0 0; line-height:1.38;'>{ci['fact']}</p></div></div>")
                with b2:
                    if st.button("Active" if is_cur else "Apply", key=f"studio_cohort_{idx_c}", type="primary" if is_cur else "secondary", disabled=is_cur, width="stretch"):
                        st.session_state.age_cohort = cn
                        st.session_state.daily_goal = ci["goal"]
                        st.session_state.last_action = "goal_change"
                        st.rerun()

render_html(f"<div style='text-align:center; color:{T['muted']}; font-size:0.8rem; padding:1.4rem 0 0.6rem 0;'><strong>WaterBuddy Daily Hydration Companion</strong> • IDAI 102 • Candidate: <strong>Parth Pravinbhai Gajera</strong> (1000544) • WellNest Technologies Pvt. Ltd.</div>")

# Dashboard-only motivational card with progress-aware, time-based quote rotation.
MOTIVATIONAL_QUOTES = [
    "First sip down. You’re off to a great start today.",
    "A glass of water this morning is the easiest win you’ll get all day.",
    "Before the day gets crazy, take a quick second for your first glass.",
    "A little water now will thank you when that afternoon slump hits.",
    "One glass down. Easy, simple, and already doing something good for yourself.",
    "You’re a quarter of the way there. Nice and steady.",
    "Brain feeling a little foggy? A quick glass of water usually helps.",
    "Your body is quietly thanking you for every glass right now.",
    "You’re almost halfway through today’s goal—keep doing what you’re doing.",
    "No rush, just steady sips. You’re building a really solid habit.",
    "Halfway there! Honestly, you’re making this look easy.",
    "Before you reach for another coffee, try a glass of water first.",
    "You’re over the halfway hump. Keep that good energy going.",
    "It really does add up, one glass at a time.",
    "Past the halfway mark—you’ve got plenty of time to finish strong.",
    "75% done. The finish line is right around the corner.",
    "Just a glass or two left and you’ve officially nailed today.",
    "You’re so close—finish off that last bit before you wind down for the night.",
    "Don't stop at 90% when you're this close to wrapping it up.",
    "One last pour and you’re completely done for the day.",
    "You did it! Your body is seriously feeling the love today.",
    "110%—you didn't just hit your goal, you went right past it.",
    "Three days in a row. Look at you showing up for yourself.",
    "A whole week of hitting your water goal. That’s something to feel proud of.",
    "100% done. One less thing to worry about today—great job.",
    "Having one of those busy days? Totally fine—just grab a quick sip when you can.",
    "Hey, it’s been a little while since your last glass. Take ten seconds for yourself.",
    "Forget about yesterday. Today’s a fresh start, one glass at a time.",
    "Even half a glass counts right now. Just do what you can.",
    "Take a quick breather, stretch your shoulders, and grab a sip of water",
]

@st.fragment(run_every="30s")
def render_motivational_quote():
    sip_count_for_quote = len(st.session_state.intake_history)
    quote_pct = (total / max(1, goal)) * 100
    hour_now = datetime.now().hour

    if quote_pct >= 110:
        quote_choices = [21]
    elif quote_pct >= 100:
        quote_choices = [20, 24]
    elif total <= 0:
        quote_choices = [27, 25, 29]
        if hour_now < 11:
            quote_choices.extend([1, 2])
    elif quote_pct < 25:
        quote_choices = [0, 2, 3, 4, 25, 28, 29]
        if hour_now < 11:
            quote_choices.append(1)
    elif quote_pct < 50:
        quote_choices = list(range(5, 10)) + [25, 28, 29]
    elif quote_pct < 75:
        quote_choices = list(range(10, 15)) + [25, 28, 29]
    else:
        quote_choices = list(range(15, 20)) + [25, 28, 29]
        if hour_now >= 19:
            quote_choices.append(17)

    if sip_count_for_quote and quote_pct < 100:
        try:
            last_sip_time = datetime.strptime(st.session_state.intake_history[-1].get("time", ""), "%I:%M %p")
            now_for_quote = datetime.now()
            last_sip_time = last_sip_time.replace(year=now_for_quote.year, month=now_for_quote.month, day=now_for_quote.day)
            if (now_for_quote - last_sip_time).total_seconds() >= 7200:
                quote_choices.append(26)
        except Exception:
            pass

    # Streak claims stay available but are not shown without verifiable multi-day history.
    rotation_slot = int(datetime.now().timestamp() // 30)
    quote_index = quote_choices[rotation_slot % len(quote_choices)]
    quote_text = html.escape(MOTIVATIONAL_QUOTES[quote_index])

    render_html(f"""
    <div style="margin-top:1.4rem; padding:1.1rem 1.35rem; border:1px solid {T['border']}; border-radius:20px; background:linear-gradient(115deg, {T['surface']} 0%, {T['soft']} 100%); box-shadow:{T['shadow']}; display:flex; align-items:center; gap:1rem;">
      <div style="width:44px; height:44px; flex:0 0 44px; border-radius:15px; display:flex; align-items:center; justify-content:center; color:{T['accent']}; background:{T['accent_soft']};">
        <svg width="22" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M12 2.5s7 7.1 7 12.2a7 7 0 1 1-14 0C5 9.6 12 2.5 12 2.5Z" fill="currentColor" opacity=".9"/><path d="M9 16.5c.4 1.1 1.3 1.8 2.6 2" fill="none" stroke="white" stroke-width="1.5" stroke-linecap="round"/></svg>
      </div>
      <div style="min-width:0;">
        <div style="font-size:.7rem; font-weight:800; letter-spacing:.09em; color:{T['accent']}; text-transform:uppercase; margin-bottom:.22rem;">A little encouragement</div>
        <div style="font-size:.96rem; line-height:1.5; font-weight:650; color:{T['ink']};">{quote_text}</div>
      </div>
    </div>
    """)

if st.session_state.nav_view == "Dashboard":
    render_motivational_quote()
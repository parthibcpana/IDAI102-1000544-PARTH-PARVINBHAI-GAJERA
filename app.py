import base64
import html
import io
import math
import random
from datetime import date, datetime
import pandas as pd
from PIL import Image, ImageDraw
import streamlit as st

try:
    import altair as alt
    HAS_ALTAIR = True
except ImportError:
    HAS_ALTAIR = False

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
    "6–12 years (Kids)": {"goal": 1600, "cups": 6.4, "tier": "Children", "fact": "Children turn over fluids rapidly due to high surface-to-mass ratios. Regular hydration prevents playground fatigue."},
    "13–18 years (Teens)": {"goal": 2000, "cups": 8.0, "tier": "Teens", "fact": "Rapid adolescent physical growth and athletic activity demand steady water intake for cognitive school focus."},
    "19–50 years (Adults)": {"goal": 2500, "cups": 10.0, "tier": "Adults", "fact": "Combats air-conditioned office screen fatigue. Mild 1-2% dehydration triggers tension headaches and brain fog."},
    "65+ years (Seniors)": {"goal": 1800, "cups": 7.2, "tier": "Seniors", "fact": "Age-related hypodipsia blunts natural thirst receptors. Scheduled routine sipping protects kidney and cardiovascular health."},
}

VESSELS = [
    {"id": "mug", "name": "Coffee Mug", "amount": 250},
    {"id": "glass", "name": "Water Glass", "amount": 250},
    {"id": "tumbler", "name": "Travel Tumbler", "amount": 350},
    {"id": "bottle", "name": "Sports Bottle", "amount": 500},
    {"id": "flask", "name": "Hydro Flask", "amount": 750},
]

def render_vessel_svg(v_id: str, size: int = 30) -> str:
    shapes = {
        "mug": '<path d="M5 7h11v10a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V7zm11 2h2.5a2.5 2.5 0 0 1 0 5H16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M8 4v1.5M12 4v1.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" opacity="0.65"/>',
        "glass": '<path d="M6.5 4h11l-1.4 16H7.9L6.5 4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M7.4 11h9.2l-.6 8.2H8L7.4 11z" fill="currentColor" opacity="0.22"/>',
        "tumbler": '<path d="M8 7h8l-1.1 13H9.1L8 7z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M7 7h10M12 7l2.2-4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M8.8 13h6.4l-.6 6.2H9.4z" fill="currentColor" opacity="0.22"/>',
        "bottle": '<path d="M9.5 3h5v2.8l2 2.4V19a2 2 0 0 1-2 2h-5a2 2 0 0 1-2-2V8.2l2-2.4V3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><rect x="8.5" y="11" width="7" height="7" rx="1" fill="currentColor" opacity="0.22"/><line x1="9" y1="5.5" x2="15" y2="5.5" stroke="currentColor" stroke-width="1.8"/>',
        "flask": '<rect x="7" y="6" width="10" height="15" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M9.5 6V4a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v2" fill="none" stroke="currentColor" stroke-width="1.8"/><rect x="8" y="11" width="8" height="8" rx="1" fill="currentColor" opacity="0.24"/>',
    }
    inner = shapes.get(v_id, shapes["glass"])
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="display:inline-block; color:#1A7887;">{inner}</svg>'

def render_badge_svg(b_id: str, unlocked: bool) -> str:
    if not unlocked:
        return '<svg width="36" height="36" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="display:block;"><rect x="5" y="11" width="14" height="10" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 11V7.5a4 4 0 0 1 8 0V11" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="16" r="1.4" fill="currentColor"/></svg>'
    icons = {
        "first_sip": '<path d="M12 20V11M12 13c0-4 3.5-6.5 7-6.5 0 4-2.5 7-7 6.5zM12 15c0-3.2-2.8-5.2-6-5.2 0 3.2 2.2 5.7 6 5.2z" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "steady_pacer": '<circle cx="12" cy="13" r="7.5" fill="none" stroke="#FFFFFF" stroke-width="2"/><path d="M12 9v4.2l2.8 1.6M9.5 3h5" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>',
        "halfway_hydrated": '<path d="M3 10c2.2-2 4.4-2 6.6 0s4.4 2 6.6 0 3.4-1.5 4.8 0M3 15.5c2.2-2 4.4-2 6.6 0s4.4 2 6.6 0 3.4-1.5 4.8 0" fill="none" stroke="#FFFFFF" stroke-width="2.1" stroke-linecap="round"/>',
        "hydro_champion": '<path d="M4 17l-1-9 5 4 4-6 4 6 5-4-1 9H4zm0 3h16" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>',
        "calibration_master": '<circle cx="12" cy="12" r="8.5" fill="none" stroke="#FFFFFF" stroke-width="2"/><circle cx="12" cy="12" r="4.5" fill="none" stroke="#FFFFFF" stroke-width="1.8"/><circle cx="12" cy="12" r="1.5" fill="#FFFFFF"/>',
    }
    return f'<svg width="36" height="36" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="display:block;">{icons.get(b_id, icons["first_sip"])}</svg>'

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
# ANIMATED SVG WATER BOTTLE & 5 HYDRATION MASCOTS
# ------------------------------------------------------------------------------

def render_animated_bottle_svg(progress_pct, total_ml, goal_ml, width=165, height=232):
    display_pct = max(0.0, float(progress_pct))
    fill_h = (min(100.0, display_pct) / 100.0) * 195
    water_y = 248 - fill_h
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 290" width="{width}" height="{height}" style="display:block; margin:0 auto;">
      <defs>
        <clipPath id="wb2-clip">
          <path d="M 74 44 L 126 44 C 128 54, 144 66, 152 82 L 152 232 C 152 248, 140 254, 122 254 L 78 254 C 60 254, 48 248, 48 232 L 48 82 C 56 66, 72 54, 74 44 Z"/>
        </clipPath>
      </defs>
      <style>
        @keyframes wb-wave {{ 0%, 100% {{ transform: translateX(0px); }} 50% {{ transform: translateX(-28px); }} }}
        .wb-wv {{ animation: wb-wave 4s ease-in-out infinite; }}
      </style>
      <rect x="76" y="14" width="48" height="14" rx="4" fill="#1A7887"/>
      <rect x="70" y="28" width="60" height="16" fill="#CFEAF0" stroke="#1A7887" stroke-width="1.8"/>
      <path d="M 74 44 L 126 44 C 128 54, 144 66, 152 82 L 152 232 C 152 248, 140 254, 122 254 L 78 254 C 60 254, 48 248, 48 232 L 48 82 C 56 66, 72 54, 74 44 Z" fill="#EDF7F9" stroke="#1A7887" stroke-width="2.6"/>
      <g clip-path="url(#wb2-clip)">
        <rect x="40" y="{water_y}" width="120" height="{fill_h + 26}" fill="#268C9C"/>
        <path class="wb-wv" d="M -20 {water_y} Q 30 {water_y - 5} 80 {water_y} T 180 {water_y} T 280 {water_y} L 280 270 L -20 270 Z" fill="#5EB3C2" opacity="0.68"/>
      </g>
      <path d="M 56 88 L 56 224" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.55"/>
      <rect x="64" y="150" width="72" height="44" rx="12" fill="rgba(15,41,51,0.78)"/>
      <text x="100" y="172" text-anchor="middle" fill="#FFFFFF" font-size="18" font-weight="900" font-family="sans-serif">{display_pct:.0f}%</text>
      <text x="100" y="187" text-anchor="middle" fill="#D5EFF4" font-size="9.2" font-weight="700" font-family="sans-serif">{total_ml:,} / {goal_ml:,} ml</text>
      <text x="100" y="276" text-anchor="middle" fill="#4D6B73" font-size="10.2" font-weight="700" font-family="sans-serif">Daily Hydration Chamber</text>
    </svg>
    """

def render_animated_avatar_svg(companion_str, mood="start", width=135, height=135):
    c_lower = companion_str.lower()
    c_type = "dolphin" if "dolphin" in c_lower else "otter" if "otter" in c_lower else "raindrop" if ("raindrop" in c_lower or "cloud" in c_lower) else "penguin" if "penguin" in c_lower else "turtle"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="{width}" height="{height}" style="max-width:100%; height:auto;"><style>@keyframes f-c {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }} .fg {{ animation: f-c 3.2s ease-in-out infinite; }}</style><g class="fg">"""

    if c_type == "dolphin":
        svg += """<path d="M 40 130 C 60 70, 120 50, 165 95 C 175 105, 185 110, 190 100 C 180 125, 150 145, 110 145 C 75 145, 50 140, 40 130 Z" fill="#1A7887" stroke="#114F59" stroke-width="2.4"/><path d="M 60 135 C 90 142, 125 140, 150 115 C 130 135, 95 140, 60 135 Z" fill="#E3F4F7"/><polygon points="105,62 120,40 128,64" fill="#1A7887" stroke="#114F59" stroke-width="2"/><polygon points="175,100 195,85 190,105 195,120" fill="#1A7887" stroke="#114F59" stroke-width="2"/><ellipse cx="85" cy="115" rx="18" ry="8" fill="#5EB3C2" transform="rotate(20 85 115)"/>"""
    elif c_type == "otter":
        svg += """<ellipse cx="100" cy="130" rx="46" ry="48" fill="#7D502D" stroke="#4D2F18" stroke-width="2.4"/><ellipse cx="100" cy="138" rx="30" ry="34" fill="#FAF0D2"/><circle cx="70" cy="46" r="10" fill="#7D502D"/><circle cx="130" cy="46" r="10" fill="#7D502D"/><ellipse cx="100" cy="68" rx="36" ry="30" fill="#91603A" stroke="#4D2F18" stroke-width="2.4"/><ellipse cx="100" cy="74" rx="20" ry="14" fill="#FAF0D2"/><polygon points="96,68 104,68 100,74" fill="#0F2933"/><circle cx="100" cy="120" r="12" fill="#5EB3C2" stroke="#1A7887" stroke-width="2"/>"""
    elif c_type == "raindrop":
        svg += """<path d="M 100 25 C 100 25, 45 95, 45 135 C 45 165, 70 185, 100 185 C 130 185, 155 165, 155 135 C 155 95, 100 25, 100 25 Z" fill="#268C9C" stroke="#135D69" stroke-width="2.8"/><path d="M 68 110 C 62 130, 70 160, 92 170 C 76 160, 68 135, 74 115 Z" fill="#E3F4F7" opacity="0.7"/>"""
    elif c_type == "penguin":
        svg += """<ellipse cx="100" cy="125" rx="46" ry="54" fill="#182B36" stroke="#0F1C24" stroke-width="2.4"/><ellipse cx="100" cy="132" rx="32" ry="42" fill="#FFFFFF"/><circle cx="100" cy="62" r="32" fill="#182B36"/><polygon points="94,64 106,64 100,76" fill="#D69838"/><ellipse cx="78" cy="172" rx="14" ry="7" fill="#D69838"/><ellipse cx="122" cy="172" rx="14" ry="7" fill="#D69838"/>"""
    else:
        svg += """<ellipse cx="60" cy="155" rx="14" ry="20" fill="#2C828E" stroke="#134C54" stroke-width="2" transform="rotate(-25 60 155)"/><ellipse cx="140" cy="155" rx="14" ry="20" fill="#2C828E" stroke="#134C54" stroke-width="2" transform="rotate(25 140 155)"/><ellipse cx="48" cy="95" rx="15" ry="25" fill="#4AA4B2" stroke="#134C54" stroke-width="2" transform="rotate(-30 48 95)"/><ellipse cx="152" cy="95" rx="15" ry="25" fill="#4AA4B2" stroke="#134C54" stroke-width="2" transform="rotate(30 152 95)"/><ellipse cx="100" cy="125" rx="52" ry="46" fill="#1A6470" stroke="#134C54" stroke-width="2.8"/><ellipse cx="100" cy="125" rx="40" ry="34" fill="#2C828E" stroke="#134C54" stroke-width="2"/><ellipse cx="100" cy="125" rx="24" ry="20" fill="#74BEC9" stroke="#1A6470" stroke-width="2"/><ellipse cx="100" cy="62" rx="26" ry="24" fill="#74BEC9" stroke="#134C54" stroke-width="2"/>"""

    if mood == "ecstatic":
        svg += """<rect x="74" y="52" width="22" height="12" rx="3" fill="#0F2933"/><rect x="104" y="52" width="22" height="12" rx="3" fill="#0F2933"/><line x1="96" y1="56" x2="104" y2="56" stroke="#0F2933" stroke-width="2.4"/><path d="M 88 70 Q 100 84 112 70" fill="none" stroke="#D69838" stroke-width="3.2" stroke-linecap="round"/>"""
    elif mood in ("happy", "energized"):
        svg += """<circle cx="88" cy="58" r="5" fill="#0F2933"/><circle cx="112" cy="58" r="5" fill="#0F2933"/><circle cx="86" cy="56" r="1.8" fill="#FFF"/><circle cx="110" cy="56" r="1.8" fill="#FFF"/><path d="M 88 68 Q 100 80 112 68" fill="none" stroke="#0F2933" stroke-width="3" stroke-linecap="round"/>"""
    else:
        svg += """<circle cx="88" cy="58" r="4.5" fill="#0F2933"/><circle cx="112" cy="58" r="4.5" fill="#0F2933"/><path d="M 90 68 Q 100 75 110 68" fill="none" stroke="#0F2933" stroke-width="2.5" stroke-linecap="round"/>"""

    return svg + "</g></svg>"

# ------------------------------------------------------------------------------
# CLOUD-SAFE HEADLESS TURTLE PILLOW GRAPHICS ENGINE (Coastal Teal & Sage)
# ------------------------------------------------------------------------------

class HeadlessTurtle:
    """Pure Python Turtle engine drawing on Pillow RGBA canvases without Tkinter."""
    def __init__(self, w=280, h=280):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)
        self.x, self.y, self.heading = w / 2, h / 2, 90
        self.down, self.color, self.width = True, (26, 120, 135, 255), 3

    def forward(self, d):
        rad = math.radians(self.heading)
        nx, ny = self.x + d * math.cos(rad), self.y - d * math.sin(rad)
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
        sl = (2 * math.pi * r * (abs(ext) / 360.0)) / steps
        for _ in range(steps):
            self.forward(sl)
            self.left(ext / steps)

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

def get_mascot_speech(companion_str, user_name, total_ml, goal_ml, pct, mood):
    c_name = companion_str.split()[0]
    fn = user_name.strip() if user_name.strip() else "Friend"
    if mood == "ecstatic":
        return f"Goal reached, {fn}! {total_ml:,} ml logged ({pct:.0f}%). {c_name} put on gold shades to celebrate!"
    if mood == "energized":
        return f"Nearly there, {fn} at {pct:.0f}% ({total_ml:,} ml). One refreshing glass finishes your daily goal."
    if mood == "happy":
        return f"Halfway milestone cleared, {fn}! Steady hydration keeps concentration sharp all afternoon."
    if mood == "attentive":
        return f"Nice momentum, {fn}! {total_ml:,} ml recorded ({pct:.0f}%). Keep your bottle close for calm, steady sips."
    return f"Welcome, {fn}. I am {c_name}. Log your first glass below or via + Log Drink at the top."

def log_drink(amount_ml: int, source_label: str, goal_ml: int, time_lbl: str = None):
    st.session_state.total_intake += int(amount_ml)
    st.session_state.intake_history.append({
        "id": len(st.session_state.intake_history) + 1,
        "time": time_lbl or datetime.now().strftime("%I:%M %p"),
        "vessel": source_label,
        "amount": int(amount_ml),
        "running_total": int(st.session_state.total_intake),
    })
    npct = (st.session_state.total_intake / max(1, goal_ml)) * 100.0
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
if "show_reset_confirm" not in st.session_state: st.session_state.show_reset_confirm = False
if "nav_view" not in st.session_state:
    qv = st.query_params.get("view")
    st.session_state.nav_view = "Wall of Badges" if qv == "badges" else ("Vessel Studio" if qv == "studio" else "Dashboard")

if "intake_history" not in st.session_state:
    st.session_state.intake_history = []
    st.session_state.total_intake = 0
    dm = st.query_params.get("demo")
    if dm in ["true", "1"]:
        for amt, lbl, tm in [(250, "Coffee Mug", "08:30 AM"), (350, "Travel Tumbler", "11:15 AM"), (500, "Sports Bottle", "02:40 PM")]:
            log_drink(amt, lbl, st.session_state.daily_goal, tm)
    elif dm == "full":
        st.session_state.daily_goal = 2000
        for amt, lbl, tm in [(250, "Water Glass", "08:00 AM"), (350, "Travel Tumbler", "10:15 AM"), (500, "Sports Bottle", "01:30 PM"), (750, "Hydro Flask", "04:45 PM"), (250, "1.0 Cup", "07:20 PM")]:
            log_drink(amt, lbl, st.session_state.daily_goal, tm)

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

  [data-testid="stDialog"] [role="dialog"], div[role="dialog"] {{
    background: var(--surface) !important; color: var(--ink) !important;
    border: 1px solid var(--border) !important; border-radius: 22px !important;
  }}
  [data-testid="stDialog"] button[aria-label="Close"], [data-testid="stDialog"] button[aria-label="Close"] svg,
  div[role="dialog"] button[aria-label="Close"] svg {{
    color: var(--ink) !important; fill: currentColor !important;
  }}
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

  .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {{
    background: var(--surface) !important; color: var(--ink) !important;
    border: 1px solid var(--border) !important; border-radius: 12px !important;
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

  .studio-grid {{
    display: grid; grid-template-columns: 1fr 1.38fr 1fr; gap: 18px;
    align-items: stretch; margin: 0.4rem 0 1.1rem 0;
  }}
  .studio-panel {{
    background: var(--surface); border: 1px solid var(--border); border-radius: 22px;
    padding: 1.25rem 1.35rem; box-shadow: var(--shadow);
    display: flex; flex-direction: column; justify-content: space-between;
  }}
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
    border-radius: 20px !important; padding: 1.05rem 1.15rem !important; box-shadow: var(--shadow) !important;
  }}
  [data-testid="stMetricValue"] * {{ color: var(--ink) !important; }}
  [data-testid="stMetricLabel"] * {{ color: var(--muted) !important; font-weight: 700 !important; font-size: 0.84rem !important; }}
  [data-testid="stMetricDelta"] {{
    background: var(--accent-soft) !important; border-radius: 99px !important;
    padding: 0.14rem 0.58rem !important; width: fit-content !important;
  }}
  [data-testid="stMetricDelta"] div, [data-testid="stMetricDelta"] span, [data-testid="stMetricDelta"] svg {{
    color: var(--accent) !important;
  }}
  .vessel-chip {{
    background: var(--surface); border: 1px solid var(--border); border-radius: 18px;
    padding: 0.7rem 0.45rem; text-align: center; height: 112px; margin-bottom: 0.45rem;
    display: flex; flex-direction: column; justify-content: center; box-shadow: var(--shadow);
  }}
  .badge-on {{
    background: #1A7887 !important; border-radius: 20px; padding: 1.15rem;
    color: #FFFFFF !important; margin-bottom: 0.85rem; box-shadow: 0 8px 24px rgba(26, 120, 135, 0.24);
  }}
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
        render_html(f"""
        <div class="studio-panel" style="align-items:center; text-align:center;">
          {render_animated_avatar_svg(in_avatar, "happy", 155, 155)}
          <div style="text-align:left; width:100%; font-size:0.88rem; line-height:1.6; color:{T['muted']};">
            <div class="eyebrow">Calm Hydration Suite</div>
            <div>• <strong>100% Session Memory:</strong> private local tracking with CSV &amp; report export</div>
            <div>• <strong>WHO / EFSA Baselines:</strong> calibrated across Kids, Teens, Adults &amp; Seniors</div>
            <div>• <strong>Hydro Art Rewards:</strong> unlock Droplet, Hiker &amp; Turtle, Sprout &amp; Rosette</div>
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

    st.session_state.mascot_mood = "ecstatic" if percentage >= 100 else "energized" if percentage >= 75 else "happy" if percentage >= 50 else "attentive" if percentage >= 25 else "start"

    with st.sidebar:
        render_html(f"""
        <div style="text-align:center; margin-bottom:0.8rem;">
          <div class="avatar-circle">{render_animated_avatar_svg(st.session_state.user_avatar, st.session_state.mascot_mood, 72, 72)}</div>
          <div style="font-size:1.12rem; font-weight:800; margin-top:0.5rem;">{html.escape(st.session_state.user_name)}</div>
          <div style="font-size:0.78rem; font-weight:700; color:{T['accent']};">{user_rank}</div>
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
        st.session_state.nav_view = st.radio("Navigation", nav_opts, index=nav_opts.index(st.session_state.nav_view) if st.session_state.nav_view in nav_opts else 0)
        dark_toggle = st.toggle("Deep Tide Dark Mode", value=st.session_state.dark_theme)
        if dark_toggle != st.session_state.dark_theme:
            st.session_state.dark_theme = dark_toggle
            st.rerun()

        st.markdown("---")
        st.caption(f"*{random.choice(HYDRATION_TIPS)}*")
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
                st.rerun()
            if rc2.button("Cancel", width="stretch"):
                st.session_state.show_reset_confirm = False
                st.rerun()

    # CLEAN TOP ACTION BAR WITH FIRST-VIEW "+ Log Drink" BUTTON
    h1, h2 = st.columns([1.45, 1.75])
    with h1:
        render_html(f"""
        <div class="nav-head">
          <div>
            <span style="font-size:1.45rem; font-weight:900; letter-spacing:-0.4px; color:{T['ink']};">WaterBuddy</span>
            <span style="font-size:0.86rem; color:{T['muted']}; margin-left:0.6rem;"><strong>{html.escape(st.session_state.user_name)}</strong> • {total:,} / {goal:,} ml</span>
          </div>
          <span class="rank-pill">{user_rank}</span>
        </div>
        """)
    with h2:
        b_log, b1, b2, b3 = st.columns([1.1, 0.9, 1.0, 1.0])
        if b_log.button("+ Log Drink", type="primary", width="stretch", key="top_log_drink_btn"):
            open_custom_drink_dialog(goal)
        if b1.button("● Dashboard" if st.session_state.nav_view == "Dashboard" else "Dashboard", type="secondary", width="stretch", key="nav_dash"):
            st.session_state.nav_view = "Dashboard"
            st.rerun()
        if b2.button(f"{'● ' if st.session_state.nav_view == 'Wall of Badges' else ''}Badges ({unlocked_cnt}/{len(badges)})", type="secondary", width="stretch", key="nav_badges"):
            st.session_state.nav_view = "Wall of Badges"
            st.rerun()
        if b3.button("● Vessels" if st.session_state.nav_view == "Vessel Studio" else "Vessels", type="secondary", width="stretch", key="nav_vessels"):
            st.session_state.nav_view = "Vessel Studio"
            st.rerun()

    # --------------------------------------------------------------------------
    # VIEW 1: DASHBOARD
    # --------------------------------------------------------------------------
    if st.session_state.nav_view == "Dashboard":
        c_short = st.session_state.user_avatar.split()[0]
        speech_msg = get_mascot_speech(st.session_state.user_avatar, st.session_state.user_name, total, goal, percentage, st.session_state.mascot_mood)
        active_art = st.session_state.recent_art or "preview"
        art_img = draw_vector_art(active_art)
        art_uri = image_to_data_uri(art_img)
        art_labels = {"preview": "Spring Seed (Log sip to unlock)", "drop": "Crystal Water Droplet", "leaf": "Hydration Sprout", "traveler": "Walker Man & Turtle", "badge": "Ocean Championship Rosette"}
        locked_b = [b for b in badges if not b["unlocked"]]
        next_b_lbl = "All 5 Badges Complete!" if not locked_b else f"Next: {locked_b[0]['name']} ({locked_b[0]['progress']})"
        next_b_pct = 100 if not locked_b else locked_b[0]["pct"]

        render_html(f"""
        <div class="studio-grid">
          <div class="studio-panel">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span class="eyebrow">Fluid Chamber</span>
              <span style="font-size:0.78rem; font-weight:700; color:{T['muted']};">{percentage:.0f}% filled</span>
            </div>
            {render_animated_bottle_svg(percentage, total, goal, 165, 224)}
            <div class="soft-bar"><div class="soft-fill" style="width:{min(100, int(percentage))}%;"></div></div>
          </div>

          <div class="studio-panel">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span class="eyebrow">Companion Coach</span>
              <span style="font-size:0.75rem; font-weight:700; color:{T['accent']};">{len(st.session_state.intake_history)} sips today</span>
            </div>
            <div style="display:flex; align-items:center; gap:1rem; margin:0.4rem 0;">
              <div style="flex:0 0 116px; text-align:center;">{render_animated_avatar_svg(st.session_state.user_avatar, st.session_state.mascot_mood, 116, 116)}</div>
              <div style="background:{T['soft']}; border-radius:16px; padding:0.9rem 1rem; font-size:0.86rem; line-height:1.45; flex:1;">
                <div style="font-weight:800; color:{T['accent']}; margin-bottom:0.2rem;">{c_short} says:</div>
                "{html.escape(speech_msg)}"
              </div>
            </div>
            <div style="border-top:1px solid {T['border']}; padding-top:0.55rem;">
              <div style="display:flex; justify-content:space-between; font-size:0.78rem; font-weight:700;">
                <span>{next_b_lbl}</span><span style="color:{T['accent']};">{next_b_pct}%</span>
              </div>
              <div class="soft-bar"><div class="soft-fill" style="width:{next_b_pct}%;"></div></div>
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
            _, dlc = st.columns([2.2, 1.0])
            dlc.download_button("Download Earned Artwork (.png)", image_to_png_bytes(art_img), f"waterbuddy_{active_art}.png", "image/png", width="stretch")

        # 4 KPI METRICS
        delta_std = goal - std_baseline
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Water Logged", f"{total:,} ml", f"{percentage:.1f}% of goal")
        k2.metric("Daily Target", f"{goal:,} ml", f"~{goal / 250:.1f} standard cups")
        k3.metric("Remaining to Go", f"{remaining:,} ml", "Target Achieved" if remaining == 0 else f"~{remaining / 250:.1f} cups left")
        k4.metric("WHO Baseline", f"{std_baseline:,} ml", f"{delta_std:+} ml vs cohort" if delta_std != 0 else "Matched baseline")

        # RAPID VESSELS
        render_section_header("Rapid Vessels", "Log by Everyday Container", "One-tap logging calibrated to real-world glass and bottle capacities.")
        v_cols = st.columns(len(VESSELS))
        for idx, v in enumerate(VESSELS):
            with v_cols[idx]:
                render_html(f"<div class='vessel-chip'><div>{render_vessel_svg(v['id'], 30)}</div><div style='font-weight:700; font-size:0.82rem; margin-top:0.15rem;'>{v['name']}</div><div style='font-size:0.78rem; color:{T['accent']}; font-weight:800;'>+{v['amount']} ml</div></div>")
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

        # CHRONOLOGICAL LEDGER + INTAKE PACE CHART
        render_section_header("History & Analytics", "Today's Hydration Ledger & Progression", "Inspect intake pacing across drinks today or undo/export your log.")
        if st.session_state.intake_history:
            df_h = pd.DataFrame(st.session_state.intake_history)[["id", "time", "vessel", "amount", "running_total"]]
            df_h.columns = ["#", "Time", "Vessel / Source", "Amount (ml)", "Running Total (ml)"]
            c_left, c_right = st.columns([1.05, 1.35], gap="large")
            with c_left:
                st.markdown("**Cumulative Hydration Trajectory**")
                if HAS_ALTAIR:
                    chart = alt.Chart(df_h).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, color=T["accent"]).encode(
                        x=alt.X("#:O", title="Sip Entry #"),
                        y=alt.Y("Running Total (ml):Q", title="Cumulative Volume (ml)"),
                        tooltip=["Time:N", "Vessel / Source:N", "Amount (ml):Q", "Running Total (ml):Q"],
                    ).configure(background="transparent").configure_axis(labelColor=T["ink"], titleColor=T["muted"], gridColor=T["border"]).properties(height=240)
                    st.altair_chart(chart, width="stretch")
                else:
                    st.bar_chart(df_h.set_index("#")["Running Total (ml)"], color=T["accent"])
            with c_right:
                st.dataframe(df_h, width="stretch", hide_index=True, column_config={"Running Total (ml)": st.column_config.ProgressColumn("Running Total (ml)", format="%d ml", min_value=0, max_value=max(goal, int(df_h["Running Total (ml)"].max())))})
                u1, u2 = st.columns(2)
                if u1.button("Undo Last Drink", width="stretch"):
                    removed = st.session_state.intake_history.pop()
                    st.session_state.total_intake = max(0, st.session_state.total_intake - removed["amount"])
                    np = (st.session_state.total_intake / max(1, goal)) * 100
                    st.session_state.recent_art = ("badge" if np >= 100 else "leaf" if np >= 50 else "drop") if st.session_state.intake_history else None
                    st.rerun()
                u2.download_button("Export Intake CSV", df_h.to_csv(index=False).encode("utf-8"), f"waterbuddy_log_{date.today().isoformat()}.csv", "text/csv", width="stretch")
        else:
            st.caption("No drinks logged yet today. Use + Log Drink above or tap any vessel card.")

    # --------------------------------------------------------------------------
    # VIEW 2: WALL OF BADGES & HYDRO ART VAULT
    # --------------------------------------------------------------------------
    elif st.session_state.nav_view == "Wall of Badges":
        st.title("Wall of Badges & Hydration Milestones")
        st.caption("Unlocked milestones light up in coastal teal while pending milestones stay quiet gray until earned.")
        st.metric("Milestones Unlocked", f"{unlocked_cnt} of {len(badges)}", f"{int((unlocked_cnt / len(badges)) * 100)}% Complete")

        wb1, wb2 = st.columns(2, gap="large")
        for i, b in enumerate(badges):
            b_icon = render_badge_svg(b["id"], b["unlocked"])
            with (wb1 if i % 2 == 0 else wb2):
                if b["unlocked"]:
                    render_html(f"<div class='badge-on'><div style='display:flex; gap:1rem; align-items:center;'><div style='width:52px; height:52px; border-radius:14px; background:rgba(255,255,255,0.16); display:flex; align-items:center; justify-content:center; flex-shrink:0;'>{b_icon}</div><div><h3 style='margin:0;'>{b['name']}</h3><p style='margin:0.2rem 0; font-size:0.9rem;'>{b['desc']}</p><span style='background:rgba(255,255,255,0.22); font-weight:800; font-size:0.75rem; padding:0.2rem 0.65rem; border-radius:99px;'>UNLOCKED ({b['progress']})</span></div></div></div>")
                else:
                    render_html(f"<div class='badge-off'><div style='display:flex; gap:1rem; align-items:center;'><div style='width:52px; height:52px; border-radius:14px; background:{T['surface']}; border:1px solid {T['border']}; display:flex; align-items:center; justify-content:center; flex-shrink:0; color:{T['muted']};'>{b_icon}</div><div><h3 style='margin:0;'>{b['name']}</h3><p style='margin:0.2rem 0; font-size:0.9rem;'>{b['desc']}</p><span style='font-weight:700; font-size:0.75rem;'>LOCKED ({b['progress']})</span></div></div></div>")

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
    # VIEW 3: VESSEL & HYDRATION CALIBRATION STUDIO
    # --------------------------------------------------------------------------
    elif st.session_state.nav_view == "Vessel Studio":
        st.title("Vessel & Hydration Calibration Studio")
        st.caption("Reference beverage vessel capacities and WHO / EFSA daily fluid recommendations.")
        vc1, vc2 = st.columns(2, gap="large")
        with vc1:
            render_section_header("Capacities", "Beverage Vessel Ratios", "Real-world volumes mapped to quick-log pills.")
            for v in VESSELS:
                render_html(f"<div style='background:{T['surface']}; border:1px solid {T['border']}; border-radius:16px; padding:0.85rem 1.1rem; margin-bottom:0.55rem; display:flex; justify-content:space-between; align-items:center;'><div style='display:flex; align-items:center; gap:0.65rem;'>{render_vessel_svg(v['id'], 24)}<strong>{v['name']}</strong></div><span style='font-weight:800; color:{T['accent']};'>{v['amount']} ml (~{v['amount'] / 250:.1f} cups)</span></div>")
        with vc2:
            render_section_header("Age Baselines", "Clinical Baselines (WHO / EFSA)", "Recommended daily baseline before personal climate adjustment.")
            for cn, ci in AGE_GOALS.items():
                render_html(f"<div style='background:{T['surface']}; border:1px solid {T['border']}; border-radius:16px; padding:0.85rem 1.1rem; margin-bottom:0.55rem;'><div style='display:flex; justify-content:space-between;'><strong>{ci['tier']} ({cn})</strong><span style='color:{T['accent']}; font-weight:800;'>{ci['goal']:,} ml/day</span></div><p style='font-size:0.84rem; color:{T['muted']}; margin:0.25rem 0 0 0;'>{ci['fact']}</p></div>")

render_html(f"<div style='text-align:center; color:{T['muted']}; font-size:0.8rem; padding:1.4rem 0 0.6rem 0;'><strong>WaterBuddy Daily Hydration Companion</strong> • IDAI 102 • Candidate: <strong>Parth Pravinbhai Gajera</strong> (1000544) • WellNest Technologies Pvt. Ltd.</div>")

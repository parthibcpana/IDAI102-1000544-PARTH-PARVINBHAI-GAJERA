<div align="center">

# WaterBuddy: Your Daily Hydration Companion
### *Simple, Calibrated Hydration Tracking & Visual Habit Companion*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://waterbuddy-parth-gajera.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-1A7887.svg)](https://www.python.org/)
[![Framework: Streamlit](https://img.shields.io/badge/framework-Streamlit%201.35+-FF4B4B.svg)](https://streamlit.io/)
[![Charts: Altair](https://img.shields.io/badge/charts-Altair%205+-1A7887.svg)](https://altair-viz.github.io/)
[![Design: Human--Centered](https://img.shields.io/badge/design-Human--Centered-8B5CF6.svg)]()
[![Theme: Coastal%20Oasis](https://img.shields.io/badge/theme-Coastal%20Oasis-1A7887.svg)]()

</div>

> **Course:** Artificial Intelligence: Real-World Applications & Implications  
> **Course Code:** `IDAI 102` (Python Programming)  
> **Assignment Title:** Design 'WaterBuddy': Your Daily Hydration Companion  
> **Type of Assessment:** Formative Assessment 2 (FA-2: Developing and Deploying App Using Python)  
> **Scenario Track:** WellNest Technologies Pvt. Ltd. | Hydration Habit System  
> **Student Developer:** Parth Pravinbhai Gajera (Candidate ID: `1000544`)  
> **Project Partner:** Subhan Syed  
> **School / Institutional Partner:** Aspee Nutan Academy / WACP International  
> **Foundational Planning Atlas:** [Canva Visual Atlas ID: DAHars3Lfk4](https://www.canva.com/design/DAHars3Lfk4/1NikvoNTGVTVM2JzmDzuBQ/edit)  
> **Live Interactive Application:** [https://waterbuddy-parth-gajera.streamlit.app/](https://waterbuddy-parth-gajera.streamlit.app/)  
> **GitHub Repository URL:** [https://github.com/parthibcpana/IDAI102-1000544-PARTH-PARVINBHAI-GAJERA](https://github.com/parthibcpana/IDAI102-1000544-PARTH-PARVINBHAI-GAJERA)

---

## Table of Contents

1. [Project Purpose & Student Learning Journey](#1-project-purpose--student-learning-journey)
2. [Intended Learning Outcomes: Knowledge Acquired & Practical Evidence](#2-intended-learning-outcomes-knowledge-acquired--practical-evidence)
3. [Problem Understanding & Clinical Hydration Baselines (WHO / EFSA)](#3-problem-understanding--clinical-hydration-baselines-who--efsa)
4. [System Architecture & Core Logic Flow](#4-system-architecture--core-logic-flow)
5. [Interface Architecture & Live Screenshot Gallery](#5-interface-architecture--live-screenshot-gallery)
6. [Animated Fluid Chamber & Companion Coach Engine](#6-animated-fluid-chamber--companion-coach-engine)
7. [Five Companion Spirit Mascots & Reactive States](#7-five-companion-spirit-mascots--reactive-states)
8. [Cloud-Safe Headless Turtle Vector Art Vault (Pillow)](#8-cloud-safe-headless-turtle-vector-art-vault-pillow)
9. [Living Wall of Badges & Habit Milestones](#9-living-wall-of-badges--habit-milestones)
10. [Rapid Vessel Logging, Cup Converter & Hydration Ledger](#10-rapid-vessel-logging-cup-converter--hydration-ledger)
11. [Verification & Multi-Scenario Test Proof](#11-verification--multi-scenario-test-proof)
12. [Deployment & Local Installation Guide](#12-deployment--local-installation-guide)
13. [System Standards & Technical Alignment](#13-system-standards--technical-alignment)
14. [Academic Integrity Statement](#14-academic-integrity-statement)

---

## 1. Project Purpose & Student Learning Journey

WaterBuddy transforms our FA-1 conceptual storyboard into a live, privacy-first Streamlit web app that helps people track daily water intake without noisy alarms or generic "8 glasses for everyone" rules. Users set an age-calibrated daily fluid target, log drinks in one click via real container cards or the first-view `+ Log Drink` modal, watch their companion spirit and animated water chamber respond live, and collect custom vector badges and artwork.

### What We Built Around the User Brief
1. **Age-Calibrated Baselines:** Instead of a one-size-fits-all target, WaterBuddy tailors daily fluid goals across four age groups (Kids, Teens, Adults, Seniors) with an adjustable fine-tuner.
2. **Low-Friction First-View Logging:** A prominent `+ Log Drink` button at the top right lets any returning user record a drink immediately without scrolling past charts.
3. **Calm Visual Feedback:** Pure CSS fluid wave motion, subtle droplet dividers, and five expressive mascot companions replace nagging push alerts.
4. **Cloud-Safe Procedural Art:** Standard Python `turtle` crashes on Linux cloud servers lacking a display (`TclError: no display name`), so we built an in-memory `HeadlessTurtle` engine on Pillow.

```mermaid
flowchart TD
    subgraph Core_Mission ["WaterBuddy Core Functional Mission"]
        M1["Age-Based Goals: Calibrate daily targets across 4 cohorts (1,600 ml to 2,500 ml)"]
        M2["One-Tap Vessels: Log 5 real containers (250 ml to 750 ml) with custom SVG silhouettes"]
        M3["Quick Modal + Cup Converter: Record exact ml via top CTA modal or 250 ml cup steps"]
        M4["Live Visual Studio: Animated SVG water bottle, 5 companion mascots & Hero Art preview"]
        M5["Badges & Headless Art: 5 milestone cards + 4 Pillow vector emblems unlocked live"]
        M6["Private Session History: In-memory log with Altair progression chart, Undo & CSV export"]
    end
```

---

## 2. Intended Learning Outcomes: Knowledge Acquired & Practical Evidence

| Intended Learning Outcome | What I Learned | How I Applied It in WaterBuddy |
| :--- | :--- | :--- |
| **ILO 1: Modular Python Applications** | Breaking formatting, calculations, graphics, and UI state into small helper functions makes debugging and UI refreshes far faster. | Structured [app.py](app.py) into discrete helpers (`calculate_progress`, `render_coastal_spring_svg`, `render_animated_bottle_svg`, `HeadlessTurtle`, `draw_vector_art`, `evaluate_badges`, `log_drink`, `open_custom_drink_dialog`). |
| **ILO 2: Real-Time Data Processing** | Storing structured intake dictionaries inside `st.session_state` keeps totals, Altair charts, badge thresholds, and undo actions synchronized automatically. | Built an instant `intake_history` list storing `id`, `time`, `vessel`, `amount`, and cumulative `running_total` so KPI cards, Altair bars, and the ledger update together. |
| **ILO 3: Interactive Streamlit Web Interface** | A calm, cohesive color token table, modal dialogs, and `.streamlit/config.toml` prevent harsh contrast clashes across light mode, dark mode, and mobile screens. | Configured Coastal Oasis Light default + Deep Tide Dark toggle, top-bar `+ Log Drink` `@st.dialog` modal, equal-height 3-panel Hero Studio, and `@media (max-width: 920px)` phone stacking. |
| **ILO 4: Creative Visual Elements** | Base64-encoded SVG art and Pillow trigonometric turtle geometry eliminate OS display dependencies and render crisply across Windows, macOS, and cloud Linux. | Created a panoramic coastal waterfall welcome scene with hiker man and sea turtle, bespoke SVG vessel and badge icons, and a 4-piece `HeadlessTurtle` art vault. |
| **ILO 5: Public Cloud Deployment** | Pinning minimal libraries in `requirements.txt` and shipping `.streamlit/config.toml` keeps cloud builds fast and theme-accurate on first visit. | Deployed `app.py`, `requirements.txt`, and `.streamlit/config.toml` publicly on [Streamlit Community Cloud](https://waterbuddy-parth-gajera.streamlit.app/). |

---

## 3. Problem Understanding & Clinical Hydration Baselines (WHO / EFSA)

Generic reminders tell a 9-year-old child, an office adult, and a senior over 65 to drink the exact same 2,000 ml target. From observing friends, students, and older family members, we noticed two practical gaps: busy people forget how much their own bottle holds (`350 ml` tumbler vs. `750 ml` flask), and older adults often ignore mild thirst until fatigue or headaches start. WaterBuddy maps age cohorts from World Health Organization (WHO) and European Food Safety Authority (EFSA) guidance directly onto everyday container sizes.

```mermaid
flowchart TD
    CohortSelect["Age Cohort Calibration"] --> C1["Children (6-12 years)<br>Target: 1,600 ml / 6.4 cups"]
    CohortSelect --> C2["Teens (13-18 years)<br>Target: 2,000 ml / 8.0 cups"]
    CohortSelect --> C3["Adults (19-50 years)<br>Target: 2,500 ml / 10.0 cups"]
    CohortSelect --> C4["Seniors (65+ years)<br>Target: 1,800 ml / 7.2 cups"]
```

### 3.1 Age Cohort Reference Matrix

| Age Cohort | Baseline Goal | Equivalent Cups (250 ml) | Practical Hydration Context |
| :--- | :---: | :---: | :--- |
| **Children (6 to 12 years)** | **1,600 ml** | 6.4 cups | Active kids lose fluids quickly during play and school sports, needing smaller frequent refills. |
| **Teens (13 to 18 years)** | **2,000 ml** | 8.0 cups | Growth spurts and afternoon classes call for steady water intake to avoid late-day fatigue. |
| **Adults (19 to 50 years)** | **2,500 ml** | 10.0 cups | Counters dry air-conditioned offices and long screen hours where even mild dehydration causes brain fog. |
| **Seniors (65+ years)** | **1,800 ml** | 7.2 cups | Natural thirst signals soften with age, so steady routine sipping protects energy and kidney comfort. |

---

## 4. System Architecture & Core Logic Flow

Whenever a user clicks a vessel button, submits the `+ Log Drink` modal, or uses the Cup Converter, one shared `log_drink()` pipeline updates totals, redraws the fluid chamber, shifts companion mood, updates Altair chart data, and unlocks badges and vector artwork.

```mermaid
flowchart LR
    Input["Tap Vessel / + Log Drink Modal / Cup Converter"] --> Validate["Validate 10 ml to 2,500 ml"]
    Validate --> State["Update total_intake & Append intake_history"]
    State --> Calc["Compute Progress % & Remaining Deficit"]
    Calc --> Visuals["Resize Bottle Water Fill & Update Companion Mood"]
    Calc --> Rewards["Check 5 Badges & Unlock 4 Pillow Vector Artworks"]
    State --> Analytics["Refresh Altair Trajectory Bar Chart & Progress Table"]
```

### 4.1 Simple Formulas & Real-World Examples

Every formula runs directly in Python inside `calculate_progress()` and `render_animated_bottle_svg()` with transparent numbers:

1. **Daily Progress Percentage:**  
   `Progress % = (Logged ml / Daily Goal ml) x 100`  
   *Example:* Logging `1,100 ml` out of a `2,500 ml` adult goal equals `(1100 / 2500) x 100 = 44.0%`.

2. **Remaining Water Needed:**  
   `Remaining ml = max(0, Daily Goal ml - Logged ml)`  
   *Example:* At `1,100 ml` logged toward `2,500 ml`, you have `1,400 ml` remaining (about `5.6` standard 250 ml cups).

3. **Cup-to-Milliliter Conversion:**  
   `Added ml = Cups x 250`  
   *Example:* Sliding the Cup Converter to `1.5` cups converts immediately to `375 ml`.

4. **SVG Fluid Fill Height:**  
   `Fill Height (px) = (min(100, Progress %) / 100) x 195` and `Water Top Y = 248 - Fill Height`  
   *Example:* At `44%`, water rises `85.8 px` inside the `195 px` glass chamber (`Y = 162.2`), keeping percentage text legible at every height.

### 4.2 Session State Schema (`st.session_state`)

```python
st.session_state = {
    "onboarded": bool,           # Separates Welcome Landscape from the Main Dashboard
    "dark_theme": bool,          # False = Coastal Oasis Light (default), True = Deep Tide Dark
    "nav_view": str,             # "Dashboard" | "Wall of Badges" | "Vessel Studio"
    "user_name": str,            # Personalized greeting and sidebar header name
    "user_avatar": str,          # Selected companion key from COMPANIONS
    "age_cohort": str,           # Selected age bracket from AGE_GOALS
    "daily_goal": int,           # Personalized daily volume target in ml
    "total_intake": int,         # Running cumulative water total for today
    "intake_history": list,      # [{"id", "time", "vessel", "amount", "running_total"}]
    "recent_art": str | None,    # Latest earned HeadlessTurtle key ("drop"|"traveler"|"leaf"|"badge")
    "mascot_mood": str,          # "start"|"attentive"|"happy"|"energized"|"ecstatic"
    "show_reset_confirm": bool,  # Two-step daily reset guard flag
}
```

---

## 5. Interface Architecture & Live Screenshot Gallery

WaterBuddy follows our 5-screen Canva Visual Atlas (`DAHars3Lfk4`) across an onboarding gateway and three live sidebar-switchable views:

```mermaid
flowchart TD
    S1["Welcome Gateway<br>(Panoramic Coastal Waterfall SVG + Cohort Config)"] -->|Enter Dashboard| S2["Dashboard Studio<br>(+ Log Drink Modal CTA, 3-Card Hero, KPIs & Rapid Vessels)"]
    S2 --> S3["Precision Converter & Analytics<br>(Altair Trajectory Bar Chart, Ledger & CSV Export)"]
    S2 --> S4["Wall of Badges<br>(5 Habit Badges + 4-Piece HeadlessTurtle Vault)"]
    S2 --> S5["Vessel & Calibration Studio<br>(5 Custom SVG Containers + WHO/EFSA Age Guide)"]
```

### 5.1 Welcome & Onboarding Landscape (`onboarding_v2.png`)
The opening screen pairs a custom base64-encoded coastal waterfall SVG scene (featuring alpine ridges, animated cascading falls, coastal coral lighthouse, reeds, a hydrated hiker holding a teal bottle, and HydroBuddy the Sea Turtle) with cohort calibration and live companion preview.

<div align="center">
<img src="assets/screenshots/onboarding_v2.png" alt="Screen 1: Coastal Spring Welcome & Onboarding Gateway" width="850" style="border-radius: 12px; border: 1.5px solid #1A7887; box-shadow: 0 8px 24px rgba(15,41,51,0.12);"/>
<p><em>Figure 1: Coastal Oasis Light welcome screen with animated waterfall horizon art, hiker & turtle companions, cohort calibration, and Calm Hydration Suite summary.</em></p>
</div>

### 5.2 Main Dashboard Studio Light Mode (`dashboard_v2.png`)
The top action bar keeps the primary `+ Log Drink` button in first view alongside quick tab pills (`Dashboard`, `Badges`, `Vessels`), above an equal-height 3-panel Hero Studio (`Fluid Chamber`, `Companion Coach`, `Hydro Art Vault`), four KPI cards, and one-tap bespoke SVG vessel chips.

<div align="center">
<img src="assets/screenshots/dashboard_v2.png" alt="Screen 2: Dashboard Studio in Coastal Oasis Light Mode" width="850" style="border-radius: 12px; border: 1.5px solid #1A7887; box-shadow: 0 8px 24px rgba(15,41,51,0.12);"/>
<p><em>Figure 2: Coastal Oasis Light Dashboard showing the equal-height 3-panel Hero Studio, first-view + Log Drink CTA, 4 KPI metrics, and custom SVG vessel logging chips.</em></p>
</div>

### 5.3 Deep Tide Dark Mode at 105% Goal (`dashboard_dark_v1.png`)
Toggling Deep Tide Dark Mode adapts every card surface, divider ornament, Altair chart axis, modal dialog, and vessel icon cleanly to low-glare coastal slate (`#101B21`), while showing HydroBuddy's celebratory gold sunglasses and the unlocked Ocean Championship Rosette.

<div align="center">
<img src="assets/screenshots/dashboard_dark_v1.png" alt="Screen 3: Deep Tide Dark Mode at 105% Goal" width="850" style="border-radius: 12px; border: 1.5px solid #1A7887; box-shadow: 0 8px 24px rgba(0,0,0,0.3);"/>
<p><em>Figure 3: Deep Tide Dark Mode showcasing adaptive surface contrast, ecstatic companion sunglasses state, and Ocean Championship Rosette reward.</em></p>
</div>

### 5.4 Wall of Badges & Hydro Art Collector Vault (`badges_v2.png`)
Unlocked milestones illuminate in deep coastal teal (`#1A7887`) with crisp white custom vector icons alongside the 4-piece Pillow `HeadlessTurtle` Collector Vault (`Crystal Droplet`, `Spring Hiker & Turtle`, `Hydration Sprout`, and `Ocean Rosette`).

<div align="center">
<img src="assets/screenshots/badges_v2.png" alt="Screen 4: Wall of Badges & Hydro Art Vault" width="850" style="border-radius: 12px; border: 1.5px solid #1A7887; box-shadow: 0 8px 24px rgba(15,41,51,0.12);"/>
<p><em>Figure 4: Living Wall of Badges at 5 of 5 Complete plus all 4 unlocked procedural artworks rendered in-memory by HeadlessTurtle + Pillow.</em></p>
</div>

### 5.5 Vessel & Hydration Calibration Studio (`vessel_studio_v1.png`)
Reference studio comparing all five container silhouettes (`Coffee Mug`, `Water Glass`, `Travel Tumbler`, `Sports Bottle`, `Hydro Flask`) directly beside age-calibrated fluid targets.

<div align="center">
<img src="assets/screenshots/vessel_studio_v1.png" alt="Screen 5: Vessel & Hydration Calibration Studio" width="850" style="border-radius: 12px; border: 1.5px solid #1A7887; box-shadow: 0 8px 24px rgba(15,41,51,0.12);"/>
<p><em>Figure 5: Vessel & Hydration Calibration Studio displaying standardized container volumes alongside WHO / EFSA cohort baselines.</em></p>
</div>

---

## 6. Animated Fluid Chamber & Companion Coach Engine

In place of flat horizontal progress bars, WaterBuddy pairs two synced hero modules inside an equal-height CSS grid (`studio-grid`):

```mermaid
flowchart LR
    Log["User Logs Water"] --> Chamber["Fluid Chamber SVG<br>- Dynamic Height Clip Path<br>- Continuous Sine Wave Loop<br>- High-Contrast Dark Pill Readout"]
    Log --> Coach["Companion Coach Card<br>- Live Mascot Expression Tier<br>- Contextual Dialogue Bubble<br>- Next Badge Progress Bar"]
```

1. **Clipped Water Boundary:** `<clipPath id="wb2-clip">` confines all wave geometry inside the ergonomic glass contour.
2. **Smooth Sine-Wave Flow:** CSS `@keyframes wb-wave` gently shifts the wave surface across 4-second loops without JavaScript timers.
3. **Always-Legible Center Badge:** A high-contrast pill inside the chamber (`44%`, `1,100 / 2,500 ml`) stays readable whether empty, half full, or above 100%.

---

## 7. Five Companion Spirit Mascots & Reactive States

Every user selects a companion spirit on onboarding that moves through five expressive moods as hydration progresses during the day:

```mermaid
stateDiagram-v2
    [*] --> start: 0% to 24% (Gentle Invitation)
    start --> attentive: 25% to 49% (Momentum Building)
    attentive --> happy: 50% to 74% (Halfway Cleared)
    happy --> energized: 75% to 99% (Final Glass Stretch)
    energized --> ecstatic: 100%+ (Gold Sunglasses Victory)
    ecstatic --> start: New Day Reset
```

| Companion Name | Character Design | Hydration Encouragement Focus |
| :--- | :--- | :--- |
| **HydroBuddy the Sea Turtle** | Layered coastal teal shell explorer | Wise ocean navigator focused on calm, steady sipping rhythm |
| **Bubbles the Playful Dolphin** | Streamlined agile sea swimmer | High-energy celebrator for rapid multi-drink streaks |
| **Splash the River Otter** | Warm brown river otter holding crystal drop | Consistent mover encouraging regular hourly refills |
| **Misty the Friendly Raindrop** | Minimalist droplet elemental with highlight | Gentle reminder of steady focus and temperature balance |
| **Pippin the Polar Penguin** | Crisp black-and-white Antarctic penguin | Refreshing fan of chilled water bottles and recovery |

---

## 8. Cloud-Safe Headless Turtle Vector Art Vault (Pillow)

Because Python's standard `turtle` library opens a native desktop `tkinter` window, importing it on Linux cloud hosting immediately throws:
```text
_tkinter.TclError: no display name and no $DISPLAY environment variable
```
Our custom `HeadlessTurtle` class mirrors `forward`, `left`, `right`, `penup`, `pendown`, `goto`, and `arc` trigonometry directly onto an in-memory `280x280` `PIL.Image` RGBA canvas, generating four downloadable coastal emblems:

| Artwork Key | Artwork Title | Unlock Requirement | Procedural Geometry |
| :--- | :--- | :--- | :--- |
| `drop` | **Crystal Water Droplet** | Log your 1st drink | Smooth multi-point teardrop outline with coastal teal refraction arc |
| `traveler` | **Spring Hiker & Turtle** | Log any 2+ drinks today | Minimalist lakeside walker carrying an insulated bottle with turtle companion |
| `leaf` | **Hydration Sprout** | Reach 50% of daily goal | Symmetrical botanical sprout leaf with central stem and angled side veins |
| `badge` | **Ocean Championship Rosette** | Reach 100% of daily goal | 64-vertex scalloped sunburst medal with twin swallowtail ribbons and star core |

---

## 9. Living Wall of Badges & Habit Milestones

```mermaid
flowchart TD
    History["Session Intake History"] --> B1{"Logged drinks >= 1?"}
    B1 -- Yes --> U1["First Sip (Unlocked Teal)"]
    History --> B2{"Logged drinks >= 3?"}
    B2 -- Yes --> U2["Steady Pacer (Unlocked Teal)"]
    History --> B3{"Total >= 50% Goal?"}
    B3 -- Yes --> U3["Halfway Hydrated (Unlocked Teal)"]
    History --> B4{"Total >= 100% Goal?"}
    B4 -- Yes --> U4["Hydro Champion (Unlocked Teal)"]
    History --> B5{"Goal != Cohort Baseline?"}
    B5 -- Yes --> U5["Calibration Master (Unlocked Teal)"]
```

Every badge evaluates live against `intake_history`, illuminates in coastal teal (`#1A7887`) with crisp white SVG vector icons (`render_badge_svg`) once earned, and gracefully returns to muted gray lock tiles when resetting the day.

---

## 10. Rapid Vessel Logging, Cup Converter & Hydration Ledger

1. **One-Tap Rapid Vessels:** Five uniform cards with custom coastal teal SVG container silhouettes (`Coffee Mug 250 ml`, `Water Glass 250 ml`, `Travel Tumbler 350 ml`, `Sports Bottle 500 ml`, `Hydro Flask 750 ml`).
2. **First-View `+ Log Drink` Modal:** Clicking `+ Log Drink` in the top navigation bar opens `@st.dialog("Log Custom Water Intake")` to record any custom volume (`10` to `2,500 ml`) and custom beverage label immediately.
3. **Aligned Precision Steppers & Cup Converter:** Twin bordered cards pair a custom milliliter form (`10` to `2,500 ml`) right next to a live Cup Converter (`0.5` to `15.0` cups multiplied cleanly by `250 ml`).
4. **Altair Trajectory Bar Chart & Progress Ledger:** Visualizes cumulative daily growth alongside a clean table featuring inline progress bars, one-click `Undo Last Drink`, `Export Intake CSV`, and guarded daily reset confirmation.

---

## 11. Verification & Multi-Scenario Test Proof

We verified end-to-end state changes (`AppTest` automated assertions covering onboarding, all 5 vessels, custom form, cup converter, undo rollback, Deep Tide Dark toggle, modal opening, badge counts, and vessel studio) alongside headless Chrome desktop (`1420px`) and mobile (`412px`) inspections.

| Test Case | Setup / Action | Logged Total | Progress & Rank | Badges Unlocked | Hydro Art Unlocked |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **1. Initial Coastal Onboarding** | Adults (`2,500 ml` target), HydroBuddy selected | `0 ml` | `0.0%` (`Seedling Sipper`) | `0 of 5` | Spring Seed Preview |
| **2. Midday Studio Sequence** | `250` Mug + `350` Tumbler + `500` Bottle (`?demo=true`) | `1,100 ml` | `44.0%` (`Flowing Stream`) | `2 of 5` (`First Sip`, `Steady Pacer`) | `Crystal Water Droplet` + `Hiker` |
| **3. Cup Converter & Custom Step** | Log Custom `150 ml` + Convert `1.5` cups (`+375 ml`), then Undo | `2,250 ml` | `102.3%` (`Ocean Master`) | `5 of 5` (calibrated `2,200 ml` goal) | All 4 Artworks Unlocked |
| **4. 105% Goal Victory Sequence** | `5` drinks (`?demo=full` on custom `2,000 ml` goal) | `2,100 ml` | `105.0%` (`Ocean Master`) | `5 of 5 (100% Complete)` | `Ocean Championship Rosette` |
| **5. Mobile & Dark Modal Check** | Toggle Deep Tide Dark + open `+ Log Drink` + `412x915` viewport | Live parity | Clean readable contrast | Responsive stacked layout | Crisp SVG icons across views |

<div align="center">
<img src="assets/screenshots/test_proof_collage_v2.png" alt="Multi-Scenario Verification Test Proof Collage" width="900" style="border-radius: 12px; border: 1.5px solid #1A7887; box-shadow: 0 8px 24px rgba(15,41,51,0.12);"/>
<p><em>Figure 6: Side-by-side live verification capturing Test 1 (Coastal Oasis Studio & Hero Cards), Test 2 (Cup Converter, Altair Trajectory Chart & Progress Ledger), and Test 3 (5/5 Badges & 4-Piece Hydro Art Vault).</em></p>
</div>

---

## 12. Deployment & Local Installation Guide

### 12.1 Running Locally
```bash
# 1. Clone the repository
git clone https://github.com/parthibcpana/IDAI102-1000544-PARTH-PARVINBHAI-GAJERA.git
cd IDAI102-1000544-PARTH-PARVINBHAI-GAJERA

# 2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies and launch
pip install -r requirements.txt
streamlit run app.py
```

### 12.2 Deployed Files for Streamlit Community Cloud
1. Ensure [app.py](app.py), [requirements.txt](requirements.txt), [.streamlit/config.toml](.streamlit/config.toml), and [README.md](README.md) are pushed to `main`.
2. Connect repository `parthibcpana/IDAI102-1000544-PARTH-PARVINBHAI-GAJERA` on [share.streamlit.io](https://share.streamlit.io/) with main file path `app.py`.

---

## 13. System Standards & Technical Alignment

| Requirement Area | Implementation Standard in WaterBuddy | Verification Outcome |
| :--- | :--- | :--- |
| **Age Cohort Calibration** | 4 WHO/EFSA cohorts (`1,600` to `2,500 ml/day`) plus live custom target override | Dynamically recalculates KPIs, fill %, and `Calibration Master` badge |
| **Dual Visual Feedback** | Animated clipped SVG Fluid Chamber + 5 Companion mascots across 5 emotional states | Verified SVG state transitions at `0%`, `44%`, and `105%` fills |
| **Headless Turtle Engine** | In-memory Pillow `HeadlessTurtle` rendering 4 `280x280` RGBA emblems | Zero Tkinter crashes in headless environments; PNG downloads verified |
| **Low-Friction Logging** | Top `+ Log Drink` modal, 5 SVG rapid vessels, custom stepper, and Cup Converter | Verified sub-second updates across `AppTest` and live Chrome captures |
| **Data Transparency & Undo** | Altair progression bar chart, `ProgressColumn` ledger, `Undo Last Drink`, and CSV export | Non-destructive undo restores totals, mascot mood, and active artwork |
| **Dual Theme & Mobile Layout** | Native Coastal Oasis Light (`.streamlit/config.toml`) + Deep Tide Dark + `<=920px` CSS | Verified high legibility on desktop (`1420px`) and mobile (`412px`) |

---

## 14. Academic Integrity Statement

This submission comprises our complete Streamlit codebase ([app.py](app.py)), Streamlit theme config ([.streamlit/config.toml](.streamlit/config.toml)), dependency manifest ([requirements.txt](requirements.txt)), and documentation ([README.md](README.md)) built by **Parth Pravinbhai Gajera** (Candidate ID: `1000544`) and project partner **Subhan Syed** for **IDAI 102: Python Programming** at **Aspee Nutan Academy / WACP International** under the **WellNest Technologies Pvt. Ltd.** brief.

Foundational text-based starter routines were contributed by Subhan Syed, while the full Streamlit visual architecture, coastal waterfall welcome scene, animated SVG fluid chamber, five-avatar companion coach, custom container silhouettes, `+ Log Drink` modal workflow, cup converter, living wall of badges, in-memory Pillow `HeadlessTurtle` art vault, Altair progression chart, light/dark dual palette system, and cloud deployment were engineered by Parth Pravinbhai Gajera in alignment with our FA-1 Canva visual atlas (`DAHars3Lfk4`).

**Student Developer:** Parth Pravinbhai Gajera (Candidate ID: `1000544`)  
**Project Partner:** Subhan Syed  
**Institution:** Aspee Nutan Academy / WACP International  
**Status:** Complete & Verified

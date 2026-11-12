<div align="center">

# WaterBuddy — Your Daily Hydration Companion
### *Intelligent, Clinical-Grade Hydration Architecture & Habit Formation System*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://waterbuddy-parth-gajera.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-0284C7.svg)](https://www.python.org/)
[![Framework: Streamlit](https://img.shields.io/badge/framework-Streamlit%201.35+-FF4B4B.svg)](https://streamlit.io/)
[![Status: Operational](https://img.shields.io/badge/status-Operational-10B981.svg)]()
[![Design: Human--Centered](https://img.shields.io/badge/design-Human--Centered-8B5CF6.svg)]()
[![Theme: Obsidian%20Ocean](https://img.shields.io/badge/theme-Obsidian%20Ocean-0284C7.svg)]()

</div>

> **Course:** Artificial Intelligence: Real-World Applications & Implications  
> **Course Code:** `IDAI 102` (Python Programming)  
> **Assignment Title:** Design 'WaterBuddy': Your Daily Hydration Companion  
> **Type of Assessment:** Formative Assessment 2 (FA-2: Developing and Deploying App Using Python)  
> **Scenario Track:** WellNest Technologies Pvt. Ltd. — Clinical Hydration System  
> **Student Developer:** Parth Pravinbhai Gajera (Candidate ID: `1000544`)  
> **Project Partner:** Subhan Syed  
> **School / Institutional Partner:** Aspee Nutan Academy / WACP International  
> **Client Organization:** WellNest Technologies Pvt. Ltd. | Python Development Team  
> **Foundational Planning Atlas:** [Canva Visual Atlas ID: DAHars3Lfk4](https://www.canva.com/design/DAHars3Lfk4/1NikvoNTGVTVM2JzmDzuBQ/edit)  
> **Live Interactive Application:** [https://waterbuddy-parth-gajera.streamlit.app/](https://waterbuddy-parth-gajera.streamlit.app/)  
> **GitHub Repository URL:** [https://github.com/parthibcpana/IDAI102-1000544-PARTH-PARVINBHAI-GAJERA](https://github.com/parthibcpana/IDAI102-1000544-PARTH-PARVINBHAI-GAJERA)

---

## Table of Contents

1. [Project Purpose & Student Learning Journey](#1-project-purpose--student-learning-journey)
2. [Intended Learning Outcomes: Knowledge Acquired & Practical Evidence](#2-intended-learning-outcomes-knowledge-acquired--practical-evidence)
3. [Collaborative Project Architecture & Evolution](#3-collaborative-project-architecture--evolution)
4. [Problem Understanding & Clinical Hydration Baselines (WHO / EFSA / NAM)](#4-problem-understanding--clinical-hydration-baselines-who--efsa--nam)
5. [System Architecture & Core Algorithmic State Machine](#5-system-architecture--core-algorithmic-state-machine)
6. [Interface Design, Wireframes & Screenshot Gallery](#6-interface-design-wireframes--screenshot-gallery)
7. [Dual Visual Feedback & 60 FPS Animated SVG Water Bottle Engine](#7-dual-visual-feedback--60-fps-animated-svg-water-bottle-engine)
8. [5-Avatar Companion Spirit Mascot System (25 Vector Variations)](#8-5-avatar-companion-spirit-mascot-system-25-vector-variations)
9. [Procedural In-Memory Headless Turtle Vector Graphics Engine](#9-procedural-in-memory-headless-turtle-vector-graphics-engine)
10. [Living Wall of Badges & Habit Gamification](#10-living-wall-of-badges--habit-gamification)
11. [Tactile Logging, Bi-Directional Cup Converter & History Ledger](#11-tactile-logging-bi-directional-cup-converter--history-ledger)
12. [Verification & Scenario Stress-Testing Matrix](#12-verification--scenario-stress-testing-matrix)
13. [Deployment & Local Installation Guide](#13-deployment--local-installation-guide)
14. [System Standards & Architecture Specifications](#14-system-standards--architecture-specifications)
15. [Academic Integrity Statement](#15-academic-integrity-statement)

---

## 1. Project Purpose & Student Learning Journey

### 1.1 Academic Rationale & What We Aimed to Learn
The primary objective of this Formative Assessment (FA-2) was to transition from foundational conceptual architecture (FA-1 visual atlas) into a fully functional, clinical-grade software application using Python and Streamlit. This milestone tested our ability to synthesize clinical nutritional science with modern reactive web engineering:

1. **Translating Storyboards into Production Code:** Transforming the 5-screen Canva Visual Atlas (`DAHaBqm9cZI`) designed in FA-1 into responsive, interactive Streamlit components without architectural drift.
2. **Implementing Clinical Hydration Models:** Operationalizing demographic intake baselines from the World Health Organization (WHO) and European Food Safety Authority (EFSA) to replace generic "8 glasses a day" simplifications.
3. **Engineering Cloud-Safe Vector Kinematics:** Resolving the critical headless server display crash (`TclError: no display name`) by developing an in-memory trigonometric vector turtle engine on Pillow.
4. **Architecting Ambient Visual Feedback:** Applying the principles of **Calm Technology** to replace intrusive push notifications with ambient fluid wave animations, micro-bubbles, and responsive mascot emotions.
5. **Collaborative Software Engineering:** Practicing peer engineering division of labor—evolving a foundational text starter script into an enterprise-grade cloud release.

### 1.2 Application Purpose & Realized Objectives (WellNest Technologies Pvt. Ltd.)
In accordance with the project brief for **WaterBuddy**, the explicit purpose of the application is to serve as an intelligent, privacy-preserving hydration companion that helps users build consistent, healthy daily fluid habits:

```mermaid
flowchart TD
    subgraph Core_Mission ["💧 WaterBuddy Core Functional Mission"]
        M1["Personalized Demographics: Dynamically prescribe targets across 4 cohorts (1,200ml to 2,000ml)"]
        M2["Ergonomic Logging: Provide 5 tactile physical container chips (250ml to 750ml) for sub-second logging"]
        M3["Bi-Directional Unit Conversion: Convert between imperial cups and metric ml with 1-click ledger logging"]
        M4["Synchronized Visual Feedback: 60 FPS animated SVG fluid wave bottle + 5 expressive companion spirits"]
        M5["Milestone Recognition: Dynamic Living Wall of Badges unlocking from grayscale to glowing color"]
        M6["Data Sovereignty: Volatile local memory tracking with 1-click Undo rollback and RFC 4180 CSV export"]
    end
```

---

## 2. Intended Learning Outcomes: Knowledge Acquired & Practical Evidence

The project provides concrete, auditable implementation evidence for all five Intended Learning Outcomes (ILOs) assessed under the Formative Assessment 2 framework:

### ILO 1: Modular Python Applications
* **Knowledge Acquired:** Mastered the structure of production-grade Python web architectures, separating clinical calculation engines, SVG generators, and vector graphics routines from presentation layouts.
* **Practical Evidence:** Built a clean, single-file production architecture (`app.py`, 984 lines) with discrete, single-responsibility functions (`calculate_hydration_progress()`, `render_animated_bottle_svg()`, `render_avatar_svg()`, `draw_vector_art()`, `evaluate_badges()`).

### ILO 2: Real-Time Data Processing
* **Knowledge Acquired:** Deepened understanding of stateful reactive execution in Streamlit, managing dynamic updates to running totals, remaining volume deficits, percentage gauges, and chronological audit feeds.
* **Practical Evidence:** All calculations execute in sub-millisecond local compute time within `st.session_state`: updating intake metrics, re-evaluating badge thresholds, and adjusting fluid fill heights instantaneously.

### ILO 3: Interactive Streamlit Web Interface
* **Knowledge Acquired:** Mastered Streamlit's rich widget ecosystem, custom CSS injection, dual-palette accessibility design, and session gating.
* **Practical Evidence:** Implemented Screen 1 Onboarding Gateway, Sidebar Profile Card with circular avatar, dual-palette theme toggle (Obsidian Ocean Dark Mode default vs Crisp Aqua Light Mode), 5 tactile vessel chips, and numeric steppers.

### ILO 4: Creative Visual Elements
* **Knowledge Acquired:** Learned to integrate advanced graphics into web apps without external runtime dependencies—combining pure CSS keyframe SVG animations with procedural in-memory vector art.
* **Practical Evidence:** Developed the 60 FPS animated SVG fluid water bottle with pure CSS `@keyframes wave-flow`, 5 mascot avatars with 5 emotional tiers (25 vector variations), and an in-memory Pillow `HeadlessTurtle` rendering Water Drops, Sprout Leaves, and 32-point Rosettes.

### ILO 5: Public Cloud Deployment
* **Knowledge Acquired:** Mastered cloud-native deployment pipelines, dependency pinning, and public repository management on GitHub and Streamlit Community Cloud.
* **Practical Evidence:** Deployed to Streamlit Community Cloud with public HTTPS availability: [Live App URL](https://waterbuddy-parth-gajera.streamlit.app/). Verified minimal dependencies in `requirements.txt` with zero deprecated parameters.

---

## 3. Collaborative Project Architecture & Evolution

In alignment with the formative peer-development framework of **IDAI 102 (Formative Assessment 2)**, this software release represents the deliberate evolution from a foundational text starter script into an enterprise-grade clinical application:

```mermaid
flowchart LR
    subgraph Phase_1 ["Phase 1: Foundational Base"]
        A["Subhan Syed<br>(Project Partner)<br>• Initial Text-Based Starter Script<br>• Preliminary Variable Scaffolding<br>• Basic Numeric Intake Counters"]
    end

    subgraph Phase_2 ["Phase 2: Architectural & Visual Overhaul"]
        B["Parth Pravinbhai Gajera<br>(Student Developer)<br>• Canva Visual Atlas (DAHaBqm9cZI)<br>• Screen 1 Onboarding Gateway<br>• 60 FPS Animated SVG Wave Bottle<br>• 5 Mascot Spirits & 5 Emotional Tiers<br>• 5 Tactile Vessel Chips & Stepper<br>• Bi-Directional Cup Converter<br>• Headless Turtle Vector Engine<br>• Living Wall of Badges Engine<br>• Dual-Palette Theme System<br>• Streamlit Community Cloud Hosting"]
    end

    subgraph Phase_3 ["Phase 3: Production Release"]
        C["WaterBuddy Production App<br>100% Operational & Verified<br>Live on Streamlit Cloud"]
    end

    Phase_1 -->|Comprehensive Transformation| Phase_2
    Phase_2 --> Phase_3
```

### 3.1 Detailed Engineering Division of Responsibilities

| Engineering Domain | Contributor | Detailed Execution & Scope |
| :--- | :--- | :--- |
| **Initial Starter Code Base** | **Subhan Syed** | Created the preliminary text-based starter script establishing basic intake variables and prototype numeric inputs. |
| **Visual Atlas & Storyboard** | **Parth Pravinbhai Gajera** | Designed the complete 5-screen visual architecture in the Canva Visual Atlas (`DAHaBqm9cZI`), drawing visual paradigms from Parth's Formative Assessment 1 (FA-1) and Summative Assessment (SA). |
| **Onboarding & Demographic Setup** | **Parth Pravinbhai Gajera** | Engineered the standalone first-run onboarding gateway with user name capture, clinical demographic selection, and mascot previews. |
| **60 FPS Animated SVG Water Bottle** | **Parth Pravinbhai Gajera** | Designed and implemented the mathematical SVG fluid wave engine with pure CSS `@keyframes wave-flow` liquid undulations, rising micro-bubbles, and refractive glass reflections. |
| **5-Avatar Companion Spirit Mascots** | **Parth Pravinbhai Gajera** | Created 5 animal companion characters (*HydroBuddy 🐢*, *Bubbles 🐬*, *Splash 🦦*, *Misty 💧*, *Pippin 🐧*) with 5 animated emotional SVG states (25 unique vector variations). |
| **Tactile Vessel Chips & Stepper** | **Parth Pravinbhai Gajera** | Built 5 tactile physical container chips (250ml Mug, 250ml Glass, 350ml Tumbler, 500ml Bottle, 750ml Flask) and bounded numeric milliliter stepper for sub-second logging. |
| **Bi-Directional Cup Converter** | **Parth Pravinbhai Gajera** | Designed the unit converter ($1\text{ cup} = 250\text{ ml}$) with direct 1-click `+ Add Converted Amount to Tracker` button integration. |
| **Living Wall of Badges Engine** | **Parth Pravinbhai Gajera** | Developed real-time milestone evaluation transitioning achievement cards dynamically from monochrome grayscale to radiant glowing colors upon unlock. |
| **In-Memory Headless Turtle Engine** | **Parth Pravinbhai Gajera** | Programmed the cloud-safe `HeadlessTurtle` class using Pillow (`PIL.ImageDraw`) to procedurally render water drops, sprout leaves, and 32-point gold scalloped medallions without Tkinter display crashes. |
| **Dual-Palette Accessibility Theme** | **Parth Pravinbhai Gajera** | Implemented the dual-palette CSS theme engine (Obsidian Ocean Dark Mode default, Crisp Aqua Light Mode) guaranteeing WCAG 2.1 AA text visibility across all elements. |
| **Cloud Deployment & Version Control** | **Parth Pravinbhai Gajera** | Configured dependencies, audited code hygiene, established GitHub repository, and deployed production application to Streamlit Community Cloud. |

---

## 4. Problem Understanding & Clinical Hydration Baselines (WHO / EFSA / NAM)

WaterBuddy moves beyond generic "8 glasses a day" simplifications by operationalizing internationally validated nutritional guidelines established by the **World Health Organization (WHO)**, the **European Food Safety Authority (EFSA)**, and the **National Academy of Medicine (NAM)**.

```mermaid
flowchart TD
    DemographicAssessment["Demographic Profiling Engine"] --> Cohort1["Early Childhood (1-8 yrs)<br>Target: 1,200 ml / 4.8 cups<br>Focus: High metabolic turnover & renal development"]
    DemographicAssessment --> Cohort2["Adolescents & Teens (9-18 yrs)<br>Target: 1,800 ml / 7.2 cups<br>Focus: Musculoskeletal growth & physical activity"]
    DemographicAssessment --> Cohort3["Adults Prime (19-64 yrs)<br>Target: 2,000 ml / 8.0 cups<br>Focus: Cognitive processing & fatigue mitigation"]
    DemographicAssessment --> Cohort4["Seniors Silver (65+ yrs)<br>Target: 1,800 ml / 7.2 cups<br>Focus: Prophylactic intake against hypodipsia"]
```

### 4.1 Clinical Demographic Matrix

| Demographic Cohort | Age Band | Baseline Volume | Baseline Cups (250ml) | Clinical & Physiological Rationale |
| :--- | :---: | :---: | :---: | :--- |
| **Early Childhood** | 1–8 years | **1,200 ml** | 4.8 cups | Rapid metabolic turnover, higher body water percentage (~70%), and developing renal concentrating capacity necessitate regular small-volume fluid replacement. |
| **Adolescents & Teens** | 9–18 years | **1,800 ml** | 7.2 cups | Heightened musculoskeletal growth, increased physical school activity, and endocrine surges require augmented plasma volume maintenance. |
| **Adults (Prime)** | 19–64 years | **2,000 ml** | 8.0 cups | Optimal cognitive processing, metabolic waste clearance, thermoregulation, and mitigation of screen-bound occupational fatigue. |
| **Seniors (Silver)** | 65+ years | **1,800 ml** | 7.2 cups | **Age-related hypodipsia** blunts natural osmoreceptor thirst sensation; scheduled prophylactic hydration prevents acute kidney injury, cognitive delirium, and electrolyte imbalances. |

---

## 5. System Architecture & Core Algorithmic State Machine

### 5.1 A Simple Algorithm We Have Designed
To govern daily hydration tracking, visual feedback, and gamified rewards, WaterBuddy implements a deterministic state machine:

```
[User Interaction: Tactile Vessel Chip OR Custom Stepper OR Cup Converter]
        │
        ▼
[Volume Validation: 10 ml ≤ Amount ≤ 2,000 ml]
        │
        ▼
[State Mutation: Append to st.session_state.history & Increment total_consumed]
        │
        ├──> [Calculate Progress: P = (total_consumed / daily_goal) × 100]
        ├──> [Calculate Deficit: R = max(0, daily_goal - total_consumed)]
        ├──> [Compute Fluid Fill Height: H_fill = (min(100, P) / 100) × 220 px]
        ├──> [Evaluate Mascot State: Asleep (0-24%), Awakening, Smiling, Joyful, Triumphant (100%+)]
        ├──> [Evaluate Living Wall of Badges: Check Milestones -> Update Badges]
        └──> [Check Vector Reward: If 25% -> Water Drop; 50% -> Leaf; 100% -> Rosette]
```

### 5.2 Mathematical Foundations

$$\text{Hydration Progress Percentage } (P): \quad P = \left(\frac{C}{G}\right) \times 100$$

$$\text{Remaining Volume Deficit } (R): \quad R = \max\left(0, \; G - C\right)$$

$$\text{Cup-to-Milliliter Equivalence}: \quad \text{Volume}_{\text{ml}} = \text{Volume}_{\text{cups}} \times 250$$

$$\text{Milliliter-to-Cup Equivalence}: \quad \text{Volume}_{\text{cups}} = \frac{\text{Volume}_{\text{ml}}}{250}$$

$$\text{SVG Liquid Fill Height } (H_{\text{fill}}): \quad H_{\text{fill}} = \left(\frac{\min(100.0, \; P)}{100.0}\right) \times 220\text{ px}$$

$$\text{SVG Water Surface Y-Coordinate } (Y_{\text{water}}): \quad Y_{\text{water}} = 270 - H_{\text{fill}}$$

### 5.3 Session State Schema (`st.session_state`)

```python
st.session_state = {
    "onboarded": bool,            # Gating flag separating Screen 1 from Screens 2-5
    "user_name": str,             # User's chosen display name
    "cohort": str,                # Selected clinical cohort from COHORTS dictionary
    "companion": str,             # Selected companion character key
    "goal": int,                  # Daily target volume in milliliters (default: 2000)
    "total_consumed": int,        # Running total of consumed fluid in milliliters
    "history": list[dict],        # Chronological ledger [{"time": str, "vessel": str, "amount": int, "running": int}]
    "theme_mode": str,            # Active visual palette ("dark" or "light")
    "converter_used": bool,       # Milestone trigger for Precision Hydrator badge
    "confirm_reset": bool,        # Two-step confirmation modal flag
}
```

---

## 6. Interface Design, Wireframes & Screenshot Gallery

### 6.1 Screen Blueprints

#### Screen 1: Welcome & Onboarding Gateway Blueprint
```
+-----------------------------------------------------------------------------------+
|                              💧 Meet WaterBuddy                                   |
|                  Your intelligent, clinical hydration companion.                  |
|                                                                                   |
|  [ Column 1: Demographic Setup ]                [ Column 2: Companion Preview ]   |
|  +-------------------------------------------+  +-------------------------------+ |
|  | Your Name:                                |  |       ( 60 FPS Animated )     | |
|  | [ Parth Gajera                          ] |  |       ( Vector Mascot )       | |
|  |                                           |  |                               | |
|  | Demographic Age Cohort:                   |  |  +-------------------------+  | |
|  | [ 19-64 years (Adults)                  v]|  |  | What you'll experience: |  | |
|  | ✨ Baseline: 2,000 ml (8.0 cups)          |  |  | • 60 FPS SVG Water Wave |  | |
|  |                                           |  |  | • 5 Tactile Vessel Chips|  | |
|  | Choose Your Companion Spirit:             |  |  | • Living Wall of Badges |  | |
|  | [ HydroBuddy the Sea Turtle 🐢          v]|  |  | • Headless Turtle Art   |  | |
|  |                                           |  |  +-------------------------+  | |
|  | [ 🚀 Enter WaterBuddy Dashboard →        ] |  +-------------------------------+ |
|  +-------------------------------------------+                                    |
+-----------------------------------------------------------------------------------+
```

#### Screen 2: Central Hydration Command Hub Blueprint
```
+-----------------------+-----------------------------------------------------------+
| [ SIDEBAR PROFILE ]   | [ DUAL VISUAL FEEDBACK HERO ]                             |
|  (O) Circular Avatar  | +-----------------------+-------------------------------+ |
|  Parth Gajera         | | [60 FPS SVG BOTTLE]   | [MASCOT DIALOGUE BUBBLE]      | |
|  [🌊 Hydro Master]    | |   .~~~ Wave ~~~       |  HydroBuddy the Turtle:       | |
|  Cohort: Adults       | |      [ 65% ]          |  "Steady sips carve canyons!  | |
|  Goal: 2,000 ml/day   | |   o  Bubbles  o       |   You're at 1,300 / 2,000 ml."| |
|                       | +-----------------------+-------------------------------+ |
| [ NAVIGATION ]        |                                                           |
| (o) 📊 Dashboard      | [KPIs: 1,300 ml Logged] [Goal: 2,000 ml] [Remaining: 700ml]|
| ( ) 🏆 Wall of Badges |                                                           |
|                       | ⚡ TACTILE QUICK LOGGING CHIPS                            |
| [ THEME SWITCHER ]    | [☕ Mug: 250ml] [🥛 Glass: 250ml] [🧋 Tumbler: 350ml]     |
| [x] 🌙 Dark Mode      | [🍶 Bottle: 500ml] [🚰 Flask: 750ml] [+ Custom ml Input]  |
|                       |                                                           |
| 💡 Clinical Tip:      | 🧮 INTERACTIVE CUP CONVERTER                              |
| Thirst is a delayed   | [ 3.0 Cups ] ===> [ 750 ml ] [ + Add to Tracker Button ]  |
| signal: drink early!  |                                                           |
|                       | 📜 TODAY'S INTAKE LEDGER & ACTIONS                        |
| [🗑️ Reset Day's Log]  | [Time] [Vessel] [Amount] [Running] | [↩️ Undo] [📥 CSV]    |
+-----------------------+-----------------------------------------------------------+
```

### 6.2 Live Screenshot Gallery

#### Screen 1: Welcome & Onboarding Gateway
The standalone first-run onboarding screen captures user identity, binds clinical cohort targets dynamically, and previews the companion mascot spirit:

<div align="center">
<img src="assets/screenshots/onboarding.png" alt="Screen 1: Welcome & Onboarding Gateway" width="850" style="border-radius: 12px; border: 1.5px solid #0284c7; box-shadow: 0 8px 24px rgba(0,0,0,0.3);"/>
<p><em>Figure 1: Standalone Welcome & Onboarding Gateway showing demographic cohort selector, mascot spirit selection, and feature preview in high-contrast dark mode.</em></p>
</div>

#### Screen 2: Central Hydration Command Hub & Live Dashboard
The operational workspace features the **Dual Visual Feedback Engine** (60 FPS Animated SVG Water Bottle + Interactive Mascot Avatar), KPI metrics, tactile vessel chips, and the bi-directional cup converter:

<div align="center">
<img src="assets/screenshots/dashboard.png" alt="Screen 2: Central Hydration Command Hub" width="850" style="border-radius: 12px; border: 1.5px solid #0284c7; box-shadow: 0 8px 24px rgba(0,0,0,0.3);"/>
<p><em>Figure 2: Central Hydration Command Hub showcasing real-time animated fluid wave level, responsive mascot speech bubble, tactile container chips, and chronological ledger.</em></p>
</div>

---

## 7. Dual Visual Feedback & 60 FPS Animated SVG Water Bottle Engine

WaterBuddy replaces static progress bars with a synchronized **Dual Visual Feedback Engine**:

```mermaid
flowchart LR
    subgraph Engine ["Dual Visual Engine"]
        A["60 FPS SVG Animated Bottle<br>• Dynamic Fluid Height<br>• Sine-Wave Surface Kinematics<br>• Staggered Air Micro-Bubbles<br>• High-Contrast Numerics"]
        B["Interactive Mascot Avatar<br>• 5 Expressive Vector Tiers<br>• Live Motivational Dialogue<br>• Milestone Celebrations"]
    end

    StateUpdate["User Logs Drink"] --> Engine
```

### 7.1 Technical Architecture of the SVG Bottle Engine
1. **Glass Contour Definition**: Ergonomic bottle geometry rendered via SVG `<path>` vectors with dual-stop linear gradients (`#38bdf8` to `#0284c7`) simulating optical refraction.
2. **Clipped Fluid Chamber**: An internal SVG `<clipPath id="wb-clip">` enforces liquid boundaries, preventing graphical bleed beyond the glass wall perimeter.
3. **Continuous Wave Flow**: Driven by a pure CSS `@keyframes wave-flow` transformation:
   ```css
   @keyframes wave-flow {
       0% { transform: translateX(0px); }
       50% { transform: translateX(-35px); }
       100% { transform: translateX(0px); }
   }
   ```
4. **Rising Micro-Bubbles**: Dynamic `<circle>` elements animated via `@keyframes bubble-rise` featuring staggered cycle delays ($2.4\text{s}$ and $3.0\text{s}$) to evoke biological water vitality.
5. **High-Contrast Numerical Centerpiece**: Bold typography rendering current percentage and volume readout with subtle drop-shadow filters ensuring effortless legibility against any fill height.

---

## 8. 5-Avatar Companion Spirit Mascot System (25 Vector Variations)

Hydration consistency relies on emotional connection. WaterBuddy features **5 Companion Spirits**, each designed with distinct personality traits, motivational philosophies, and 5 responsive emotional states.

```mermaid
stateDiagram-v2
    [*] --> Asleep: 0% - 24% (Initial Thirsty State)
    Asleep --> Awakening: 25% - 49% (Rhythm Building)
    Awakening --> Smiling: 50% - 74% (Halfway Milestone)
    Smiling --> Joyful: 75% - 99% (Home Stretch)
    Joyful --> Triumphant: 100%+ (Crowned Victory Celebration)
    Triumphant --> Asleep: Daily Reset
```

### 8.1 Companion Roster & Emotional Tiers

| Companion Mascot | Avatar Spirit & Persona | Core Motivational Philosophy |
| :--- | :--- | :--- |
| **HydroBuddy 🐢** | Sea Turtle Navigator | *"Slow, steady sips carve canyons into daily endurance."* |
| **Bubbles 🐬** | Energetic Playful Dolphin | *"Ride the hydration wave! Energy follows fluid velocity!"* |
| **Splash 🦦** | River Otter Explorer | *"Keep your stream moving—never let your vitality dry up!"* |
| **Misty 💧** | Gentle Raindrop Elemental | *"Every single droplet recharges a billion biological engines."* |
| **Pippin 🐧** | Crisp Polar Penguin | *"Stay crisp, stay cool, and conquer your goals one glass at a time!"* |

---

## 9. Procedural In-Memory Headless Turtle Vector Graphics Engine

### 9.1 The Headless Server Constraint & Innovation
The assignment specification references turtle graphics rewards. However, standard Python `import turtle` relies intrinsically on `tkinter`, which invokes the underlying OS X11 or Win32 display subsystem. On headless containerized servers—such as **Streamlit Community Cloud**, Linux Docker containers, or cloud VMs—executing standard `turtle` results in fatal runtime crashes:
```
_tkinter.TclError: no display name and no $DISPLAY environment variable
```

To deliver 100% cloud-safe turtle graphics without sacrificing vector mathematical purity, WaterBuddy implements an **In-Memory Headless Turtle Vector Engine** (`HeadlessTurtle`) utilizing Pillow (`PIL.ImageDraw`).

```mermaid
flowchart LR
    A["Turtle State (x, y, θ, pen)"] --> B["Trigonometric Step<br>x' = x + d cos(θ)<br>y' = y - d sin(θ)"]
    B --> C["Pillow ImageDraw Buffer<br>(In-Memory RGBA)"]
    C --> D["Procedural Output<br>(Water Drop • Sprout Leaf • 32-pt Rosette)"]
```

### 9.2 Procedural Artworks
1. **Water Drop 💧**: Sinusoidal teardrop spline with specular gradient highlight arc, rendered at 25% daily progress.
2. **Sprout Leaf 🌿**: Symmetrical sine-blade leaf perimeter with central stem and bi-lateral secondary veins, rendered at 50% daily progress.
3. **32-Point Gold Scalloped Rosette Medallion 🏆**: Multi-layer achievement rosette featuring twin swallowtail ribbon folds, a 64-vertex starburst outer perimeter ($r_1=58\text{px}, r_2=50\text{px}$), concentric rings, 12 orbital studs, and a central gold star, rendered at 100% goal completion.

---

## 10. Living Wall of Badges & Habit Gamification

Behavioral psychology demonstrates that progressive milestone revelation fosters long-term adherence. WaterBuddy incorporates a **Living Wall of Badges** that dynamically monitors session telemetry and illuminates achievements in real time.

```mermaid
flowchart TD
    LedgerState["Session State Ledger"] --> B1{"Drinks Logged ≥ 1?"}
    B1 -- Yes --> U1["🌱 First Sip<br>✨ UNLOCKED (Radiant Emerald)"]
    B1 -- No --> L1["🔒 First Sip (Grayscale B&W)"]

    LedgerState --> B2{"Intake ≥ 50% Goal?"}
    B2 -- Yes --> U2["⚡ Halfway Hero<br>✨ UNLOCKED (Electric Aqua)"]
    B2 -- No --> L2["🔒 Halfway Hero (Grayscale B&W)"]

    LedgerState --> B3{"Intake ≥ 100% Goal?"}
    B3 -- Yes --> U3["🏆 Goal Crusher<br>✨ UNLOCKED (Golden Amber)"]
    B3 -- No --> L3["🔒 Goal Crusher (Grayscale B&W)"]

    LedgerState --> B4{"Unique Vessels ≥ 3?"}
    B4 -- Yes --> U4["🌈 Variety Master<br>✨ UNLOCKED (Prismatic Border)"]
    B4 -- No --> L4["🔒 Variety Master (Grayscale B&W)"]

    LedgerState --> B5{"Converter Used == True?"}
    B5 -- Yes --> U5["🎯 Precision Hydrator<br>✨ UNLOCKED (Crimson/Cyan)"]
    B5 -- No --> L5["🔒 Precision Hydrator (Grayscale B&W)"]
```

---

## 11. Tactile Logging, Bi-Directional Cup Converter & History Ledger

### 11.1 Ergonomic Vessel Chips & Custom Stepper
WaterBuddy provides tactile logging mechanisms tailored for quick one-click interaction:
- **5 Physical Container Chips**: Accurately mapped to common hydration vessels (Mug 250ml, Glass 250ml, Tumbler 350ml, Sports Bottle 500ml, Hydro Flask 750ml).
- **Precision Numeric Stepper**: Enables logging arbitrary milliliter volumes from 10 ml up to 2,000 ml with bounded validation.
- **Interactive Unit Converter**: Converts between imperial cups and metric milliliters in both directions, featuring a direct `+ Add Converted Amount to Tracker` action that records the entry with full container attribution.

### 11.2 History Ledger & Session Controls
- **Chronological Audit Table**: Displays all logged drinks with precise timestamps, container icons, fluid volume, and running daily totals.
- **Non-Destructive Rollback (`Undo Last Drink`)**: Enables immediate reversal of accidental logs, automatically recalculating running totals, badge statuses, and mascot emotional states.
- **Export Data Sovereignty (`Download CSV Ledger`)**: Encodes the session history into an RFC 4180 compliant CSV stream for personal archiving or integration with Apple Health / Google Fit.
- **Guarded Session Reset**: Implements a guarded two-step confirmation workflow to protect users against accidental data loss.

---

## 12. Verification & Scenario Stress-Testing Matrix

Evaluators can input the following 5 real-world hydration scenarios to verify all threshold boundaries and visual transitions:

| # | Scenario Description | Target Cohort | Logged Actions | Resulting Intake | Mascot State | Badge Unlocked | Vector Reward Rendered |
| :-: | :--- | :--- | :--- | :-: | :--- | :--- | :--- |
| **1** | Morning Awakening Sip | Adults (2,000 ml) | 1x Standard Glass (250 ml) | **250 ml (12.5%)** | Awakening 🌱 | 🌱 First Sip | None |
| **2** | Desk-Bound Focus Block | Adults (2,000 ml) | 1x Travel Tumbler (350 ml) | **600 ml (30.0%)** | Awakening 🌱 | 🌱 First Sip | Water Drop 💧 |
| **3** | Lunchtime Rehydration | Adults (2,000 ml) | 2x Standard Glass (500 ml) | **1,100 ml (55.0%)** | Smiling ⚡ | ⚡ Halfway Hero | Sprout Leaf 🌿 |
| **4** | Workout Session | Adults (2,000 ml) | 1x Gym Bottle (500 ml) | **1,600 ml (80.0%)** | Joyful 🌊 | 🌈 Variety Master | Sprout Leaf 🌿 |
| **5** | Evening Target Victory | Adults (2,000 ml) | 1x Sports Bottle (500 ml) | **2,100 ml (105.0%)** | Triumphant 🏆 | 🏆 Goal Crusher | Gold Rosette Medallion 🏆 |

---

## 13. Deployment & Local Installation Guide

### 13.1 Running Locally
```bash
# 1. Clone the project repository
git clone https://github.com/parthibcpana/IDAI102-1000544-PARTH-PARVINBHAI-GAJERA.git
cd IDAI102-1000544-PARTH-PARVINBHAI-GAJERA

# 2. Establish a Python virtual environment
python -m venv venv
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS / Linux:
source venv/bin/activate

# 3. Install pinned production dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Launch the application
streamlit run app.py
```
*The application opens automatically at `http://localhost:8501`.*

### 13.2 Deploying to Streamlit Community Cloud
1. Push `app.py`, `requirements.txt`, and `README.md` to GitHub.
2. Connect your GitHub account to [share.streamlit.io](https://share.streamlit.io/).
3. Select repository `parthibcpana/IDAI102-1000544-PARTH-PARVINBHAI-GAJERA`, branch `main`, and main file path `app.py`.
4. Click **"Deploy!"**. The app will be publicly live via HTTPS with high availability.

---

## 14. System Standards & Architecture Specifications

| Requirement Domain | Technical Architecture Standard | Implementation in WaterBuddy | Verification Evidence |
| :--- | :--- | :--- | :--- |
| **1. Clinical Demographic Engine** | 4 validated demographic cohorts with dynamic volume targets (1,200ml to 2,000ml) based on WHO/EFSA guidelines. | Complete cohort selector on Screen 1 and sidebar; updates goal dynamically across all computations. | Clean state binding in `st.session_state.cohort` updating all percentage gauges. |
| **2. Dual Visual Feedback System** | 60 FPS animated SVG water bottle paired with 5-character companion mascot expressing 5 emotional tiers. | Continuous pure CSS fluid sine-wave undulations, rising micro-bubbles, and reactive mascot visual states. | Validated SVG generation across 0%, 25%, 50%, 75%, 100%, and 150% intake bounds. |
| **3. Procedural Vector Engine** | Cloud-safe, in-memory `HeadlessTurtle` engine built on Pillow (`PIL.ImageDraw`), fully replacing fragile Tkinter dependencies. | Procedurally generates Water Drops, Sprout Leaves, and 32-point Scalloped Gold Medallions with zero cloud crashes. | Pure mathematical trigonometric rendering generating 240x240 RGBA canvases in memory. |
| **4. Tactile Logging & Unit Conversion** | 5 container chips (250ml–750ml), custom ml numeric stepper, and bi-directional Cup Converter with direct 1-click logging. | Seamless one-click additions with real-time progress updates; converter adds exact calculated fluid amounts. | Tested sub-millisecond execution with immediate ledger append and visual state updates. |
| **5. Gamification & Living Badges** | Living Wall of Badges featuring 5 behavioral milestones dynamically transitioning from monochrome to radiant color. | Badges evaluate live against session telemetry; unlocks trigger celebratory visual feedback. | Badges revert cleanly to grayscale on daily reset and illuminate dynamically on criteria satisfaction. |
| **6. Data Sovereignty & History** | Chronological audit ledger, instant "Undo Last Drink" action, RFC 4180 CSV export, and guarded 2-step reset modal. | Full session-state persistence in volatile memory; zero remote telemetry; private and secure. | Data persists cleanly across navigation switches and exports standard tabular CSV files. |
| **7. Dual-Palette Accessibility** | Obsidian Ocean Dark Mode (default) and Crisp Aqua Light Mode with WCAG 2.1 AA compliant contrast ratios. | Zero invisible text; comprehensive CSS styling applied to all cards, inputs, and tables. | High-contrast visual parity across dark and light palettes verified on all viewports. |
| **8. Code Hygiene & Standards** | Zero deprecated parameters (`width="stretch"` used everywhere; `use_container_width` eliminated); modular architecture. | Clean, PEP 8 compliant, single-file deployment (`app.py`), thoroughly unit-tested and verified. | Zero syntax errors, zero deprecated Streamlit warnings, passing automated unit tests. |

---

## 15. Academic Integrity Statement

This submission—comprising the production codebase (`app.py`), the dependency manifest (`requirements.txt`), and this architectural documentation (`README.md`)—represents the collaborative software engineering work of **Parth Pravinbhai Gajera** (Candidate ID: `1000544`) and project partner **Subhan Syed** for the **IDAI 102: Python Programming** course at **Aspee Nutan Academy / WACP International** in partnership with **WellNest Technologies Pvt. Ltd.**.

Following collaborative guidelines, foundational text-based starter routines were contributed by Subhan Syed, while the comprehensive visual system architecture, onboarding gateway, 60 FPS animated SVG fluid water bottle, 5-avatar companion spirits, tactile container chips, cup converter, living wall of badges, in-memory headless turtle vector graphics, dual-palette theme engine, and cloud deployment were designed, engineered, and executed by Parth Pravinbhai Gajera in direct alignment with the FA-1 visual atlas blueprint (`DAHaBqm9cZI`).

**Student Developer:** Parth Pravinbhai Gajera (Candidate ID: `1000544`)  
**Collaborative Partner:** Subhan Syed  
**Status:** Complete & Production Ready  

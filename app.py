import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
from model import SynapticMemoryModel

# ──────────────────────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Can a Connection Remember? · Synaptic Memory Experience",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────
# CSS Design System — High-Contrast Editorial Museum Aesthetic
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400;1,6..72,600&family=JetBrains+Mono:wght@400;600;700&display=swap');

/* Global Reset & Base Typography */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #0f172a !important;
    background-color: #faf9f6 !important;
}

html {
    scroll-behavior: smooth !important;
}

.stApp {
    background-image: 
        radial-gradient(at 0% 0%, rgba(238, 242, 255, 0.7) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(254, 243, 199, 0.5) 0px, transparent 50%),
        radial-gradient(at 50% 30%, rgba(240, 253, 244, 0.4) 0px, transparent 60%) !important;
    background-attachment: fixed !important;
}

/* Structural Container */
.block-container {
    max-width: 1040px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 6rem !important;
    margin: 0 auto !important;
}

/* Hide default streamlit chrome */
#MainMenu, header, footer { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }

/* Global Header Text Contrast for Light Sections */
h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #0f172a !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

/* Scene Anchors for Smooth Navigation */
.scene-anchor {
    position: relative;
    top: -70px;
    height: 0;
    visibility: hidden;
    display: block;
}

/* Top Progress Rail (Sticky & Fully Clickable) */
.progress-rail {
    display: flex !important;
    gap: 0.45rem !important;
    padding: 0.65rem 0.4rem !important;
    margin-bottom: 2rem !important;
    border-bottom: 1px solid #e2e8f0 !important;
    overflow-x: auto !important;
    position: sticky !important;
    top: 0 !important;
    background: rgba(250, 249, 246, 0.95) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    z-index: 999 !important;
}
.progress-link {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #475569 !important;
    text-decoration: none !important;
    padding: 0.35rem 0.65rem !important;
    border-radius: 9999px !important;
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    white-space: nowrap !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
.progress-link:hover {
    color: #4338ca !important;
    border-color: #a5b4fc !important;
    background: #eef2ff !important;
    transform: translateY(-1px) !important;
}

/* Eyebrows & Meta Labels */
.hero-eyebrow {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: #4338ca !important;
    display: inline-block !important;
    animation: fadeIn 0.6s ease-out;
}

/* Staggered Cinematic Hero Title — Strictly Left-Aligned */
.hero-title-container {
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-start !important;
    margin: 0.8rem 0 1.25rem 0 !important;
    line-height: 0.98 !important;
}

.hero-line {
    font-family: 'Newsreader', Georgia, serif !important;
    font-size: clamp(3.2rem, 6.2vw, 5.2rem) !important;
    font-weight: 700 !important;
    letter-spacing: -0.035em !important;
    text-align: left !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0;
    transform: translateY(16px);
    animation: slideUpWord 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.hero-line-1 { animation-delay: 0.1s; color: #0f172a !important; }
.hero-line-2 { animation-delay: 0.3s; color: #1e1b4b !important; }
.hero-line-3 { 
    animation-delay: 0.5s; 
    background: linear-gradient(135deg, #312e81 0%, #4338ca 45%, #e11d48 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    filter: drop-shadow(0 4px 16px rgba(67, 56, 202, 0.2)) !important;
}

@keyframes slideUpWord {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero-tagline {
    font-size: clamp(1.25rem, 2.2vw, 1.48rem) !important;
    font-weight: 600 !important;
    line-height: 1.45 !important;
    color: #1e293b !important;
    margin-bottom: 0.6rem !important;
}

.hero-subtext {
    font-size: 1.05rem !important;
    line-height: 1.65 !important;
    color: #334155 !important;
    max-width: 780px !important;
    margin-bottom: 1.75rem !important;
}

/* Badges & Status Pills */
.pill-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.4rem !important;
    padding: 0.35rem 0.85rem !important;
    border-radius: 9999px !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}
.badge-demo {
    background: #fef3c7 !important;
    color: #92400e !important;
    border: 1px solid #fcd34d !important;
}
.badge-clean {
    background: #ecfdf5 !important;
    color: #065f46 !important;
    border: 1px solid #6ee7b7 !important;
}
.badge-toy {
    background: #eff6ff !important;
    color: #1e40af !important;
    border: 1px solid #bfdbfe !important;
}
.badge-bdh {
    background: #faf5ff !important;
    color: #6b21a8 !important;
    border: 1px solid #e9d5ff !important;
}

/* Central Claim Banner */
.claim-banner {
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%) !important;
    border: 1.5px solid #fde68a !important;
    border-radius: 20px !important;
    padding: 1.75rem 2rem !important;
    margin: 1.75rem 0 !important;
    box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.12) !important;
}
.claim-banner h4 {
    font-size: 0.82rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #92400e !important;
    margin-bottom: 0.45rem !important;
}
.claim-banner p {
    font-family: 'Newsreader', Georgia, serif !important;
    font-size: 1.32rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
    color: #78350f !important;
    margin: 0 !important;
}

/* Floating Light Narrative Cards */
.editorial-card {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 24px !important;
    padding: 2.2rem !important;
    margin: 2.5rem 0 1.25rem 0 !important;
    box-shadow: 0 16px 36px -12px rgba(15, 23, 42, 0.06) !important;
    position: relative !important;
}

.card-step-num {
    font-family: 'Newsreader', serif !important;
    font-style: italic !important;
    font-size: 2.4rem !important;
    font-weight: 400 !important;
    color: #6366f1 !important;
    line-height: 1 !important;
    margin-bottom: 0.4rem !important;
}

.card-heading {
    font-family: 'Newsreader', Georgia, serif !important;
    font-size: 2.1rem !important;
    font-weight: 600 !important;
    color: #0f172a !important;
    letter-spacing: -0.015em !important;
    margin-bottom: 0.6rem !important;
}

.card-subtext {
    font-size: 1.05rem !important;
    line-height: 1.65 !important;
    color: #334155 !important;
    margin-bottom: 0.5rem !important;
}

/* Dedicated Semantic Classes for Dark Cards (Scene 10) */
.dark-editorial-card {
    background: linear-gradient(135deg, #090d16 0%, #17153b 50%, #1e1b4b 100%) !important;
    border: 1.5px solid #3730a3 !important;
    border-radius: 24px !important;
    padding: 2.2rem !important;
    margin: 2.5rem 0 1.25rem 0 !important;
    box-shadow: 0 16px 36px -12px rgba(15, 23, 42, 0.4) !important;
}

.dark-editorial-card .dark-section-number {
    font-family: 'Newsreader', serif !important;
    font-style: italic !important;
    font-size: 2.4rem !important;
    font-weight: 400 !important;
    color: #c7d2fe !important;
    line-height: 1 !important;
    margin-bottom: 0.4rem !important;
}

.dark-editorial-card .dark-section-heading {
    color: #ffffff !important;
    font-family: 'Newsreader', Georgia, serif !important;
    font-size: 2.1rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.015em !important;
    margin-bottom: 0.6rem !important;
}

.dark-editorial-card .dark-section-body {
    color: #e2e8f0 !important;
    font-size: 1.05rem !important;
    line-height: 1.65 !important;
    margin-bottom: 0.5rem !important;
}

/* Beginner Intuition Box (Consistent High-Contrast Component) */
.beginner-box {
    background: #f0fdf4 !important;
    border: 1.5px solid #bbf7d0 !important;
    border-radius: 14px !important;
    padding: 0.85rem 1.15rem !important;
    margin: 1.1rem 0 0.4rem 0 !important;
}
.beginner-box-title {
    font-size: 0.78rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #166534 !important;
    margin-bottom: 0.25rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.35rem !important;
}
.beginner-box-text {
    font-size: 0.94rem !important;
    line-height: 1.55 !important;
    color: #14532d !important;
    font-weight: 500 !important;
    margin: 0 !important;
}

/* Button Overrides */
div.stButton > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: -0.01em !important;
    padding: 0.72rem 1.5rem !important;
    border-radius: 9999px !important;
    border: none !important;
    background: #0f172a !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px -2px rgba(15, 23, 42, 0.25) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    width: 100% !important;
}
div.stButton > button:hover {
    background: #312e81 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px -4px rgba(49, 46, 129, 0.35) !important;
    color: #ffffff !important;
}
div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Stat & Concept Pills */
.stat-pill {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.35rem !important;
    padding: 0.42rem 1.05rem !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
}
.stat-coral { background: #ffe4e6 !important; color: #be123c !important; border: 1px solid #fecdd3 !important; }
.stat-mint  { background: #dcfce7 !important; color: #15803d !important; border: 1px solid #bbf7d0 !important; }
.stat-lavender { background: #ede9fe !important; color: #6d28d9 !important; border: 1px solid #ddd6fe !important; }
.stat-peach { background: #ffedd5 !important; color: #c2410c !important; border: 1px solid #fed7aa !important; }
.stat-neutral { background: #f1f5f9 !important; color: #334155 !important; border: 1px solid #e2e8f0 !important; }

/* Radio Button High Contrast */
div[data-testid="stRadio"] label {
    font-weight: 700 !important;
    color: #1e293b !important;
    font-size: 1.02rem !important;
    padding: 0.72rem 0.9rem !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    background: #ffffff !important;
    margin-bottom: 0.45rem !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: #a5b4fc !important;
    background: #f8fafc !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 0.35rem !important;
}
.result-correct {
    color:#059669 !important;
    font-weight:800 !important;
    font-size:0.98rem !important;
}
.result-incorrect {
    color:#dc2626 !important;
    font-weight:800 !important;
    font-size:0.98rem !important;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# State Management & Separation: Demo Preset vs. Clean Baseline
# ──────────────────────────────────────────────────────────────
if 'decay' not in st.session_state:
    st.session_state.decay = 0.85
if 'learning_rate' not in st.session_state:
    st.session_state.learning_rate = 0.80
if 'experiment_mode' not in st.session_state:
    # Start directly from a clean educational baseline (w = 0).
    st.session_state.experiment_mode = 'guided'

if 'model' not in st.session_state:
    st.session_state.model = SynapticMemoryModel(
        decay=st.session_state.decay,
        learning_rate=st.session_state.learning_rate
    )

model: SynapticMemoryModel = st.session_state.model

# Keep model hyper-parameters synchronized
model.decay = float(st.session_state.decay)
model.learning_rate = float(st.session_state.learning_rate)

def reset_to_clean_experiment():
    """Reset the experiment to a clean, known baseline where all weights are 0."""
    st.session_state.model.reset()
    st.session_state.experiment_mode = 'guided'
    if 'conflict_resolved' in st.session_state:
        del st.session_state['conflict_resolved']
    if 'recall_tested' in st.session_state:
        del st.session_state['recall_tested']

# ──────────────────────────────────────────────────────────────
# Scaled SVG Synapse Canvas Generator (Iframe Component)
# ──────────────────────────────────────────────────────────────
def build_synapse_html(w_red: float, w_green: float = 0.0, mode: str = 'single', show_pulse: bool = True) -> str:
    """
    Returns standalone HTML/SVG string containing the physical synaptic network.
    Line thickness, opacity, node scale, and particle motion are bound to live weights.
    """
    stroke_red = max(2.5, min(18.0, w_red * 13.0))
    stroke_green = max(2.5, min(18.0, w_green * 13.0))
    alpha_red = max(0.18, min(1.0, 0.15 + w_red * 0.95))
    alpha_green = max(0.18, min(1.0, 0.15 + w_green * 0.95))
    r_red_node = 36 + min(16, int(w_red * 10))
    r_green_node = 36 + min(16, int(w_green * 10))

    has_active_red = w_red > 0.03
    has_active_green = w_green > 0.03

    if mode == 'dual' or w_green > 0.01:
        svg_content = f"""
        <svg viewBox="0 0 720 370" width="100%" height="370" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="gradRed" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#6366f1" />
                    <stop offset="100%" stop-color="#f43f5e" />
                </linearGradient>
                <linearGradient id="gradGreen" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#6366f1" />
                    <stop offset="100%" stop-color="#10b981" />
                </linearGradient>
                <filter id="glowF" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="5" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
            </defs>

            <rect width="720" height="370" rx="28" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>

            <!-- Synapse Path to RED -->
            <path id="pathRed" d="M 360 90 C 360 170, 210 180, 210 260" 
                  fill="none" 
                  stroke="url(#gradRed)" 
                  stroke-width="{stroke_red:.1f}" 
                  stroke-linecap="round"
                  stroke-opacity="{alpha_red:.2f}"
                  class="{'active-synapse' if has_active_red else ''}" />

            <!-- Synapse Path to GREEN -->
            <path id="pathGreen" d="M 360 90 C 360 170, 510 180, 510 260" 
                  fill="none" 
                  stroke="url(#gradGreen)" 
                  stroke-width="{stroke_green:.1f}" 
                  stroke-linecap="round"
                  stroke-opacity="{alpha_green:.2f}"
                  class="{'active-synapse' if has_active_green else ''}" />

            <!-- Signal Particle on RED (Only active when w_red > 0.03) -->
            {f'''
            <circle r="4.5" fill="#f43f5e" opacity="0.9">
                <animateMotion dur="2.4s" repeatCount="indefinite" path="M 360 90 C 360 170, 210 180, 210 260" />
            </circle>
            ''' if has_active_red else ''}

            <!-- Signal Particle on GREEN (Only active when w_green > 0.03) -->
            {f'''
            <circle r="4.5" fill="#10b981" opacity="0.9">
                <animateMotion dur="2.4s" repeatCount="indefinite" path="M 360 90 C 360 170, 510 180, 510 260" />
            </circle>
            ''' if has_active_green else ''}

            <!-- Branching Junction Node -->
            <circle cx="360" cy="155" r="11" fill="#4f46e5" opacity="0.9" />
            <circle cx="360" cy="155" r="19" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-dasharray="3 3"/>

            <!-- Weight Badges beside Synapses -->
            <g transform="translate(230, 160)">
                <rect x="-42" y="-12" width="84" height="24" rx="12" fill="#fff1f2" stroke="#fda4af" stroke-width="1.2"/>
                <text x="0" y="4" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#be123c">w = {w_red:.3f}</text>
            </g>
            <g transform="translate(490, 160)">
                <rect x="-42" y="-12" width="84" height="24" rx="12" fill="#f0fdf4" stroke="#86efac" stroke-width="1.2"/>
                <text x="0" y="4" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#15803d">w = {w_green:.3f}</text>
            </g>

            <!-- Pre-synaptic Node: APPLE -->
            <g transform="translate(360, 72)">
                <circle r="44" fill="#fff7ed" stroke="#fdba74" stroke-width="2.5" filter="url(#glowF)"/>
                <text y="-4" text-anchor="middle" font-size="26">🍎</text>
                <text y="19" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="800" fill="#c2410c">APPLE</text>
            </g>

            <!-- Post-synaptic Node: RED -->
            <g transform="translate(210, 275)">
                <circle r="{r_red_node}" fill="#fff1f2" stroke="#fda4af" stroke-width="2.5" filter="url(#glowF)"/>
                <text y="-4" text-anchor="middle" font-size="26">🔴</text>
                <text y="19" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="800" fill="#e11d48">RED</text>
                <text y="{r_red_node + 20}" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#64748b">Trace: {w_red:.3f}</text>
            </g>

            <!-- Post-synaptic Node: GREEN -->
            <g transform="translate(510, 275)">
                <circle r="{r_green_node}" fill="#f0fdf4" stroke="#86efac" stroke-width="2.5" filter="url(#glowF)"/>
                <text y="-4" text-anchor="middle" font-size="26">🟢</text>
                <text y="19" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="800" fill="#16a34a">GREEN</text>
                <text y="{r_green_node + 20}" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#64748b">Trace: {w_green:.3f}</text>
            </g>
        </svg>
        """
    else:
        svg_content = f"""
        <svg viewBox="0 0 600 350" width="100%" height="350" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="gradDirect" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#6366f1" />
                    <stop offset="100%" stop-color="#f43f5e" />
                </linearGradient>
                <filter id="glowS" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="5" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
            </defs>

            <rect width="600" height="350" rx="28" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>

            <!-- Direct Synapse Line -->
            <line x1="300" y1="95" x2="300" y2="250" 
                  stroke="url(#gradDirect)" 
                  stroke-width="{stroke_red:.1f}" 
                  stroke-linecap="round" 
                  stroke-opacity="{alpha_red:.2f}" 
                  class="{'active-synapse' if has_active_red else ''}" />

            <!-- Signal Particle on Direct Path -->
            {f'''
            <circle r="5" fill="#f43f5e" opacity="0.95">
                <animateMotion dur="2.0s" repeatCount="indefinite" path="M 300 95 L 300 250" />
            </circle>
            ''' if has_active_red else ''}

            <!-- Weight Pill floating on the Synapse -->
            <g transform="translate(300, 172)">
                <rect x="-65" y="-14" width="130" height="28" rx="14" fill="#ede9fe" stroke="#c7d2fe" stroke-width="1.3"/>
                <text x="0" y="4" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="800" fill="#5b21b6">SYNAPSE: {w_red:.3f}</text>
            </g>

            <!-- Pre-synaptic Node: Apple -->
            <g transform="translate(300, 72)">
                <circle r="44" fill="#fff7ed" stroke="#fdba74" stroke-width="2.5" filter="url(#glowS)"/>
                <text y="-4" text-anchor="middle" font-size="26">🍎</text>
                <text y="19" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="800" fill="#c2410c">APPLE</text>
            </g>

            <!-- Post-synaptic Node: Red -->
            <g transform="translate(300, 270)">
                <circle r="{r_red_node}" fill="#fff1f2" stroke="#fda4af" stroke-width="2.5" filter="url(#glowS)"/>
                <text y="-4" text-anchor="middle" font-size="26">🔴</text>
                <text y="19" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="800" fill="#e11d48">RED</text>
            </g>
        </svg>
        """

    return f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }}
            @keyframes pulseGlow {{
                0% {{ filter: drop-shadow(0 0 2px rgba(99,102,241,0.3)); }}
                50% {{ filter: drop-shadow(0 0 10px rgba(99,102,241,0.65)); }}
                100% {{ filter: drop-shadow(0 0 2px rgba(99,102,241,0.3)); }}
            }}
            .active-synapse {{
                animation: pulseGlow 2.5s infinite ease-in-out;
            }}
            @media (prefers-reduced-motion: reduce) {{
                .active-synapse, animateMotion {{
                    animation: none !important;
                }}
            }}
        </style>
    </head>
    <body>
        {svg_content}
    </body>
    </html>
    """

# ──────────────────────────────────────────────────────────────
# Interactive Visual Progress Rail (Smooth Sticky Anchors)
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="progress-rail">
    <a href="#scene-hero" target="_self" class="progress-link">00 HERO</a>
    <a href="#scene-01" target="_self" class="progress-link">01 TEACH</a>
    <a href="#scene-02" target="_self" class="progress-link">02 WAIT</a>
    <a href="#scene-03" target="_self" class="progress-link">03 RECALL</a>
    <a href="#scene-04" target="_self" class="progress-link">04 CONFLICT</a>
    <a href="#scene-05" target="_self" class="progress-link">05 LAB</a>
    <a href="#scene-06" target="_self" class="progress-link">06 EQUATION</a>
    <a href="#scene-07" target="_self" class="progress-link">07 PAPERS</a>
    <a href="#scene-08" target="_self" class="progress-link">08 BDH</a>
    <a href="#scene-09" target="_self" class="progress-link">09 LIMITS</a>
    <a href="#scene-10" target="_self" class="progress-link">10 CHALLENGE</a>
</div>
<div id="scene-hero" class="scene-anchor"></div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# HERO SCENE — The Wow Moment
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div style="padding: 0.5rem 0 1rem 0;">
    <div style="display:flex; align-items:center; gap: 0.75rem; margin-bottom: 0.5rem; flex-wrap: wrap;">
        <span class="hero-eyebrow">AN INTERACTIVE EXPLORATION OF SYNAPTIC PLASTICITY</span>
        <span class="pill-badge badge-toy">EDUCATIONAL TOY SUBSTRATE</span>
''', unsafe_allow_html=True)

st.markdown('''
    <span class="pill-badge badge-clean">🌱 CLEAN EXPERIMENT BASELINE (w = 0)</span>
</div>
''', unsafe_allow_html=True)

# Huge dramatic title entrance — Perfectly Left-Aligned
st.markdown('''
    <div class="hero-title-container">
        <div class="hero-line hero-line-1">CAN A</div>
        <div class="hero-line hero-line-2">CONNECTION</div>
        <div class="hero-line hero-line-3">REMEMBER?</div>
    </div>
    <div class="hero-tagline">
        Give a tiny neural network a memory. Then see what happens when a new memory arrives.
    </div>
    <div class="hero-subtext">
        Explore how changing synaptic states can hold recent information — and how new information can compete with what came before.
    </div>
</div>
''', unsafe_allow_html=True)

# Central Claim Banner (Rigorous Competition Anchor)
st.markdown('''
<div class="claim-banner">
    <h4>Central Claim</h4>
    <p>
        “Short-term synaptic plasticity can store recent information in changing synaptic states, 
        but the persistence of these traces creates a trade-off between remembering recent information 
        and being influenced by new or competing information.”
    </p>
</div>
''', unsafe_allow_html=True)

# Live Hero Canvas
w_red_now = model.weight_of('apple', 'red')
w_green_now = model.weight_of('apple', 'green')
has_green_weight = ('apple', 'green') in model.get_synaptic_state()

col_h_canvas, col_h_panel = st.columns([1.5, 1], gap="large")

with col_h_canvas:
    components.html(
        build_synapse_html(w_red_now, w_green_now, mode='dual' if has_green_weight else 'single'),
        height=380
    )
    st.caption("⚡ Live physical rendering: Connection stroke width, node radius, and signal particle flow track live model weights directly.")

with col_h_panel:
    st.markdown('''
    <div style="padding-top: 0.25rem;">
        <h3 style="font-family:'Newsreader', serif; font-size:1.75rem; margin-bottom: 0.35rem; color:#0f172a;">Live Substrate State</h3>
        <p style="color: #334155; font-size: 0.98rem; line-height: 1.6; margin-bottom: 1.1rem;">
            In this educational model, changing synaptic strength acts as the memory substrate.
            Memory is embedded directly within the <strong>transmission weight</strong> of the physical connection.
        </p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("""
        <div style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:14px; padding:0.9rem; margin-bottom:1rem; font-size:0.88rem; color:#065f46;">
            🌱 <strong>Clean Baseline:</strong> The synaptic weight starts at $0.000$. Scroll to Scene 01 to teach the first memory.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'''
    <div style="margin-top: 1.1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
        <span class="stat-pill stat-peach">Input: 🍎 Apple</span>
        <span class="stat-pill stat-coral">w(apple→red): {w_red_now:.3f}</span>
        {f'<span class="stat-pill stat-mint">w(apple→green): {w_green_now:.3f}</span>' if has_green_weight else ''}
    </div>
    ''', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# BEGINNER GLOSSARY / TERM BRIDGE
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 18px; padding: 1.25rem 1.5rem; margin: 2.25rem 0 1.5rem 0; box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.03);">
    <div style="font-size: 0.78rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; color: #4338ca; margin-bottom: 0.75rem;">
        📖 Words to Know · A Beginner Bridge
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.9rem;">
        <div>
            <strong style="color: #0f172a; font-size: 0.88rem;">SYNAPSE</strong>
            <div style="font-size: 0.84rem; color: #475569; line-height: 1.45;">A connection between neurons.</div>
        </div>
        <div>
            <strong style="color: #0f172a; font-size: 0.88rem;">WEIGHT (w)</strong>
            <div style="font-size: 0.84rem; color: #475569; line-height: 1.45;">A number representing current connection strength.</div>
        </div>
        <div>
            <strong style="color: #0f172a; font-size: 0.88rem;">TRACE</strong>
            <div style="font-size: 0.84rem; color: #475569; line-height: 1.45;">The temporary change left in that connection.</div>
        </div>
        <div>
            <strong style="color: #0f172a; font-size: 0.88rem;">PLASTICITY (η)</strong>
            <div style="font-size: 0.84rem; color: #475569; line-height: 1.45;">How strongly new events change the connection.</div>
        </div>
        <div>
            <strong style="color: #0f172a; font-size: 0.88rem;">PERSISTENCE (δ)</strong>
            <div style="font-size: 0.84rem; color: #475569; line-height: 1.45;">How much of an old trace survives each time step.</div>
        </div>
        <div>
            <strong style="color: #0f172a; font-size: 0.88rem;">READOUT</strong>
            <div style="font-size: 0.84rem; color: #475569; line-height: 1.45;">The network's current answer when queried.</div>
        </div>
    </div>
    <div style="margin-top: 0.85rem; padding-top: 0.75rem; border-top: 1px solid #f1f5f9; font-size: 0.86rem; color: #334155;">
        💡 <em>Core Metaphor:</em> In this toy model, the <strong>weight is the current strength of the connection</strong> — and that changing strength acts as the temporary memory trace.
    </div>
</div>
<hr style='border:none; border-top:1px solid #e2e8f0; margin: 2rem 0 1rem 0;'>
''', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SCENE 01 — TEACH A MEMORY (Physical Write)
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div id="scene-01" class="scene-anchor"></div>
<div class="editorial-card">
    <div class="card-step-num">01</div>
    <div class="card-heading">Teach it something.</div>
    <div class="card-subtext">
        Present the concept 🍎 <strong>Apple</strong> simultaneously with the label 🔴 <strong>Red</strong>. 
        In this educational toy, coincident neural activation triggers a Hebbian write: the connection physically strengthens.
    </div>
    <div class="beginner-box">
        <div class="beginner-box-title">🧠 IN SIMPLE WORDS</div>
        <div class="beginner-box-text">
            Think of the weight as the strength of the connection. When Apple and Red appear together, this connection gets stronger, making that association easier to retrieve later.
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

col_t1, col_t2 = st.columns([1.3, 1], gap="large")

with col_t1:
    current_w_red = model.weight_of('apple', 'red')
    is_zero = (current_w_red < 0.001)
    bar_pct = min(100, int((current_w_red / 1.5) * 100))

    st.markdown(f'''
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:20px; padding:1.6rem;">
        <div style="font-size:0.8rem; text-transform:uppercase; color:#64748b; font-weight:800; letter-spacing:0.06em; margin-bottom:0.75rem;">
            LIVE SYNAPTIC TRANSMISSION STATE
        </div>
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1.1rem;">
            <div>
                <span style="font-size:1.15rem; font-weight:700; color:#0f172a;">Apple ➔ Red</span>
                <div style="font-size:0.85rem; color:{'#64748b' if is_zero else '#059669'}; font-weight:600; margin-top:0.2rem;">
                    {'Connection waiting... (unbound trace)' if is_zero else '✓ Memory written into synaptic state'}
                </div>
            </div>
            <span class="stat-pill {'stat-neutral' if is_zero else 'stat-coral'}" style="font-size:1.05rem;">
                w = {current_w_red:.3f}
            </span>
        </div>
        <div style="background:#f1f5f9; height:14px; border-radius:7px; overflow:hidden;">
            <div style="background:linear-gradient(90deg, #6366f1, #f43f5e); height:100%; width:{bar_pct}%; border-radius:7px; transition: width 0.4s ease;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#64748b; font-weight:600; margin-top:0.45rem;">
            <span>0.000 (No transmission)</span>
            <span>{model.learning_rate:.2f} (Single write η)</span>
            <span>1.500 (Saturation)</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col_t2:
    st.markdown('''
    <div style="padding: 0.2rem 0;">
        <p style="font-size:0.98rem; color:#334155; line-height:1.6;">
            Click below to co-activate pre-synaptic <em>Apple</em> and post-synaptic <em>Red</em>.
        </p>
    </div>
    ''', unsafe_allow_html=True)

    if st.button("🍎 TEACH MEMORY (Apple → Red)", key="btn_teach_scene1"):
        model.learn('apple', 'red')
        st.rerun()

    st.markdown(f'''
    <div style="margin-top: 1.1rem; font-size:0.92rem; color:#334155; background:#f8fafc; padding:1rem; border-radius:14px; border-left:4px solid #6366f1; line-height:1.55;">
        <strong>Mechanism:</strong> In this educational toy, coincident activity changes the synaptic state:
        <br><code style="background:#ede9fe; padding:0.15rem 0.35rem; border-radius:4px; font-weight:700; color:#4338ca;">Δw = η · pre · post = +{model.learning_rate:.2f}</code>
    </div>
    ''', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SCENE 02 — TIME & PASSIVE DECAY
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div id="scene-02" class="scene-anchor"></div>
<div class="editorial-card">
    <div class="card-step-num">02</div>
    <div class="card-heading">Now wait.</div>
    <div class="card-subtext">
        Biological synapses do not remain potentiated indefinitely. Short-term synaptic plasticity exhibits 
        rapid temporal decay. Step time forward and watch passive persistence fade.
    </div>
    <div class="beginner-box">
        <div class="beginner-box-title">🧠 IN SIMPLE WORDS</div>
        <div class="beginner-box-text">
            The memory trace is temporary. Each time step removes some of its strength, so the connection gradually fades if nothing reinforces it.
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

col_d_ctrl, col_d_plot = st.columns([1, 1.8], gap="large")

with col_d_ctrl:
    delta_t = st.slider("Time steps to advance (Δt):", min_value=1, max_value=15, value=4, key="slider_decay_steps")

    if st.button(f"LET TIME PASS (+{delta_t} steps) →", key="btn_decay_step"):
        model.step_time(delta_t)
        st.rerun()

    w_red_decay = model.weight_of('apple', 'red')
    pct_remaining = int((w_red_decay / max(0.001, model.learning_rate)) * 100) if w_red_decay <= model.learning_rate else int(w_red_decay * 100)

    st.markdown(f'''
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:0.85rem; margin-top:1.4rem;">
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:16px; padding:1.1rem; text-align:center;">
            <div style="font-size:0.75rem; text-transform:uppercase; color:#64748b; font-weight:800; letter-spacing:0.06em;">LOGICAL CLOCK</div>
            <div style="font-family:'Newsreader', serif; font-size:2.2rem; font-weight:700; color:#0f172a; margin-top:0.2rem;">t = {model.current_time}</div>
        </div>
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:16px; padding:1.1rem; text-align:center;">
            <div style="font-size:0.75rem; text-transform:uppercase; color:#64748b; font-weight:800; letter-spacing:0.06em;">CURRENT TRACE</div>
            <div style="font-family:'Newsreader', serif; font-size:2.2rem; font-weight:700; color:#4338ca; margin-top:0.2rem;">{w_red_decay:.3f}</div>
        </div>
    </div>
    <div style="margin-top:0.9rem; font-size:0.88rem; color:#475569; line-height:1.5;">
        Decay factor per step: <strong>δ = {model.decay:.2f}</strong>. Over {delta_t} steps: trace multiplied by <strong>δ^{delta_t} = {model.decay**delta_t:.3f}</strong>.
    </div>
    ''', unsafe_allow_html=True)

with col_d_plot:
    history = model.get_history()
    ts = [h['t'] for h in history]
    red_trace = [h['weights'].get(('apple', 'red'), 0.0) for h in history]
    green_trace = [h['weights'].get(('apple', 'green'), 0.0) for h in history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ts, y=red_trace,
        mode='lines+markers',
        name='w(Apple → Red)',
        line=dict(color='#f43f5e', width=3.5, shape='spline'),
        marker=dict(size=7, color='#f43f5e'),
        fill='tozeroy',
        fillcolor='rgba(244, 63, 94, 0.08)'
    ))

    if any(g > 0 for g in green_trace):
        fig.add_trace(go.Scatter(
            x=ts, y=green_trace,
            mode='lines+markers',
            name='w(Apple → Green)',
            line=dict(color='#10b981', width=3.5, shape='spline'),
            marker=dict(size=7, color='#10b981'),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.08)'
        ))

    fig.update_layout(
        title=dict(text="Live Synaptic Weight Trajectory Over Time", font=dict(family="Newsreader", size=18, color="#0f172a")),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        xaxis=dict(title=dict(text="Logical Time Step (t)", font=dict(color="#334155", size=12)), gridcolor="#f1f5f9", zeroline=False, tickfont=dict(color="#334155")),
        yaxis=dict(title=dict(text="Synaptic Weight (w)", font=dict(color="#334155", size=12)), gridcolor="#f1f5f9", zeroline=False, range=[0, 1.8], tickfont=dict(color="#334155")),
        margin=dict(l=45, r=25, t=45, b=45),
        height=270,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#0f172a", size=11))
    )
    st.plotly_chart(fig, width="stretch")

# ──────────────────────────────────────────────────────────────
# SCENE 03 — RECALL CHALLENGE
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div id="scene-03" class="scene-anchor"></div>
<div class="editorial-card">
    <div class="card-step-num">03</div>
    <div class="card-heading">What does Apple remember?</div>
    <div class="card-subtext">
        Query the network with 🍎 <strong>Apple</strong>. The network reads out whichever associated label 
        currently exhibits the strongest synaptic connection.
    </div>
    <div class="beginner-box">
        <div class="beginner-box-title">🧠 IN SIMPLE WORDS</div>
        <div class="beginner-box-text">
            Recall is like asking the network, “What do you currently associate with Apple?” The strongest surviving connection gets selected.
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

col_rec1, col_rec2 = st.columns([1, 1.3], gap="large")

with col_rec1:
    st.markdown('''
    <div style="text-align:center; padding: 1.2rem 0;">
        <div style="font-size:3.5rem; margin-bottom:0.4rem;">🍎 ➔ ❓</div>
        <div style="font-size:1.05rem; font-weight:600; color:#1e293b;">Query the synaptic memory</div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("🔍 ASK THE NETWORK", key="btn_ask_recall"):
        st.session_state.recall_tested = True

with col_rec2:
    recall_winner = model.recall('apple')
    scores = model.recall_scores('apple')
    has_tested = st.session_state.get('recall_tested', False)

    if has_tested or recall_winner:
        if recall_winner:
            winner_emoji = '🔴' if recall_winner == 'red' else '🟢'
            st.markdown(f'''
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:20px; padding:1.75rem;">
                <div style="font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em; color:#4338ca; font-weight:800;">
                    MODEL READOUT
                </div>
                <div style="font-family:'Newsreader', serif; font-size:2.8rem; font-weight:700; color:#0f172a; margin:0.3rem 0;">
                    {recall_winner.upper()} {winner_emoji}
                </div>
                <div style="margin-top:0.6rem; font-size:0.95rem; color:#334155; line-height:1.6;">
                    <strong>Reference association:</strong> Apple ➔ Red (initial learned state)<br>
                    <strong>Readout winner:</strong> {recall_winner.upper()} (Connection weight: <strong>{scores.get(recall_winner, 0.0):.3f}</strong>)<br>
                    <strong>All active traces:</strong> {', '.join([f'{k.upper()}: {v:.3f}' for k, v in scores.items()])}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:20px; padding:1.5rem; color:#475569;">
                ⚠️ <strong>Trace Exhausted:</strong> All synaptic traces have decayed to baseline ($w \\approx 0$). No association could be recalled.
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div style="background:#f8fafc; border:1.5px dashed #cbd5e1; border-radius:20px; padding:2rem; text-align:center; color:#64748b;">
            Click <strong>ASK THE NETWORK</strong> to trigger readout of the highest active weight.
        </div>
        ''', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SCENE 04 — CREATE A CONFLICT (The Wow Moment)
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div id="scene-04" class="scene-anchor"></div>
<div class="editorial-card" style="background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(240,253,244,0.4) 100%);">
    <div class="card-step-num">04</div>
    <div class="card-heading">Now give it a competing memory.</div>
    <div class="card-subtext">
        An apple isn't always red. What happens when the system encounters a Granny Smith apple?
        First teach 🍏 <strong>Apple → Green</strong>. Then predict which association will dominate.
    </div>
    <div class="beginner-box">
        <div class="beginner-box-title">🧠 IN SIMPLE WORDS</div>
        <div class="beginner-box-text">
            The old and new memories are not literally deleting each other here. They are two competing traces,
            and whichever connection is stronger when we ask the network wins the readout.
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div style="background:#ffffff; border:1.5px solid #bbf7d0; border-radius:16px; padding:1.2rem 1.35rem; margin:1.2rem 0 1rem 0;">
    <div style="font-size:0.78rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#15803d; margin-bottom:0.35rem;">
        STEP 1 — TEACH THE NEW MEMORY
    </div>
    <div style="font-size:1rem; color:#334155; line-height:1.5; margin-bottom:0.8rem;">
        Write the new association into the live synaptic state before making your prediction.
    </div>
</div>
''', unsafe_allow_html=True)

if st.button("🍏  TEACH APPLE → GREEN", key="btn_teach_green"):
    model.learn('apple', 'green')
    st.rerun()

w_r_val = model.weight_of('apple', 'red')
w_g_val = model.weight_of('apple', 'green')
green_taught = w_g_val > 0

st.markdown('''
<div style="margin-top:1.25rem; margin-bottom:0.35rem;">
    <div style="font-size:0.78rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#4338ca;">
        STEP 2 — WATCH THE LIVE SYNAPTIC STATE
    </div>
</div>
''', unsafe_allow_html=True)

components.html(
    build_synapse_html(w_r_val, w_g_val, mode='dual'),
    height=380
)

if green_taught:
    st.markdown('''
    <div style="margin-top:0.5rem; margin-bottom:0.35rem;">
        <div style="font-size:0.78rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#4338ca;">
            STEP 3 — MAKE YOUR PREDICTION
        </div>
        <div style="font-family:'Newsreader', Georgia, serif; font-size:1.55rem; font-weight:600; color:#0f172a; margin-top:0.2rem;">
            Which association will dominate the readout?
        </div>
        <div style="font-size:0.92rem; color:#475569; line-height:1.5; margin-top:0.2rem;">
            Choose the connection you think is stronger right now.
        </div>
    </div>
    ''', unsafe_allow_html=True)

    user_pred = st.radio(
        "Your Prediction:",
        options=["🔴 RED — First learned association", "🟢 GREEN — Recently learned association"],
        key="radio_conflict_pred"
    )

    st.markdown('''
    <div class="beginner-box" style="margin-top:0.55rem;">
        <div class="beginner-box-title">🧠 IN SIMPLE WORDS</div>
        <div class="beginner-box-text">
            <strong>Weight</strong> = the connection's current strength. Predict which trace is stronger before the network gives its answer.
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div style="margin-top:1rem; margin-bottom:0.35rem;">
        <div style="font-size:0.78rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#4338ca;">
            STEP 4 — RESOLVE THE CONFLICT
        </div>
    </div>
    ''', unsafe_allow_html=True)

    if st.button("▶  RESOLVE CONFLICT & COMPARE", key="btn_resolve_conflict"):
        st.session_state.conflict_resolved = True

    if st.session_state.get('conflict_resolved', False):
        w_r = model.weight_of('apple', 'red')
        w_g = model.weight_of('apple', 'green')
        actual_winner = model.recall('apple')

        user_picked_red = ("RED" in user_pred)
        model_is_red = (actual_winner == 'red')

        if (user_picked_red and model_is_red) or (not user_picked_red and not model_is_red):
            outcome_badge = "<span style='color:#059669; font-weight:800; font-size:0.95rem;'>✓ PREDICTION MATCHED</span>"
        else:
            outcome_badge = "<span style='color:#dc2626; font-weight:800; font-size:0.95rem;'>✗ PREDICTION MISMATCH</span>"

        diff = abs(w_g - w_r)
        if diff < 0.05:
            dynamic_reason = f"The two traces are close in strength (Red: {w_r:.3f}, Green: {w_g:.3f}), so the readout is near a boundary."
        elif w_g > w_r:
            dynamic_reason = f"Green wins because its current trace ({w_g:.3f}) is stronger than Red's ({w_r:.3f}). Red had more time to decay, while Green received a fresh write."
        else:
            dynamic_reason = f"Red survives because its accumulated trace ({w_r:.3f}) remains stronger than Green's single new write ({w_g:.3f})."

        st.markdown(f'''
        <div style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:18px; padding:1.35rem; margin-top:1rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
                {outcome_badge}
                <span class="stat-pill {'stat-coral' if actual_winner=='red' else 'stat-mint'}">
                    Model Readout: {actual_winner.upper() if actual_winner else 'NONE'}
                </span>
            </div>
            <div style="margin-top:0.85rem; font-size:0.92rem; color:#1e293b; line-height:1.55;">
                <strong>Your prediction:</strong> {user_pred.split(" ")[1]}<br>
                <strong>Red trace:</strong> {w_r:.3f} &nbsp; · &nbsp; <strong>Green trace:</strong> {w_g:.3f}
                <div style="margin-top:0.55rem; color:#334155;">
                    <strong>Why?</strong> {dynamic_reason}
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
else:
    st.markdown('''
    <div style="background:#f8fafc; border:1.5px dashed #cbd5e1; border-radius:16px; padding:1.2rem; margin-top:1rem; color:#64748b;">
        <strong>Teach Apple → Green first.</strong> The prediction step appears after the new memory has been written.
    </div>
    ''', unsafe_allow_html=True)

st.markdown('''
<div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:16px; padding:1.25rem; margin-top:1.5rem; font-size:0.92rem; color:#334155; line-height:1.6;">
    ⚖️ <strong>Scientific Simplification: Competing Association Traces at Readout:</strong><br>
    In this educational toy, competing memories are represented as <em>separate traces</em> whose relative strengths determine the readout via <em>argmax</em>.
    Learning Green does not physically destroy or overwrite the Red synapse; rather, competition occurs at retrieval.
</div>
''', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SCENE 05 — THE MEMORY LAB (Contextual Controls)
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div id="scene-05" class="scene-anchor"></div>
<div class="editorial-card" style="background: linear-gradient(180deg, #ffffff 0%, #f5f3ff 100%);">
    <div class="card-step-num">05</div>
    <div class="card-heading">The Memory Lab: Change the Rules.</div>
    <div class="card-subtext">
        Adjust the intrinsic physics of the synapse. Observe how the trade-off between 
        <em>remembering recent information</em> and <em>being influenced by new information</em> responds.
    </div>
    <div class="beginner-box">
        <div class="beginner-box-title">🧠 IN SIMPLE WORDS</div>
        <div class="beginner-box-text">
            Plasticity controls how strongly new experiences change the connection. Persistence controls how long the old change sticks around.
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

lab_c1, lab_c2, lab_c3 = st.columns(3, gap="medium")

with lab_c1:
    st.markdown("<strong style='color:#0f172a;'>PLASTICITY STRENGTH (η)</strong>", unsafe_allow_html=True)
    st.caption("How strongly does a new event change the trace?")
    new_lr = st.slider("Plasticity (Learning Rate)", 0.10, 1.20, float(st.session_state.learning_rate), 0.05, key="slider_lab_lr")
    if new_lr != st.session_state.learning_rate:
        st.session_state.learning_rate = new_lr
        model.learning_rate = new_lr

with lab_c2:
    st.markdown("<strong style='color:#0f172a;'>PERSISTENCE FACTOR (δ)</strong>", unsafe_allow_html=True)
    st.caption("How much of the trace survives each time step?")
    new_decay = st.slider("Persistence (Decay Factor)", 0.40, 0.98, float(st.session_state.decay), 0.02, key="slider_lab_decay")
    if new_decay != st.session_state.decay:
        st.session_state.decay = new_decay
        model.decay = new_decay

with lab_c3:
    st.markdown("<strong style='color:#0f172a;'>WHAT CHANGED?</strong>", unsafe_allow_html=True)
    half_life = np.log(0.5) / np.log(model.decay) if model.decay < 0.999 else 999.0
    st.markdown(f'''
    <div style="background:#ffffff; border:1px solid #e9d5ff; border-radius:16px; padding:1.15rem; font-size:0.9rem; color:#1e293b; line-height:1.55;">
        <div><strong>Trace Half-life:</strong> ~{half_life:.1f} steps</div>
        <div style="margin-top:0.4rem; color:#6b21a8; font-weight:600;">
            { '⚡ HIGHER PLASTICITY: New memories written strongly; fast one-shot acquisition.' if model.learning_rate >= 0.8 else '🐢 LOWER PLASTICITY: Slower acquisition; requires repeated rehearsal.' }
        </div>
        <div style="margin-top:0.4rem; color:#312e81; font-weight:600;">
            { '🛡️ HIGHER PERSISTENCE: Older traces survive longer, resisting immediate displacement.' if model.decay >= 0.85 else '🍃 LOWER PERSISTENCE: Rapid fading; recent signals overwhelmingly dominate.' }
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SCENE 06 — UNDER THE HOOD (The Mathematical Rule)
# ──────────────────────────────────────────────────────────────
st.markdown('<div id="scene-06" class="scene-anchor"></div>', unsafe_allow_html=True)
with st.expander("🔬 Look under the hood: The Educational Toy Update Rule", expanded=False):
    st.markdown('''
    <div style="padding:0.75rem 0;">
        <span class="pill-badge badge-toy" style="margin-bottom:0.75rem;">EDUCATIONAL TOY UPDATE RULE</span>
        <p style="font-size:0.98rem; color:#334155; line-height:1.6; margin-top:0.5rem;">
            This educational model computes state transitions via an explicit, transparent Hebbian recurrence with exponential decay:
        </p>
    </div>
    ''', unsafe_allow_html=True)

    st.latex(r"w(t+1) = \delta \cdot w(t) + \eta \cdot \text{pre} \cdot \text{post}")

    st.markdown('''
    <div class="beginner-box">
        <div class="beginner-box-title">🧠 IN SIMPLE WORDS</div>
        <div class="beginner-box-text">
            Every update does two things: it lets some old memory survive, then adds new strength when both neurons are active together.
        </div>
    </div>
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:1rem; margin-top:1.25rem;">
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:1.1rem;">
            <div style="font-weight:700; color:#4338ca; margin-bottom:0.3rem;">δ · w(t) — Old Trace</div>
            <div style="font-size:0.88rem; color:#334155; line-height:1.5;">What survives passively from the previous state via decay factor δ ∈ [0, 1].</div>
        </div>
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:1.1rem;">
            <div style="font-weight:700; color:#e11d48; margin-bottom:0.3rem;">η · pre · post — New Write</div>
            <div style="font-size:0.88rem; color:#334155; line-height:1.5;">What gets written by coincident pre- and post-synaptic activity scaled by plasticity η.</div>
        </div>
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:1.1rem;">
            <div style="font-weight:700; color:#059669; margin-bottom:0.3rem;">w(t+1) — New Synaptic State</div>
            <div style="font-size:0.88rem; color:#334155; line-height:1.5;">The resulting connection strength that determines subsequent retrieval.</div>
        </div>
    </div>
    <div style="margin-top:1.1rem; font-size:0.86rem; color:#64748b;">
        *Note: This simplified update rule is designed for pedagogical clarity and does not implement the exact matrix equations of BDH or complex biological biophysics.
    </div>
    ''', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SCENE 07 — EVIDENCE TRAIL (Verified 2022–2026 Primary Literature)
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div id="scene-07" class="scene-anchor"></div>
<div class="editorial-card">
    <div class="card-step-num">07</div>
    <div class="card-heading">The Evidence Trail.</div>
    <div class="card-subtext">
        Four primary papers connecting biological neurodynamics, working memory, and frontier artificial intelligence.
    </div>
    <div class="beginner-box">
        <div class="beginner-box-title">🧠 WHY ARE WE SHOWING THESE PAPERS?</div>
        <div class="beginner-box-text">
            The toy model is simplified. These papers provide the research context for short-term plasticity, memory traces, recency, and related computational mechanisms.
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

evidence_items = [
    {
        "num": "01",
        "authors": "Garcia Rodriguez, H., Guo, Q., & Moraitis, T. (2022)",
        "title": "Short-Term Plasticity Neurons Learning to Learn and Forget",
        "venue": "ICML 2022 / PMLR 162:18704–18722",
        "link": "https://proceedings.mlr.press/v162/rodriguez22b.html",
        "finding": "STPNs use synapses with internal state propagated through time, enabling rapid short-term learning and forgetting without changing permanent structural weights.",
        "impact": "Safe connection: Motivates representing short-term memory as dynamic synaptic state rather than static parameters. (Our toy does not claim to implement STPN)."
    },
    {
        "num": "02",
        "authors": "Kozachkov, L., Tauber, J., Lundqvist, M., Brincat, S. L., Slotine, J.-J., & Miller, E. K. (2022)",
        "title": "Robust and brain-like working memory through short-term synaptic plasticity",
        "venue": "PLOS Computational Biology 18(12): e1010776",
        "link": "https://doi.org/10.1371/journal.pcbi.1010776",
        "finding": "Demonstrated that recurrent neural networks equipped with short-term synaptic plasticity could maintain working memories despite distractors, exhibiting robust brain-like activity.",
        "impact": "Safe connection: In their RNN experiments, STSP supported working-memory maintenance and was associated with more brain-like activity and greater robustness to network degradation."
    },
    {
        "num": "03",
        "authors": "Chrysanthidis, N., Fiebig, F., Lansner, A., & Herman, P. (2025)",
        "title": "Short-term plasticity influences episodic memory recall: an interplay of synaptic traces in a spiking neural network model",
        "venue": "Scientific Reports 15: 28164",
        "link": "https://doi.org/10.1038/s41598-025-12611-5",
        "finding": "Investigates interactions between episodic memory recall and short-term recency effects through interacting synaptic traces in a spiking neural network.",
        "impact": "Safe connection: Our conflict experiment is an educational simplification inspired by the paper's treatment of interacting synaptic traces and recency."
    },
    {
        "num": "04",
        "authors": "Kosowski, A. et al. (2025)",
        "title": "The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain",
        "venue": "arXiv:2509.26507",
        "link": "https://arxiv.org/abs/2509.26507",
        "finding": "Introduces a brain-inspired architecture where working memory during inference relies on synaptic plasticity with Hebbian learning using spiking neurons, with individual synapses strengthening around concepts.",
        "impact": "Safe connection: Demonstrates that synaptic plasticity can serve as a substantive working-memory mechanism in large-scale frontier AI models."
    }
]

for ev in evidence_items:
    st.markdown(f'''
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; padding:1.4rem; margin-bottom:1rem; display:flex; gap:1.25rem; align-items:flex-start;">
        <div style="font-family:'Newsreader', serif; font-style:italic; font-size:1.8rem; color:#6366f1; line-height:1;">{ev['num']}</div>
        <div style="flex:1;">
            <div style="display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:0.5rem;">
                <span style="font-weight:700; color:#0f172a; font-size:1rem;">{ev['authors']}</span>
                <a href="{ev['link']}" target="_blank" style="text-decoration:none;">
                    <span class="pill-badge badge-toy" style="font-size:0.7rem; cursor:pointer;">{ev['venue']} ↗</span>
                </a>
            </div>
            <div style="font-style:italic; color:#334155; margin:0.3rem 0 0.5rem 0; font-size:0.95rem; font-weight:500;">{ev['title']}</div>
            <div style="font-size:0.9rem; color:#1e293b; line-height:1.5;"><strong>What it shows:</strong> {ev['finding']}</div>
            <div style="font-size:0.87rem; color:#4338ca; margin-top:0.4rem; line-height:1.5;"><strong>Why it matters here:</strong> {ev['impact']}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SCENE 08 — SCALE UP: FROM SYNAPSE TO DRAGON HATCHLING (BDH)
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div id="scene-08" class="scene-anchor"></div>
<div class="editorial-card" style="background: linear-gradient(135deg, #ffffff 0%, #faf5ff 100%); border-color: #e9d5ff;">
    <div class="card-step-num">08</div>
    <div class="card-heading">From a single synapse to Dragon Hatchling (BDH)</div>
    <div class="card-subtext">
        You just saw a tiny version of the idea. Now scale the idea up. 
        BDH provides a frontier architecture where synaptic plasticity plays a substantive role in working memory during inference.
    </div>
    <div class="beginner-box">
        <div class="beginner-box-title">🧠 IN SIMPLE WORDS</div>
        <div class="beginner-box-text">
            Our toy uses one simple number to make the idea visible. BDH scales the idea up into a much richer neural architecture with high-dimensional synaptic state.
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:22px; padding:1.8rem; margin-bottom:1.75rem;">
    <div style="display:grid; grid-template-columns: 1fr auto 1fr; gap:1.25rem; align-items:center; text-align:center;">
        <div style="background:#fff7ed; border:1px solid #fed7aa; border-radius:16px; padding:1.25rem;">
            <span class="pill-badge badge-toy">OUR EDUCATIONAL TOY</span>
            <div style="font-size:2rem; margin:0.6rem 0;">🍎 ➔ 🔗 ➔ 🔴</div>
            <div style="font-size:0.88rem; color:#334155; line-height:1.45;">
                Scalar synaptic weight dictionary · Single concept pairs · Educational Hebbian update
            </div>
        </div>
        <div style="font-size:1.8rem; color:#7c3aed; font-weight:700;">➔</div>
        <div style="background:#faf5ff; border:1px solid #e9d5ff; border-radius:16px; padding:1.25rem;">
            <span class="pill-badge badge-bdh">PUBLISHED BDH ARCHITECTURE</span>
            <div style="font-size:2rem; margin:0.6rem 0;">🧠 ⚡ 🔗</div>
            <div style="font-size:0.88rem; color:#334155; line-height:1.45;">
                High-dimensional synaptic state within a brain-inspired spiking neuron architecture
            </div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Detailed Comparison Matrix
comparison_rows = [
    ("Memory Substrate", "Scalar dictionary weights w(concept, label)", "High-dimensional synaptic state within a brain-inspired architecture"),
    ("Write Mechanism", "Simplified Hebbian increment (w ← δw + η·pre·post)", "Synaptic plasticity with Hebbian learning using spiking neurons"),
    ("Decay / Dynamics", "Uniform multiplicative decay per step (δ^Δt)", "Transient biological synaptic decay and activation dynamics"),
    ("Readout", "Argmax over active scalar traces", "Attention-like projection and readout through spiking neuron layers"),
    ("Scale", "Educational toy (1–2 concept associations)", "Full sequence-level language / representation scale"),
    ("Evidence Status", "Transparent live computational code in model.py", "Published frontier research (Kosowski et al., 2025, arXiv:2509.26507)")
]

table_html = "<table style='width:100%; border-collapse:collapse; background:#ffffff; border-radius:16px; overflow:hidden; border:1px solid #e2e8f0;'>"
table_html += "<tr style='background:#f8fafc; border-bottom:1.5px solid #e2e8f0;'><th style='padding:0.9rem; text-align:left; font-size:0.84rem; color:#0f172a; font-weight:800;'>DIMENSION</th><th style='padding:0.9rem; text-align:left; font-size:0.84rem; color:#4338ca; font-weight:800;'>OUR EDUCATIONAL TOY</th><th style='padding:0.9rem; text-align:left; font-size:0.84rem; color:#7e22ce; font-weight:800;'>PUBLISHED BDH ARCHITECTURE</th></tr>"
for dim, toy, bdh in comparison_rows:
    table_html += f"<tr style='border-bottom:1px solid #f1f5f9;'><td style='padding:0.85rem; font-weight:700; font-size:0.88rem; color:#0f172a;'>{dim}</td><td style='padding:0.85rem; font-size:0.88rem; color:#334155;'>{toy}</td><td style='padding:0.85rem; font-size:0.88rem; color:#334155;'>{bdh}</td></tr>"
table_html += "</table>"
st.markdown(table_html, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SCENE 09 — LIMITATIONS ("One Thing This Model Does NOT Tell You")
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div id="scene-09" class="scene-anchor"></div>
<div class="editorial-card" style="background:#fef2f2; border:1.5px solid #fecaca;">
    <div class="card-step-num" style="color:#dc2626;">09</div>
    <div class="card-heading" style="color:#991b1b;">One Thing This Model Does NOT Tell You</div>
    <div class="card-subtext" style="color:#7f1d1d;">
        Scientific honesty is paramount. This is an educational toy model, not a biological simulation and not an implementation of BDH.
    </div>
    <div class="beginner-box" style="background:#fff1f2; border-color:#fecdd3; margin-top:0.75rem;">
        <div class="beginner-box-title" style="color:#9f1239;">🧠 WHY THIS MATTERS</div>
        <div class="beginner-box-text" style="color:#881337;">
            A simpler model is easier to understand and experiment with, but it is not the same as simulating a biological brain or reproducing the full BDH architecture.
        </div>
    </div>
    <div style="margin-top:1.25rem; display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:1rem;">
        <div style="background:#ffffff; border:1px solid #fee2e2; border-radius:14px; padding:1rem;">
            <div style="font-weight:700; color:#b91c1c; font-size:0.92rem;">Scalar vs. High-Dimensional State</div>
            <div style="font-size:0.86rem; color:#475569; margin-top:0.25rem;">Our toy tracks single scalar floats. Real biological synapses and BDH utilize multi-dimensional state embeddings.</div>
        </div>
        <div style="background:#ffffff; border:1px solid #fee2e2; border-radius:14px; padding:1rem;">
            <div style="font-weight:700; color:#b91c1c; font-size:0.92rem;">Simplified Hebbian Update</div>
            <div style="font-size:0.86rem; color:#475569; margin-top:0.25rem;">Biological plasticity involves complex vesicle depletion, calcium kinetics, and spike-timing-dependent plasticity (STDP).</div>
        </div>
        <div style="background:#ffffff; border:1px solid #fee2e2; border-radius:14px; padding:1rem;">
            <div style="font-weight:700; color:#b91c1c; font-size:0.92rem;">Simplified Readout</div>
            <div style="font-size:0.86rem; color:#475569; margin-top:0.25rem;">We choose the max-weight label via argmax. Biological memory retrieval emerges from complex attractor dynamics across entire neural populations.</div>
        </div>
        <div style="background:#ffffff; border:1px solid #fee2e2; border-radius:14px; padding:1rem;">
            <div style="font-weight:700; color:#b91c1c; font-size:0.92rem;">No Biological Proof</div>
            <div style="font-size:0.86rem; color:#475569; margin-top:0.25rem;">This simulation does not prove that the brain uses this exact mechanism; it illustrates the mathematical logic of the stability-plasticity trade-off.</div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SCENE 10 — FINAL CHALLENGE (Live Numerical Computation)
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div id="scene-10" class="scene-anchor"></div>
<div class="dark-editorial-card">
    <div class="dark-section-number">10</div>
    <div class="dark-section-heading">The Final Challenge: Test Your Scientific Intuition</div>
    <div class="dark-section-body">
        Change the memory conditions, make a prediction, then test it with the live mathematical model.
    </div>
    <div class="beginner-box" style="background:rgba(255,255,255,0.08); border-color:rgba(199,210,254,0.3); margin-top:0.75rem;">
        <div class="beginner-box-title" style="color:#c7d2fe;">🧠 IN SIMPLE WORDS</div>
        <div class="beginner-box-text" style="color:#f1f5f9;">
            You are testing whether an older, repeatedly reinforced memory can survive long enough to beat a newer memory.
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:20px; padding:1.8rem; margin-bottom:1.5rem; box-shadow:0 8px 24px -4px rgba(15, 23, 42, 0.05);">
    <div style="font-weight:800; font-size:1.15rem; color:#0f172a; margin-bottom:0.4rem;">
        Scenario: Repeated Learning vs. Delay vs. New Write
    </div>
    <div style="color:#334155; font-size:0.96rem; line-height:1.6;">
        A neural network experiences:
        <ol style="margin-top:0.4rem; padding-left:1.3rem;">
            <li><strong>5 × consecutive presentations</strong> of 🍎 <strong>Apple → Red</strong></li>
            <li><strong>A delay of Δt steps</strong> with passive decay</li>
            <li><strong>1 × presentation</strong> of 🍏 <strong>Apple → Green</strong></li>
        </ol>
        Your task is to change the conditions, predict the stronger trace, and then test your prediction.
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div style="margin-top:0.4rem; margin-bottom:0.8rem;">
    <div style="font-size:0.82rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#4338ca;">
        1 — Set the Memory Conditions
    </div>
    <div style="font-size:0.94rem; color:#475569; line-height:1.5; margin-top:0.2rem;">
        Change the conditions before deciding what you think will happen.
    </div>
</div>
''', unsafe_allow_html=True)

control_a, control_b = st.columns(2, gap="large")

with control_a:
    st.markdown('''
    <div style="margin-bottom:0.2rem;">
        <div style="font-weight:800; font-size:1.02rem; color:#0f172a;">🕰️ PERSISTENCE (δ)</div>
        <div style="font-size:0.88rem; color:#475569; line-height:1.45;">
            How much of the old memory survives each time step?
            <strong>Higher persistence → slower decay → older traces last longer.</strong>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    challenge_decay = st.slider(
        "Persistence (Decay Factor)", 0.60, 0.99, float(model.decay), 0.01,
        key="slider_challenge_decay", label_visibility="collapsed"
    )

with control_b:
    st.markdown('''
    <div style="margin-bottom:0.2rem;">
        <div style="font-weight:800; font-size:1.02rem; color:#0f172a;">⏳ DELAY (Δt)</div>
        <div style="font-size:0.88rem; color:#475569; line-height:1.45;">
            How many time steps pass before the new memory is written?
            <strong>Longer delay → more time for the old trace to decay.</strong>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    challenge_delay = st.slider(
        "Delay (time steps Δt)", 5, 30, 20, 1,
        key="slider_challenge_delay", label_visibility="collapsed"
    )

st.markdown(f'''
<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:16px; padding:1.15rem 1.3rem; margin-top:1.25rem;">
    <div style="font-size:0.82rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#4338ca; margin-bottom:0.55rem;">
        2 — Your Experiment
    </div>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:0.65rem; font-size:0.92rem; color:#334155;">
        <div>🔴 Red presentations: <strong>5</strong></div>
        <div>⏳ Delay: <strong>{challenge_delay} steps</strong></div>
        <div>🟢 Green presentations: <strong>1</strong></div>
        <div>🧠 Plasticity (η): <strong>{model.learning_rate:.2f}</strong></div>
        <div>🕰️ Persistence (δ): <strong>{challenge_decay:.2f}</strong></div>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div style="margin-top:1.35rem; margin-bottom:0.35rem;">
    <div style="font-size:0.82rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#4338ca;">
        3 — Make Your Prediction
    </div>
    <div style="font-family:'Newsreader', Georgia, serif; font-size:1.6rem; font-weight:600; color:#0f172a; margin-top:0.2rem;">
        Which association will have the stronger trace?
    </div>
    <div style="font-size:0.9rem; color:#475569; line-height:1.5; margin-top:0.2rem;">
        Predict before the model reveals the answer.
    </div>
</div>
''', unsafe_allow_html=True)

challenge_user_pred = st.radio(
    "Your Prediction:",
    ["🔴 RED — Accumulated earlier trace", "🟢 GREEN — Single recent write"],
    key="radio_final_challenge"
)

st.markdown('''
<div class="beginner-box" style="margin-top:0.6rem;">
    <div class="beginner-box-title">🧠 IN SIMPLE WORDS</div>
    <div class="beginner-box-text">
        <strong>Weight</strong> = the connection's current strength. Your job is to predict which connection will be stronger after the selected delay and new write.
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div style="margin-top:1.35rem; margin-bottom:0.45rem;">
    <div style="font-size:0.82rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#4338ca;">
        4 — Test Your Prediction
    </div>
    <div style="font-size:0.9rem; color:#475569; line-height:1.5; margin-top:0.2rem;">
        Now run the exact live computation from the educational update rule.
    </div>
</div>
''', unsafe_allow_html=True)

check_clicked = st.button("▶  RUN LIVE COMPUTATION & EVALUATE", key="btn_check_challenge")

if check_clicked:
    sim_res = SynapticMemoryModel.simulate_scenario(
        decay=challenge_decay,
        learning_rate=model.learning_rate,
        red_reps=5,
        delay=challenge_delay,
        green_reps=1
    )

    w_red_learned = sim_res['w_red_after_learning']
    w_red_decayed = sim_res['w_red_after_delay']
    w_red_fin = sim_res['w_red_final']
    w_green_fin = sim_res['w_green_final']
    sim_winner = sim_res['winner']

    user_pred_red = ("RED" in challenge_user_pred)
    sim_is_red = (sim_winner == 'red')

    if (user_pred_red and sim_is_red) or (not user_pred_red and not sim_is_red):
        eval_badge = "✓ PREDICTION CORRECT"
        badge_class = "result-correct"
    else:
        eval_badge = "✗ PREDICTION INCORRECT"
        badge_class = "result-incorrect"

    if sim_winner == 'red':
        why_text = (
            f"Red wins because its surviving trace ({w_red_fin:.3f}) is stronger than "
            f"Green's new trace ({w_green_fin:.3f}). Repeated learning built Red's trace, "
            f"and enough of it survived the selected delay."
        )
    else:
        why_text = (
            f"Green wins because its fresh trace ({w_green_fin:.3f}) is stronger than "
            f"Red's surviving trace ({w_red_fin:.3f}). The selected delay allowed Red to "
            f"lose enough strength before Green was written."
        )

    st.markdown(f'''
    <div style="margin-top:1.5rem; background:#ffffff; border:1.5px solid #cbd5e1; border-radius:20px; padding:1.6rem; box-shadow:0 10px 28px -8px rgba(15,23,42,0.08);">
        <div style="font-size:0.82rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#4338ca; margin-bottom:0.65rem;">
            5 — What Actually Happened?
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.7rem; margin-bottom:1rem;">
            <span class="{badge_class}">{eval_badge}</span>
            <span class="stat-pill {'stat-coral' if sim_winner=='red' else 'stat-mint'}">
                Model Readout: {sim_winner.upper()}
            </span>
        </div>
        <div style="font-size:0.95rem; color:#0f172a; line-height:1.7;">
            <strong>Your prediction:</strong> {'RED' if user_pred_red else 'GREEN'}<br>
            <strong>Red final trace:</strong> <code>w = {w_red_fin:.3f}</code><br>
            <strong>Green final trace:</strong> <code>w = {w_green_fin:.3f}</code>
            <ul style="margin:0.65rem 0 0.75rem 1.2rem; padding:0; color:#1e293b;">
                <li>Red after 5 writes: <code>w = {w_red_learned:.3f}</code></li>
                <li>Red after {challenge_delay} delay steps: <code>w = {w_red_decayed:.3f}</code></li>
                <li>Decay factor over the delay: <code>δ^{challenge_delay} = {challenge_decay**challenge_delay:.4f}</code></li>
                <li>Green after 1 write: <code>w = {w_green_fin:.3f}</code></li>
            </ul>
            <div style="background:#ffffff; border-left:3.5px solid #4338ca; padding:0.85rem 1rem; border-radius:8px; margin-top:0.65rem; color:#1e293b; border-top:1px solid #f1f5f9; border-right:1px solid #f1f5f9; border-bottom:1px solid #f1f5f9;">
                <strong>Why?</strong> {why_text}
            </div>
            <div style="background:#eef2ff; border:1px solid #c7d2fe; padding:0.85rem 1rem; border-radius:10px; margin-top:0.7rem; color:#312e81;">
                <strong>What this tests:</strong> The winner depends on the interaction between accumulated learning,
                persistence, delay, and the strength of the new write.
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('''
    <div style="background:#f8fafc; border:1.5px dashed #cbd5e1; border-radius:16px; padding:1.25rem; margin-top:1rem; text-align:center; color:#64748b;">
        <strong>Ready to test.</strong> Your result will appear directly below the button after you make your prediction.
    </div>
    ''', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# MEMORABLE FINAL TAKEAWAY & FOOTER
# ──────────────────────────────────────────────────────────────
st.markdown('''
<div style="text-align:center; padding: 3.5rem 1rem 1rem 1rem; border-top: 1px solid #e2e8f0;">
    <div style="font-family:'Plus Jakarta Sans', sans-serif; font-size:0.8rem; font-weight:800; letter-spacing:0.18em; text-transform:uppercase; color:#64748b; margin-bottom:0.8rem;">
        THE CORE TAKEAWAY
    </div>
    <div style="font-family:'Newsreader', Georgia, serif; font-size:clamp(2.1rem, 4.2vw, 2.9rem); font-weight:600; color:#0f172a; max-width:820px; margin:0 auto 1.25rem auto; line-height:1.25;">
        “Memory can live in a changing state.”
    </div>
    <div style="font-size:1.15rem; color:#334155; max-width:700px; margin:0 auto; line-height:1.65;">
        The very plasticity that allows an intelligent system to rapidly adapt to a changing environment 
        inherently forces recent signals to compete with what came before.
    </div>
    <div style="margin-top:2.75rem; font-size:0.82rem; color:#64748b; line-height:1.6;">
        DataForge 2026 Hackathon · Pathway Track · “Explain the Frontier” · Synaptic Plasticity & BDH<br>
        <span style="color:#94a3b8;">Built with Streamlit & Plotly · Live Computational Substrate</span>
    </div>
</div>
''', unsafe_allow_html=True)

"""
AI Powered Online Home and Interior Design System
Main Application – Streamlit
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, date, timedelta
import time
import random

from database import (
    init_db, register_user, login_user, save_design_request,
    get_user_designs, get_all_designers, create_booking,
    get_user_bookings, admin_stats, admin_all_users, admin_all_bookings,
)
from ai_engine import generate_recommendations, COLOR_PALETTES, BUDGET_ADVICE

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interior Design Studio",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Fonts & Base ---- */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, .brand-title {
    font-family: 'Playfair Display', serif !important;
}

/* ---- Hide Streamlit chrome ---- */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f1f1f1; }
::-webkit-scrollbar-thumb { background: #8B5E3C; border-radius: 3px; }

/* ---- Hero Banner ---- */
.hero-banner {
    background: linear-gradient(135deg, #2C1810 0%, #5C3317 40%, #8B5E3C 80%, #C4956A 100%);
    border-radius: 20px;
    padding: 60px 40px;
    text-align: center;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(44,24,16,0.3);
}
.hero-banner::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 3.2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 10px 0;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
    letter-spacing: -1px;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #E8D5C0;
    font-weight: 300;
    letter-spacing: 1px;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    color: #FFE8CC;
    padding: 4px 16px;
    border-radius: 50px;
    font-size: 0.8rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

/* ---- Cards ---- */
.card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid rgba(139,94,60,0.08);
    margin-bottom: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.1);
}

/* ---- Stat Cards ---- */
.stat-card {
    background: linear-gradient(135deg, #8B5E3C, #C4956A);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 24px rgba(139,94,60,0.3);
}
.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
}
.stat-label {
    font-size: 0.85rem;
    opacity: 0.85;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ---- Palette Chip ---- */
.palette-chip {
    display: inline-block;
    width: 30px; height: 30px;
    border-radius: 50%;
    border: 2px solid white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    margin: 0 3px;
    vertical-align: middle;
}

/* ---- Designer Card ---- */
.designer-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #EDE5DC;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
}
.designer-card:hover {
    border-color: #8B5E3C;
    box-shadow: 0 12px 40px rgba(139,94,60,0.15);
    transform: translateY(-4px);
}
.designer-rating {
    color: #F4C542;
    font-size: 1rem;
}

/* ---- Score Badge ---- */
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #27AE60, #2ECC71);
    color: white;
    font-size: 2rem;
    font-weight: 700;
    width: 90px; height: 90px;
    border-radius: 50%;
    line-height: 90px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(39,174,96,0.35);
    font-family: 'Playfair Display', serif;
}

/* ---- Concept Card ---- */
.concept-card {
    background: linear-gradient(135deg, #FAF7F4 0%, #F0EAE2 100%);
    border-radius: 14px;
    padding: 20px;
    border-left: 4px solid #8B5E3C;
    margin-bottom: 15px;
    transition: all 0.2s ease;
}
.concept-card:hover {
    background: white;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

/* ---- Tip Tag ---- */
.tip-tag {
    background: #F0EAE2;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 5px 0;
    font-size: 0.9rem;
    border-left: 3px solid #8B5E3C;
    color: #4A3728;
}

/* ---- Section Header ---- */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 2px solid #F0EAE2;
}
.section-icon {
    font-size: 1.8rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #2C1810;
    margin: 0;
}

/* ---- Auth Form ---- */
.auth-container {
    max-width: 460px;
    margin: 0 auto;
    background: white;
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.08);
    border: 1px solid #EDE5DC;
}

/* ---- Toast-style alerts ---- */
.success-toast {
    background: linear-gradient(135deg, #D4EDDA, #C3E6CB);
    border-left: 4px solid #28A745;
    border-radius: 10px;
    padding: 14px 18px;
    color: #155724;
    margin: 10px 0;
    font-weight: 500;
}
.info-toast {
    background: linear-gradient(135deg, #D1ECF1, #BEE5EB);
    border-left: 4px solid #17A2B8;
    border-radius: 10px;
    padding: 14px 18px;
    color: #0C5460;
    margin: 10px 0;
    font-weight: 500;
}
.warning-toast {
    background: linear-gradient(135deg, #FFF3CD, #FFEEBA);
    border-left: 4px solid #FFC107;
    border-radius: 10px;
    padding: 14px 18px;
    color: #856404;
    margin: 10px 0;
    font-weight: 500;
}

/* ---- Nav Pills ---- */
.nav-pills {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}
.nav-pill {
    background: #F0EAE2;
    border: none;
    border-radius: 50px;
    padding: 8px 20px;
    font-size: 0.9rem;
    color: #5C3317;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Inter', sans-serif;
}
.nav-pill.active {
    background: #8B5E3C;
    color: white;
    box-shadow: 0 4px 12px rgba(139,94,60,0.3);
}

/* ---- Booking Timeline ---- */
.booking-item {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 16px;
    border-radius: 12px;
    background: #FAFAF8;
    border: 1px solid #EDE5DC;
    margin-bottom: 12px;
}
.booking-dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    background: #8B5E3C;
    margin-top: 5px;
    flex-shrink: 0;
}

/* ---- Step Indicator ---- */
.step-indicator {
    display: flex;
    justify-content: center;
    gap: 0;
    margin-bottom: 30px;
}
.step {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    max-width: 160px;
}
.step-circle {
    width: 40px; height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 6px;
    z-index: 1;
}
.step-active { background: #8B5E3C; color: white; box-shadow: 0 4px 12px rgba(139,94,60,0.4); }
.step-done { background: #27AE60; color: white; }
.step-pending { background: #EDE5DC; color: #8B7355; }
.step-label { font-size: 0.75rem; color: #666; text-align: center; }

/* ---- Footer ---- */
.app-footer {
    text-align: center;
    padding: 24px;
    color: #9B8A7A;
    font-size: 0.82rem;
    border-top: 1px solid #EDE5DC;
    margin-top: 40px;
}

/* ---- Sidebar ---- */
.sidebar-brand {
    text-align: center;
    padding: 20px 0 10px;
}
.sidebar-logo {
    font-size: 2.5rem;
    margin-bottom: 6px;
}
.sidebar-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: #2C1810;
    font-weight: 700;
}
.sidebar-tagline {
    font-size: 0.75rem;
    color: #9B8A7A;
    letter-spacing: 1px;
}

/* ---- Streamlit input overrides ---- */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    border-radius: 10px !important;
    border: 1.5px solid #E0D5CA !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #8B5E3C !important;
    box-shadow: 0 0 0 3px rgba(139,94,60,0.12) !important;
}

.stButton > button {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Initialise DB & Session State ───────────────────────────────────────────────
init_db()

def init_session():
    defaults = {
        "logged_in": False, "user": None,
        "page": "home", "last_design": None,
        "show_results": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ── Helper Components ──────────────────────────────────────────────────────────
def star_rating(rating):
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + "⯨" * half + "☆" * empty

def colour_swatch(hex_color, size=40, label=""):
    return f"""<div style="display:inline-block;text-align:center;margin:4px;">
        <div style="width:{size}px;height:{size}px;border-radius:50%;background:{hex_color};
                    border:2px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.2);margin:0 auto 4px;"></div>
        <div style="font-size:0.65rem;color:#666;">{label}</div>
    </div>"""

def section_header(icon, title):
    st.markdown(f"""
    <div class="section-header">
        <span class="section-icon">{icon}</span>
        <h2 class="section-title">{title}</h2>
    </div>""", unsafe_allow_html=True)

def toast_success(msg):
    st.markdown(f'<div class="success-toast">✅ {msg}</div>', unsafe_allow_html=True)

def toast_info(msg):
    st.markdown(f'<div class="info-toast">ℹ️ {msg}</div>', unsafe_allow_html=True)

def toast_warning(msg):
    st.markdown(f'<div class="warning-toast">⚠️ {msg}</div>', unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
def render_header():
    # Using columns to create a horizontal navigation bar at the top
    col_logo, col_nav = st.columns([1, 4])
    
    with col_logo:
        st.markdown('<h2 style="margin:0; color:#8B5E3C;">🏠 InteriorAI</h2>', unsafe_allow_html=True)

    with col_nav:
        # Define role safely to prevent UnboundLocalError
        is_logged_in = st.session_state.get('logged_in', False)
        user = st.session_state.get('user', {})
        role = user.get('role', 'user') if user else 'user'

        # Create horizontal buttons
        if is_logged_in:
            cols = st.columns(7)
            nav_items = [
                ("📊 Dash", "dashboard"), ("✨ AI Wizard", "design"), 
                ("📋 Designs", "my_designs"), ("📅 Bookings", "bookings"),
                ("👨‍🎨 Designers", "designers"), ("💳 Pay", "payment")
            ]
            
            for i, (label, page_key) in enumerate(nav_items):
                if cols[i].button(label, key=f"head_{page_key}", use_container_width=True):
                    st.session_state.page = page_key
                    st.rerun()
            
            if cols[6].button("🚪 Logout", type="secondary", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.page = "home"
                st.rerun()
        else:
            # Guest header buttons
            cols = st.columns([3, 1, 1, 1])
            if cols[1].button("🏠 Home", use_container_width=True):
                st.session_state.page = "home"; st.rerun()
            if cols[2].button("🔐 Login", use_container_width=True):
                st.session_state.page = "login"; st.rerun()
            if cols[3].button("📝 Register", use_container_width=True, type="primary"):
                st.session_state.page = "register"; st.rerun()
    st.markdown("---")

# ── Pages ──────────────────────────────────────────────────────────────────────

def page_home():
    # Hero
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">✦ AI-Powered Interior Design ✦</div>
        <h1 class="hero-title">Transform Your Space,<br>Intelligently.</h1>
        <p class="hero-subtitle">Personalised design recommendations · Professional bookings · Stunning results</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature Cards
    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("🤖", "AI Recommendations", "Smart suggestions based on your style, budget, and lifestyle"),
        ("🎨", "500+ Design Styles", "From minimalist to maximalist, we cover every aesthetic"),
        ("👨‍🎨", "Expert Designers", "Book certified interior designers for hands-on help"),
        ("💰", "Budget-Friendly", "Solutions for every budget — from ₹50K to luxury builds"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;min-height:180px;">
                <div style="font-size:2.4rem;margin-bottom:12px;">{icon}</div>
                <h4 style="font-family:'Playfair Display',serif;color:#2C1810;margin:0 0 8px;">{title}</h4>
                <p style="font-size:0.85rem;color:#6B5A4A;margin:0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How it works
    section_header("⚡", "How It Works")
    steps = [
        ("1", "Create Account", "Register in 30 seconds — free forever", "📝"),
        ("2", "Describe Your Space", "Tell us about your room, style & budget", "🏡"),
        ("3", "Get AI Design", "Our AI generates personalised recommendations", "🤖"),
        ("4", "Book a Designer", "Optionally hire a pro to bring it to life", "👨‍🎨"),
    ]
    cols = st.columns(4)
    for col, (num, title, desc, icon) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:20px 10px;">
                <div style="width:60px;height:60px;background:linear-gradient(135deg,#8B5E3C,#C4956A);
                            border-radius:50%;display:flex;align-items:center;justify-content:center;
                            margin:0 auto 14px;font-size:1.6rem;box-shadow:0 8px 20px rgba(139,94,60,0.3);">
                    {icon}
                </div>
                <div style="font-size:0.7rem;color:#8B5E3C;font-weight:600;letter-spacing:2px;text-transform:uppercase;">STEP {num}</div>
                <h4 style="font-family:'Playfair Display',serif;color:#2C1810;margin:6px 0;">{title}</h4>
                <p style="font-size:0.83rem;color:#6B5A4A;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Style Showcase
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("🎨", "Explore Design Styles")
    styles = [
        ("Modern", "#2C2C2C", "Clean lines, neutral tones"),
        ("Classic", "#8B6914", "Timeless elegance"),
        ("Minimalist", "#BDBDBD", "Less is more"),
        ("Rustic", "#8B4513", "Natural warmth"),
        ("Bohemian", "#E84393", "Global eclectic"),
        ("Industrial", "#607D8B", "Raw urban chic"),
        ("Scandinavian", "#78909C", "Nordic simplicity"),
        ("Luxury", "#C9A84C", "Premium opulence"),
    ]
    cols = st.columns(4)
    for i, (style_name, color, tagline) in enumerate(styles):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{color}22,{color}44);
                        border:1px solid {color}66;border-radius:12px;padding:14px;
                        text-align:center;margin-bottom:10px;cursor:pointer;
                        transition:all 0.2s ease;">
                <div style="width:36px;height:36px;background:{color};border-radius:50%;
                            margin:0 auto 8px;"></div>
                <div style="font-weight:600;color:#2C1810;font-size:0.9rem;">{style_name}</div>
                <div style="font-size:0.75rem;color:#6B5A4A;">{tagline}</div>
            </div>
            """, unsafe_allow_html=True)

    # CTA
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#2C1810,#8B5E3C);border-radius:20px;
                padding:50px 40px;text-align:center;box-shadow:0 20px 60px rgba(44,24,16,0.25);">
        <h2 style="font-family:'Playfair Display',serif;color:white;font-size:2rem;margin:0 0 12px;">
            Ready to Redesign Your Home?
        </h2>
        <p style="color:#E8D5C0;margin:0 0 24px;font-size:1rem;">
            Join thousands of homeowners who've transformed their spaces with AI.
        </p>
        <p style="color:#C4956A;font-size:0.9rem;">👈 Register or Login from the sidebar to get started!</p>
    </div>
    """, unsafe_allow_html=True)


def page_login():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    section_header("🔐", "Welcome Back")

    with st.form("login_form"):
        email = st.text_input("📧 Email Address", placeholder="your@email.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        col1, col2 = st.columns([3, 2])
        with col1:
            submitted = st.form_submit_button("Login →", use_container_width=True, type="primary")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)

    if submitted:
        if not email or not password:
            toast_warning("Please fill in all fields.")
        else:
            with st.spinner("Authenticating..."):
                time.sleep(0.5)
                user = login_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.page = "admin" if user['role'] == 'admin' else "dashboard"
                st.rerun()
            else:
                toast_warning("Invalid email or password. Please try again.")

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;font-size:0.85rem;color:#6B5A4A;">
        Don't have an account? → Use sidebar <strong>Register</strong>
        <br><br>
        <strong>Demo Credentials:</strong><br>
        Admin: admin@interiordesign.com / admin123
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def page_register():
    st.markdown('<div style="max-width:500px;margin:0 auto;">', unsafe_allow_html=True)
    section_header("📝", "Create Your Account")

    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name", placeholder="John Doe")
        with col2:
            phone = st.text_input("📱 Phone", placeholder="+91 9876543210")
        email = st.text_input("📧 Email Address", placeholder="your@email.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Min 6 characters")
        confirm = st.text_input("🔑 Confirm Password", type="password", placeholder="Repeat password")
        agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        submitted = st.form_submit_button("🚀 Create Account", use_container_width=True, type="primary")

    if submitted:
        if not all([name, email, password, confirm]):
            toast_warning("Please fill in all required fields.")
        elif len(password) < 6:
            toast_warning("Password must be at least 6 characters.")
        elif password != confirm:
            toast_warning("Passwords do not match.")
        elif not agree:
            toast_warning("Please agree to the Terms of Service.")
        else:
            with st.spinner("Creating your account..."):
                time.sleep(0.8)
                success, msg = register_user(name, email, password, phone)
            if success:
                toast_success(f"Account created! Welcome, {name}. Please login.")
                time.sleep(1)
                st.session_state.page = "login"
                st.rerun()
            else:
                toast_warning(msg)

    st.markdown('</div>', unsafe_allow_html=True)


def page_dashboard():
    user = st.session_state.user
    hour = datetime.now().hour
    greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 17 else "Good Evening"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#FAF7F4,#F0EAE2);border-radius:16px;
                padding:30px;margin-bottom:24px;border:1px solid #EDE5DC;">
        <h2 style="font-family:'Playfair Display',serif;color:#2C1810;margin:0 0 6px;">
            {greeting}, {user['name'].split()[0]}! 🏠
        </h2>
        <p style="color:#6B5A4A;margin:0;">Ready to design something beautiful today?</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    designs = get_user_designs(user['id'])
    bookings = get_user_bookings(user['id'])
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        (len(designs), "Designs Created", "🎨"),
        (len(bookings), "Bookings Made", "📅"),
        (len([b for b in bookings if b['payment_status'] == 'completed']), "Payments Done", "💳"),
        (len(get_all_designers()), "Expert Designers", "👨‍🎨"),
    ]
    for col, (val, label, icon) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:2rem;margin-bottom:4px;">{icon}</div>
                <div class="stat-number">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])
    with col_left:
        section_header("⚡", "Quick Actions")
        actions = [
            ("✨ Start AI Design Wizard", "design", "Create a new AI-powered design recommendation"),
            ("👨‍🎨 Browse Expert Designers", "designers", "Find and book professional interior designers"),
            ("📋 View My Designs", "my_designs", "Review all your saved design recommendations"),
            ("📅 My Bookings", "bookings", "Track your designer appointments"),
        ]
        for label, page_key, desc in actions:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{label}**  \n<small style='color:#6B5A4A;'>{desc}</small>", unsafe_allow_html=True)
            with col_b:
                if st.button("Go →", key=f"qa_{page_key}", use_container_width=True):
                    st.session_state.page = page_key
                    st.rerun()
            st.markdown("<hr style='border-color:#F0EAE2;margin:10px 0;'>", unsafe_allow_html=True)

    with col_right:
        section_header("💡", "Design Tips")
        tips = [
            "Natural light is the best accessory for any room.",
            "A room without plants is like a life without music.",
            "Mix textures to add depth — linen, wood, metal, velvet.",
            "The 60-30-10 colour rule: dominant, secondary, accent.",
            "Good lighting can transform an average room into magic.",
            "Plants always make a room feel more alive and welcoming.",
        ]
        for tip in random.sample(tips, 4):
            st.markdown(f'<div class="tip-tag">💡 {tip}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if designs:
            last = designs[0]
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#FAF7F4,#E8DCC8);border-radius:12px;
                        padding:16px;border:1px solid #D4C4B0;">
                <div style="font-size:0.75rem;color:#8B5E3C;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
                    Last Design
                </div>
                <div style="font-weight:600;color:#2C1810;margin:4px 0;">{last['room_type']} — {last['furniture_style']}</div>
                <div style="font-size:0.8rem;color:#6B5A4A;">{last['created_at'][:10]}</div>
            </div>
            """, unsafe_allow_html=True)


def page_design_wizard():
    section_header("✨", "AI Design Wizard")
    st.markdown("""
    <p style="color:#6B5A4A;margin:-10px 0 24px;">
        Answer a few questions and our AI will generate a personalised interior design plan for your space.
    </p>
    """, unsafe_allow_html=True)

    # Step indicator
    step = st.session_state.get("wizard_step", 1)
    st.markdown(f"""
    <div class="step-indicator">
        <div class="step">
            <div class="step-circle {'step-done' if step>1 else 'step-active' if step==1 else 'step-pending'}">
                {'✓' if step>1 else '1'}
            </div>
            <div class="step-label">Room Info</div>
        </div>
        <div style="flex:1;height:2px;background:{'#27AE60' if step>1 else '#EDE5DC'};margin-top:20px;"></div>
        <div class="step">
            <div class="step-circle {'step-done' if step>2 else 'step-active' if step==2 else 'step-pending'}">
                {'✓' if step>2 else '2'}
            </div>
            <div class="step-label">Style Preferences</div>
        </div>
        <div style="flex:1;height:2px;background:{'#27AE60' if step>2 else '#EDE5DC'};margin-top:20px;"></div>
        <div class="step">
            <div class="step-circle {'step-done' if step>3 else 'step-active' if step==3 else 'step-pending'}">
                {'✓' if step>3 else '3'}
            </div>
            <div class="step-label">AI Results</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if step == 1:
        with st.form("wizard_step1"):
            st.subheader("🏡 Step 1: Tell Us About Your Room")
            col1, col2 = st.columns(2)
            with col1:
                room_type = st.selectbox("Room Type *", ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office", "Dining Room"])
                room_size = st.selectbox("Room Size *", ["Small (< 100 sq ft)", "Medium (100–250 sq ft)", "Large (250–500 sq ft)", "Very Large (500+ sq ft)"])
            with col2:
                budget = st.selectbox("Budget Range *", list(BUDGET_ADVICE.keys()))
                lifestyle = st.selectbox("Your Lifestyle *", ["Young Professional", "Couple", "Family with Kids", "Senior Living", "Work From Home", "Entertainer"])

            next1 = st.form_submit_button("Next: Style Preferences →", use_container_width=True, type="primary")

        if next1:
            st.session_state.w_room_type = room_type
            st.session_state.w_room_size = room_size
            st.session_state.w_budget = budget
            st.session_state.w_lifestyle = lifestyle
            st.session_state.wizard_step = 2
            st.rerun()

    elif step == 2:
        with st.form("wizard_step2"):
            st.subheader("🎨 Step 2: Your Style Preferences")
            col1, col2 = st.columns(2)
            with col1:
                color_theme = st.selectbox("Colour Theme *", [
                    "Warm & Cosy", "Cool & Calm", "Nature Inspired",
                    "Bold & Vibrant", "Neutral & Elegant", "Soft Pastels",
                    "Dark & Luxurious", "Mediterranean",
                ])
                furniture_style = st.selectbox("Furniture Style *", [
                    "Modern", "Classic", "Minimalist", "Rustic", "Bohemian", "Industrial", "Scandinavian",
                ])
            with col2:
                special_notes = st.text_area("Special Requirements / Notes",
                    placeholder="E.g. I have two cats, need pet-friendly fabrics. I work night shifts so need blackout options...",
                    height=120)

            # Live preview of selected styles
            st.markdown("**🎨 Your Selected Palette Preview:**")
            palette_map = {
                "Warm & Cosy": "Warm Neutrals", "Cool & Calm": "Cool Blues",
                "Nature Inspired": "Earthy Greens", "Bold & Vibrant": "Vibrant Bold",
                "Neutral & Elegant": "Monochrome Elegance", "Soft Pastels": "Pastel Dream",
                "Dark & Luxurious": "Dark Luxury", "Mediterranean": "Terracotta Warmth",
            }

            col_prev, col_next = st.columns([1, 3])
            with col_prev:
                back2 = st.form_submit_button("← Back", use_container_width=True)
            with col_next:
                generate = st.form_submit_button("🤖 Generate AI Design →", use_container_width=True, type="primary")

        if back2:
            st.session_state.wizard_step = 1
            st.rerun()

        if generate:
            st.session_state.w_color_theme = color_theme
            st.session_state.w_furniture_style = furniture_style
            st.session_state.w_special_notes = special_notes
            st.session_state.wizard_step = 3
            st.rerun()

    elif step == 3:
        # Gather all inputs
        data = {
            "room_type": st.session_state.get("w_room_type", "Living Room"),
            "room_size": st.session_state.get("w_room_size", "Medium (100–250 sq ft)"),
            "budget": st.session_state.get("w_budget", "₹50,000–₹1,50,000 / $600–$1,800"),
            "color_theme": st.session_state.get("w_color_theme", "Warm & Cosy"),
            "furniture_style": st.session_state.get("w_furniture_style", "Modern"),
            "lifestyle": st.session_state.get("w_lifestyle", "Young Professional"),
            "special_notes": st.session_state.get("w_special_notes", ""),
        }

        with st.spinner("🤖 AI is analysing your preferences and generating personalised recommendations..."):
            time.sleep(1.5)
            recs = generate_recommendations(**data)

        # Save to DB
        design_id = save_design_request(st.session_state.user['id'], data)
        st.session_state.last_design_id = design_id

        # === RESULTS ===
        st.balloons()
        toast_success(f"Your personalised design plan is ready! (Design #{design_id})")

        # AI Compatibility Score
        col_score, col_info = st.columns([1, 3])
        with col_score:
            st.markdown(f"""
            <div style="text-align:center;padding:20px 0;">
                <div class="score-badge">{recs['compatibility_score']}</div>
                <div style="font-size:0.8rem;color:#6B5A4A;margin-top:8px;">AI Match Score</div>
                <div style="font-size:0.75rem;color:#27AE60;font-weight:600;">Excellent ✓</div>
            </div>
            """, unsafe_allow_html=True)
        with col_info:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#FAF7F4,#F0EAE2);border-radius:14px;padding:20px;border:1px solid #EDE5DC;">
                <h3 style="font-family:'Playfair Display',serif;color:#2C1810;margin:0 0 8px;">
                    {data['furniture_style']} {data['room_type']} Design
                </h3>
                <p style="color:#5C3317;margin:0 0 10px;font-size:0.9rem;">{recs['style_description']}</p>
                <div style="display:flex;gap:8px;flex-wrap:wrap;">
                    <span style="background:#8B5E3C;color:white;padding:3px 10px;border-radius:20px;font-size:0.75rem;">{data['room_type']}</span>
                    <span style="background:#C4956A;color:white;padding:3px 10px;border-radius:20px;font-size:0.75rem;">{data['furniture_style']}</span>
                    <span style="background:#2C5F8A;color:white;padding:3px 10px;border-radius:20px;font-size:0.75rem;">{data['color_theme']}</span>
                    <span style="background:#27AE60;color:white;padding:3px 10px;border-radius:20px;font-size:0.75rem;">⏱ {recs['estimated_time']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        tabs = st.tabs(["🎨 Colour Palette", "🛋️ Furniture & Layout", "📐 Design Concepts", "💰 Budget Plan", "🌿 Extras"])

        with tabs[0]:
            palette = recs['palette']
            col_pal, col_desc = st.columns([1, 2])
            with col_pal:
                swatches = colour_swatch(palette['primary'], 60, "Primary") + \
                           colour_swatch(palette['secondary'], 60, "Secondary") + \
                           colour_swatch(palette['accent'], 60, "Accent") + \
                           colour_swatch(palette['wall'], 60, "Wall")
                st.markdown(f"<div style='text-align:center;padding:20px;'>{swatches}</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="text-align:center;margin-top:10px;">
                    <span style="background:{palette['primary']};color:white;padding:4px 10px;border-radius:6px;font-size:0.75rem;margin:2px;">{palette['primary']}</span>
                    <span style="background:{palette['secondary']};color:white;padding:4px 10px;border-radius:6px;font-size:0.75rem;margin:2px;">{palette['secondary']}</span>
                    <span style="background:{palette['accent']};color:white;padding:4px 10px;border-radius:6px;font-size:0.75rem;margin:2px;">{palette['accent']}</span>
                </div>
                """, unsafe_allow_html=True)
            with col_desc:
                st.markdown(f"""
                <h3 style="font-family:'Playfair Display',serif;color:#2C1810;">{recs['palette_name']}</h3>
                <p style="color:#5C3317;">{palette['description']}</p>
                """, unsafe_allow_html=True)

                # Colour Usage Donut Chart
                fig = go.Figure(data=[go.Pie(
                    labels=["Primary (60%)", "Secondary (30%)", "Accent (10%)"],
                    values=[60, 30, 10],
                    hole=0.5,
                    marker_colors=[palette['primary'], palette['secondary'], palette['accent']],
                    textinfo="label+percent",
                    textfont_size=11,
                )])
                fig.update_layout(
                    title="Colour Distribution Rule (60-30-10)",
                    showlegend=False,
                    height=280,
                    margin=dict(l=10, r=10, t=40, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)

        with tabs[1]:
            col_furn, col_layout = st.columns([1, 1])
            with col_furn:
                st.markdown("### 🛋️ Recommended Furniture")
                for i, item in enumerate(recs['furniture'], 1):
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:10px 12px;
                                background:{'#F0EAE2' if i%2==0 else 'white'};border-radius:8px;margin-bottom:6px;
                                border:1px solid #EDE5DC;">
                        <span style="background:#8B5E3C;color:white;width:24px;height:24px;border-radius:50%;
                                     display:inline-flex;align-items:center;justify-content:center;
                                     font-size:0.75rem;font-weight:700;flex-shrink:0;">{i}</span>
                        <span style="color:#2C1810;font-size:0.9rem;">{item}</span>
                    </div>
                    """, unsafe_allow_html=True)

            with col_layout:
                st.markdown("### 📐 Layout & Placement Tips")
                for tip in recs['layout_tips']:
                    st.markdown(f'<div class="tip-tag">{tip}</div>', unsafe_allow_html=True)

        with tabs[2]:
            st.markdown("### 💡 Three Design Concepts for Your Space")
            for i, concept in enumerate(recs['concepts'], 1):
                with st.expander(f"Concept {i}: {concept['name']} — {concept['mood']}", expanded=(i==1)):
                    st.markdown(f"""
                    <div class="concept-card">
                        <h4 style="color:#2C1810;margin:0 0 8px;">{concept['name']}</h4>
                        <p style="color:#5C3317;margin:0 0 12px;">{concept['description']}</p>
                        <div style="display:flex;gap:8px;flex-wrap:wrap;">
                            {''.join([f"<span style='background:#F0EAE2;color:#5C3317;padding:3px 10px;border-radius:20px;font-size:0.8rem;border:1px solid #C4956A;'>✓ {h}</span>" for h in concept['highlights']])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with tabs[3]:
            budget_info = recs['budget_info']
            st.markdown(f"### 💰 {budget_info['label']} Budget Strategy")
            col_pie, col_tips = st.columns([1, 1])
            with col_pie:
                fig = px.pie(
                    values=list(budget_info['allocation'].values()),
                    names=list(budget_info['allocation'].keys()),
                    title="Recommended Budget Allocation",
                    color_discrete_sequence=["#8B5E3C", "#C4956A", "#D4AF7A", "#E8D5B0", "#F0EAE2"],
                    hole=0.35,
                )
                fig.update_layout(height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig, use_container_width=True)
            with col_tips:
                st.markdown("**💡 Budget Tips:**")
                for tip in budget_info['tips']:
                    st.markdown(f'<div class="tip-tag">💰 {tip}</div>', unsafe_allow_html=True)

        with tabs[4]:
            col_sus, col_smart = st.columns(2)
            with col_sus:
                st.markdown("### 🌿 Sustainability Tips")
                for tip in recs['sustainability_tips']:
                    st.markdown(f'<div class="tip-tag">♻️ {tip}</div>', unsafe_allow_html=True)
            with col_smart:
                st.markdown("### 🏠 Smart Home Suggestions")
                for item in recs['smart_home']:
                    st.markdown(f'<div class="tip-tag">💡 {item}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("🔄 Create Another Design", use_container_width=True):
                st.session_state.wizard_step = 1
                st.rerun()
        with col_b:
            if st.button("👨‍🎨 Book a Designer", use_container_width=True, type="primary"):
                st.session_state.page = "designers"
                st.rerun()
        with col_c:
            if st.button("📋 View My Designs", use_container_width=True):
                st.session_state.page = "my_designs"
                st.rerun()


def page_my_designs():
    section_header("📋", "My Design Recommendations")
    designs = get_user_designs(st.session_state.user['id'])

    if not designs:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;">
            <div style="font-size:4rem;margin-bottom:16px;">🎨</div>
            <h3 style="color:#2C1810;">No Designs Yet</h3>
            <p style="color:#6B5A4A;">Start your AI Design Wizard to get personalised recommendations!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✨ Start AI Design Wizard", type="primary"):
            st.session_state.page = "design"
            st.rerun()
        return

    for design in designs:
        with st.expander(f"🏡 {design['room_type']} — {design['furniture_style']} Style | {design['created_at'][:10]}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Room:** {design['room_type']}")
                st.markdown(f"**Size:** {design['room_size']}")
                st.markdown(f"**Budget:** {design['budget']}")
            with col2:
                st.markdown(f"**Style:** {design['furniture_style']}")
                st.markdown(f"**Colour:** {design['color_theme']}")
                st.markdown(f"**Lifestyle:** {design['lifestyle']}")
            with col3:
                st.markdown(f"**Date:** {design['created_at'][:10]}")
                status_color = "#27AE60" if design['status'] == 'pending' else "#E67E22"
                st.markdown(f"**Status:** <span style='color:{status_color};'>●</span> Active", unsafe_allow_html=True)

            if design['special_notes']:
                st.markdown(f"**Notes:** *{design['special_notes']}*")

            if st.button(f"📅 Book Designer for this Room", key=f"book_{design['id']}"):
                st.session_state.page = "designers"
                st.rerun()


def page_designers():
    section_header("👨‍🎨", "Expert Interior Designers")
    st.markdown("<p style='color:#6B5A4A;margin:-10px 0 24px;'>Book a certified professional to bring your AI design to life.</p>", unsafe_allow_html=True)

    designers = get_all_designers()

    filter_col, _ = st.columns([2, 3])
    with filter_col:
        availability = st.selectbox("Filter by Availability", ["All", "Available", "Busy"])

    filtered = [d for d in designers if availability == "All" or d['availability'] == availability]

    cols = st.columns(3)
    for i, designer in enumerate(filtered):
        with cols[i % 3]:
            stars = "★" * int(designer['rating']) + "☆" * (5 - int(designer['rating']))
            avail_color = "#27AE60" if designer['availability'] == "Available" else "#E74C3C"
            st.markdown(f"""
            <div class="designer-card">
                <img src="{designer['image_url']}" style="width:80px;height:80px;border-radius:50%;
                     border:3px solid #8B5E3C;object-fit:cover;margin-bottom:12px;" onerror="this.src='https://via.placeholder.com/80'">
                <h4 style="font-family:'Playfair Display',serif;color:#2C1810;margin:0 0 4px;">{designer['name']}</h4>
                <div style="font-size:0.82rem;color:#6B5A4A;margin-bottom:8px;">{designer['specialization']}</div>
                <div class="designer-rating">{stars}</div>
                <div style="font-size:0.82rem;color:#6B5A4A;margin:4px 0;">{designer['rating']}/5 · {designer['experience']}</div>
                <div style="margin:8px 0;">
                    <span style="background:{avail_color}22;color:{avail_color};border:1px solid {avail_color}66;
                                 padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;">
                        ● {designer['availability']}
                    </span>
                </div>
                <div style="font-size:1rem;font-weight:700;color:#8B5E3C;margin:6px 0;">
                    ₹{int(designer['price_per_hour']*75):,} / hour
                </div>
            </div>
            """, unsafe_allow_html=True)

            if designer['availability'] == "Available":
                if st.button(f"📅 Book {designer['name'].split()[0]}", key=f"book_d_{designer['id']}", use_container_width=True, type="primary"):
                    st.session_state.booking_designer_id = designer['id']
                    st.session_state.booking_designer_name = designer['name']
                    st.session_state.booking_designer_price = designer['price_per_hour']
                    st.session_state.page = "payment"
                    st.rerun()
            else:
                st.button("🕐 Unavailable", key=f"busy_{designer['id']}", use_container_width=True, disabled=True)


def page_payment():
    section_header("💳", "Book & Pay")
    designer_name = st.session_state.get("booking_designer_name", "Expert Designer")
    designer_id = st.session_state.get("booking_designer_id", 1)
    hourly_price = st.session_state.get("booking_designer_price", 120)
    designs = get_user_designs(st.session_state.user['id'])

    col1, col2 = st.columns([2, 1])
    with col1:
        with st.form("booking_form"):
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#F0EAE2,#E8DCC8);border-radius:12px;padding:16px;margin-bottom:20px;">
                <h4 style="margin:0;color:#2C1810;">Booking with: {designer_name} 👨‍🎨</h4>
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                booking_date = st.date_input("📅 Select Date", min_value=date.today() + timedelta(days=1))
                time_slot = st.selectbox("⏰ Time Slot", [
                    "09:00 AM – 11:00 AM", "11:00 AM – 01:00 PM",
                    "02:00 PM – 04:00 PM", "04:00 PM – 06:00 PM",
                ])
            with col_b:
                service_type = st.selectbox("🛠️ Service Type", [
                    "Full Room Consultation (2hrs)",
                    "Quick Design Review (1hr)",
                    "3D Visualisation Package (4hrs)",
                    "Shopping Assistance (3hrs)",
                    "Full Project Management (8hrs)",
                ])
                design_id = None
                if designs:
                    design_labels = [f"Design #{d['id']}: {d['room_type']}" for d in designs]
                    chosen = st.selectbox("Link to Design (optional)", ["None"] + design_labels)
                    if chosen != "None":
                        idx = design_labels.index(chosen)
                        design_id = designs[idx]['id']

            hours = {"Full Room Consultation (2hrs)": 2, "Quick Design Review (1hr)": 1,
                     "3D Visualisation Package (4hrs)": 4, "Shopping Assistance (3hrs)": 3,
                     "Full Project Management (8hrs)": 8}
            total_usd = hourly_price * hours.get(service_type, 2)
            total_inr = int(total_usd * 75)

            st.markdown(f"""
            <div style="background:#2C1810;color:white;border-radius:12px;padding:16px;margin:12px 0;">
                <div style="font-size:1rem;opacity:0.8;margin-bottom:4px;">Total Amount</div>
                <div style="font-size:2rem;font-family:'Playfair Display',serif;font-weight:700;">
                    ₹{total_inr:,} <span style="font-size:1rem;opacity:0.7;">(${total_usd})</span>
                </div>
                <div style="font-size:0.8rem;opacity:0.65;">{hours.get(service_type, 2)} hrs × ${hourly_price}/hr</div>
            </div>
            """, unsafe_allow_html=True)

# UPI & QR SECTION
            upi_id = "9080599509@naviaxis"
            upi_url = f"upi://pay?pa={upi_id}&pn=Krishnan%20R&am={total_inr}&cu=INR"
            qr_api = f"https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl={upi_url}"
            
            st.info(f"**UPI ID:** {upi_id}")
            st.image(qr_api, caption="Scan to Pay")
            txn_id_input = st.text_input("Transaction ID / UTR Number", placeholder="E.g. 1234567890")

            if st.form_submit_button("✅ I have Paid - Confirm Booking", use_container_width=True, type="primary"):
                if txn_id_input:
                    create_booking(st.session_state.user['id'], designer_id, None, str(booking_date), time_slot, service_type, total_inr/75)
                    st.balloons()
                    toast_success("Booking Confirmed!")
                else:
                    st.warning("Please enter Transaction ID.")


def page_bookings():
    section_header("📅", "My Bookings")
    bookings = get_user_bookings(st.session_state.user['id'])

    if not bookings:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;">
            <div style="font-size:4rem;margin-bottom:16px;">📅</div>
            <h3 style="color:#2C1810;">No Bookings Yet</h3>
            <p style="color:#6B5A4A;">Browse our expert designers to book your first appointment!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👨‍🎨 Browse Designers", type="primary"):
            st.session_state.page = "designers"
            st.rerun()
        return

    for booking in bookings:
        status_color = "#27AE60" if booking['payment_status'] == 'completed' else "#E67E22"
        st.markdown(f"""
        <div class="booking-item">
            <div class="booking-dot"></div>
            <div style="flex:1;">
                <div style="font-weight:600;color:#2C1810;margin-bottom:4px;">{booking['service_type']}</div>
                <div style="font-size:0.85rem;color:#6B5A4A;">
                    Designer: <strong>{booking['designer_name']}</strong> · 
                    Date: <strong>{booking['booking_date']}</strong> · 
                    Time: <strong>{booking['time_slot']}</strong>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-weight:700;color:#8B5E3C;">₹{int(booking['amount']*75):,}</div>
                <div style="font-size:0.78rem;color:{status_color};font-weight:600;">● {booking['payment_status'].title()}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Admin Pages ────────────────────────────────────────────────────────────────
def page_admin():
    section_header("📊", "Admin Dashboard")
    stats = admin_stats()

    col1, col2, col3, col4 = st.columns(4)
    data = [
        (stats['users'], "Total Users", "👥"),
        (stats['designs'], "Designs Created", "🎨"),
        (stats['bookings'], "Total Bookings", "📅"),
        (f"₹{int(stats['revenue']*75):,}", "Total Revenue", "💰"),
    ]
    for col, (val, label, icon) in zip([col1, col2, col3, col4], data):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:2rem;margin-bottom:4px;">{icon}</div>
                <div class="stat-number" style="font-size:{'1.8rem' if len(str(val))>6 else '2.5rem'};">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    col_left, col_right = st.columns(2)
    with col_left:
        # Simulated bookings over time
        months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb"]
        bookings_data = [3, 7, 12, 18, 15, max(stats['bookings'], 8)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=bookings_data,
            fill='tozeroy',
            line=dict(color='#8B5E3C', width=3),
            fillcolor='rgba(139,94,60,0.15)',
            mode='lines+markers',
            marker=dict(size=8, color='#8B5E3C'),
            name='Bookings',
        ))
        fig.update_layout(
            title="Bookings Trend (6 Months)", height=300,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#F0EAE2"), xaxis=dict(gridcolor="#F0EAE2"),
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        styles_count = {"Modern": 35, "Minimalist": 25, "Classic": 15, "Bohemian": 12, "Others": 13}
        fig = go.Figure(data=[go.Bar(
            x=list(styles_count.keys()),
            y=list(styles_count.values()),
            marker_color=["#8B5E3C", "#C4956A", "#D4AF7A", "#E8D5B0", "#F0EAE2"],
            marker_line_color='white',
            marker_line_width=2,
        )])
        fig.update_layout(
            title="Popular Design Styles",
            height=300,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#F0EAE2"),
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)


def page_admin_users():
    section_header("👥", "Manage Users")
    users = admin_all_users()
    if users:
        df = pd.DataFrame(users)
        df = df.rename(columns={"id": "ID", "name": "Name", "email": "Email",
                                 "phone": "Phone", "role": "Role", "created_at": "Joined"})
        df["Joined"] = df["Joined"].str[:10]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No users found.")


def page_admin_bookings():
    section_header("📋", "All Bookings")
    bookings = admin_all_bookings()
    if bookings:
        df = pd.DataFrame(bookings)
        cols_show = ["id", "user_name", "user_email", "designer_name", "service_type",
                     "booking_date", "time_slot", "amount", "payment_status", "booking_status"]
        cols_show = [c for c in cols_show if c in df.columns]
        df = df[cols_show]
        df["amount"] = df["amount"].apply(lambda x: f"₹{int(x*75):,}" if x else "-")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No bookings found.")


# ── Router ─────────────────────────────────────────────────────────────────────
def route():
    # Call the new header instead of the sidebar
    render_header()
    
    page = st.session_state.page

    # Auth guard
    protected = ["dashboard", "design", "my_designs", "designers", "payment", "bookings",
                 "admin", "admin_users", "admin_bookings"]
    if page in protected and not st.session_state.logged_in:
        st.session_state.page = "login"
        page = "login"

    admin_only = ["admin", "admin_users", "admin_bookings"]
    if page in admin_only and st.session_state.user and st.session_state.user.get("role") != "admin":
        st.session_state.page = "dashboard"
        page = "dashboard"

    router = {
        "home": page_home,
        "login": page_login,
        "register": page_register,
        "dashboard": page_dashboard,
        "design": page_design_wizard,
        "my_designs": page_my_designs,
        "designers": page_designers,
        "payment": page_payment,
        "bookings": page_bookings,
        "admin": page_admin,
        "admin_users": page_admin_users,
        "admin_bookings": page_admin_bookings,
    }
    router.get(page, page_home)()


if __name__ == "__main__":
    route()

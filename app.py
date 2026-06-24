import streamlit as st
import joblib
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="MediCare AI | Advanced Medical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "chat" not in st.session_state:
    st.session_state.chat = []

# ================= ULTRA CREATIVE CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Orbitron:wght@400;700;900&display=swap');

/* ============= GLOBAL STYLES ============= */
.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
    font-family: 'Poppins', sans-serif;
}

.block-container {
    padding-top: 1rem !important;
    max-width: 100% !important;
}

/* ============= ANIMATED VIRUS PARTICLES ============= */
.virus-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
}

.virus {
    position: absolute;
    font-size: 30px;
    opacity: 0.1;
    animation: float-virus 15s infinite ease-in-out;
}

.virus-1 { top: 10%; left: 5%; animation-delay: 0s; }
.virus-2 { top: 20%; right: 10%; animation-delay: 2s; }
.virus-3 { top: 40%; left: 15%; animation-delay: 4s; }
.virus-4 { top: 60%; right: 20%; animation-delay: 6s; }
.virus-5 { top: 80%; left: 25%; animation-delay: 8s; }
.virus-6 { top: 30%; right: 30%; animation-delay: 10s; }
.virus-7 { top: 70%; left: 40%; animation-delay: 12s; }
.virus-8 { top: 50%; right: 5%; animation-delay: 14s; }

@keyframes float-virus {
    0%, 100% {
        transform: translate(0, 0) rotate(0deg);
    }
    25% {
        transform: translate(50px, -50px) rotate(90deg);
    }
    50% {
        transform: translate(0, -100px) rotate(180deg);
    }
    75% {
        transform: translate(-50px, -50px) rotate(270deg);
    }
}

/* ============= DNA HELIX BACKGROUND ============= */
.dna-helix {
    position: fixed;
    top: 0;
    right: -100px;
    width: 300px;
    height: 100%;
    opacity: 0.03;
    z-index: 0;
    pointer-events: none;
}

.dna-strand {
    position: absolute;
    width: 100%;
    height: 100%;
    animation: rotate-dna 30s linear infinite;
}

@keyframes rotate-dna {
    from { transform: rotateY(0deg); }
    to { transform: rotateY(360deg); }
}

/* ============= HEADER ============= */
.header-bar {
    background: rgba(10, 14, 39, 0.95);
    backdrop-filter: blur(20px);
    border-bottom: 2px solid rgba(79, 172, 254, 0.2);
    padding: 20px 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 1000;
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.5);
}

.logo-section {
    display: flex;
    align-items: center;
    gap: 20px;
}

.logo {
    font-size: 48px;
    filter: drop-shadow(0 0 20px rgba(79, 172, 254, 0.8));
    animation: pulse-glow 3s infinite;
}

@keyframes pulse-glow {
    0%, 100% { filter: drop-shadow(0 0 20px rgba(79, 172, 254, 0.8)); }
    50% { filter: drop-shadow(0 0 35px rgba(79, 172, 254, 1)); }
}

.brand {
    font-family: 'Orbitron', sans-serif;
    font-size: 36px;
    font-weight: 900;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #4facfe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 2px;
    text-shadow: 0 0 30px rgba(79, 172, 254, 0.5);
}

.nav-buttons {
    display: flex;
    gap: 15px;
}

/* ============= LANDING PAGE STYLES ============= */
.landing-hero {
    position: relative;
    z-index: 10;
    padding: 80px 50px;
    min-height: 85vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 72px;
    font-weight: 900;
    text-align: center;
    margin-bottom: 30px;
    background: linear-gradient(135deg, #ffffff 0%, #4facfe 50%, #00f2fe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 40px rgba(79, 172, 254, 0.4);
    animation: title-glow 3s infinite;
}

@keyframes title-glow {
    0%, 100% { filter: drop-shadow(0 0 20px rgba(79, 172, 254, 0.6)); }
    50% { filter: drop-shadow(0 0 40px rgba(79, 172, 254, 1)); }
}

.hero-subtitle {
    text-align: center;
    font-size: 24px;
    color: #b0b8c9;
    margin-bottom: 60px;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
}

/* ============= DOCTOR SHOWCASE ============= */
.doctors-showcase {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 30px;
    margin: 60px 0;
    position: relative;
    z-index: 10;
}

.doctor-card {
    background: rgba(26, 31, 58, 0.6);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(79, 172, 254, 0.2);
    border-radius: 20px;
    padding: 30px 20px;
    text-align: center;
    transition: all 0.4s;
    position: relative;
    overflow: hidden;
}

.doctor-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(79, 172, 254, 0.1), transparent);
    transform: rotate(45deg);
    transition: all 0.6s;
}

.doctor-card:hover::before {
    left: 100%;
}

.doctor-card:hover {
    transform: translateY(-15px) scale(1.05);
    border-color: #4facfe;
    box-shadow: 0 20px 60px rgba(79, 172, 254, 0.4);
}

.doctor-icon {
    font-size: 80px;
    margin-bottom: 15px;
    filter: drop-shadow(0 5px 15px rgba(79, 172, 254, 0.3));
}

.doctor-title {
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 8px;
}

.doctor-specialty {
    font-size: 13px;
    color: #4facfe;
    font-weight: 500;
}

/* ============= FEATURES GRID ============= */
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin: 60px 0;
    position: relative;
    z-index: 10;
}

.feature-card {
    background: rgba(26, 31, 58, 0.7);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(79, 172, 254, 0.15);
    border-radius: 24px;
    padding: 40px;
    text-align: center;
    transition: all 0.4s;
    position: relative;
    overflow: hidden;
}

.feature-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    transform: scaleX(0);
    transition: transform 0.4s;
}

.feature-card:hover::after {
    transform: scaleX(1);
}

.feature-card:hover {
    transform: translateY(-10px);
    border-color: #4facfe;
    box-shadow: 0 20px 60px rgba(79, 172, 254, 0.3);
}

.feature-icon {
    font-size: 64px;
    margin-bottom: 20px;
}

.feature-title {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 12px;
}

.feature-desc {
    font-size: 15px;
    color: #b0b8c9;
    line-height: 1.6;
}

.feature-number {
    font-family: 'Orbitron', sans-serif;
    font-size: 48px;
    font-weight: 900;
    color: #4facfe;
    margin-bottom: 10px;
}

/* ============= MEDICAL STATS ============= */
.stats-section {
    background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(0, 242, 254, 0.05));
    border: 2px solid rgba(79, 172, 254, 0.2);
    border-radius: 30px;
    padding: 60px;
    margin: 60px 0;
    position: relative;
    z-index: 10;
}

.stats-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 36px;
    font-weight: 700;
    text-align: center;
    color: #ffffff;
    margin-bottom: 50px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 40px;
}

.stat-item {
    text-align: center;
}

.stat-icon {
    font-size: 56px;
    margin-bottom: 15px;
}

.stat-number {
    font-family: 'Orbitron', sans-serif;
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.stat-label {
    font-size: 16px;
    color: #b0b8c9;
    font-weight: 500;
}

/* ============= CTA BUTTON ============= */
.cta-section {
    text-align: center;
    margin: 80px 0;
    position: relative;
    z-index: 10;
}

.cta-button {
    display: inline-block;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: #0a0e27;
    font-family: 'Orbitron', sans-serif;
    font-size: 24px;
    font-weight: 700;
    padding: 25px 60px;
    border-radius: 50px;
    border: none;
    cursor: pointer;
    transition: all 0.4s;
    box-shadow: 0 10px 40px rgba(79, 172, 254, 0.5);
    text-decoration: none;
    position: relative;
    overflow: hidden;
}

.cta-button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.cta-button:hover::before {
    width: 400px;
    height: 400px;
}

.cta-button:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 15px 60px rgba(79, 172, 254, 0.8);
}

/* ============= DIAGNOSIS PAGE ============= */
.diagnosis-container {
    padding: 40px 50px;
    position: relative;
    z-index: 10;
}

.page-header {
    text-align: center;
    margin-bottom: 50px;
}

.page-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff, #4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 15px;
}

.page-subtitle {
    font-size: 18px;
    color: #b0b8c9;
}

/* ============= TWO COLUMN LAYOUT ============= */
.two-column {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-top: 40px;
}

/* ============= GLASS PANEL ============= */
.glass-panel {
    background: rgba(26, 31, 58, 0.6);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(79, 172, 254, 0.2);
    border-radius: 24px;
    padding: 35px;
    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
}

.panel-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
    padding-bottom: 20px;
    border-bottom: 2px solid rgba(79, 172, 254, 0.2);
}

.panel-icon {
    font-size: 36px;
    filter: drop-shadow(0 0 10px rgba(79, 172, 254, 0.5));
}

.panel-title {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
}

/* ============= CHAT AREA ============= */
.chat-area {
    max-height: 600px;
    overflow-y: auto;
    padding: 20px;
    margin-bottom: 25px;
    background: rgba(10, 14, 39, 0.4);
    border-radius: 16px;
}

.chat-area::-webkit-scrollbar {
    width: 10px;
}

.chat-area::-webkit-scrollbar-track {
    background: rgba(79, 172, 254, 0.05);
    border-radius: 10px;
}

.chat-area::-webkit-scrollbar-thumb {
    background: rgba(79, 172, 254, 0.4);
    border-radius: 10px;
}

.chat-area::-webkit-scrollbar-thumb:hover {
    background: rgba(79, 172, 254, 0.6);
}

.message {
    margin: 20px 0;
    animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.user-msg {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: #0a0e27;
    padding: 18px 24px;
    border-radius: 20px 20px 5px 20px;
    max-width: 75%;
    margin-left: auto;
    font-weight: 500;
    box-shadow: 0 5px 20px rgba(79, 172, 254, 0.4);
    font-size: 15px;
}

.bot-msg {
    background: rgba(79, 172, 254, 0.1);
    border: 2px solid rgba(79, 172, 254, 0.2);
    color: #e8eaf0;
    padding: 18px 24px;
    border-radius: 20px 20px 20px 5px;
    max-width: 75%;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
    font-size: 15px;
    line-height: 1.7;
}

.bot-msg strong {
    color: #4facfe;
    display: block;
    margin-bottom: 10px;
    font-size: 16px;
}

/* ============= MEDICAL INFO SIDEBAR ============= */
.medical-info {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.info-card {
    background: rgba(79, 172, 254, 0.08);
    border: 2px solid rgba(79, 172, 254, 0.15);
    border-radius: 16px;
    padding: 25px;
    transition: all 0.3s;
}

.info-card:hover {
    background: rgba(79, 172, 254, 0.12);
    border-color: #4facfe;
    transform: translateX(5px);
}

.info-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
}

.info-icon {
    font-size: 32px;
}

.info-title {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
}

.info-content {
    color: #b0b8c9;
    font-size: 14px;
    line-height: 1.6;
}

.virus-showcase {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-top: 15px;
}

.virus-item {
    text-align: center;
    padding: 15px;
    background: rgba(10, 14, 39, 0.5);
    border-radius: 12px;
    transition: all 0.3s;
}

.virus-item:hover {
    background: rgba(79, 172, 254, 0.1);
    transform: scale(1.1);
}

.virus-emoji {
    font-size: 36px;
    margin-bottom: 8px;
}

.virus-label {
    font-size: 11px;
    color: #4facfe;
    font-weight: 600;
}

/* ============= FORM ELEMENTS ============= */
.stTextInput > div > div > input {
    background: rgba(10, 14, 39, 0.9) !important;
    border: 2px solid rgba(79, 172, 254, 0.3) !important;
    border-radius: 16px !important;
    color: #ffffff !important;
    padding: 16px 24px !important;
    font-size: 16px !important;
    transition: all 0.3s !important;
}

.stTextInput > div > div > input:focus {
    border-color: #4facfe !important;
    box-shadow: 0 0 25px rgba(79, 172, 254, 0.4) !important;
    background: rgba(10, 14, 39, 1) !important;
}

.stSelectbox > div > div {
    background: rgba(10, 14, 39, 0.9) !important;
    border: 2px solid rgba(79, 172, 254, 0.3) !important;
    border-radius: 16px !important;
}

.stSelectbox > div > div > div {
    color: #ffffff !important;
}

/* ============= BUTTONS ============= */
.stButton > button {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
    color: #0a0e27 !important;
    border: none !important;
    padding: 16px 40px !important;
    border-radius: 16px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    transition: all 0.3s !important;
    box-shadow: 0 6px 25px rgba(79, 172, 254, 0.5) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 40px rgba(79, 172, 254, 0.7) !important;
}

/* ============= DISCLAIMER ============= */
.disclaimer-box {
    background: rgba(245, 87, 108, 0.1);
    border: 2px solid rgba(245, 87, 108, 0.3);
    border-radius: 16px;
    padding: 20px 25px;
    margin: 30px 0;
    display: flex;
    align-items: center;
    gap: 15px;
}

.disclaimer-icon {
    font-size: 32px;
}

.disclaimer-text {
    color: #f5576c;
    font-size: 14px;
    font-weight: 500;
    line-height: 1.5;
}

/* ============= FOOTER ============= */
.footer {
    background: rgba(10, 14, 39, 0.9);
    border-top: 2px solid rgba(79, 172, 254, 0.2);
    padding: 40px 50px;
    margin-top: 80px;
    text-align: center;
}

.footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
}

.footer-text {
    color: #b0b8c9;
    font-size: 14px;
}

.footer-links {
    display: flex;
    gap: 25px;
}

.footer-link {
    color: #4facfe;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s;
}

.footer-link:hover {
    color: #00f2fe;
    text-decoration: underline;
}

</style>
""", unsafe_allow_html=True)

# ================= VIRUS PARTICLES BACKGROUND =================
st.markdown("""
<div class="virus-container">
    <div class="virus virus-1">🦠</div>
    <div class="virus virus-2">🧬</div>
    <div class="virus virus-3">🦠</div>
    <div class="virus virus-4">🧫</div>
    <div class="virus virus-5">🦠</div>
    <div class="virus virus-6">🧬</div>
    <div class="virus virus-7">🦠</div>
    <div class="virus virus-8">🧫</div>
</div>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="header-bar">
    <div class="logo-section">
        <div class="logo">🏥</div>
        <div class="brand">MEDICARE AI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= PAGE ROUTING =================

# ==================== LANDING PAGE ====================
if st.session_state.page == "landing":
    
    st.markdown("""
    <div class="landing-hero">
        <h1 class="hero-title">Revolutionary AI Medical Diagnosis</h1>
        <p class="hero-subtitle">
            Experience the future of healthcare with our advanced artificial intelligence system.
            Get instant, accurate medical insights powered by cutting-edge machine learning technology.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ================= DOCTORS SHOWCASE =================
    st.markdown("""
    <div class="doctors-showcase">
        <div class="doctor-card">
            <div class="doctor-icon">👨‍⚕️</div>
            <div class="doctor-title">Dr. Neural</div>
            <div class="doctor-specialty">General Medicine</div>
        </div>
        <div class="doctor-card">
            <div class="doctor-icon">👩‍⚕️</div>
            <div class="doctor-title">Dr. Cardiac</div>
            <div class="doctor-specialty">Cardiology</div>
        </div>
        <div class="doctor-card">
            <div class="doctor-icon">🧑‍⚕️</div>
            <div class="doctor-title">Dr. Pulmo</div>
            <div class="doctor-specialty">Pulmonology</div>
        </div>
        <div class="doctor-card">
            <div class="doctor-icon">👨‍⚕️</div>
            <div class="doctor-title">Dr. Neuro</div>
            <div class="doctor-specialty">Neurology</div>
        </div>
        <div class="doctor-card">
            <div class="doctor-icon">👩‍⚕️</div>
            <div class="doctor-title">Dr. Ortho</div>
            <div class="doctor-specialty">Orthopedics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ================= FEATURES GRID =================
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Precision Diagnosis</div>
            <div class="feature-desc">
                Advanced machine learning algorithms analyze symptoms with exceptional accuracy
                to provide reliable preliminary diagnosis.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Instant Results</div>
            <div class="feature-desc">
                Get comprehensive medical insights in seconds. Our AI processes information
                faster than traditional diagnostic methods.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure & Private</div>
            <div class="feature-desc">
                Your health data is protected with enterprise-grade security. Complete
                confidentiality guaranteed for all consultations.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ================= STATISTICS SECTION =================
    st.markdown("""
    <div class="stats-section">
        <h2 class="stats-title">Our Performance Metrics</h2>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-icon">📊</div>
                <div class="stat-number">98.5%</div>
                <div class="stat-label">Accuracy Rate</div>
            </div>
            <div class="stat-item">
                <div class="stat-icon">⚡</div>
                <div class="stat-number">&lt;3s</div>
                <div class="stat-label">Response Time</div>
            </div>
            <div class="stat-item">
                <div class="stat-icon">👥</div>
                <div class="stat-number">150K+</div>
                <div class="stat-label">Users Served</div>
            </div>
            <div class="stat-item">
                <div class="stat-icon">🏆</div>
                <div class="stat-number">500+</div>
                <div class="stat-label">Diseases Detected</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ================= MORE FEATURES =================
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-number">01</div>
            <div class="feature-title">Smart Analysis</div>
            <div class="feature-desc">
                Neural networks trained on millions of medical cases for superior
                diagnostic capabilities.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-number">02</div>
            <div class="feature-title">Expert Matching</div>
            <div class="feature-desc">
                Automatically connects you with specialized doctors in your area
                based on diagnosis results.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-number">03</div>
            <div class="feature-title">24/7 Availability</div>
            <div class="feature-desc">
                Round-the-clock AI assistance whenever you need medical guidance
                and support.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ================= CTA BUTTON =================
    st.markdown('<div class="cta-section">', unsafe_allow_html=True)
    if st.button("🚀 START DIAGNOSIS NOW", key="cta_main", use_container_width=False):
        st.session_state.page = "diagnosis"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== DIAGNOSIS PAGE ====================
elif st.session_state.page == "diagnosis":
    
    # Back button
    if st.button("← Back to Home", key="back_btn"):
        st.session_state.page = "landing"
        st.rerun()
    
    st.markdown("""
    <div class="diagnosis-container">
        <div class="page-header">
            <h1 class="page-title">AI Medical Diagnosis System</h1>
            <p class="page-subtitle">Describe your symptoms and get instant medical insights</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ================= TWO COLUMN LAYOUT =================
    col_left, col_right = st.columns([1.3, 1])
    
    with col_left:
        # ================= CHAT PANEL =================
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("""
        <div class="panel-header">
            <div class="panel-icon">💬</div>
            <div class="panel-title">Diagnostic Chat</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat history
        st.markdown("<div class='chat-area'>", unsafe_allow_html=True)
        if len(st.session_state.chat) == 0:
            st.markdown("""
            <div class='bot-msg'>
                👋 <strong>Hello! I'm your AI Medical Assistant.</strong><br>
                Please describe your symptoms in detail, and I'll provide you with:
                <br>• Preliminary diagnosis
                <br>• Recommended precautions
                <br>• Specialist doctor recommendations
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat:
                if msg["role"] == "user":
                    st.markdown(f"<div class='message user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='message bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ================= INPUT FORM =================
        st.markdown("<div class='glass-panel' style='margin-top: 20px;'>", unsafe_allow_html=True)
        st.markdown("""
        <div class="panel-header">
            <div class="panel-icon">📝</div>
            <div class="panel-title">Enter Symptoms</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("diagnosis_form", clear_on_submit=True):
            symptoms = st.text_input(
                "Symptoms",
                placeholder="e.g., high fever, severe headache, body aches, fatigue...",
                label_visibility="collapsed"
            )
            
            city = st.selectbox(
                "Select your city",
                ["Pune", "Mumbai", "Nashik", "Nagpur"]
            )
            
            submit = st.form_submit_button("🔬 Analyze Symptoms")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_right:
        # ================= MEDICAL INFO PANEL =================
        st.markdown("<div class='medical-info'>", unsafe_allow_html=True)
        
        # Info Card 1
        st.markdown("""
        <div class='info-card'>
            <div class='info-header'>
                <div class='info-icon'>🩺</div>
                <div class='info-title'>Medical Experts</div>
            </div>
            <div class='info-content'>
                Our AI is trained on data from thousands of certified medical professionals
                and clinical studies to ensure accurate preliminary diagnosis.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Info Card 2 - Common Pathogens
        st.markdown("""
        <div class='info-card'>
            <div class='info-header'>
                <div class='info-icon'>🧬</div>
                <div class='info-title'>Common Pathogens</div>
            </div>
            <div class='virus-showcase'>
                <div class='virus-item'>
                    <div class='virus-emoji'>🦠</div>
                    <div class='virus-label'>Bacteria</div>
                </div>
                <div class='virus-item'>
                    <div class='virus-emoji'>🧬</div>
                    <div class='virus-label'>Viruses</div>
                </div>
                <div class='virus-item'>
                    <div class='virus-emoji'>🧫</div>
                    <div class='virus-label'>Fungi</div>
                </div>
                <div class='virus-item'>
                    <div class='virus-emoji'>🦠</div>
                    <div class='virus-label'>Parasites</div>
                </div>
                <div class='virus-item'>
                    <div class='virus-emoji'>🧬</div>
                    <div class='virus-label'>Prions</div>
                </div>
                <div class='virus-item'>
                    <div class='virus-emoji'>🧫</div>
                    <div class='virus-label'>Toxins</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Info Card 3
        st.markdown("""
        <div class='info-card'>
            <div class='info-header'>
                <div class='info-icon'>⚕️</div>
                <div class='info-title'>How It Works</div>
            </div>
            <div class='info-content'>
                <strong>1. Input Symptoms:</strong> Describe what you're experiencing<br>
                <strong>2. AI Analysis:</strong> Our system analyzes patterns<br>
                <strong>3. Get Results:</strong> Receive diagnosis & recommendations<br>
                <strong>4. Find Doctor:</strong> Connect with specialists near you
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Info Card 4
        st.markdown("""
        <div class='info-card'>
            <div class='info-header'>
                <div class='info-icon'>🏥</div>
                <div class='info-title'>Specialist Network</div>
            </div>
            <div class='info-content'>
                Access to 500+ specialized doctors across major cities in India.
                Get matched with the right specialist for your condition.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ================= LOAD MODELS AND PROCESS =================
    # ================= LOAD MODELS =================
try:
    model = joblib.load("model/disease_model.pkl")
    vectorizer = joblib.load("model/vectorizer.pkl")
    precautions_df = pd.read_csv("dataset/precautions.csv")
    doctors_df = pd.read_csv("dataset/doctors.csv")
    models_loaded = True
except:
    models_loaded = False
    st.error("⚠️ Models not found. Please train the model first.")

# ================= PROCESS INPUT =================
if submit:
    if not symptoms.strip():
        st.warning("⚠️ Please enter symptoms")
    
    elif not models_loaded:
        st.error("⚠️ Model not loaded properly")
    
    else:
        # Add user message
        st.session_state.chat.append({
            "role": "user",
            "content": symptoms
        })

        # Vectorize input
        vec = vectorizer.transform([symptoms.lower()])
        disease = model.predict(vec)[0]

        # Build response
        reply = f"🔬 Diagnosis: {disease}\n\n"

        # Get precautions
        row = precautions_df[precautions_df["disease"] == disease]
        if not row.empty:
            reply += "⚕️ Precautions:\n"
            for p in row.iloc[0]["precautions"].split("|"):
                reply += f"- {p}\n"

        # Get doctor
        doc = doctors_df[
            (doctors_df["disease"] == disease) &
            (doctors_df["location"] == city)
        ]

        if not doc.empty:
            d = doc.iloc[0]
            reply += f"\n👨‍⚕️ Doctor: Dr. {d['doctor_name']}\n"
            reply += f"Specialization: {d['specialization']}"
        else:
            reply += "\nConsult a general physician."

        # Add bot response
        st.session_state.chat.append({
            "role": "bot",
            "content": reply
        })

        st.rerun()
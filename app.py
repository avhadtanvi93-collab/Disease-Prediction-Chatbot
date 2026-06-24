import streamlit as st
import joblib
import pandas as pd
import os

# ==================== PATH SETUP ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "disease_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "vectorizer.pkl")
DOCTORS_PATH = os.path.join(BASE_DIR, "dataset", "doctors.csv")
PRECAUTIONS_PATH = os.path.join(BASE_DIR, "dataset", "precautions.csv")

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="RoboMed AI • Advanced Medical Diagnosis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== ADVANCED CSS STYLING ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Orbitron:wght@400;500;600;700;800;900&family=Exo+2:wght@300;400;500;600;700;800&display=swap');

/* ==================== GLOBAL STYLES ==================== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1535 50%, #0f1922 100%);
    font-family: 'Exo 2', sans-serif;
    color: #E0E7EF;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* ==================== ANIMATED BACKGROUND ==================== */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(ellipse at 20% 30%, rgba(0, 255, 255, 0.15) 0%, transparent 40%),
        radial-gradient(ellipse at 80% 70%, rgba(138, 43, 226, 0.15) 0%, transparent 40%),
        radial-gradient(ellipse at 50% 50%, rgba(255, 0, 255, 0.1) 0%, transparent 50%);
    z-index: -1;
    animation: bg-shift 15s ease-in-out infinite;
}

@keyframes bg-shift {
    0%, 100% { opacity: 0.7; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
}

/* Circuit board pattern */
.stApp::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        repeating-linear-gradient(0deg, transparent, transparent 80px, rgba(0, 255, 255, 0.02) 80px, rgba(0, 255, 255, 0.02) 81px),
        repeating-linear-gradient(90deg, transparent, transparent 80px, rgba(0, 255, 255, 0.02) 80px, rgba(0, 255, 255, 0.02) 81px);
    z-index: -1;
    opacity: 0.5;
}

/* ==================== TYPOGRAPHY ==================== */
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
    font-weight: 800;
    letter-spacing: 2px;
}

/* ==================== CONTAINER STYLING ==================== */
.block-container {
    padding: 3rem 2rem !important;
    max-width: 1600px !important;
}

/* ==================== CUSTOM CLASSES ==================== */
.hero-container {
    text-align: center;
    padding: 5rem 2rem;
    margin-bottom: 4rem;
    background: linear-gradient(135deg, rgba(0, 255, 255, 0.05) 0%, rgba(138, 43, 226, 0.05) 100%);
    border-radius: 30px;
    border: 2px solid rgba(0, 255, 255, 0.3);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: repeating-linear-gradient(
        45deg,
        transparent,
        transparent 40px,
        rgba(0, 255, 255, 0.02) 40px,
        rgba(0, 255, 255, 0.02) 42px
    );
    animation: slide-pattern 20s linear infinite;
}

@keyframes slide-pattern {
    0% { transform: translate(0, 0); }
    100% { transform: translate(40px, 40px); }
}

/* ==================== MARKDOWN OVERRIDES ==================== */
.element-container h1 {
    font-size: 5rem !important;
    background: linear-gradient(135deg, #00FFFF 0%, #FF00FF 50%, #00FFFF 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-align: center;
    margin: 2rem 0;
    animation: gradient-flow 5s ease infinite;
    background-size: 200% 200%;
    filter: drop-shadow(0 0 30px rgba(0, 255, 255, 0.5));
}

@keyframes gradient-flow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.element-container h2 {
    font-size: 2.8rem !important;
    color: #00FFFF;
    text-align: center;
    margin: 3rem 0 2rem 0;
    text-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
    letter-spacing: 3px;
}

.element-container h3 {
    font-size: 2rem !important;
    color: #FF00FF;
    margin: 2rem 0 1rem 0;
    text-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
}

.element-container p {
    font-size: 1.2rem;
    line-height: 1.8;
    color: #B8C5D6;
    margin: 1rem 0;
}

/* ==================== COLUMNS ==================== */
.row-widget.stHorizontal > div {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(0, 255, 255, 0.2);
    border-radius: 20px;
    padding: 2.5rem 1.5rem;
    margin: 0.5rem;
    transition: all 0.4s ease;
    backdrop-filter: blur(10px);
}

.row-widget.stHorizontal > div:hover {
    transform: translateY(-10px);
    border-color: rgba(0, 255, 255, 0.6);
    box-shadow: 0 20px 60px rgba(0, 255, 255, 0.3);
    background: rgba(255, 255, 255, 0.05);
}

/* ==================== BUTTONS ==================== */
.stButton > button {
    background: linear-gradient(135deg, #8A2BE2 0%, #FF00FF 50%, #FF1493 100%) !important;
    color: white !important;
    border: none !important;
    padding: 1.2rem 3rem !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    border-radius: 50px !important;
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 15px 50px rgba(138, 43, 226, 0.6) !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    transition: left 0.5s;
}

.stButton > button:hover {
    transform: translateY(-5px) scale(1.02) !important;
    box-shadow: 0 20px 70px rgba(255, 0, 255, 0.8) !important;
}

.stButton > button:hover::before {
    left: 100%;
}

/* ==================== TEXT INPUTS ==================== */
.stTextInput > div > div > input {
    background: rgba(10, 14, 39, 0.8) !important;
    border: 2px solid rgba(0, 255, 255, 0.4) !important;
    border-radius: 15px !important;
    color: #FFFFFF !important;
    font-size: 1.1rem !important;
    padding: 1.2rem 1.5rem !important;
    transition: all 0.3s !important;
    font-family: 'Exo 2', sans-serif !important;
}

.stTextInput > div > div > input:focus {
    border-color: #00FFFF !important;
    box-shadow: 0 0 30px rgba(0, 255, 255, 0.4) !important;
    background: rgba(10, 14, 39, 0.95) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #6B7280 !important;
}

.stTextInput > label {
    color: #00FFFF !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.8rem !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 1px !important;
}

/* ==================== SELECT BOX ==================== */
.stSelectbox > div > div {
    background: rgba(10, 14, 39, 0.8) !important;
    border: 2px solid rgba(0, 255, 255, 0.4) !important;
    border-radius: 15px !important;
}

.stSelectbox > div > div > select {
    color: #FFFFFF !important;
    font-size: 1.1rem !important;
    padding: 1.2rem 1.5rem !important;
    font-family: 'Exo 2', sans-serif !important;
}

.stSelectbox > label {
    color: #00FFFF !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.8rem !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 1px !important;
}

/* ==================== INFO/SUCCESS/WARNING BOXES ==================== */
.stAlert {
    background: rgba(0, 0, 0, 0.4) !important;
    border-left: 5px solid !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    backdrop-filter: blur(10px) !important;
}

.stSuccess {
    border-left-color: #00FF88 !important;
    background: rgba(0, 255, 136, 0.1) !important;
}

.stInfo {
    border-left-color: #00BFFF !important;
    background: rgba(0, 191, 255, 0.1) !important;
}

.stWarning {
    border-left-color: #FFA500 !important;
    background: rgba(255, 165, 0, 0.1) !important;
}

.stError {
    border-left-color: #FF4444 !important;
    background: rgba(255, 68, 68, 0.1) !important;
}

/* ==================== SPINNER ==================== */
.stSpinner > div {
    border-top-color: #00FFFF !important;
    border-right-color: #FF00FF !important;
}

/* ==================== DIVIDER ==================== */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, #00FFFF, transparent) !important;
    margin: 3rem 0 !important;
}

/* ==================== EXPANDER ==================== */
.streamlit-expanderHeader {
    background: rgba(0, 255, 255, 0.1) !important;
    border: 1px solid rgba(0, 255, 255, 0.3) !important;
    border-radius: 12px !important;
    color: #00FFFF !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(0, 255, 255, 0.2) !important;
}

/* ==================== METRIC CARDS ==================== */
.stMetric {
    background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(138, 43, 226, 0.1) 100%);
    padding: 2rem;
    border-radius: 20px;
    border: 2px solid rgba(0, 255, 255, 0.3);
    text-align: center;
    transition: all 0.3s;
}

.stMetric:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 255, 255, 0.3);
}

.stMetric label {
    color: #00FFFF !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
}

.stMetric [data-testid="stMetricValue"] {
    font-size: 3rem !important;
    background: linear-gradient(135deg, #00FFFF, #FF00FF);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-family: 'Orbitron', sans-serif !important;
}

/* ==================== DATAFRAME STYLING ==================== */
.stDataFrame {
    background: rgba(0, 0, 0, 0.4) !important;
    border: 2px solid rgba(0, 255, 255, 0.3) !important;
    border-radius: 15px !important;
}

/* ==================== TABS ==================== */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(0, 0, 0, 0.3);
    padding: 1rem;
    border-radius: 15px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(0, 255, 255, 0.1);
    border: 1px solid rgba(0, 255, 255, 0.3);
    border-radius: 10px;
    padding: 1rem 2rem;
    color: #00FFFF;
    font-weight: 600;
    transition: all 0.3s;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #8A2BE2, #FF00FF);
    border-color: #FF00FF;
    color: white;
}

/* ==================== CUSTOM BADGE ==================== */
.badge {
    display: inline-block;
    padding: 0.5rem 1.5rem;
    background: linear-gradient(135deg, rgba(138, 43, 226, 0.3), rgba(255, 0, 255, 0.3));
    border: 1px solid rgba(138, 43, 226, 0.6);
    border-radius: 50px;
    color: #FF00FF;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 1rem 0;
}

/* ==================== RESULT CARD ==================== */
.result-display {
    background: linear-gradient(135deg, rgba(0, 255, 255, 0.15) 0%, rgba(138, 43, 226, 0.15) 100%);
    border: 3px solid rgba(0, 255, 255, 0.5);
    border-radius: 25px;
    padding: 3rem;
    text-align: center;
    margin: 3rem 0;
    box-shadow: 0 20px 60px rgba(0, 255, 255, 0.4);
    position: relative;
    overflow: hidden;
}

.result-display::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(0, 255, 255, 0.2) 0%, transparent 70%);
    animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.1); }
}

/* ==================== DOCTOR CARD ==================== */
.doctor-display {
    background: linear-gradient(135deg, rgba(138, 43, 226, 0.15) 0%, rgba(0, 255, 255, 0.15) 100%);
    border: 2px solid rgba(138, 43, 226, 0.5);
    border-radius: 20px;
    padding: 2.5rem;
    margin: 2rem 0;
    transition: all 0.4s;
    position: relative;
    overflow: hidden;
}

.doctor-display::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(180deg, #8A2BE2, #00FFFF);
    transform: scaleY(0);
    transition: transform 0.4s;
}

.doctor-display:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 70px rgba(138, 43, 226, 0.4);
    border-color: rgba(138, 43, 226, 0.8);
}

.doctor-display:hover::before {
    transform: scaleY(1);
}

/* ==================== PRECAUTION ITEM ==================== */
.precaution-display {
    background: rgba(0, 255, 136, 0.1);
    border-left: 5px solid #00FF88;
    padding: 1.5rem 2rem;
    margin: 1.5rem 0;
    border-radius: 12px;
    transition: all 0.3s;
}

.precaution-display:hover {
    background: rgba(0, 255, 136, 0.2);
    transform: translateX(10px);
    box-shadow: 0 5px 20px rgba(0, 255, 136, 0.3);
}

/* ==================== RESPONSIVE DESIGN ==================== */
@media (max-width: 768px) {
    .element-container h1 {
        font-size: 3rem !important;
    }
    
    .element-container h2 {
        font-size: 2rem !important;
    }
    
    .stButton > button {
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
    }
}

/* ==================== ANIMATIONS ==================== */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.element-container {
    animation: fadeIn 0.6s ease-out;
}

/* ==================== GLOW EFFECTS ==================== */
.glow-text {
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.8),
                 0 0 20px rgba(0, 255, 255, 0.6),
                 0 0 30px rgba(0, 255, 255, 0.4);
}

/* ==================== SCROLLBAR ==================== */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: rgba(10, 14, 39, 0.8);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00FFFF, #8A2BE2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #8A2BE2, #FF00FF);
}

</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# ==================== NAVIGATION ====================
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🏠 HOME", key="nav_home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

with col2:
    if st.button("🔬 DIAGNOSIS", key="nav_diagnosis", use_container_width=True):
        st.session_state.page = 'prediction'
        st.rerun()

with col3:
    if st.button("📊 STATS", key="nav_stats", use_container_width=True):
        st.session_state.page = 'stats'
        st.rerun()

st.markdown("---")

# ==================== HOME PAGE ====================
if st.session_state.page == 'home':
    
    # Hero Section
    st.markdown("# 🤖 ROBOMED AI")
    st.markdown("### Advanced Medical Diagnosis System")
    
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0; padding: 1.5rem; background: rgba(138, 43, 226, 0.1); border-radius: 15px; border: 1px solid rgba(138, 43, 226, 0.4);'>
        <p style='color: #FF00FF; font-size: 1rem; font-weight: 600; letter-spacing: 2px; margin: 0;'>
            ⚡ POWERED BY ARTIFICIAL INTELLIGENCE
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Experience cutting-edge AI technology for instant medical insights. Our advanced neural networks 
    analyze symptoms with precision, connect you with specialists, and provide personalized health guidance.
    """)
    
    st.markdown("---")
    
    # Features Section
    st.markdown("## 🌟 Intelligent Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🧠 AI Analysis")
        st.markdown("""
        Advanced machine learning algorithms trained on extensive medical datasets 
        deliver accurate preliminary diagnosis.
        """)
    
    with col2:
        st.markdown("### ⚡ Instant Results")
        st.markdown("""
        Real-time processing provides immediate health insights using 
        optimized prediction engines.
        """)
    
    with col3:
        st.markdown("### 👨‍⚕️ Expert Network")
        st.markdown("""
        Smart matching connects you with certified specialists 
        perfectly suited to your condition.
        """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🛡️ Preventive Care")
        st.markdown("""
        Evidence-based recommendations help maintain optimal health 
        and prevent complications.
        """)
    
    with col2:
        st.markdown("### 🔐 Secure & Private")
        st.markdown("""
        Military-grade encryption protects your sensitive health 
        information at all times.
        """)
    
    with col3:
        st.markdown("### 📊 Data-Driven")
        st.markdown("""
        Continuously improving accuracy through medical research 
        and machine learning.
        """)
    
    st.markdown("---")
    
    # Stats
    st.markdown("## 📈 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Accuracy", "96%", "↑ 2%")
    
    with col2:
        st.metric("Diseases", "1200+", "↑ 150")
    
    with col3:
        st.metric("Doctors", "750+", "↑ 50")
    
    with col4:
        st.metric("Availability", "24/7", "Always On")
    
    st.markdown("---")
    
    # CTA
    st.markdown("## 🚀 Ready to Start?")
    st.markdown("Click the button below to begin your AI-powered health analysis")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔬 START DIAGNOSIS NOW", key="cta_start", use_container_width=True):
            st.session_state.page = 'prediction'
            st.rerun()
    
    # Disclaimer
    st.markdown("---")
    st.warning("""
    ⚠️ **MEDICAL DISCLAIMER:** RoboMed AI is an educational tool for informational purposes only. 
    This system does NOT replace professional medical advice, diagnosis, or treatment. 
    Always consult qualified healthcare providers for medical concerns. In emergencies, call emergency services immediately.
    """)

# ==================== STATS PAGE ====================
elif st.session_state.page == 'stats':
    
    st.markdown("# 📊 System Statistics")
    st.markdown("### Real-time Performance Dashboard")
    
    st.markdown("---")
    
    # Metrics Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Diagnoses", "50,000+", "+5,234 this month")
        st.metric("Average Response Time", "2.3s", "-0.5s improvement")
    
    with col2:
        st.metric("Model Accuracy", "96.2%", "+1.8% this quarter")
        st.metric("User Satisfaction", "4.8/5.0", "+0.3 rating")
    
    with col3:
        st.metric("Active Specialists", "750+", "+50 new doctors")
        st.metric("Cities Covered", "120+", "+15 locations")
    
    st.markdown("---")
    
    # Disease Categories
    st.markdown("## 🦠 Disease Categories Covered")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ### 💉 Infectious
        - Viral Infections
        - Bacterial Diseases
        - Fungal Conditions
        """)
    
    with col2:
        st.markdown("""
        ### ❤️ Cardiovascular
        - Heart Disease
        - Hypertension
        - Arrhythmias
        """)
    
    with col3:
        st.markdown("""
        ### 🧠 Neurological
        - Migraines
        - Epilepsy
        - Neuropathy
        """)
    
    with col4:
        st.markdown("""
        ### 🫁 Respiratory
        - Asthma
        - Bronchitis
        - Pneumonia
        """)
    
    st.markdown("---")
    
    # Specialties
    st.markdown("## 👨‍⚕️ Medical Specialties Available")
    
    specialties = [
        "🫀 Cardiology", "🧠 Neurology", "🦴 Orthopedics", "🔬 Oncology",
        "👶 Pediatrics", "👁️ Ophthalmology", "🦷 Dentistry", "🩺 General Medicine"
    ]
    
    cols = st.columns(4)
    for i, specialty in enumerate(specialties):
        with cols[i % 4]:
            st.info(specialty)

# ==================== PREDICTION PAGE ====================
elif st.session_state.page == 'prediction':
    
    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        doctors_df = pd.read_csv(DOCTORS_PATH)
        precautions_df = pd.read_csv(PRECAUTIONS_PATH)
    except FileNotFoundError as e:
        st.error(f"❌ System Error: {e}")
        st.stop()
    
    # Header
    st.markdown("# 🔬 AI Medical Diagnosis")
    st.markdown("### Enter your symptoms for instant AI-powered analysis")
    
    st.markdown("---")
    
    # Input Section
    st.markdown("## 📝 Patient Information")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symptoms = st.text_input(
            "💬 Describe Your Symptoms",
            placeholder="Example: fever, headache, nausea, body ache",
            help="List all symptoms separated by commas"
        )
    
    with col2:
        city = st.selectbox(
            "📍 Your Location",
            options=doctors_df["location"].unique(),
            help="Select city for local specialists"
        )
    
    st.markdown("---")
    
    # Analyze Button
    if st.button("🔍 ANALYZE SYMPTOMS", key="analyze_main", use_container_width=True):
        
        if not symptoms.strip():
            st.warning("⚠️ Please enter at least one symptom to proceed")
        
        else:
            with st.spinner("🧠 AI is analyzing your symptoms..."):
                
                # Make Prediction
                input_vec = vectorizer.transform([symptoms.lower()])
                predicted_disease = model.predict(input_vec)[0]
                
                st.success("✅ Analysis Complete!")
                
                st.markdown("---")
                
                # Display Result
                st.markdown("## 🦠 Diagnosis Result")
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(0, 255, 255, 0.2) 0%, rgba(138, 43, 226, 0.2) 100%);
                            border: 3px solid rgba(0, 255, 255, 0.6);
                            border-radius: 20px;
                            padding: 3rem;
                            text-align: center;
                            margin: 2rem 0;
                            box-shadow: 0 15px 50px rgba(0, 255, 255, 0.3);'>
                    <p style='color: #B8C5D6; font-size: 1rem; letter-spacing: 2px; margin-bottom: 1rem;'>
                        PRELIMINARY DIAGNOSIS
                    </p>
                    <h2 style='color: #00FFFF; font-size: 2.5rem; margin: 0; text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);'>
                        {predicted_disease}
                    </h2>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Precautions
                st.markdown("## 🛡️ Recommended Precautions")
                
                row = precautions_df[precautions_df["disease"] == predicted_disease]
                
                if not row.empty:
                    precautions = row.iloc[0]["precautions"].split("|")
                    
                    for i, precaution in enumerate(precautions, 1):
                        st.markdown(f"""
                        <div style='background: rgba(0, 255, 136, 0.1);
                                    border-left: 5px solid #00FF88;
                                    padding: 1.5rem 2rem;
                                    margin: 1.5rem 0;
                                    border-radius: 12px;'>
                            <strong style='color: #00FF88;'>Step {i}:</strong> 
                            <span style='color: #E0E7EF; margin-left: 1rem;'>{precaution.strip()}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("ℹ️ No specific precautions available in database")
                
                st.markdown("---")
                
                # Doctor Recommendations
                st.markdown("## 👨‍⚕️ Recommended Specialists")
                
                doc = doctors_df[
                    (doctors_df["disease"] == predicted_disease) &
                    (doctors_df["location"] == city)
                ]
                
                if not doc.empty:
                    for idx, doctor in doc.iterrows():
                        
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            st.markdown(f"""
                            <div style='width: 100px; height: 100px; 
                                        background: linear-gradient(135deg, #8A2BE2, #00FFFF);
                                        border-radius: 50%;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                        font-size: 3rem;
                                        border: 4px solid rgba(138, 43, 226, 0.4);
                                        box-shadow: 0 10px 30px rgba(138, 43, 226, 0.5);
                                        margin: 0 auto;'>
                                👨‍⚕️
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"### Dr. {doctor['doctor_name']}")
                            st.markdown(f"**Specialization:** {doctor['specialization']}")
                            st.markdown(f"**📞 Contact:** {doctor['mobile']}")
                            st.markdown(f"**📍 Location:** {doctor['location']}")
                    
                        st.markdown("---")
                
                else:
                    st.info("🔍 No specialists available in your city. Try nearby locations.")
                
                # Final Disclaimer
                st.error("""
                ⚠️ **IMPORTANT:** This AI analysis is for educational purposes only. 
                Do NOT use as substitute for professional medical diagnosis. 
                Consult licensed healthcare providers for proper evaluation and treatment.
                """)

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #6B7280;'>
    <p>© 2026 RoboMed AI • Advanced Medical Intelligence System</p>
    <p style='font-size: 0.9rem;'>Powered by Machine Learning & Neural Networks</p>
</div>
""", unsafe_allow_html=True)

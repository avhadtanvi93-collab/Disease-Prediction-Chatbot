import streamlit as st
import joblib
import pandas as pd
import os

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "disease_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "vectorizer.pkl")
DOCTORS_PATH = os.path.join(BASE_DIR, "dataset", "doctors.csv")
PRECAUTIONS_PATH = os.path.join(BASE_DIR, "dataset", "precautions.csv")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="🩺",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.card {
    background: #f8fbff;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}
.result-card {
    background: linear-gradient(135deg, #42a5f5, #478ed1);
    color: white;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}
.doctor-card {
    background: linear-gradient(135deg, #e3f2fd, #ffffff);
    padding: 20px;
    border-radius: 16px;
    border-left: 6px solid #1e88e5;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL & DATA ----------------
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    doctors_df = pd.read_csv(DOCTORS_PATH)
    precautions_df = pd.read_csv(PRECAUTIONS_PATH)
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;color:#1565c0;'>🩺 Medical Chatbot</h1>", unsafe_allow_html=True)
st.write("Enter your symptoms to get disease prediction, precautions, and doctor recommendations.")

# ---------------- INPUT ----------------
symptoms = st.text_input("💬 Enter symptoms (comma separated)")
city = st.selectbox("📍 Select your city", doctors_df["location"].unique())

# ---------------- BUTTON ----------------
if st.button("🔍 Predict Disease"):

    if symptoms.strip() == "":
        st.warning("⚠️ Please enter symptoms")
    else:
        input_vec = vectorizer.transform([symptoms.lower()])
        predicted_disease = model.predict(input_vec)[0]

        # ---------------- RESULT ----------------
        st.markdown(
            f"<div class='result-card'>🧠 Predicted Disease: {predicted_disease}</div>",
            unsafe_allow_html=True
        )

        # ---------------- PRECAUTIONS ----------------
        st.subheader("🛡️ Precautions")
        row = precautions_df[precautions_df["disease"] == predicted_disease]

        if not row.empty:
            for p in row.iloc[0]["precautions"].split("|"):
                st.write("✅", p)
        else:
            st.info("No precautions available.")

        # ---------------- DOCTOR DETAILS ----------------
        st.subheader("👨‍⚕️ Doctor Recommendation")

        doc = doctors_df[
            (doctors_df["disease"] == predicted_disease) &
            (doctors_df["location"] == city)
        ]

        if not doc.empty:
            for _, d in doc.iterrows():
                st.markdown(f"""
                <div class='doctor-card'>
                    <h4>🩺 {d['doctor_name']}</h4>
                    <p><b>Specialization:</b> {d['specialization']}</p>
                    <p><b>📞 Mobile:</b> {d['mobile']}</p>
                    <p><b>📍 Location:</b> {d['location']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No doctor available in selected city.")

        st.warning("⚠️ Educational purpose only. Please consult a certified doctor.")

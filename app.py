import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Air Quality Predictor", page_icon="🌫️", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: #0f1117;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Glass Card */
.card {
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.02);
    box-shadow: 0 0 30px rgba(255,255,255,0.2);
}

/* AQI Number */
.aqi {
    font-size: 50px;
    font-weight: bold;
}

/* SAFE (Green Glow) */
.safe {
    color: #00ff9f;
    animation: glowGreen 1.5s infinite alternate;
}
@keyframes glowGreen {
    from { text-shadow: 0 0 10px #00ff9f; }
    to { text-shadow: 0 0 25px #00ff9f; }
}

/* RISK (Red Flash) */
.danger {
    color: #ff4d4d;
    animation: flashRed 1s infinite;
}
@keyframes flashRed {
    0% { opacity: 1; text-shadow: 0 0 10px red; }
    50% { opacity: 0.4; text-shadow: 0 0 25px red; }
    100% { opacity: 1; text-shadow: 0 0 10px red; }
}

/* Moderate (Yellow Pulse) */
.moderate {
    color: #ffd166;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #ff4d4d, #ff9966);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: bold;
    padding: 10px 20px;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #151922;
}

</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
data = pd.DataFrame({
    'temperature':[22,24,26,25,23,21,20,19,18,22,24,27,28,29,30],
    'humidity':[60,65,70,68,72,75,78,80,82,65,60,55,50,48,45],
    'wind_speed':[10,12,8,7,6,5,4,3,2,9,11,14,15,16,18],
    'pm25':[40,50,60,65,70,75,80,85,90,55,50,45,40,35,30],
    'pm10':[80,90,100,110,120,130,140,150,160,95,90,85,80,75,70],
    'co2':[400,420,450,470,500,520,550,580,600,430,410,390,370,360,350],
    'AQI':[110,120,140,150,160,170,180,190,200,130,125,115,105,95,90]
})

X = data[['temperature','humidity','wind_speed','pm25','pm10','co2']]
y = data['AQI']

model = LinearRegression().fit(X, y)

# ---------------- RISK FUNCTION ----------------
def get_risk(aqi):
    if aqi <= 50:
        return "Low", "safe"
    elif aqi <= 100:
        return "Moderate", "moderate"
    elif aqi <= 200:
        return "High", "danger"
    else:
        return "Severe", "danger"

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🌫️ Smart Air Quality Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Real-time aesthetic AQI insights</p>", unsafe_allow_html=True)

# ---------------- INPUTS ----------------
st.sidebar.header("🌦 Inputs")

temp = st.sidebar.slider("Temperature", 0, 50, 25)
humidity = st.sidebar.slider("Humidity", 0, 100, 70)
wind = st.sidebar.slider("Wind Speed", 0, 30, 6)

st.sidebar.header("🏭 Pollution")

pm25 = st.sidebar.slider("PM2.5", 0, 200, 50)
pm10 = st.sidebar.slider("PM10", 0, 300, 100)
co2 = st.sidebar.slider("CO₂", 300, 1000, 420)

# ---------------- PREDICT ----------------
if st.button("⚡ Predict AQI"):

    aqi = model.predict([[temp, humidity, wind, pm25, pm10, co2]])[0]
    risk, css_class = get_risk(aqi)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("AQI Value")
        st.markdown(f'<div class="aqi {css_class}">{aqi:.1f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Health Risk")
        st.markdown(f'<div class="aqi {css_class}">{risk}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Advice
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Advice")

    if css_class == "danger":
        st.error("🚨 Avoid going outside. Wear N95 mask. Stay indoors.")
    elif css_class == "moderate":
        st.warning("⚠️ Limit outdoor exposure if sensitive.")
    else:
        st.success("✅ Air is clean. Enjoy your day!")

    st.markdown('</div>', unsafe_allow_html=True)
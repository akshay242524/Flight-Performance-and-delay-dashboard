import streamlit as st
from models.predictor import predict_delay

st.set_page_config(page_title="ML Prediction", layout="centered")
st.title("🎯 Flight Delay Prediction (ML Model)")

st.markdown("Enter flight parameters below to get a delay prediction.")

distance = st.slider("Flight Distance (miles)", 100, 3000, 500)
departure_hour = st.slider("Departure Hour", 0, 23, 10)
weather_delay = st.slider("Weather Delay Impact (%)", 0, 100, 10)
carrier_delay = st.slider("Carrier Delay Impact (%)", 0, 100, 10)

if st.button("🔮 Predict Delay"):
    prediction = predict_delay(distance, departure_hour, weather_delay, carrier_delay)
    st.success(f"Predicted Departure Delay: {prediction:.2f} minutes")

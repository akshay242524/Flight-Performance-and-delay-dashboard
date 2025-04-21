import streamlit as st
from utils.weather_api import get_current_weather
from utils.timezone_api import get_local_time

st.set_page_config(page_title="Live Weather & Time", layout="centered")
st.title("🌦️ Live Weather and 🕒 Local Time")

st.markdown("Check real-time weather and current time at major U.S. airports.")

airport_codes = ["JFK", "LAX", "ORD", "DFW", "ATL", "DEN"]
airport = st.selectbox("Select Airport", airport_codes)

if st.button("Get Live Info"):
    weather = get_current_weather(airport)
    current_time = get_local_time(airport)

    st.markdown("### 🕒 Local Time")
    st.info(current_time)

    st.markdown("### 🌦️ Current Weather")
    if "Error" in weather:
        st.error(weather["Error"])
    else:
        for key, value in weather.items():
            st.write(f"**{key}:** {value}")

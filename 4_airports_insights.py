import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Weather Delays", layout="wide")
st.title("⛅ Weather Delay Analysis")

df = pd.read_csv("data/data1.csv", parse_dates=["FL_DATE"])

st.subheader("Total Weather Delay Time")
st.metric("Minutes", int(df["DELAY_DUE_WEATHER"].sum()))

st.subheader("✈️ Weather Delays by Airline")
weather_airline = df.groupby("AIRLINE")["DELAY_DUE_WEATHER"].sum().sort_values(ascending=False)
fig1 = px.bar(weather_airline, title="Weather Delay by Airline")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📅 Weather Delay Over Time")
fig2 = px.line(df.groupby("FL_DATE")["DELAY_DUE_WEATHER"].sum().reset_index(),
               x="FL_DATE", y="DELAY_DUE_WEATHER", title="Weather Delay Over Time")
st.plotly_chart(fig2, use_container_width=True)

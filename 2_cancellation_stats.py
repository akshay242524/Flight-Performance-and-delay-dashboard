import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cancellation Stats", layout="wide")
st.title("❌ Cancellation Statistics")

df = pd.read_csv("data/data1.csv", parse_dates=["FL_DATE"])

cancelled_df = df[df["CANCELLED"] == 1]

st.metric("Total Cancellations", len(cancelled_df))

st.subheader("🛫 Cancellation by Airline")
fig1 = px.bar(cancelled_df.groupby("AIRLINE")["CANCELLED"].count().sort_values(ascending=False),
              title="Cancellations by Airline")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📅 Cancellation Trend Over Time")
fig2 = px.histogram(cancelled_df, x="FL_DATE", nbins=30, title="Cancellations Over Time")
st.plotly_chart(fig2, use_container_width=True)

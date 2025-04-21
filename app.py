import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from utils.analytics import generate_kpis, delay_heatmap_data, map_delay_data

st.set_page_config(page_title="Flight Delay Dashboard", layout="wide")
st.title("✈️ Flight Performance and Delay Visualization")

# Load Data
df = pd.read_csv("data/data1.csv", parse_dates=["FL_DATE"])

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filters")
    selected_airlines = st.multiselect("Select Airlines", df["AIRLINE"].unique(), default=df["AIRLINE"].unique())
    selected_origin = st.multiselect("Select Origin Airports", df["ORIGIN"].unique(), default=df["ORIGIN"].unique())
    selected_dest = st.multiselect("Select Destination Airports", df["DEST"].unique(), default=df["DEST"].unique())
    date_range = st.date_input("Select Date Range", [df["FL_DATE"].min(), df["FL_DATE"].max()])

# Apply Filters

df_filtered = df[
    (df["AIRLINE"].isin(selected_airlines)) &
    (df["ORIGIN"].isin(selected_origin)) &
    (df["DEST"].isin(selected_dest)) 
]

# KPIs
st.subheader("📈 Key Metrics")
flights, delay_pct, avg_delay, cancelled_pct = generate_kpis(df_filtered)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Flights", flights)
col2.metric("Delayed %", f"{delay_pct:.2f}%")
col3.metric("Avg Departure Delay", f"{avg_delay:.1f} min")
col4.metric("Cancellation %", f"{cancelled_pct:.2f}%")

# Time Series: Flight Count
st.subheader("📅 Flights Over Time")
fig1 = px.histogram(df_filtered, x="FL_DATE", nbins=50, title="Flights Over Time")
st.plotly_chart(fig1, use_container_width=True)

# Delay by Airline
st.subheader("🚨 Top 10 Airlines by Avg Departure Delay")
top10 = df_filtered.groupby("AIRLINE")["DEP_DELAY"].mean().sort_values(ascending=False).head(10)
fig2 = px.bar(top10, x=top10.index, y=top10.values, labels={'y': 'Avg Departure Delay'}, title="Worst Delayed Airlines")
st.plotly_chart(fig2, use_container_width=True)

# Heatmap
st.subheader("🔥 Delay Heatmap (Hour vs Day)")
heat_df = delay_heatmap_data(df_filtered)
fig3 = px.density_heatmap(heat_df, x="HOUR", y="DAY", z="DEP_DELAY", histfunc="avg", title="Average Departure Delay")
st.plotly_chart(fig3, use_container_width=True)

# Map of Delays
st.subheader("🌍 Map of Average Delays by Airport")
map_df = map_delay_data(df_filtered)
m = folium.Map(location=[37.1, -95.7], zoom_start=4)
for _, row in map_df.iterrows():
    folium.CircleMarker(
        location=[row["LAT"], row["LON"]],
        radius=7,
        popup=f"{row['ORIGIN']} - {row['DEP_DELAY']:.1f} min",
        color="crimson",
        fill=True
    ).add_to(m)
st_folium(m, width=700)

airport_coords = {
    "JFK": (40.6413, -73.7781),
    "LAX": (33.9416, -118.4085),
    "ORD": (41.9742, -87.9073),
    "DFW": (32.8998, -97.0403),
    "ATL": (33.6407, -84.4277),
    "DEN": (39.8561, -104.6737)
}

# Delay Reasons
st.subheader("🌍 Delay Cause Maps by Airport")

delay_causes = {
    "DELAY_DUE_WEATHER": "Weather",
    "DELAY_DUE_CARRIER": "Carrier",
    "DELAY_DUE_NAS": "NAS",
    "DELAY_DUE_SECURITY": "Security",
    "DELAY_DUE_LATE_AIRCRAFT": "Late Aircraft"
}

for col, label in delay_causes.items():
    st.markdown(f"### {label} Delay Map")

    # Add lat/lon based on origin
    df["LAT"] = df["ORIGIN"].map(lambda x: airport_coords.get(x, (0, 0))[0])
    df["LON"] = df["ORIGIN"].map(lambda x: airport_coords.get(x, (0, 0))[1])

    delay_map = df.groupby(["ORIGIN", "LAT", "LON"])[col].mean().reset_index()
    delay_map = delay_map[delay_map[col] > 0]  # show only airports with some delay

    m = folium.Map(location=[37, -95], zoom_start=4)
    for _, row in delay_map.iterrows():
        folium.CircleMarker(
            location=[row["LAT"], row["LON"]],
            radius=6,
            popup=f"{row['ORIGIN']} - {row[col]:.1f} min",
            color="blue",
            fill=True
        ).add_to(m)

    st_folium(m, width=700)




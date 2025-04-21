import pandas as pd

def generate_kpis(df):
    total = len(df)
    delayed = df[df["DEP_DELAY"] > 15]
    delay_pct = len(delayed) / total * 100 if total else 0
    avg_delay = df["DEP_DELAY"].mean() if total else 0
    cancelled_pct = df["CANCELLED"].mean() * 100 if "CANCELLED" in df.columns else 0
    return total, delay_pct, avg_delay, cancelled_pct


def delay_heatmap_data(df):
    df["HOUR"] = df["DEP_TIME"] // 100
    df["DAY"] = df["FL_DATE"].dt.day_name()
    return df[["HOUR", "DAY", "DEP_DELAY"]]

def map_delay_data(df):
    airport_coords = {
        "JFK": (40.6413, -73.7781),
        "LAX": (33.9416, -118.4085),
        "ORD": (41.9742, -87.9073),
        "DFW": (32.8998, -97.0403),
        "ATL": (33.6407, -84.4277),
        "DEN": (39.8561, -104.6737)
    }
    df["LAT"] = df["ORIGIN"].apply(lambda x: airport_coords.get(x, (0,0))[0])
    df["LON"] = df["ORIGIN"].apply(lambda x: airport_coords.get(x, (0,0))[1])
    return df.groupby(["ORIGIN", "LAT", "LON"])["DEP_DELAY"].mean().reset_index()


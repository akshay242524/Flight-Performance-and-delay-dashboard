import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Trained once on dummy data — plug your real data here
def train_model():
    data = {
        "DISTANCE": [200, 800, 1500, 2500, 1000, 1800],
        "HOUR": [10, 15, 8, 12, 18, 5],
        "WEATHER": [5, 15, 10, 20, 8, 30],
        "CARRIER": [10, 20, 40, 30, 15, 25],
        "DELAY": [25, 50, 75, 90, 55, 80]
    }
    df = pd.DataFrame(data)
    X = df.drop("DELAY", axis=1)
    y = df["DELAY"]
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

rf_model = train_model()

def predict_delay(distance, hour, weather, carrier):
    X_input = pd.DataFrame([[distance, hour, weather, carrier]],
                           columns=["DISTANCE", "HOUR", "WEATHER", "CARRIER"])
    return rf_model.predict(X_input)[0]



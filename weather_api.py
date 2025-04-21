import requests

API_KEY = "2be77928baa36c3eb1221bb7e0bfbca4"

airport_to_city = {
    "JFK": "New York",
    "LAX": "Los Angeles",
    "ORD": "Chicago",
    "DFW": "Dallas",
    "ATL": "Atlanta",
    "DEN": "Denver"
}

def get_current_weather(iata_code):
    city = airport_to_city.get(iata_code, "New York")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "City": city,
                "Temperature (°C)": data["main"]["temp"],
                "Weather": data["weather"][0]["description"].title(),
                "Wind Speed (m/s)": data["wind"]["speed"],
                "Humidity (%)": data["main"]["humidity"]
            }
        else:
            return {"Error": f"API Error {response.status_code}"}
    except Exception as e:
        return {"Error": str(e)}

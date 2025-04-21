from datetime import datetime
import pytz

airport_timezones = {
    "JFK": "America/New_York",
    "LAX": "America/Los_Angeles",
    "ORD": "America/Chicago",
    "DFW": "America/Chicago",
    "ATL": "America/New_York",
    "DEN": "America/Denver"
}

def get_local_time(iata_code):
    tz = pytz.timezone(airport_timezones.get(iata_code, "UTC"))
    now = datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")

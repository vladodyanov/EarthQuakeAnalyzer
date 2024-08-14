import requests


def fetch_earthquake_data(start_date, end_date, min_magnitude):
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
        "minmagnitude": min_magnitude
    }
    response = requests.get(url, params=params)
    return response.json()

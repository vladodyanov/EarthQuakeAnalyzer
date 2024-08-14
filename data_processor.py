import pandas as pd
from utils import get_continent


def process_data(data):
    features = data['features']
    processed_data = []
    for feature in features:
        properties = feature['properties']
        coordinates = feature['geometry']['coordinates']
        latitude = coordinates[1]
        longitude = coordinates[0]
        country = properties.get('place', '').split(', ')[-1] if properties.get('place') else 'Неизвестна'
        processed_data.append({
            'magnitude': properties['mag'],
            'place': properties['place'],
            'time': pd.to_datetime(properties['time'], unit='ms'),
            'depth': coordinates[2],
            'latitude': latitude,
            'longitude': longitude,
            'country': country,
            'nearest_city': properties.get('place'),
            'continent': get_continent(latitude, longitude)
        })
    return pd.DataFrame(processed_data)

"""Constants for MeteoNetwork Weather component."""

DOMAIN = "meteonetwork_weather"

API_BASE = "https://api.meteonetwork.it/v3"

SENSOR_TYPES = {
    "native_temperature": {
        "name": "Temperature",
        "unit": "°C",
        "device_class": "temperature",
        "data_key": "temperature",
    },
    "humidity": {
        "name": "Humidity",
        "unit": "%",
        "device_class": "humidity",
        "data_key": "humidity",
    },
    "native_pressure": {
        "name": "Pressure",
        "unit": "hPa",
        "device_class": "pressure",
        "data_key": "pressure",
    },
    "daily_rain": {
        "name": "Daily rain",
        "unit": "mm",
        "device_class": "precipitation",
        "data_key": "daily_rain",
    },
    "wind_bearing": {
        "name": "Wind bearing",
        "device_class": "direction",
        "data_key": "wind_bearing",
    },
    "native_wind_speed": {
        "name": "Wind speed",
        "unit": "km/h",
        "device_class": "wind",
        "data_key": "wind_speed",
    },
    "uv_index": {
        "name": "UV index",
        "unit": "UV index",
        "device_class": "uv_index",
        "data_key": "uv_index",
    },
    "native_dew_point": {
        "name": "Dew point",
        "unit": "°C",
        "device_class": "dew_point",
        "data_key": "dew_point",
    },
    "rain_rate": {
        "name": "Rain rate",
        "unit": "mm/h",
        "device_class": "precipitation",
        "data_key": "rain_rate",
    },
}

CARDINAL_DIRECTIONS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE',
                       'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']

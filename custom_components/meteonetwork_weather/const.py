"""Constants for MeteoNetwork Weather component."""

DOMAIN = "meteonetwork_weather"

API_BASE = "https://api.meteonetwork.it/v3"

SENSOR_TYPES = {
    "native_temperature": {
        "name": "Temperature",
        "unit": "°C",
        "device_class": "temperature",
    },
    "humidity": {
        "name": "Humidity",
        "unit": "%",
        "device_class": "humidity",
    },
    "native_pressure": {
        "name": "pressure",
        "unit": "hPa",
        "device_class": "pressure",
    },
    "native_precipitation": {
        "name": "Precipitation",
        "unit": "mm",
        "device_class": "precipitation",
    },
    "wind_bearing": {
        "name": "Wind bearing",
        "device_class": "direction",
    },
    "native_wind_speed": {
        "name": "Wind speed",
        "unit": "km/h",
        "device_class": "wind",
    },
    "uv_index": {
        "name": "UV index",
        "unit": "UV index",
        "device_class": "uv_index",
    },
    "native_dew_point": {
        "name": "Dew point",
        "unit": "°C",
        "device_class": "dew_point",
    },
}

CARDINAL_DIRECTIONS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE',
                       'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']

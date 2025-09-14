"""Constants for MeteoNetwork Weather component."""

DOMAIN = "meteonetwork_weather"

API_BASE = "https://api.meteonetwork.it/v3"

CONF_EXPOSE_RAW_DATA = "expose_raw_data"
CONF_EXPOSE_EXTENDED_SENSORS = "expose_extended_sensors"
CONF_EXPOSE_STATION_ATTRS_AS_SENSORS = "expose_station_attrs_as_sensors"
CONF_INFER_CONDITION = "infer_condition"
CONF_INFER_CONDITION_FROM_SENSORS = "infer_condition_from_sensors"
CONF_INFER_CONDITION_FROM_SENSORS_WITH_CUSTOM_THRESHOLDS = "infer_condition_from_sensors_with_custom_thresholds"
CONF_INFER_CONDITION_DISABLED = "infer_condition_disabled"

CONF_INFER_CONDITION_DAY_CLEAR_THRESHOLD = "day_clear_threshold"
CONF_INFER_CONDITION_DAY_CLEAR_THRESHOLD_DEFAULT = 0.75
CONF_INFER_CONDITION_DAY_PARTLY_THRESHOLD = "day_partly_threshold"
CONF_INFER_CONDITION_DAY_PARTLY_THRESHOLD_DEFAULT = 0.40

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

SENSOR_TYPES_EXTENDED = {
    "observation_time_local": {
        "name": "Observation time",
        "unit": None,
        "device_class": None,
        "data_key": "observation_time_local",
    },
    "observation_time_utc": {
        "name": "Observation time UTC",
        "unit": None,
        "device_class": None,
        "data_key": "observation_time_utc",
    },
    "rad": {
        "name": "Solar radiation",
        "unit": "W/m2",
        "device_class": "uv_index",
        "data_key": "rad",
    },
    "wind_direction": {
        "name": "Wind direction (cardinals)",
        "unit": "cardinals",
        "device_class": "direction",
        "data_key": "wind_direction",
    },
    "wind_direction_degree": {
        "name": "Wind direction (degree)",
        "unit": "°",
        "device_class": "direction",
        "data_key": "wind_direction_degree",
    },
    "wind_gust": {
        "name": "Wind gust",
        "unit": "km/h",
        "device_class": "wind",
        "data_key": "wind_gust",
    },
    "uv": {
        "name": "UV",
        "unit": "UV index",
        "device_class": "uv_index",
        "data_key": "uv",
    },
    "current_tmin": {
        "name": "Current daily low temperature",
        "unit": "°C",
        "device_class": "temperature",
        "data_key": "current_tmin",
    },
    "current_tmed": {
        "name": "Current daily average temperature",
        "unit": "°C",
        "device_class": "temperature",
        "data_key": "current_tmed",
    },
    "current_tmax": {
        "name": "Current daily high temperature",
        "unit": "°C",
        "device_class": "temperature",
        "data_key": "current_tmax",
    },
    "current_rhmin": {
        "name": "Current daily low relative humidity",
        "unit": "%",
        "device_class": "humidity",
        "data_key": "current_rhmin",
    },
    "current_rhmed": {
        "name": "Current daily average relative humidity",
        "unit": "%",
        "device_class": "humidity",
        "data_key": "current_rhmed",
    },
    "current_rhmax": {
        "name": "Current daily high relative humidity",
        "unit": "%",
        "device_class": "humidity",
        "data_key": "current_rhmax",
    },
    "current_wgustmax": {
        "name": "Current daily max wind gust",
        "unit": "km/h",
        "device_class": "wind",
        "data_key": "current_wgustmax",
    },
    "current_wspeedmax": {
        "name": "Current daily max wind speed",
        "unit": "km/h",
        "device_class": "wind",
        "data_key": "current_wspeedmax",
    },
    "current_wspeedmed": {
        "name": "Current daily average wind speed",
        "unit": "km/h",
        "device_class": "wind",
        "data_key": "current_wspeedmed",
    },
    "current_uvmed": {
        "name": "Current daily average UV",
        "unit": "W/m2",
        "device_class": "uv_index",
        "data_key": "current_uvmed",
    },
    "current_uvmax": {
        "name": "Current daily high UV",
        "unit": "W/m2",
        "device_class": "uv_index",
        "data_key": "current_uvmax",
    },
    "current_radmed": {
        "name": "Current daily average radiation",
        "unit": "index",
        "device_class": "uv_index",
        "data_key": "current_radmed",
    },
    "current_radmax": {
        "name": "Current daily high radiation",
        "unit": "index",
        "device_class": "uv_index",
        "data_key": "current_radmax",
    },
}

SENSOR_TYPES_STATION = {
    "station_code": {
        "name": "Station code",
        "unit": None,
        "device_class": None,
        "data_key": "station_code",
    },
    "station_name": {
        "name": "Station name",
        "unit": None,
        "device_class": None,
        "data_key": "name",
    },
    "station_place": {
        "name": "Station place",
        "unit": None,
        "device_class": None,
        "data_key": "place",
    },
    "station_area": {
        "name": "Station area",
        "unit": None,
        "device_class": None,
        "data_key": "area",
    },
    "latitude": {
        "name": "Latitude",
        "unit": "°",
        "device_class": None,
        "data_key": "latitude",
    },
    "longitude": {
        "name": "Longitude",
        "unit": "°",
        "device_class": None,
        "data_key": "longitude",
    },
    "altitude": {
        "name": "Sea level altitude",
        "unit": "m",
        "device_class": "elevation",
        "data_key": "altitude",
    },
    "country": {
        "name": "ISO 3166-1 alpha-2 country code",
        "unit": None,
        "device_class": None,
        "data_key": "country",
    },
    "region_name": {
        "name": "Region/State",
        "unit": None,
        "device_class": None,
        "data_key": "region_name",
    },
}

SENSOR_TYPES_ALL = {**SENSOR_TYPES, **SENSOR_TYPES_EXTENDED, **SENSOR_TYPES_STATION}

BANNED_SENSORS = [
    "temperature",
    "rh",
    "humidity",
    "wind_direction",
    "pressure",
    "wind_speed",
    "wind_gust",
    "daily_rain",
    "uv",
    "dew_point",
    "rain_rate",
    "altitude",
    "latitude",
    "longitude",
]

CARDINAL_DIRECTIONS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE',
                       'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']

"""Coordinator for consuming REST api endpoints on MeteoNetwork Weather component."""
import asyncio
import logging

import aiohttp
import pytz

from custom_components.meteonetwork_weather.thresholds import DayThresholds
from . import const
from .const import API_BASE, CARDINAL_DIRECTIONS, DOMAIN


from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.util import dt as homeassistant_dt

from datetime import datetime
from re import sub
from astral import LocationInfo
from astral.sun import sun, elevation
from math import radians, sin

_LOGGER = logging.getLogger(__name__)

class MeteoNetworkDataUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for MeteoNetwork."""

    def __init__(self, hass, config_entry, update_interval, rate_limiter):
        """Initialize the data update coordinator."""
        self.rate_limiter = rate_limiter
        self.station_type = config_entry.data.get("station_type")
        self.latitude = config_entry.data.get("latitude")
        self.longitude = config_entry.data.get("longitude")
        self.station_name = config_entry.data.get("station_name")
        self.station_id = config_entry.data.get("station_id")
        self.token = config_entry.data.get("token")
        self.is_virtual = self.station_type == "virtual"
        self.infer_condition = config_entry.options.get(const.CONF_INFER_CONDITION)
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{_slugify(self.station_name) if self.is_virtual else self.station_id}",
            update_method=self._async_update_data,
            update_interval=update_interval,
        )
        self._lock = asyncio.Lock()  # To throttle manual updates

    async def _async_update_data(self):
        """Fetch the latest data from the API."""
        sensor_data = await self.fetch_station_data()
        day_cfg = DayThresholds()
        latitude = sensor_data.get('latitude')
        longitude = sensor_data.get('longitude')

        # Determine the current condition based on configuration
        match self.infer_condition:
            case const.CONF_INFER_CONDITION_FROM_SENSORS:
                sensor_data["condition"] = await self._compute_condition_from_sensors(latitude, longitude, sensor_data)
            case const.CONF_INFER_CONDITION_FROM_SENSORS_WITH_CUSTOM_THRESHOLDS:
                opts = self.config_entry.options
                if opts.get("override_thresholds"):
                    day_cfg = DayThresholds(
                        clear_ratio=opts.get(
                            "day_clear_ratio", const.CONF_INFER_CONDITION_DAY_CLEAR_THRESHOLD_DEFAULT),
                        partly_ratio=opts.get(
                            "day_partly_ratio", const.CONF_INFER_CONDITION_DAY_PARTLY_THRESHOLD_DEFAULT),
                    )

                sensor_data["condition"] = await self._compute_condition_from_sensors(latitude, longitude, sensor_data, day_cfg)
            case _:  # CONF_INFER_CONDITION_DISABLED or any other value
                pass  # Do not compute condition

        return {
            "sensors": sensor_data,  # Include sensor data like temperature
        }

    async def async_throttled_update(self):
        """Manually trigger an update with throttling."""
        async with self._lock:  # Ensures only one update happens at a time
            return await self.async_request_refresh()

    def _store_float(self, source, source_key, target, target_key):
        if (value := source.get(source_key)) is not None:
            try:
                target[target_key] = float(value)
            except ValueError:
                target[target_key] = None

    async def fetch_station_data(self):
        """Fetch data from the station."""
        headers = {"Authorization": f"Bearer {self.token}"}
        _station_id = self.station_id
        async with aiohttp.ClientSession(headers=headers) as session:
            async def fetch_data():
                params = {}
                if self.is_virtual:
                    url = f"{API_BASE}/interpolated-realtime"
                    params["lat"] = self.latitude
                    params["lon"] = self.longitude
                else:
                    url = f"{API_BASE}/data-realtime/{_station_id}"

                return await session.get(url=url, params=params)

            response = await self.rate_limiter.throttle(lambda: fetch_data())
            if response.status != 200:
                raise UpdateFailed(f"Error fetching data: {response.status}")

        extracted_data = {}
        if self.is_virtual:
            data = (await response.json())
            extracted_data["station_name"] = self.station_name
        else:
            data = (await response.json())[0]
            extracted_data["station_name"] = data["name"]

        extracted_data["raw"] = data

        # Extract temperature, humidity, and other data
        for key, value in data.items():
            if isinstance(value, str) and value.replace('.', '', 1).isdigit():
                self._store_float(data, key, extracted_data, key)
            else:
                extracted_data[key] = value
        self._store_float(data, "temperature", extracted_data, "temperature")
        self._store_float(data, "rh", extracted_data, "humidity")
        self._store_float(data, "wind_direction", extracted_data, "wind_bearing")
        self._store_float(data, "smlp", extracted_data, "pressure")
        self._store_float(data, "wind_speed", extracted_data, "wind_speed")
        self._store_float(data, "wind_gust", extracted_data, "wind_gust")
        self._store_float(data, "daily_rain", extracted_data, "daily_rain")
        self._store_float(data, "uv", extracted_data, "uv_index")
        self._store_float(data, "dew_point", extracted_data, "dew_point")
        self._store_float(data, "smlp", extracted_data, "pressure")
        self._store_float(data, "rain_rate", extracted_data, "rain_rate")

        if (extracted_data.get("wind_bearing")) is None:
            if (value := data.get("wind_direction_degree")) is not None:
                extracted_data["wind_bearing"] = CARDINAL_DIRECTIONS[int(
                    (float(value) + 11.25)/22.5)]

        if (extracted_data.get("uv_index")) is None:
            if (value := data.get("rad")) is not None:
                # Assuming UV Fraction = 6% => 0.06
                # For W/m², the scaling factor is 0.04 because it represents instantaneous power
                extracted_data["uv_index"] = round(float(value) * 0.06 * 0.04)

        extracted_data["last_update"] = datetime.now().isoformat()
        extracted_data["altitude"] = data.get("altitude")
        extracted_data["latitude"] = data.get("latitude")
        extracted_data["longitude"] = data.get("longitude")

        return extracted_data

    async def _compute_condition_from_sensors(self, lat, long, sensor_data, day_cfg=DayThresholds()):
        """Compute the current condition based on sensor data."""

        dt_str = sensor_data.get("observation_time_utc")
        if dt_str is None:
            return "unknown"
        dt = await self._local_dt(dt_str)
        return await self.classify_sky(lat, long, dt, sensor_data, day_cfg)

    async def _local_dt(self, dt_str):
        """Convert a datetime string to a localized datetime object."""

        # tz = await self.hass.states.get('timezone').state
        # Step 1: naive datetime
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

        # Step 2: Make it timezone-aware (UTC)
        dt_utc = dt.replace(tzinfo=pytz.UTC)

        # Step 3: Convert to local timezone
        dt_local = homeassistant_dt.as_local(dt_utc)

        # Step 4: Convert to specific timezone
        # dt_hass = dt_utc.astimezone(pytz.timezone(tz))

        return dt_local

    async def classify_sky(self, lat, lon, dt, sensor_data, day_cfg: DayThresholds):
        """Classifies the sky condition.

        Based on:
        - Day: incident solar radiation (normalized to solar elevation)
        - Night: return always Unknows, as we miss the sky brightness (mag/arcsec²) corrected for Moon phase

        :param lat: latitude (float)
        :param lon: longitude (float)
        :param dt: datetime with tzinfo
        :param sensor_data: sensor data containing "ghi" [W/m²]
        :param day_cfg: the day thresholds configuration
        :return: string ["clear", "partlycloudy", "cloudy", "unknown"]
        """

        temperature = sensor_data.get("temperature")
        humidity = sensor_data.get("rh")
        dew_point = sensor_data.get("dew_point")
        wind_speed = sensor_data.get("wind_speed")
        precipitation = sensor_data.get("rain_rate")

        ghi = sensor_data.get("rad")  # solar radiation in W/m²

        # Precipitation overrides everything
        if precipitation is not None and precipitation > 0:
            if temperature is not None:
                if temperature <= 5:
                    return "snow"
                elif temperature <= 0:
                    return "snowy-rainy"
                if precipitation > 20:
                    return "pouring"
            return "rainy"

        # fog overrides wind
        if dew_point is not None and temperature is not None:
            temp_dp_diff = abs(temperature - dew_point)
            if temp_dp_diff <= 1.0:  # Temperature within 1°C of dew point
                return "fog"
            if humidity is not None and humidity > 97 and temp_dp_diff <= 2.0:
                return "fog"

        if wind_speed and wind_speed > 30:
            return "windy"

        city = LocationInfo(latitude=lat, longitude=lon)
        s = sun(city.observer, date=dt.date(), tzinfo=dt.tzinfo)

        is_day = s["sunrise"] <= dt <= s["sunset"]

        if is_day:
            if ghi is None:
                return "unknown"

            # Sun elevation in degrees
            h_sun = elevation(city.observer, dt)

            if h_sun <= 0:
                return "unknown"  # Sun below horizon (transitions)

            # Theoretical maximum irradiance (approximated)
            ghi_clear = 1000 * sin(radians(h_sun))

            # Normalization
            ghi_ratio = ghi / ghi_clear if ghi_clear > 0 else 0

            # Empirical thresholds (to be calibrated on local data)
            if ghi_ratio > day_cfg.clear:
                return "sunny"
            elif ghi_ratio > day_cfg.partly_cloudy:
                return "partlycloudy"
            else:
                if wind_speed and wind_speed > 30:
                    return "windy-variant"
                return "cloudy"

        else:  # if we had data about night sky brightness, we could classify night conditions here
            return "unknown"


def _slugify(s):
    s = s.lower().strip()
    s = sub(r'[^\w\s-]', '', s)
    s = sub(r'[\s_-]+', '-', s)
    s = sub(r'^-+|-+$', '', s)
    return s

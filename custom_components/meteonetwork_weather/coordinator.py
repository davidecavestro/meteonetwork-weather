"""Coordinator for consuming REST api endpoints on MeteoNetwork Weather component."""
import asyncio
import logging

import aiohttp
from .const import API_BASE, CARDINAL_DIRECTIONS, DOMAIN


from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed


from datetime import datetime
from re import sub

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
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{slugify(self.station_name) if self.is_virtual else self.station_id}",
            update_method=self._async_update_data,
            update_interval=update_interval,
        )
        self._lock = asyncio.Lock()  # To throttle manual updates

    async def _async_update_data(self):
        """Fetch the latest data from the API."""
        sensor_data = await self.fetch_station_data()
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

        # Extract temperature, humidity, and other data
        self._store_float(data, "temperature", extracted_data, "temperature")
        self._store_float(data, "rh", extracted_data, "humidity")
        self._store_float(data, "wind_direction", extracted_data, "wind_bearing")
        self._store_float(data, "smlp", extracted_data, "pressure")
        self._store_float(data, "wind_speed", extracted_data, "wind_speed")
        self._store_float(data, "wind_gust", extracted_data, "wind_gust")
        self._store_float(data, "daily_rain", extracted_data, "precipitation")
        self._store_float(data, "uv", extracted_data, "uv_index")
        self._store_float(data, "dew_point", extracted_data, "dew_point")
        self._store_float(data, "smlp", extracted_data, "pressure")

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

def slugify(s):
    s = s.lower().strip()
    s = sub(r'[^\w\s-]', '', s)
    s = sub(r'[\s_-]+', '-', s)
    s = sub(r'^-+|-+$', '', s)
    return s

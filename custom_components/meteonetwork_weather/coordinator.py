"""Coordinator for consuming REST api endpoints on MeteoNetwork Weather component."""
import asyncio
import logging

import aiohttp
from .const import API_BASE, CARDINAL_DIRECTIONS, DOMAIN


from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed


from datetime import datetime

_LOGGER = logging.getLogger(__name__)

class MeteoNetworkDataUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for MeteoNetwork."""

    def __init__(self, hass, config_entry, update_interval):
        """Initialize the data update coordinator."""
        self.station_id = config_entry.data.get("station_id")
        self.token = config_entry.data.get("token")
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{self.station_id}",
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

    async def fetch_station_data(self):
        """Fetch data from the station."""
        url = f"{API_BASE}/data-realtime/{self.station_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        async with aiohttp.ClientSession(headers=headers) as session, session.get(url) as response:
            if response.status != 200:
                raise UpdateFailed(f"Error fetching data: {response.status}")
            data = (await response.json())[0]

        extracted_data = {}
        # Extract temperature, humidity, and other data
        extracted_data["station_name"] = data["name"]
        if (value := data.get("temperature")):
            extracted_data["temperature"] = float(
                value) if value.replace('.', '', 1).isdigit() else None
        if (value := data.get("rh")):
            extracted_data["humidity"] = float(
                value) if value.replace('.', '', 1).isdigit() else None
        if (value := data.get("wind_direction")):
            extracted_data["wind_bearing"] = float(
                value) if value.replace('.', '', 1).isdigit() else None
        elif (value := data.get("wind_direction_degree")):
            extracted_data["wind_bearing"] = CARDINAL_DIRECTIONS[int(
                (value + 11.25)/22.5)] if value.replace('.', '', 1).isdigit() else None
        if (value := data.get("smlp")):
            extracted_data["pressure"] = float(
                value) if value.replace('.', '', 1).isdigit() else None
        if (value := data.get("wind_speed")):
            extracted_data["wind_speed"] = float(
                value) if value.replace('.', '', 1).isdigit() else None
        if (value := data.get("wind_gust")):
            extracted_data["wind_gust"] = float(
                value) if value.replace('.', '', 1).isdigit() else None
        if (value := data.get("daily_rain")):
            extracted_data["precipitation"] = float(
                value) if value.replace('.', '', 1).isdigit() else None
        if (value := data.get("rad")):
            extracted_data["uv_index"] = float(
                value) if value.replace('.', '', 1).isdigit() else None
        elif (value := data.get("uv")):
            extracted_data["uv_index"] = round(
                float(value) / 0.025) if value.replace('.', '', 1).isdigit() else None
        if (value := data.get("dew_point")):
            extracted_data["dew_point"] = float(
                value) if value.replace('.', '', 1).isdigit() else None
        if (value := data.get("smlp")):
            extracted_data["pressure"] = float(
                value) if value.replace('.', '', 1).isdigit() else None

        extracted_data["last_update"] = datetime.now().isoformat()
        extracted_data["altitude"] = data.get("altitude")
        extracted_data["latitude"] = data.get("latitude")
        extracted_data["longitude"] = data.get("longitude")

        return extracted_data

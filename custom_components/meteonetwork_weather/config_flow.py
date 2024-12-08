"""Config flow to configure MeteoNetwork Weather component."""
import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, API_BASE


class MeteoNetworkWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MeteoNetwork Weather."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Acquire the auth token and station_id."""
        if user_input is not None:
            token = user_input["token"]
            station_id = user_input["station_id"]

            station_name = await self.fetch_station_data(token, station_id)

            return self.async_create_entry(
                title=station_name,
                data={
                    "token": token,
                    "station_id": station_id,
                    "station_name": station_name,
                }
            )

        schema = vol.Schema({
            vol.Required("token"): str,
            vol.Required("station_id"): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def fetch_station_data(self, token, station_id):
        """Fetch the station data."""
        headers = {"Authorization": f"Bearer {token}"}
        async with aiohttp.ClientSession(headers=headers) as session, session.get(f"{API_BASE}/data-realtime/{station_id}") as response:
            response.raise_for_status()
            json_data = (await response.json())[0]
            return json_data["name"]

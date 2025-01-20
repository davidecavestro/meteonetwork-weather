"""Config flow to configure MeteoNetwork Weather component."""
import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, API_BASE


class MeteoNetworkWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MeteoNetwork Weather."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Step 1: Collect the token and choose the station type."""
        if user_input is not None:
            # Save the token and proceed based on station type
            self.token = user_input["token"]
            if user_input["station_type"] == "real":
                return await self.async_step_real_station()
            elif user_input["station_type"] == "virtual":
                return await self.async_step_virtual_station()

        # Step 1 schema: Collect token and station type
        schema = vol.Schema({
            vol.Required("token"): str,
            vol.Required("station_type", default="real"): vol.In({
                "real": "Real Station",  # Internal keys (localization is automatic)
                "virtual": "Virtual Station",
            }),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_real_station(self, user_input=None):
        """Step 2: Configure real station."""
        if user_input is not None:
            station_id = user_input["station_id"]

            # Fetch station name from API
            station_name = await self.fetch_station_data(self.token, station_id)

            return self.async_create_entry(
                title=station_name,
                data={
                    "station_type": "real",
                    "token": self.token,
                    "station_id": station_id,
                    "station_name": station_name,
                },
            )

        # Step 2 schema: Real station configuration
        schema = vol.Schema({
            vol.Required("station_id"): str,
        })

        description_placeholders = {
            "link": "<a href=\"https://www.meteonetwork.it/rete/livemap/#\" target=\"_blank\">meteonetwork.it</a>",
        }

        return self.async_show_form(
            step_id="real_station",
            data_schema=schema,
            description_placeholders=description_placeholders,
        )

    async def async_step_virtual_station(self, user_input=None):
        """Step 2: Configure virtual station."""
        if user_input is not None:
            latitude = user_input["latitude"]
            longitude = user_input["longitude"]
            station_name = user_input["station_name"]

            return self.async_create_entry(
                title=station_name,
                data={
                    "station_type": "virtual",
                    "token": self.token,
                    "latitude": latitude,
                    "longitude": longitude,
                    "station_name": station_name,
                },
            )

        latitude = self.hass.config.latitude
        longitude = self.hass.config.longitude
        # Step 2 schema: Virtual station configuration
        schema = vol.Schema({
            vol.Required("station_name", default="Virtual Station"): str,
            vol.Required("latitude", default=latitude): vol.Coerce(float),
            vol.Required("longitude", default=longitude): vol.Coerce(float),
        })

        description_placeholders = {
            "link": f"<a href=\"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=15/{latitude}/{longitude}\" target=\"_blank\">openstreetmap.org</a>",
        }

        return self.async_show_form(
            step_id="virtual_station",
            data_schema=schema,
            description_placeholders=description_placeholders,
        )

    async def fetch_station_data(self, token, station_id):
        """Fetch the station data."""
        headers = {"Authorization": f"Bearer {token}"}
        async with aiohttp.ClientSession(headers=headers) as session, session.get(f"{API_BASE}/data-realtime/{station_id}") as response:
            response.raise_for_status()
            json_data = (await response.json())[0]
            return json_data["name"]

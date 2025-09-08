"""Config flow to configure MeteoNetwork Weather component."""
import aiohttp
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.translation import async_get_translations
from .const import DOMAIN, API_BASE, CONF_EXPOSE_RAW_DATA, CONF_EXPOSE_EXTENDED_SENSORS, CONF_EXPOSE_STATION_ATTRS_AS_SENSORS

class MeteoNetworkWeatherConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MeteoNetwork Weather."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Implement OptionsFlow."""
        return MeteoNetworkWeatherOptionsFlowHandler()

    async def async_step_user(self, user_input=None):
        """Step 1: Collect the token and choose the station type."""
        if user_input is not None:
            # Save the token and proceed based on station type
            self.token = user_input["token"]
            if user_input["station_type"] == "real":
                return await self.async_step_real_station()
            elif user_input["station_type"] == "virtual":
                return await self.async_step_virtual_station()

        # Fetch translations for the current language
        # translations = await async_get_translations(self.hass, DOMAIN, "config")
        translations = await async_get_translations(
            self.hass,
            language=self.hass.config.language,  # Uses the current language of the Home Assistant instance
            category="config",
            integrations=[DOMAIN],  # integration's domain
        )

        # Retrieve localized labels with fallback
        real_label = translations.get("step.user.data.station_type_real", "Real Station")
        virtual_label = translations.get(
            "step.user.data.station_type_virtual", "Virtual Station")

        # Step 1 schema: Collect token and station type
        schema = vol.Schema({
            vol.Required("token"): str,
            vol.Required(
                "station_type",
                default="real"
            ): vol.In({
                "real": real_label,
                "virtual": virtual_label,
            }),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_real_station(self, user_input=None):
        """Step 2: Configure real station."""

        errors = {}
        description_placeholders = {
            "link": "<a href=\"https://www.meteonetwork.it/rete/livemap/#\" target=\"_blank\">meteonetwork.it</a>",
            "error_msg": ""
        }

        if user_input is not None:
            station_id = user_input["station_id"]

            try:
                # Fetch station name from API
                json_data = await self.fetch_station_data(self.token, station_id)

                # Case 1: If not a list, treat it as an error
                if not isinstance(json_data, list):
                    # Maybe it's a dict with error details
                    if isinstance(json_data, dict) and json_data.get("error") is True:
                        description_placeholders["error_msg"] = json_data.get(
                            "message", "Unknown error")
                        errors["base"] = "remote_error"
                    else:
                        raise ValueError("Unexpected response structure")

                else:
                    # Valid data, continue
                    station_name = json_data[0]["name"]

                    return self.async_create_entry(
                        title=station_name,
                        data={
                            "station_type": "real",
                            "token": self.token,
                            "station_id": station_id,
                            "station_name": station_name,
                        },
                    )

            except (aiohttp.ClientError, ValueError):
                errors["base"] = "cannot_connect"

        # Step 2 schema: Real station configuration
        schema = vol.Schema({
            vol.Required("station_id"): str,
        })

        return self.async_show_form(
            step_id="real_station",
            data_schema=schema,
            errors=errors,
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
            # response.raise_for_status()
            json_data = await response.json()
            return json_data


class MeteoNetworkWeatherOptionsFlowHandler(OptionsFlow):
    """Reconfigure integration options.

    Available options are:
        * enable raw JSON attributes
        * expose all sensors
        * expose all sensors
    """

    @property
    def config_entry(self):
        """Return the config entry."""
        return self.hass.config_entries.async_get_entry(self.handler)

    async def async_step_init(self, user_input=None):
        """Manage the options."""

        if user_input is not None:
            return self.async_create_entry(title="Configure options", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_EXPOSE_EXTENDED_SENSORS,
                        default=self.config_entry.options.get(
                            CONF_EXPOSE_EXTENDED_SENSORS) or False
                    ): bool,
                    vol.Optional(
                        CONF_EXPOSE_STATION_ATTRS_AS_SENSORS,
                        default=self.config_entry.options.get(
                            CONF_EXPOSE_STATION_ATTRS_AS_SENSORS) or False
                    ): bool,
                    vol.Optional(
                        CONF_EXPOSE_RAW_DATA,
                        default=self.config_entry.options.get(
                            CONF_EXPOSE_RAW_DATA) or True  # fo backward compatibility
                    ): bool,
                }
            ),
        )

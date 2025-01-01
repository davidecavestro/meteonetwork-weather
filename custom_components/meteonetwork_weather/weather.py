"""Main entity for MeteoNetwork Weather component."""
from __future__ import annotations

from homeassistant.components.weather import WeatherEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up MeteoNetwork sensors from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([MeteoNetworkWeatherEntity(coordinator, config_entry)])


class MeteoNetworkWeatherEntity(CoordinatorEntity, WeatherEntity):
    """Representation of the MeteoNetwork weather entity."""

    def __init__(self, coordinator, config_entry):
        """Init the entity with config data."""
        super().__init__(coordinator)  # Initialize the CoordinatorEntity
        self.token = config_entry.data['token']
        self._attr_station_name = config_entry.data['station_name']
        self._attr_station_id = config_entry.data['station_id']

        self._attr_unique_id = f"weather.meteonetwork_{self._attr_station_id}"

        self._attr_has_entity_name = True
        self._attr_translation_key = 'meteonetwork'
        self._attr_attribution = "Weather data by MeteoNetwork"

        self._attr_translation_placeholders = {
            "station_name": self._attr_station_name,
        }

    @property
    def station_id(self):
        """Return the Station ID."""
        return self._attr_station_id

    @property
    def native_temperature(self):
        """Return the temperature from the sensor data."""
        return self.coordinator.data["sensors"].get("temperature")

    @property
    def humidity(self):
        """Return the humidity from the coordinator data."""
        return self.coordinator.data["sensors"].get("humidity")

    @property
    def native_visibility(self):
        """Return the visibility from the coordinator data."""
        return self.coordinator.data["sensors"].get("visibility")

    @property
    def native_precipitation(self):
        """Return the precipitation from the coordinator data."""
        return self.coordinator.data["sensors"].get("precipitation")

    @property
    def wind_bearing(self):
        """Return the wind bearing from the coordinator data."""
        return self.coordinator.data["sensors"].get("wind_bearing")

    @property
    def native_wind_speed(self):
        """Return the wind speed from the coordinator data."""
        return self.coordinator.data["sensors"].get("wind_speed")

    @property
    def native_wind_gust_speed(self):
        """Return the wind gust from the coordinator data."""
        return self.coordinator.data["sensors"].get("wind_gust")

    @property
    def uv_index(self):
        """Return the UV index from the coordinator data."""
        return self.coordinator.data["sensors"].get("uv_index")

    @property
    def native_dew_point(self):
        """Return the dew point from the coordinator data."""
        return self.coordinator.data["sensors"].get("dew_point")

    @property
    def native_pressure(self):
        """Return the pressure from the coordinator data."""
        return self.coordinator.data["sensors"].get("pressure")

    # @property
    # def extra_state_attributes(self):
    #     """Return additional attributes."""
    #     return {
    #         "station_id": self._attr_station_id,
    #         #         # "station_name": self.station_name,
    #         #         # "native_temperature": self.native_temperature,
    #         #         # "native_temperature_unit": "°C",
    #         #         # "native_precipitation": self.native_precipitation,
    #         #         # "native_precipitation_unit": "mm",
    #         #         # "native_wind_gust_speed": self.native_wind_gust_speed,
    #         #         # "native_wind_speed": self.native_wind_speed,
    #         #         # "native_wind_speed_unit": "km/h",
    #         #         # "native_pressure": self.native_pressure,
    #         #         # "native_pressure_unit": "hPa",
    #         #         # "humidity": self.humidity,
    #         #         # "uv_index": self.uv_index,
    #         #         # "native_dew_point": self.native_dew_point,
    #         #         # "wind_bearing": self.wind_bearing,
    #     }

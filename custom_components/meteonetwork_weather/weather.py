"""Main entity for MeteoNetwork Weather component."""
from __future__ import annotations

from homeassistant.components.weather import WeatherEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_EXPOSE_RAW_DATA

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
        self.config_entry = config_entry
        self._attr_station_name = config_entry.data.get('station_name')
        self._attr_station_id = config_entry.data.get('station_id')
        self._attr_latitude = config_entry.data.get('latitude')
        self._attr_longitude = config_entry.data.get('longitude')
        self._attr_station_type = config_entry.data.get('station_type')

        self._attr_unique_id = f"weather.meteonetwork_{
            self._attr_station_id}" if self._attr_station_type == "real" else f"weather.meteonetwork_{self._attr_latitude}_{self._attr_longitude}"

        self._attr_has_entity_name = True
        self._attr_translation_key = 'meteonetwork'
        self._attr_attribution = "Weather data by MeteoNetwork"

        self._attr_translation_placeholders = {
            "station_name": self._attr_station_name,
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.entry_id)},
            name="Meteonetwork Weather",
        )

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
    def daily_rain(self):
        """Return the daily rain from the coordinator data."""
        return self.coordinator.data["sensors"].get("daily_rain")

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

    @property
    def rain_rate(self):
        """Return the rain rate from the coordinator data."""
        return self.coordinator.data["sensors"].get("rain_rate")

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        raw_data = self.coordinator.data["sensors"].get("raw", {})
        expose = self.config_entry.options.get(CONF_EXPOSE_RAW_DATA)
        return {f"raw_{k}": v for k, v in raw_data.items()} if expose is None or expose else {}

    @property
    def state(self):
        """Return the state of the entity."""

        return self.coordinator.data["sensors"].get("condition") or "unknown"

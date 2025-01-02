"""Sensors for MeteoNetwork Weather component."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from .const import DOMAIN, SENSOR_TYPES

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up MeteoNetwork sensors from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [
        MeteoNetworkSensor(coordinator, config_entry, sensor_key)
        for sensor_key, sensor_data in SENSOR_TYPES.items()
    ]
    async_add_entities(sensors)

class MeteoNetworkSensor(CoordinatorEntity[DataUpdateCoordinator], SensorEntity):
    """Representation of an MeteoNetwork sensor."""

    def __init__(self, coordinator, config_entry, sensor_type):
        """Initialize the sensor."""
        super().__init__(coordinator)  # Initialize the CoordinatorEntity
        self.coordinator = coordinator
        self._attr_station_id = config_entry.data.get("station_id")
        self.station_name = config_entry.data.get("station_name")
        self.sensor_type = sensor_type
        self._attr_device_class = SENSOR_TYPES[sensor_type].get("device_class")
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type].get("unit")

        self._attr_unique_id = f"meteonetwork_{sensor_type}_{self._attr_station_id}"

        self._attr_has_entity_name = True
        self._attr_translation_key = sensor_type
        self._attr_translation_placeholders = {"station_name": self.station_name}

        self._data_key = SENSOR_TYPES[sensor_type]["data_key"]

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data["sensors"].get(self._data_key)

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_request_refresh()

    @property
    def station_id(self):
        """Return the Station ID of the sensor."""
        return self._attr_station_id

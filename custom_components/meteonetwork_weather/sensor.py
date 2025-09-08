"""Sensors for MeteoNetwork Weather component."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_registry import async_get as async_get_registry
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN, SENSOR_TYPES, CONF_EXPOSE_EXTENDED_SENSORS, CONF_EXPOSE_STATION_ATTRS_AS_SENSORS, SENSOR_TYPES_EXTENDED, SENSOR_TYPES_STATION

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up MeteoNetwork sensors from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Store async_add_entities for later use
    hass.data[DOMAIN][config_entry.entry_id] = {
        'add_entities': async_add_entities,
        "coordinator": coordinator
    }

    # Register update listener
    config_entry.async_on_unload(
        config_entry.add_update_listener(update_listener)
    )

    # Initial setup
    await _setup_sensors(hass, config_entry, coordinator, async_add_entities)

async def update_listener(hass, config_entry):
    """Handle options updates."""
    # Get async_add_entities from our stored data
    config = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities = config['add_entities']
    coordinator = config['coordinator']

    # Call our setup function
    await _setup_sensors(hass, config_entry, coordinator, async_add_entities)

async def _setup_sensors(hass, config_entry, coordinator, async_add_entities):
    """CONfigure sensors based on current options."""
    # Remove existing sensors
    for sensor in hass.data[DOMAIN][config_entry.entry_id].get('sensors', []):
        _LOGGER.warning("async_remove")
        await sensor.async_remove()

    extended = SENSOR_TYPES_EXTENDED if config_entry.options.get(
        CONF_EXPOSE_EXTENDED_SENSORS) else {}
    station = SENSOR_TYPES_STATION if config_entry.options.get(
        CONF_EXPOSE_STATION_ATTRS_AS_SENSORS) else {}
    sensor_types = {**SENSOR_TYPES, **extended, **station}

    registry = async_get_registry(hass)

    sensors = [
        MeteoNetworkSensor(coordinator, config_entry,
                           sensor_types[sensor_key], sensor_key)
        for sensor_key in sensor_types
    ]
    hass.data[DOMAIN][config_entry.entry_id]['sensors'] = sensors

    # Handle existing entity
    for it in sensors:
        await it.amend_from_registry(registry)

    async_add_entities(sensors)


class MeteoNetworkSensor(CoordinatorEntity[DataUpdateCoordinator], SensorEntity):
    """Representation of an MeteoNetwork sensor."""

    def __init__(self, coordinator, config_entry, sensor, sensor_key):
        """Initialize the sensor."""
        super().__init__(coordinator)  # Initialize the CoordinatorEntity
        self.coordinator = coordinator
        self._attr_station_id = config_entry.data.get("station_id")
        self.station_name = config_entry.data.get("station_name")
        self.sensor_key = sensor_key
        self._attr_device_class = sensor.get("device_class")
        self._attr_native_unit_of_measurement = sensor.get("unit")
        station_type = config_entry.data.get('station_type')
        self._attr_extra_state_attributes = {
            "latitude": config_entry.data.get('latitude'),
            "longitude": config_entry.data.get('longitude'),
            "station_type": station_type,
        }
        self._attr_unique_id = generate_id(config_entry, sensor_key)

        self._attr_has_entity_name = True
        self._attr_translation_key = sensor_key
        self._attr_translation_placeholders = {"station_name": self.station_name}

        self._data_key = sensor["data_key"]

    async def amend_from_registry(self, registry):
        """Check if this entity already exists in the registry."""
        existing_entity = registry.async_get(self._attr_unique_id)

        if existing_entity:
            # Reconnect to existing entity
            self.entity_id = existing_entity.entity_id
            self._attr_device_id = existing_entity.device_id
        else:
            # New entity
            self.entity_id = None
            self._attr_device_id = None

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

def generate_id(config_entry, sensor_key):
    """Return the ID generated for the sensor."""
    station_id = config_entry.data.get("station_id")
    station_type = config_entry.data.get('station_type')
    latitude = config_entry.data.get("latitude")
    longitude = config_entry.data.get("longitude")

    return f"meteonetwork_{sensor_key}_{station_id}" if station_type == "real" else f"weather.meteonetwork_{
        sensor_key}_{latitude}_{longitude}"

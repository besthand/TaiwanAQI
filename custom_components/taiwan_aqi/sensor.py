import logging
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# 定義不同的感測器類型
SENSOR_TYPES = {
    "aqi": "AQI",
    "pm2.5": "PM2.5",
    "pm10": "PM10",
    "o3": "O3",
    "no2": "NO2",
    "so2": "SO2",
    "co": "CO"
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Taiwan AQI sensors from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    # 為每個定義的感測器類型建立對應的感測器
    entities = [AQISensor(coordinator, sensor_type) for sensor_type in SENSOR_TYPES]
    async_add_entities(entities)

class AQISensor(SensorEntity):
    """Representation of a Taiwan AQI sensor."""

    def __init__(self, coordinator, sensor_type):
        """Initialize the AQI sensor."""
        self.coordinator = coordinator
        self.sensor_type = sensor_type
        self._attr_name = f"{SENSOR_TYPES[sensor_type]} Sensor ({coordinator.config_entry.data['station']})"
        self._attr_unique_id = f"taiwan_aqi_{sensor_type}_{coordinator.config_entry.data['station']}"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(self.sensor_type)
        return None

    @property
    def extra_state_attributes(self):
        """Return extra state attributes."""
        if not self.coordinator.data:
            return {}
        return {
            "station": self.coordinator.config_entry.data["station"],
            "last_update": self.coordinator.data.get("publishtime")
        }

    async def async_update(self):
        """Request an update from the coordinator."""
        await self.coordinator.async_request_refresh()

    async def async_update_aqi_data(self):
        """Service handler to update AQI data."""
        await self.async_update()
        _LOGGER.info(f"AQI data manually updated for {self.coordinator.config_entry.data['station']}")

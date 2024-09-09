import logging
import requests
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.service import async_register_admin_service
from .const import DOMAIN, API_URL, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Taiwan AQI from a config entry."""
    coordinator = AQICoordinator(hass, config_entry)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    # 初始化感測器平台
    await hass.config_entries.async_forward_entry_setups(config_entry, ["sensor"])

    # 註冊全局服務，讓所有感測器可以手動更新
    hass.services.async_register(DOMAIN, "update_aqi_data", service_update_aqi_data)

    # 立即取得最新資料
    await coordinator.async_refresh()

    return True

async def service_update_aqi_data(service_call):
    """Handle the service call to update AQI data for all entities."""
    _LOGGER.info("Manually triggering AQI data update for all sensors.")

    # 更新所有已註冊的感測器的數據 
    entities = []
    for entity in service_call.context:
        if isinstance(entity, AQISensor):
            entities.append(entity)
    
    for entity in entities:
        await entity.async_update_aqi_data()

class AQICoordinator(DataUpdateCoordinator):
    """Class to manage fetching AQI data from the API."""

    def __init__(self, hass, config_entry):
        """Initialize the AQI coordinator."""
        self.hass = hass
        self.config_entry = config_entry
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            station = self.config_entry.data["station"]
            api_key = self.config_entry.data["api_key"]  # 使用 config_entry 中的 API Key
            response = await self.hass.async_add_executor_job(self._fetch_data, station, api_key)
            return response
        except Exception as err:
            _LOGGER.error(f"Error fetching AQI data for {station}: {err}")
            raise UpdateFailed(f"Failed to fetch data: {err}")

    def _fetch_data(self, station, api_key):
        """Fetch the AQI data from the API."""
        try:
            params = {
                "language": "zh",
                "api_key": api_key
            }
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            # 過濾出選定的測站資料
            for record in data["records"]:
                if record["sitename"] == station:
                    return record
            return None
        except Exception as e:
            _LOGGER.error(f"Error while fetching data from API for station {station}: {e}")
            raise

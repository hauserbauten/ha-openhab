"""Data update coordinator for integration blueprint."""
from __future__ import annotations
from typing import Any
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ApiClientException, OpenHabApiClient
from .const import DATA_COORDINATOR_UPDATE_INTERVAL, DOMAIN, LOGGER


class OpenHabDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, api: OpenHabApiClient) -> None:
        """Initialize."""
        self.api = api
        self.platforms: list[str] = []

        super().__init__(
            hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=DATA_COORDINATOR_UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            return await self.api.async_get_data()
        except ApiClientException as exception:
            raise UpdateFailed(exception) from exception

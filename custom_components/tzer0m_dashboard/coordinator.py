"""DataUpdateCoordinator for the HADashboard integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_STATUS_PATH, CONF_API_KEY, CONF_HOST, DEFAULT_SCAN_INTERVAL_SECONDS, DOMAIN

_LOGGER = logging.getLogger(__name__)


class DashboardUpdateCoordinator(DataUpdateCoordinator[dict[str, dict[str, Any]]]):
    """Polls the dashboard's status endpoint and exposes results keyed by service name."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialise the coordinator with the host and API key from the config entry."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL_SECONDS),
        )

        self.Host: str = entry.data[CONF_HOST].rstrip("/")
        self.ApiKey: str = entry.data[CONF_API_KEY]
        self.Session: aiohttp.ClientSession = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict[str, dict[str, Any]]:
        """Fetch the latest status payload and key it by service name for entity lookup."""
        url = f"{self.Host}{API_STATUS_PATH}"
        headers = {"X-Api-Key": self.ApiKey}

        try:
            async with self.Session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 401:
                    raise UpdateFailed("Dashboard rejected the configured API key")

                response.raise_for_status()
                payload: list[dict[str, Any]] = await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with dashboard: {err}") from err

        return {service["name"]: service for service in payload}
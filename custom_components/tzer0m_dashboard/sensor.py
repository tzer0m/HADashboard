"""Sensor platform for HADashboard, one entity per service exposing deploy badge status."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DashboardUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up one deploy status sensor per service that has a deploy badge configured."""
    coordinator: DashboardUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        DeployStatusSensor(coordinator, entry, service_name)
        for service_name, service in coordinator.data.items()
        if service.get("deployBadge") is not None
    ]

    async_add_entities(entities)


class DeployStatusSensor(CoordinatorEntity[DashboardUpdateCoordinator], SensorEntity):
    """Reports the latest GitHub Actions deploy status for a single service."""

    _attr_has_entity_name = True
    _attr_translation_key = "deploy_status"

    def __init__(self, coordinator: DashboardUpdateCoordinator, entry: ConfigEntry, service_name: str) -> None:
        """Initialise the deploy status sensor for a single service."""
        super().__init__(coordinator)

        self.ServiceName: str = service_name
        self._attr_unique_id = f"{entry.entry_id}_{service_name}_deploy_status"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
        )

    @property
    def native_value(self) -> str | None:
        """Return the deploy badge message, e.g. 'passing', 'failing', 'running', 'unknown'."""
        service = self.coordinator.data.get(self.ServiceName)

        if service is None or service.get("deployBadge") is None:
            return None

        return str(service["deployBadge"]["message"])

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Expose the badge colour as an attribute, for use in custom card styling."""
        service = self.coordinator.data.get(self.ServiceName)

        if service is None or service.get("deployBadge") is None:
            return {}

        return {"color": str(service["deployBadge"]["color"])}

    @property
    def name(self) -> str:
        """Return the display name for this entity, used alongside the device name."""
        return f"{self.ServiceName} Deploy"
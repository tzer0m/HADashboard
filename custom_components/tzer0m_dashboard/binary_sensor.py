"""Binary sensor platform for HADashboard, one entity per monitored service."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
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
    """Set up one binary sensor per service found in the coordinator's data."""
    coordinator: DashboardUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        ServiceOnlineBinarySensor(coordinator, entry, service_name)
        for service_name in coordinator.data
    ]

    async_add_entities(entities)


class ServiceOnlineBinarySensor(CoordinatorEntity[DashboardUpdateCoordinator], BinarySensorEntity):
    """Reports whether a single dashboard-monitored service is currently online."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True
    _attr_translation_key = "service_online"

    def __init__(self, coordinator: DashboardUpdateCoordinator, entry: ConfigEntry, service_name: str) -> None:
        """Initialise the binary sensor for a single service."""
        super().__init__(coordinator)

        self.ServiceName: str = service_name
        self._attr_unique_id = f"{entry.entry_id}_{service_name}_online"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
        )

    @property
    def is_on(self) -> bool | None:
        """Return True if the service's last health check reported online."""
        service = self.coordinator.data.get(self.ServiceName)

        if service is None or service.get("health") is None:
            return None

        return bool(service["health"]["isOnline"])

    @property
    def name(self) -> str:
        """Return the display name for this entity, used alongside the device name."""
        return self.ServiceName
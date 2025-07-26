"""Support for OctoPrint text entities."""

from __future__ import annotations

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import OctoprintDataUpdateCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up OctoPrint text entities."""
    coordinator: OctoprintDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]["coordinator"]
    device_id = config_entry.unique_id
    assert device_id is not None

    async_add_entities(
        [
            OctoprintToolTempText(coordinator, device_id),
            OctoprintBedTempText(coordinator, device_id),
            OctoprintZMoveText(coordinator, device_id),
            OctoprintPrinterProfileText(coordinator, device_id),
            OctoprintSerialPortText(coordinator, device_id),
            OctoprintBaudRateText(coordinator, device_id),
        ]
    )


class OctoprintTextBase(
    CoordinatorEntity[OctoprintDataUpdateCoordinator], TextEntity
):
    """Base class for OctoPrint text entities."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        text_type: str,
        device_id: str,
        initial_value: str,
    ) -> None:
        """Initialize a new OctoPrint text entity."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"OctoPrint {text_type}"
        self._attr_unique_id = f"{text_type.lower().replace(' ', '_')}-{device_id}"
        self._attr_device_info = coordinator.device_info
        self._attr_native_value = initial_value

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_set_value(self, value: str) -> None:
        """Set the text value."""
        self._attr_native_value = value
        self.async_write_ha_state()


class OctoprintToolTempText(OctoprintTextBase):
    """Text entity for tool temperature setting."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialize tool temperature text entity."""
        super().__init__(coordinator, "Tool Temperature", device_id, "215")
        self._attr_pattern = r"^\d{1,3}$"
        self._attr_mode = "text"


class OctoprintBedTempText(OctoprintTextBase):
    """Text entity for bed temperature setting."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialize bed temperature text entity."""
        super().__init__(coordinator, "Bed Temperature", device_id, "60")
        self._attr_pattern = r"^\d{1,3}$"
        self._attr_mode = "text"


class OctoprintZMoveText(OctoprintTextBase):
    """Text entity for Z-axis move distance."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialize Z move text entity."""
        super().__init__(coordinator, "Z Move Distance", device_id, "20")
        self._attr_pattern = r"^-?\d{1,3}(\.\d{1,2})?$"
        self._attr_mode = "text"


class OctoprintPrinterProfileText(OctoprintTextBase):
    """Text entity for printer profile setting."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialize printer profile text entity."""
        super().__init__(coordinator, "Printer Profile", device_id, "Prusa")
        self._attr_mode = "text"


class OctoprintSerialPortText(OctoprintTextBase):
    """Text entity for serial port setting."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialize serial port text entity."""
        super().__init__(coordinator, "Serial Port", device_id, "/dev/ttyACM0")
        self._attr_mode = "text"


class OctoprintBaudRateText(OctoprintTextBase):
    """Text entity for baud rate setting."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialize baud rate text entity."""
        super().__init__(coordinator, "Baud Rate", device_id, "115200")
        self._attr_pattern = r"^\d{4,7}$"
        self._attr_mode = "text"
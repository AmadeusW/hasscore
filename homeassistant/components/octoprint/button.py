"""Support for Octoprint buttons."""

from pyoctoprintapi import OctoprintClient, OctoprintPrinterInfo

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import OctoprintDataUpdateCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Octoprint control buttons."""
    coordinator: OctoprintDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]["coordinator"]
    client: OctoprintClient = hass.data[DOMAIN][config_entry.entry_id]["client"]
    device_id = config_entry.unique_id
    assert device_id is not None

    async_add_entities(
        [
            OctoprintResumeJobButton(coordinator, device_id, client),
            OctoprintPauseJobButton(coordinator, device_id, client),
            OctoprintStopJobButton(coordinator, device_id, client),
            OctoprintShutdownSystemButton(coordinator, device_id, client),
            OctoprintRebootSystemButton(coordinator, device_id, client),
            OctoprintRestartOctoprintButton(coordinator, device_id, client),
            OctoprintSetToolTempButton(coordinator, device_id, client),
            OctoprintSetBedTempButton(coordinator, device_id, client),
            OctoprintMoveZAxisButton(coordinator, device_id, client),
            OctoprintConnectPrinterButton(coordinator, device_id, client),
        ]
    )


class OctoprintPrinterButton(
    CoordinatorEntity[OctoprintDataUpdateCoordinator], ButtonEntity
):
    """Represent an OctoPrint binary sensor."""

    client: OctoprintClient

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        button_type: str,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator)
        self.client = client
        self._device_id = device_id
        self._attr_name = f"OctoPrint {button_type}"
        self._attr_unique_id = f"{button_type}-{device_id}"
        self._attr_device_info = coordinator.device_info

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data["printer"]


class OctoprintSystemButton(
    CoordinatorEntity[OctoprintDataUpdateCoordinator], ButtonEntity
):
    """Represent an OctoPrint binary sensor."""

    client: OctoprintClient

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        button_type: str,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator)
        self.client = client
        self._device_id = device_id
        self._attr_name = f"OctoPrint {button_type}"
        self._attr_unique_id = f"{button_type}-{device_id}"
        self._attr_device_info = coordinator.device_info

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success


class OctoprintPauseJobButton(OctoprintPrinterButton):
    """Pause the active job."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator, "Pause Job", device_id, client)

    async def async_press(self) -> None:
        """Handle the button press."""
        printer: OctoprintPrinterInfo = self.coordinator.data["printer"]

        if printer.state.flags.printing:
            await self.client.pause_job()
        elif not printer.state.flags.paused and not printer.state.flags.pausing:
            raise InvalidPrinterState("Printer is not printing")


class OctoprintResumeJobButton(OctoprintPrinterButton):
    """Resume the active job."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator, "Resume Job", device_id, client)

    async def async_press(self) -> None:
        """Handle the button press."""
        printer: OctoprintPrinterInfo = self.coordinator.data["printer"]

        if printer.state.flags.paused:
            await self.client.resume_job()
        elif not printer.state.flags.printing and not printer.state.flags.resuming:
            raise InvalidPrinterState("Printer is not currently paused")


class OctoprintStopJobButton(OctoprintPrinterButton):
    """Resume the active job."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator, "Stop Job", device_id, client)

    async def async_press(self) -> None:
        """Handle the button press."""
        printer: OctoprintPrinterInfo = self.coordinator.data["printer"]

        if printer.state.flags.printing or printer.state.flags.paused:
            await self.client.cancel_job()


class OctoprintShutdownSystemButton(OctoprintSystemButton):
    """Shutdown the system."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator, "Shutdown System", device_id, client)

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.client.shutdown()


class OctoprintRebootSystemButton(OctoprintSystemButton):
    """Reboot the system."""

    _attr_device_class = ButtonDeviceClass.RESTART

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator, "Reboot System", device_id, client)

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.client.reboot_system()


class OctoprintRestartOctoprintButton(OctoprintSystemButton):
    """Restart Octoprint."""

    _attr_device_class = ButtonDeviceClass.RESTART

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator, "Restart Octoprint", device_id, client)

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.client.restart()


class OctoprintSetToolTempButton(OctoprintPrinterButton):
    """Set tool temperature using configurable value."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator, "Set Tool Temperature", device_id, client)

    async def async_press(self) -> None:
        """Handle the button press."""
        # Get the temperature value from the text entity
        text_entity_id = f"text.octoprint_tool_temperature"
        text_state = self.hass.states.get(text_entity_id)
        
        if text_state and text_state.state.isdigit():
            temperature = int(text_state.state)
        else:
            temperature = 215  # Default fallback
            
        await self.client.set_tool_temperature(temperature, tool="tool0")


class OctoprintSetBedTempButton(OctoprintPrinterButton):
    """Set bed temperature using configurable value."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator, "Set Bed Temperature", device_id, client)

    async def async_press(self) -> None:
        """Handle the button press."""
        # Get the temperature value from the text entity
        text_entity_id = f"text.octoprint_bed_temperature"
        text_state = self.hass.states.get(text_entity_id)
        
        if text_state and text_state.state.isdigit():
            temperature = int(text_state.state)
        else:
            temperature = 60  # Default fallback
            
        await self.client.set_bed_temperature(temperature)


class OctoprintMoveZAxisButton(OctoprintPrinterButton):
    """Move tool in Z axis using configurable distance."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator, "Move Z Axis", device_id, client)

    async def async_press(self) -> None:
        """Handle the button press."""
        # Get the Z move distance from the text entity
        text_entity_id = f"text.octoprint_z_move_distance"
        text_state = self.hass.states.get(text_entity_id)
        
        if text_state and text_state.state.replace('.', '').replace('-', '').isdigit():
            z_distance = float(text_state.state)
        else:
            z_distance = 20.0  # Default fallback
            
        await self.client.issue_tool_command({"command": "jog", "z": z_distance})


class OctoprintConnectPrinterButton(OctoprintSystemButton):
    """Connect to printer using configurable settings."""

    def __init__(
        self,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        client: OctoprintClient,
    ) -> None:
        """Initialize a new OctoPrint button."""
        super().__init__(coordinator, "Connect Printer", device_id, client)

    async def async_press(self) -> None:
        """Handle the button press."""
        # Get connection settings from text entities
        profile_entity_id = f"text.octoprint_printer_profile"
        port_entity_id = f"text.octoprint_serial_port"
        baud_entity_id = f"text.octoprint_baud_rate"
        
        profile_state = self.hass.states.get(profile_entity_id)
        port_state = self.hass.states.get(port_entity_id)
        baud_state = self.hass.states.get(baud_entity_id)
        
        printer_profile = profile_state.state if profile_state else "Prusa"
        port = port_state.state if port_state else "/dev/ttyACM0"
        baud_rate = int(baud_state.state) if baud_state and baud_state.state.isdigit() else 115200
        
        await self.client.connect(
            printer_profile=printer_profile,
            port=port,
            baud_rate=baud_rate
        )


class InvalidPrinterState(HomeAssistantError):
    """Service attempted in invalid state."""

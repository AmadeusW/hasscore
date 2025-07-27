# OctoPrint Actions Documentation

This document provides comprehensive information about the custom actions (services) available in the OctoPrint integration for Home Assistant.

## Table of Contents

1. [Available Services](#available-services)
2. [Using Services from the UI](#using-services-from-the-ui)
3. [Using Services in Scripts and Automations](#using-services-in-scripts-and-automations)
4. [Complete Service API Reference](#complete-service-api-reference)
5. [Parameter Reference](#parameter-reference)

## Available Services

The OctoPrint integration provides the following custom services:

- `octoprint.printer_connect` - Connect to a printer
- `octoprint.set_tool_temperature` - Set hotend temperature
- `octoprint.set_bed_temperature` - Set heated bed temperature
- `octoprint.move_tool` - Move tool by relative offsets
- `octoprint.set_position` - Move tool to absolute positions

## Using Services from the UI

### Method 1: Developer Tools

1. Navigate to **Developer Tools** → **Services**
2. Select the desired service from the **Service** dropdown (e.g., `octoprint.set_tool_temperature`)
3. Fill in the required parameters in the **Service Data** section
4. Click **Call Service**

**Example - Setting Tool Temperature:**
```yaml
service: octoprint.set_tool_temperature
data:
  device_id: "12345abcde"
  tool_temperature: 215
```

### Method 2: Creating Dashboard Actions

You can create buttons on your dashboard to trigger these services:

```yaml
type: button
name: Heat Hotend
tap_action:
  action: call-service
  service: octoprint.set_tool_temperature
  data:
    device_id: "12345abcde"
    tool_temperature: 215
```

### Method 3: Using the Services Panel

1. Go to **Settings** → **Automations & Scenes** → **Scripts**
2. Create a new script
3. Add an action and select **Call Service**
4. Choose your OctoPrint service and configure parameters

## Using Services in Scripts and Automations

### Script Examples

#### Heat Up Printer Script
```yaml
alias: "Heat Up Printer"
sequence:
  - service: octoprint.set_bed_temperature
    data:
      device_id: "12345abcde"
      bed_temperature: 60
  - service: octoprint.set_tool_temperature
    data:
      device_id: "12345abcde" 
      tool_temperature: 215
  - delay: "00:05:00"  # Wait 5 minutes
  - service: octoprint.printer_connect
    data:
      device_id: "12345abcde"
      profile_name: "Prusa"
      port: "/dev/ttyACM0"
      baudrate: 115200
```

#### Tool Movement Script
```yaml
alias: "Move Tool to Corner"
sequence:
  - service: octoprint.set_position
    data:
      device_id: "12345abcde"
      x_position: 0
      y_position: 0
      z_position: 10
```

#### Relative Movement Script
```yaml
alias: "Adjust Z Height"
sequence:
  - service: octoprint.move_tool
    data:
      device_id: "12345abcde"
      z_offset: 5.0  # Move up 5mm
```

### Automation Examples

#### Temperature Control Automation
```yaml
alias: "Auto Heat Based on Time"
trigger:
  - platform: time
    at: "08:00:00"
condition:
  - condition: state
    entity_id: binary_sensor.workday_sensor
    state: "on"
action:
  - service: octoprint.set_tool_temperature
    data:
      device_id: "{{ states.device_tracker.octoprint_device.attributes.device_id }}"
      tool_temperature: 200
  - service: octoprint.set_bed_temperature
    data:
      device_id: "{{ states.device_tracker.octoprint_device.attributes.device_id }}"
      bed_temperature: 50
```

#### Print Start Sequence
```yaml
alias: "Print Start Sequence"
trigger:
  - platform: state
    entity_id: sensor.octoprint_current_state
    to: "Printing"
action:
  - service: octoprint.set_position
    data:
      device_id: "12345abcde"
      z_position: 0.3  # Set initial layer height
```

## Complete Service API Reference

### octoprint.printer_connect

**Description:** Connects the OctoPrint server to a 3D printer.

**Parameters:**
- `device_id` (required): The device ID of the OctoPrint server
- `profile_name` (optional): Printer profile name to use
- `port` (optional): Serial port to connect to
- `baudrate` (optional): Communication baud rate

**Example:**
```yaml
service: octoprint.printer_connect
data:
  device_id: "12345abcde"
  profile_name: "Prusa"
  port: "/dev/ttyACM0"
  baudrate: 115200
```

### octoprint.set_tool_temperature

**Description:** Sets the target temperature for the printer's hotend/tool.

**Parameters:**
- `device_id` (required): The device ID of the OctoPrint server
- `tool_temperature` (required): Target temperature in Celsius (0-400°C)

**Example:**
```yaml
service: octoprint.set_tool_temperature
data:
  device_id: "12345abcde"
  tool_temperature: 215
```

### octoprint.set_bed_temperature

**Description:** Sets the target temperature for the printer's heated bed.

**Parameters:**
- `device_id` (required): The device ID of the OctoPrint server  
- `bed_temperature` (required): Target temperature in Celsius (0-150°C)

**Example:**
```yaml
service: octoprint.set_bed_temperature
data:
  device_id: "12345abcde"
  bed_temperature: 60
```

### octoprint.move_tool

**Description:** Moves the printer tool by relative offsets in millimeters.

**Parameters:**
- `device_id` (required): The device ID of the OctoPrint server
- `x_offset` (optional): Distance to move in X direction (-500 to 500mm)
- `y_offset` (optional): Distance to move in Y direction (-500 to 500mm) 
- `z_offset` (optional): Distance to move in Z direction (-500 to 500mm)

**Notes:**
- At least one offset parameter must be provided
- Positive values: X=right, Y=away from origin, Z=up
- Negative values: X=left, Y=toward origin, Z=down

**Examples:**
```yaml
# Move diagonally up and right
service: octoprint.move_tool
data:
  device_id: "12345abcde"
  x_offset: 10.5
  y_offset: 10.5
  z_offset: 5.0

# Move only in Z direction
service: octoprint.move_tool
data:
  device_id: "12345abcde"
  z_offset: -2.0  # Move down 2mm
```

### octoprint.set_position

**Description:** Moves the printer tool to absolute positions after homing the specified axes.

**Parameters:**
- `device_id` (required): The device ID of the OctoPrint server
- `x_position` (optional): Absolute X position in millimeters (0-500mm)
- `y_position` (optional): Absolute Y position in millimeters (0-500mm)
- `z_position` (optional): Absolute Z position in millimeters (0-500mm)

**Notes:**
- At least one position parameter must be provided
- Specified axes will be homed before moving to the target position
- Use with caution as homing will move the tool to endstops first

**Examples:**
```yaml
# Move to center of 200x200 bed, 10mm high
service: octoprint.set_position
data:
  device_id: "12345abcde"
  x_position: 100
  y_position: 100
  z_position: 10

# Set only Z height (homes Z axis first)
service: octoprint.set_position
data:
  device_id: "12345abcde"
  z_position: 0.3
```

## Parameter Reference

### Common Parameters

#### device_id
- **Type:** String
- **Required:** Yes (all services)
- **Description:** The unique device identifier for your OctoPrint server
- **How to find:** Go to Settings → Devices & Services → OctoPrint → [Your Device] and copy the device ID

### Temperature Parameters

#### tool_temperature
- **Type:** Integer
- **Required:** Yes (set_tool_temperature)
- **Range:** 0-400°C
- **Description:** Target temperature for the hotend/extruder
- **Safety note:** Ensure temperature is appropriate for your filament type

#### bed_temperature  
- **Type:** Integer
- **Required:** Yes (set_bed_temperature)
- **Range:** 0-150°C
- **Description:** Target temperature for the heated bed
- **Safety note:** Ensure temperature is appropriate for your filament and bed surface

### Movement Parameters

#### Relative Movement (move_tool)
- **x_offset, y_offset, z_offset**
- **Type:** Float
- **Required:** At least one must be provided
- **Range:** -500 to 500mm
- **Step:** 0.1mm precision
- **Description:** Distance to move from current position

#### Absolute Movement (set_position)
- **x_position, y_position, z_position**
- **Type:** Float  
- **Required:** At least one must be provided
- **Range:** 0 to 500mm
- **Step:** 0.1mm precision
- **Description:** Target absolute position (after homing)

### Connection Parameters

#### profile_name
- **Type:** String
- **Required:** No
- **Description:** Name of the printer profile configured in OctoPrint
- **Default:** Uses OctoPrint's default profile

#### port
- **Type:** String
- **Required:** No  
- **Description:** Serial port device path (e.g., "/dev/ttyACM0", "COM3")
- **Default:** Uses OctoPrint's configured port

#### baudrate
- **Type:** Integer
- **Required:** No
- **Options:** 9600, 19200, 38400, 57600, 115200, 230400, 250000
- **Description:** Serial communication baud rate
- **Default:** Uses OctoPrint's configured baud rate

## Error Handling

Services will return errors in the following cases:

- **Invalid device_id:** Device not found or not an OctoPrint device
- **Parameter out of range:** Temperature or movement values outside safe limits
- **Printer offline:** Printer not connected (for printer-specific commands)
- **OctoPrint unreachable:** Network or authentication issues

Check the Home Assistant logs for detailed error messages when services fail.

## Integration with Home Assistant Features

### Template Support

You can use templates in service calls:

```yaml
service: octoprint.set_tool_temperature
data:
  device_id: "12345abcde"
  tool_temperature: "{{ states('input_number.target_temp') | int }}"
```

### Input Helpers

Create input helpers to make services user-controllable:

```yaml
# configuration.yaml
input_number:
  target_hotend_temp:
    name: "Target Hotend Temperature"
    min: 0
    max: 300
    step: 5
    unit_of_measurement: "°C"
    
  z_offset:
    name: "Z Offset"
    min: -10
    max: 10
    step: 0.1
    unit_of_measurement: "mm"
```

Then use in automations:
```yaml
service: octoprint.set_tool_temperature
data:
  device_id: "12345abcde"
  tool_temperature: "{{ states('input_number.target_hotend_temp') | int }}"
```
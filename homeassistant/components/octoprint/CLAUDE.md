# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## OctoPrint Integration Architecture

This is the Home Assistant OctoPrint integration located in `homeassistant/components/octoprint/`. The integration connects to OctoPrint 3D printer servers and provides monitoring and control capabilities.

### Key Components

- **Data Coordinator** (`coordinator.py`): Manages data updates from OctoPrint servers using a 30-second polling interval
- **Config Flow** (`config_flow.py`): Handles discovery (SSDP/Zeroconf) and manual configuration with automatic API key retrieval
- **Platform Files**: Implements sensors (`sensor.py`), binary sensors (`binary_sensor.py`), buttons (`button.py`), and camera (`camera.py`)
- **Services**: Provides `printer_connect` service for connecting to printers

### API Client Library

The integration uses `pyoctoprintapi==0.1.14` (OctoprintClient class) for communication with OctoPrint servers. Key methods include:
- `get_job_info()` - Job status and progress
- `get_printer_info()` - Printer temperature and state  
- `connect()` - Connect to printer with profile/port/baudrate
- `request_app_key()` - Automatic API key generation
- `issue_tool_command()` - Move the tool
- `set_bed_temperature()` - Set the bed temperature
- `issue_connection_command()` - Issue a connection command
- `issue_job_command()` - Issue a job command, that's used in the Button entities.

### Configuration

- **Discovery**: Supports SSDP and Zeroconf automatic discovery
- **Manual Setup**: Host, port, path, SSL settings, and API key
- **Authentication**: Uses application API keys with automatic request flow
- **Device Registry**: Creates devices with configuration URLs

### Entity Types

- **Sensors**: Temperatures, job status, time remaining/elapsed, job percentage
- **Binary Sensors**: Printing status, printing errors
- **Buttons**: Connect/disconnect actions
- **Camera**: Webcam stream access

### Error Handling

- **Printer Offline**: Gracefully handles `PrinterOffline` exceptions by preserving last known state
- **Auth Failures**: Triggers reauth flow for `UnauthorizedException`
- **Config Entry Auth**: Uses `ConfigEntryAuthFailed` for authentication issues

### Development Notes

- All platforms use the shared data coordinator pattern
- Device info includes manufacturer "OctoPrint" and configuration URL
- Service calls validate device IDs through device registry
- SSL context handling supports both verified and unverified connections
- Session management with proper cleanup on unload
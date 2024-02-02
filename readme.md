# OSC Repeater

This Python script creates an OSC (Open Sound Control) repeater server that listens for OSC messages and forwards them to a specified address. It uses the `pythonosc` library for handling OSC messages, `netifaces` for network interface information, and `tkinter` for the GUI.

## Features

- Select the IP address from the available network interfaces.
- Specify the input and output ports for the OSC server.
- Start and stop the OSC server.
- Save and load the server configuration (IP address, input port, output port) to/from a JSON file.
- Toggle a terminal window that displays received OSC messages.

## Usage

1. Run the script: `python osc-repeater.py`
2. The GUI will appear. Select an IP address from the list and click "Select IP".
3. Enter the input and output ports.
4. Click "Start Server" to start the OSC server.
5. The server will listen for OSC messages on the input port and forward them to the selected IP address on the output port.
6. Click "Stop Server" to stop the server.
7. Use "Save Config" to save the current configuration to a JSON file, and "Load Config" to load a configuration from a JSON file.
8. Click "Toggle Terminal" to open/close a terminal window that displays received OSC messages.

## Requirements

- Python 3
- `pythonosc` library
- `netifaces` library
- `tkinter` library

## Installation

1. Clone this repository.
2. Install the required Python libraries: `pip install pythonosc netifaces tkinter`

## Note

This script is intended for use in a local network. Be aware of the security implications if you plan to use it in a different context.
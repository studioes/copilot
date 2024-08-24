# Flask Machine Management Application

This is a Flask-based web application that allows you to manage machines and send Wake-on-LAN (WoL) magic packets to wake them up. The application provides functionalities to register machines, list all registered machines, edit machine details, delete machines, and send magic packets to wake up machines by their MAC addresses.

## Features

- **Register Machine**: Register a machine with its name and MAC address.
- **List Machines**: View a list of all registered machines.
- **Edit Machine**: Edit the details of a registered machine.
- **Delete Machine**: Delete a registered machine.
- **Send Magic Packet**: Send a Wake-on-LAN magic packet to wake up a machine by its MAC address.

## Routes

- `/`: Lists all available routes in the application.
- `/mac_regist`: Register a machine by providing its name and MAC address.
- `/wakeup_by_mac`: Send a magic packet to wake up a machine by its MAC address.
- `/edit_machine/<int:id>`: Edit the details of a registered machine.
- `/delete_machine/<int:id>`: Delete a registered machine.
- `/machines`: List all registered machines.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/flask-machine-management.git
    cd flask-machine-management
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    python main.py
    ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Use the provided forms to register machines, edit details, delete machines, and send magic packets.

## Code Overview

### `main.py`

- **Database Setup**: Configures and initializes the SQLite database using SQLAlchemy.
- **Machine Model**: Defines the `Machine` model with `id`, `name`, and `mac_address` fields.
- **Routes**:
  - `/`: Lists all available routes.
  - `/mac_regist`: Handles machine registration.
  - `/wakeup_by_mac`: Handles sending magic packets.
  - `/edit_machine/<int:id>`: Handles editing machine details.
  - `/delete_machine/<int:id>`: Handles deleting a machine.
  - `/machines`: Lists all registered machines.
- **Magic Packet Function**: Defines the `send_magic_packet` function to send a Wake-on-LAN magic packet.

### Example Code Snippet

```python
# Function to send a magic packet to wake up a machine by MAC address
def send_magic_packet(mac_address):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the socket options to allow broadcasting
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Create the magic packet
    mac_bytes = bytes.fromhex(mac_address.replace(':', ''))
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    # Send the magic packet to the broadcast address
    sock.sendto(magic_packet, ('<broadcast>', 9))

    # Close the socket
    sock.close()
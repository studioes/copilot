from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from getmac import get_mac_address
import socket

# Define the base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize the Flask application
app = Flask(__name__)
# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
# Initialize SQLAlchemy with the Flask app and the base class
db = SQLAlchemy(app, model_class=Base)

# Define the Machine model
class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    mac_address = db.Column(db.String(17), unique=True, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Function to list all routes in the application
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = (rule.endpoint, rule.rule, methods)
        output.append(line)
    return output

# Route to display all routes as links
@app.route('/', methods=['GET'])
def list_routes_page():
    routes = list_routes()
    links = [f'<a href="{rule}">{endpoint}</a> [{methods}]' for endpoint, rule, methods in routes]
    return '<br>'.join(links)

# Route to register a MAC address for a machine
@app.route('/mac_regist', methods=['GET', 'POST'])
def register_mac_address():
    if request.method == 'POST':
        machine_name = request.form['machine_name']
        mac_address = get_mac_address(hostname=machine_name)
        
        if mac_address:
            # Save the machine and MAC address to the database
            machine = Machine(name=machine_name, mac_address=mac_address)
            db.session.add(machine)
            db.session.commit()
            return 'MAC address registered for machine: ' + machine_name
        else:
            return 'Could not find MAC address for machine: ' + machine_name
    else:
        return '''
        <form method="POST">
            <label for="machine_name">Enter Machine Name:</label>
            <input type="text" id="machine_name" name="machine_name">
            <input type="submit" value="Register MAC Address">
        </form>
        '''

# Route to send a magic packet to wake up a machine by MAC address
@app.route('/wakeup_by_mac', methods=['GET', 'POST'])
def send_magic_packet_route():
    if request.method == 'POST':
        mac_address = request.form['mac_address']
        # Call the send_magic_packet function with the provided MAC address
        send_magic_packet(mac_address)
        return 'Magic packet sent to MAC address: ' + mac_address
    else:
        return '''
        <form method="POST">
            <label for="mac_address">Enter MAC address:</label>
            <input type="text" id="mac_address" name="mac_address">
            <input type="submit" value="Send Magic Packet">
        </form>
        '''

# Route to edit a machine's details
@app.route('/edit_machine/<int:id>', methods=['GET', 'POST'])
def edit_machine(id):
    machine = Machine.query.get_or_404(id)
    if request.method == 'POST':
        machine.name = request.form['machine_name']
        machine.mac_address = request.form['mac_address']
        db.session.commit()
        return 'Machine updated successfully'
    else:
        return f'''
        <form method="POST">
            <label for="machine_name">Enter Machine Name:</label>
            <input type="text" id="machine_name" name="machine_name" value="{machine.name}">
            <label for="mac_address">Enter MAC Address:</label>
            <input type="text" id="mac_address" name="mac_address" value="{machine.mac_address}">
            <input type="submit" value="Update Machine">
        </form>
        '''

# Route to delete a machine
@app.route('/delete_machine/<int:id>', methods=['POST'])
def delete_machine(id):
    machine = Machine.query.get_or_404(id)
    db.session.delete(machine)
    db.session.commit()
    return 'Machine deleted successfully'

# Route to list all registered machines
@app.route('/machines', methods=['GET'])
def list_machines():
    machines = Machine.query.all()
    machine_list = '<h1>Registered Machines</h1><ul>'
    for machine in machines:
        machine_list += f'''
        <li>
            {machine.name} - {machine.mac_address}
            <form method="POST" action="/wakeup_by_machinename" style="display:inline;">
                <input type="hidden" name="machine_name" value="{machine.name}">
                <input type="submit" value="Wake Up">
            </form>
            <form method="GET" action="/edit_machine/{machine.id}" style="display:inline;">
                <input type="submit" value="Edit">
            </form>
            <form method="POST" action="/delete_machine/{machine.id}" style="display:inline;">
                <input type="submit" value="Delete">
            </form>
        </li>
        '''
    machine_list += '</ul>'
    return machine_list

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

if __name__ == '__main__':
    app.run(debug=True)

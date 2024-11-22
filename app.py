import requests
from flask import Flask, render_template

app = Flask(__name__)

# My JSON Server URL (replace with your actual hosted JSON URL)
API_URL = "https://my-json-server.typicode.com/yourusername/yourrepository"

def get_devices():
    try:
        devices_response = requests.get(f"{API_URL}/devices")
        locations_response = requests.get(f"{API_URL}/locations")
        
        devices = devices_response.json()
        locations = locations_response.json()
        
        # Enhance devices with location details
        for device in devices:
            device['location'] = next(
                (loc for loc in locations if loc['id'] == device['locationId']), 
                {'name': 'Unknown', 'building': 'Unknown'}
            )
        
        return devices
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

@app.route('/')
def index():
    devices = get_devices()
    return render_template('devices.html', devices=devices)

@app.route('/location/<int:location_id>')
def location_devices(location_id):
    devices = get_devices()
    location_devices = [
        device for device in devices 
        if device['locationId'] == location_id
    ]
    return render_template('devices.html', devices=location_devices)

if __name__ == '__main__':
    app.run(debug=True)
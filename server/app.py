from flask import Flask, render_template, request
from flask_socketio import disconnect, emit, SocketIO
import random, time, eventlet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    print(1)
    cube_data = [
        {
            'position': [128.09964, 35.1532],  # Longitude, Latitude
            'altitude': 0,
            'rotation': [0, 0, 0],  # Rotation angles in radians
            'size': 10,  # Size of the cubeN
            'image': 'your_image.png'  # Image file name
        },
        {
            'position': [128.09994, 35.1532],  # Longitude, Latitude
            'altitude': 0,
            'rotation': [1.052, 0, 0],  # Rotation angles in radians
            'size': 10,  # Size of the cube
            'image': 'your_image.png'  # Image file name
        },
        {
            'position': [128.09894, 35.1532],  # Longitude, Latitude
            'altitude': 0,
            'rotation': [1.052, 0, 0],  # Rotation angles in radians
            'size': 10,  # Size of the cube
            'image': 'your_image.png'  # Image file name
        },

        {
            'position': [128.09794, 35.1532],  # Longitude, Latitude
            'altitude': 0,
            'rotation': [1.052, 0, 0],  # Rotation angles in radians
            'size': 10,  # Size of the cube
            'image': 'your_image.png'  # Image file name
        },
    ]
    
    return render_template('index.html', cube_data=cube_data,
                           mapbox_access_token='pk.eyJ1IjoieXVubiIsImEiOiJjbHR3dDYyMXAwMzR0MmtwNHo1bWk3dW1qIn0.o4nBVu9qWb5Hl13LZtebzA')

def get_random_location():
    return {
                "droneID" : 1,
                "lng" : 128.09967 + round(random.randrange(-9,9)*0.00001, 5), 
                "lat" : 35.1532 + round(random.randrange(-9,9)*0.00001, 5),
            }

@socketio.on('connect')
def connected():
    print("클라이언트 연결됨")
    
    def update_Location():
        while True:
            print("새 위치 전송 중")
            socketio.emit('droneLocation', get_random_location())
            eventlet.sleep(1)
    
    socketio.start_background_task(target=update_Location)

@socketio.on('disconnect')
def disconnected():
    print("클라이언트 연결 해제됨")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
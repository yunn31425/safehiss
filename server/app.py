from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    cube_data = [
        {
            'position': [128.09964, 35.1532],  # Longitude, Latitude
            'altitude': 0,
            'rotation': [0, 0, 0],  # Rotation angles in radians
            'size': 10,  # Size of the cube
            'image': 'your_image.png'  # Image file name
        },
        {
            'position': [128.09994, 35.1532],  # Longitude, Latitude
            'altitude': 0,
            'rotation': [1.052, 0, 0],  # Rotation angles in radians
            'size': 10,  # Size of the cube
            'image': 'your_image.png'  # Image file name
        }
    ]
    
    return render_template('index.html', cube_data=cube_data,
                           mapbox_access_token='pk.eyJ1IjoieXVubiIsImEiOiJjbHR3dDYyMXAwMzR0MmtwNHo1bWk3dW1qIn0.o4nBVu9qWb5Hl13LZtebzA')

if __name__ == '__main__':
    app.run(debug=True)
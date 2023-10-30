import socketio

sio = socketio.Client()

def initialize():
    sio.connect('http://localhost:3000')
    sio.wait()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

def send_controller_data(x: float, y: float, z: float, rx: float, ry: float, rz: float, rw: float):
    print("Sending controller data")
    sio.emit("send_controller_data", [x, y, z, rx, ry, rz, rw])
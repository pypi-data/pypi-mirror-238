import socketio

sio = socketio.AsyncClient()

async def initialize():
    await sio.connect('http://localhost:3000')

async def wait():
    await sio.wait()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

async def send_ultrasound_controller_data(x: float, y: float, z: float, rx: float, ry: float, rz: float, rw: float):
    print("Sending ultrasound controller data")
    await sio.emit("send_ultrasound_controller_data", [x, y, z, rx, ry, rz, rw])
# Data Communicator Client

Communicates between devices and WebRTC

## Usage

```python
import asyncio
import doplcommunicator

async def run():
    await doplcommunicator.initialize()
    waitTask = doplcommunicator.wait()
    await doplcommunicator.send_ultrasound_controller_data(1, 1, 1, 1, 1, 1, 1)
    await waitTask

asyncio.run(run())
```

## Setup

```shell
# Activate the virtual environment
$ source venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt
```
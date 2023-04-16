# which algo
# number of packets
# size of packet
# use websockets

import asyncio
import websockets
import json


ROUND_ROBIN = 0
WEIGHTED_ROUND_ROBIN = 1
LEAST_CONNECTION = 2
WEIGHTED_LEAST_CONNECTION = 3

numPckts = 10
sizePckts = 256

msg = {"method": ROUND_ROBIN,
       "number": numPckts,
       "size": sizePckts}

data = json.dumps(msg)


async def handler():
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:
        # name = input("What's your name? ")

        await websocket.send(data)
        print("msg sent")
        print(f">>> {data}")

        # greeting = await websocket.recv()
        # print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(handler())

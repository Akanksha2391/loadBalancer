import asyncio
import websockets
import json


ROUND_ROBIN = 0
WEIGHTED_ROUND_ROBIN = 1
LEAST_CONNECTION = 2
WEIGHTED_LEAST_CONNECTION = 3

numPckts = 10
sizePckts = 500

# parameters for the load balancer

params = {"method": ROUND_ROBIN,
       "number": numPckts,
       "size": sizePckts}

data = json.dumps(params)

# function to pass the pckt num, pckt size and choosen algo to loadbalancer
# using websockets

async def handler():
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:

        await websocket.send(data)
        print("parameters sent to loadbalancer")
        print(f">>> {data}")


if __name__ == "__main__":
    asyncio.run(handler())

from itertools import cycle
import asyncio
import websockets
import json
import requests
import concurrent
from concurrent.futures import ThreadPoolExecutor
import time
import random

# server pool = (weight, port)
server_pool = [(1000, 8080),
               (1005, 8000),
               (1002, 6000),
               (1008, 6999)]


base_url = 'http://localhost:'
threads = 20
ALGO = 0
pcktSize = 0
pcktNum = 0
max_time = 0
min_time = 1e4
total_time = 0
server1 = 0
server2 = 0
server3 = 0
server4 = 0
count = 0
weights = { 8080: 1000,
            8000: 1000,
            6000: 1000,
            6999: 1000}


ITER = cycle(server_pool)

# round robin: assigns servers sequentially
def round_robin(iter):
    ports = []
    for r in range(0, pcktNum):
        ports.append(next(iter)[1])
    sendReq(ports)
    

# weighted round robin: assigns the server with maximum weight 
def weighted_round_robin(weights):
    global count
    ports = []
    for i in range(pcktNum):
        temp = max(weights.values())
        res = [key for key in weights if weights[key] == temp]
        port = res[0]
        weights[port] -=1
        count +=1
        if(count%4 == 0):
            weights[8000] +=1
        if(count%2 == 0):
            weights[8000] +=1
        if(count%5 == 0):
            weights[8000] +=1
        if(count%7 == 0):
            weights[8000] +=1
        ports.append(port)
    print(ports)
    sendReq(ports)



# least connection: assigns the server with minimum connections
def least_conn(connections):
    global count
    ports = []
    for i in range(pcktNum):
        temp = min(connections.values())
        res = [key for key in connections if connections[key] == temp]
        port = random.choice(res)
        connections[port] += 1
        count +=1
        if(count%4 == 0):
            connections[8000] = 0 if 0 else connections[8000]-1
        if(count%2 == 0):
            connections[8080] = 0 if 0 else connections[8080]-1
        if(count%5 == 0):
            connections[6000] = 0 if 0 else connections[6000]-1
        if(count%7 == 0):
            connections[6999] = 0 if 0 else connections[6999]-1
        ports.append(port)
    sendReq(ports)


# weighted least connection: assigns the server with minimum connections and maximum weight
def weighted_least_conn(connections):
    global count
    ports = []
    for i in range(pcktNum):
        temp = min(connections.values())
        res = [key for key in connections if connections[key] == temp]
        port = res[0]
        for p in res:
            if(weights[port]< weights[p]):
                port = p
        connections[port] += 1
        weights[port] -=1
        count +=1
        if(count%4 == 0):
            connections[8000] = 0 if 0 else connections[8000]-1
            weights[8000] +=1
        if(count%2 == 0):
            connections[8080] = 0 if 0 else connections[8080]-1
            weights[8000] +=1
        if(count%5 == 0):
            connections[6000] = 0 if 0 else connections[6000]-1
            weights[8000] +=1
        if(count%7 == 0):
            connections[6999] = 0 if 0 else connections[6999]-1
            weights[8000] +=1
        ports.append(port)
    print(ports)
    sendReq(ports)



def test_req(port, index):
    global max_time, min_time, total_time,pcktSize,server1, server2, server3, server4
    start_time = time.time()
    r = requests.get(f'{base_url}{port}/', params={"reqNum": index, "weight": weights[port], "pcktSize": pcktSize})
    end_time = time.time()
    req_time = end_time - start_time
    max_time = max(max_time, req_time)
    min_time = min(min_time, req_time)
    total_time += req_time
    if(port == 8080):
        server1 +=1
    elif(port == 8000):
        server2 +=1
    elif(port == 6000):
        server3 +=1
    elif(port == 6999):
        server4 +=1
    
    return r.json()


def req_analysis(data):
    global max_time, min_time, total_time, pcktNum, server1, server2, srever3, server4
    print("max time for a single request:", max_time)
    print("min time for a single request:", min_time)
    print("throughput:", pcktNum/total_time)
    print("response time:", total_time)
    print("requests processed by srever 1:", server1)
    print("requests processed by srever 2:", server2)
    print("requests processed by srever 3:", server3)
    print("requests processed by srever 4:", server4)


def sendReq(ports):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = {executor.submit(test_req, port, index)
                         for index, port in enumerate(ports)}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
                print(data)
            except Exception as e:
                print('Looks like something went wrong:', e)

        req_analysis(data)


# #################################################
# receiving algo type, pckt number, pckt size

async def lb_params(websocket):
    global pcktNum, pcktSize, server1, server2, server3, server4
    connections = {8080: 0,
               8000: 0,
               6000: 0,
               6999: 0}
    server1 = 0
    server2 = 0
    server3 = 0
    server4 = 0
    data = await websocket.recv()
    params = json.loads(data)

    ALGO = params["method"]
    pcktNum = params["number"]
    pcktSize = params["size"]
    print(ALGO, pcktNum, pcktSize)
    if ALGO == 0:
        round_robin(ITER)
    elif ALGO == 1:
        weighted_round_robin(weights)
    elif ALGO == 2:
        least_conn(connections)
    elif ALGO == 3:
        weighted_least_conn(connections)


async def main():
    async with websockets.serve(lb_params, "localhost", 3000):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

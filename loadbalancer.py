from itertools import cycle
import heapq
import asyncio
import websockets
import json
import requests
import concurrent
from concurrent.futures import ThreadPoolExecutor
import time
# algo
# server
# how to send request and process them
# result(graph)

server_pool = [(10, 8080),
               (9, 8000),
               (20, 6000),
               (5, 6999)]

base_url = 'http://localhost:'
threads = 20
ALGO = ''
pcktSize = 0
pcktNum = 0
max_time = 0
min_time = 1e4
total_time = 0

ITER = cycle(server_pool)


def round_robin(iter):
    ports = []
    # print(pcktNum)
    for r in range(0, pcktNum):
        ports.append(next(iter)[1])
    # print(ports)
    sendReq(ports)
    #  return next(iter)


# for reqNumber in range(10):
#     server = round_robin(ITER)
#     print("PORT", server["port"], "SELECTED FOR REQ", reqNumber)

# heapq.heapify(server_pool)

# def weighted_roundRobin():
#     server = heapq.heappop(server_pool)
#     print("PORT", server["port"], "SELECTED FOR REQ", reqNumber)
#     heapq.heappush(server)


def test_req(port, index):
    global max_time,min_time,total_time
    # print(index)
    start_time = time.time()
    r = requests.get(f'{base_url}{port}/', params={"reqNum": index})
    end_time = time.time()
    req_time = end_time - start_time
    max_time = max(max_time, req_time)
    min_time = min(min_time, req_time)
    total_time += req_time


    return r.json()

def req_analysis(data):
    global max_time,min_time,total_time,pcktNum
    print("max time for a single request:", max_time)
    print("min time for a single request:", min_time)
    print("avg time taken:", total_time/pcktNum)



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

async def hello(websocket):
    global pcktNum
    data = await websocket.recv()
    msg = json.loads(data)

    ALGO = msg["method"]
    pcktNum = msg["number"]
    pcktSize = msg["size"]
    print(ALGO, pcktNum, pcktSize)
    if ALGO == 0:
        round_robin(ITER)
    elif ALGO == 1:
        weighted_roundRobin()


async def main():
    async with websockets.serve(hello, "localhost", 3000):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

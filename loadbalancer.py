from itertools import cycle
import heapq

server_pool = [(10,8080),
               (9,5000),
               (20,3000),
               (5,6999)]

ITER = cycle(server_pool)


def round_robin(iter):
    return next(iter)


for reqNumber in range(10):
    server = round_robin(ITER)
    print("PORT", server["port"], "SELECTED FOR REQ", reqNumber)

heapq.heapify(server_pool)

def weighted_roundRobin():
    server = heapq.heappop(server_pool)
    print("PORT", server["port"], "SELECTED FOR REQ", reqNumber)
    heapq.heappush(server)

import time
from multiprocessing import Process, Pool, Manager, Value, Array, Pipe


def a1(conn):
    i = 0
    conn.send((i, 'adf'))
    while True:
        i += 1
        time.sleep(1)
        conn.send(conn.recv())
        print('First process is running')
        print()

def a2(conn):
    while True:
        time.sleep(1)
        res = conn.recv()
        print(res)
        conn.send(res + ('123',))


parent, child = Pipe(duplex=True)

p = Process(target=a1, args=(parent,))
p2 = Process(target=a2, args=(child,))

p.start()
p2.start()
p.join()
p2.join()

# print(num.value)
# print(arr[:])

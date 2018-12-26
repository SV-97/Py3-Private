import socket
from multiprocessing import Process
from random import randint
from time import sleep

class Server(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind(("", 50000))
            while True:
                data, addr = s.recvfrom(1024)
                print(f"[{addr[0]}] {data.decode()}")
        finally:
            s.close()

id = 0

class Client(Process):
    def __init__(self):
        global id
        super().__init__()
        self.id = id
        id += 1 

    def run(self):
        for i in range(10):
            sleep(randint(0, 3))
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip = "localhost"
            message = f"From Client {self.id}: {i}"
            s.sendto(message.encode(), (ip, 50000))
            s.close()

server = Server()
clients = [Client() for x in range(0, 4)]
server.start()

for client in clients:
    client.start()

for client in clients:
    client.join()
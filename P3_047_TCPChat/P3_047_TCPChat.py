from multiprocessing import Process
import socket


class Server(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 50000))
        print("Bound to socket 50000")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(1)
        try:
            while True:
                print("Listening... ")
                com, addr = s.accept()
                while True:
                    data = com.recv(1024)
                    if not data:
                        com.close()
                        break
                    print(f"[{addr[0]}] {data.decode()}")
                    answer = input("Answer: ")
                    if not answer:
                        com.close()
                        break
                    com.send(answer.encode())
        finally:
            s.close()

class Client(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        server_ip = input("Input IP of target server: ")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("", 50000))
        try:
            while True:
                message = input("Message: ")
                s.send(message.encode())
                data = s.recv(1024)
                if not data:
                    break
                print(f"[{server_ip}] {data.decode()}")
        finally:
            s.close()

if __name__=="__main__":
    server = Server()
    #client = Client()
    server.run()
    #client.run()
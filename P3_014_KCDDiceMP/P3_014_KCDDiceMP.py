import socket
import sys
import _thread 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5555))
s.listen(2)
print("Welcome to KCD Dice!")

def threaded_client(conn, addr):

    conn.send(str.encode("Welcome, type your info\n"))

    while True:
        data = conn.recv(2048)
        reply = "Server output: "+ data.decode("utf-8")
        if not data:
            break
        conn.sendall(str.encode(reply))
        print("connection to {} closed".format(addr[0]))

    conn.close()


while True:
    con1, addr1 = s.accept()
    print("connected to: {}:{}\n".format(addr1[0], str(addr1[1])))
    con1.send(str.encode("Waiting for another player..."))
    con2, addr2 = s.accept()
    print("connected to: {}:{}\n".format(addr2[0], str(addr2[1])))

		
import socket as sk
import os
import time
import hashlib
import threading as th

os.system("clear")

# 서버 세팅
Server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
Server.bind(("localhost", 8080))

# 서버 리슨
Server.listen(1)
print("서버 열림!")

# 클라이언트 처리 클래스
clients = {}

class clientProcessing():
    def __init__(self, client: sk.socket, ip: list):
        self.__client = client
        self.__ip     = ip
        self.__id     = hashlib.md5(str(time.time()).encode())

        clients[self.__id] = self.__client

        Thread = th.Thread(target=self.processing)
        Thread.start()

    def processing(self):
        while True:
            data = self.__client.recv(1024)

            if data.decode() == "":
                del clients[self.__id]
                print(f"접속 끊킴, {self.__ip[0]}")

                break;

            print(f"{self.__ip[0]} 에게 {data.decode()}받음")
            print("ㄴ 모든 사람한테 보내는중..")

            for i in clients:
                clients[i].sendall(data)


while True:
    a, i = Server.accept()
    print(f"{i[0]}에서 접속시도함, 클라이언트처리 시작함")

    
    newProcessing = clientProcessing(a, i)
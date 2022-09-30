import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""#IPv4 주소
        self.port = 60000
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self): #서버와 연결
        try:
            self.client.connect(self.addr) #연결되면
            return self.client.recv(2048).decode() #bit 정보를 받으면 decode
        except:
            print("connect error") #server.py를 먼저 실행 시킨 후 network.py를 실행시켜야 에러 없음

    def send(self, data):

        try:
            self.client.send(str.encode(data)) #서버와 연결 후 data encode해서 bit로 전환 후 전송.
            return self.client.recv(2048).decode() #정상적으로 작동하면 보낸 정보를 decode해서 network 파일에 출력
        except socket.error as e:
            print(e)


n = Network()
print(n.send("Hiiii")) #send만. receive는 아직 없음. 서버가 보내긴 하는데 클라이언트에는 아직 처리하는 함수 없음
print(n.send("working "))
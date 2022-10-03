import socket

#잠깐 대기. 우선은 필요 없음.(게임 개발할 때 참고)
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""#IPv4 주소
        self.port = 60000
        self.addr = (self.server, self.port)
        self.mreq = self.connect()

    def getMReq(self): #match requst 수령하는 함수
        return self.mreq

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

#n = network()는 test 용이었으므로 삭제
import socket
from _thread import *
import sys

server = "" #local host 이건 git 할 때 지우고 올리기. cmd->ipconfig 에서 하면 됨
PORT = 60000

#서버 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#서버와 포트 연결 / try, except를 이용해서 실패했을 경우 e가 뜰 예정
try:
    s.bind((server, PORT))

except socket.error as e:
    str(e)

#서버에 접속할 클라이언트 수 제힌하고 싶으면 ()안에 수만큼 적으면 됨
s.listen()
print('서버가 시작되었습니다. waiting for a connection')


def threaded_client(conn):
    while True: #이 함수가 클라이언트가 연결 되어있을 때도 계속 무한히 데이터를 받으면서 작동 해야 하기에
        try:
            data = conn.recv(2048) #받으려는 데이터 양 2048 bit 수. 에러 뜨면 이거 사이즈 키우기
            reply = data.decode("utf-8") #받은 data는 우리가 읽을 수 있게 utf-8로 변경

            if not data: #data를 받지 않으면 연결 해제
                print("Disconnected")
                break
            else: #에러 발생했을 경우를 대비해서
                print("Received: ", reply)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply)) #정보를 보낼 떄 bit로 변경해서 전송
        except:
            print("threaded_client error")
            break #그냥.. 딱히 에러 발생할 것 같지 않지만 일단 했기에.



#conn, addr = s.accept()

#계속해서 클라이언트의 요청을 기다리는 상태
#connection과 그것의 IP 주소(addr)
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))
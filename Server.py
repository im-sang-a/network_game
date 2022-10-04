import socket
from _thread import *
import threading

import sys

server = "192.168.197.1" #IPv4주소: local host 이건 git 할 때 지우고 올리기. cmd->ipconfig 에서 하면 됨
PORT = 60000

#서버 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#서버와 포트 연결 / try, except를 이용해서 실패했을 경우 e가 뜰 예정
try:
    s.bind((server, PORT))

except socket.error as e:
    str(e)

#서버에 접속할 클라이언트 수 제힌하고 싶으면 ()안에 수만큼 적으면 됨
s.listen() #원래는 listen 으로 수 제한 가능하다고 들었는데 안됨 -> clients 리스트 길이로 접속 가능 수 제한 하기로 함
print('서버가 시작되었습니다. waiting for a connection')



##클라이언트 매칭까지 완료된 상태. 화면 전환 필요.
#대기화면이라고 간주.

#채팅 기능 생성
clients = [] #채팅 접속하면 여기로 addr 저장됨
nicknames = [] #닉네임도 여기로 같은 순서로 저장됨

# def limit_client():
#     if len(clients) > 3:
#         client.close()

def broadcast(message): #모든 client 에게로 메시지 전송
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            #client의 접속이 종료된 것으로 간주. 클라이언트가 저장된 인덱스를 찾아서 리스트에서 각각 삭제 후 클라이언트 접속 종료 시킴.
            #이 경우, 남은 클라이언트는 계속 서버에 접속된 상태로 남아 있음.. 새로운 클라이언트가 접속할 때까지 대기.
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break



def receive():
    while True:
        if len(clients) < 3: #접속 가능한 클라이언트 수 2로 제한
            client, address = s.accept() #클라이언트의 접속 허용
            print(f'connected with {str(address)}')
        else:
            client.send('room full'.encode('ascii'))

        #여기까지는 문제 없음.
        client.send('NICK'.encode('ascii')) #처음 - 클라이언트에게 클라이언트 닉네임 정보 받기 위해서 NICK 전송
        #NICK을 전송하는 것이 먼저.
        nickname = client.recv(1024).decode('ascii') #클라이언트가 닉네임을 보내오면
        #클라이언트가 닉네임 받음.받으면서 충돌하면서 생기는 문제.
        nicknames.append(nickname) #닉네임 리스트에 저장
        clients.append(client) #클라이언트는 클라이언트 리스트에 저장

        print(f'nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii')) #접속한 클라이언트 모두에게 클라이언트가 접속했음을 broadcast
        client.send("connected to the server".encode('ascii')) #접속한 클라이언트에게는 서버에 접속 되었음을 전송

        thread = threading.Thread(target=handle, args=(client,))#handle 스레드(순수 채팅 기능) 시작
        thread.start()

        # thread = threading.Thread(target=limit_client, args=(client,))  # handle 스레드(순수 채팅 기능) 시작
        # thread.start()



#대기화면 - 채팅 기능 시작.
receive()





#나중에 게임할 때 필요하면 사용하기.
# #서버와 클라이언트 그냥 연결
# def threaded_client(conn):
#     conn.send(str.encode("Connected")) #연결된 상태
#     reply = "" #ipv4
#     #curi = "net?" #보내는 reply가 network.py에서 어떻게 뜨는지 확인하고 싶었음.
#     while True: #이 함수가 클라이언트가 연결 되어있을 때도 계속 무한히 데이터를 받으면서 작동 해야 하기에
#         try:
#             data = conn.recv(2048) #받으려는 데이터 양 2048 bit 수. 에러 뜨면 이거 사이즈 키우기/데이터를 받기 전까지 보내지 X
#             reply = data.decode("utf-8") #받은 data는 우리가 읽을 수 있게 utf-8로 변경
#
#             if not data: #data를 받지 않으면 연결 해제
#                 print("Disconnected")
#                 break
#             else: #data 받은 경우,
#                 print("Received: ", reply)
#                 print("Sending : ", reply)
#
#             conn.sendall(str.encode(reply)) #정보를 보낼 떄 bit로 변경해서 전송
#         except:
#             print("threaded_client error")
#             break
#
#     print("Lost connection")
#     conn.close()
#
# #conn, addr = s.accept()
#
# currentClient = 0
# #계속해서 클라이언트의 요청을 기다리는 상태
# #connection과 그것의 IP 주소(addr)
#
# while True:
#     conn, addr = s.accept()
#     print("Connected to:", addr) #client로 부터 주소를 받고 연결된 상태.
#
#     start_new_thread(threaded_client, (conn, currentClient))
#     currentClient += 1# 연결된 클라이언트 수를 측정하기 위함
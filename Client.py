from network import Network
import socket
import threading

#채팅
nickname = input("choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('', 60000)) #IP주소, port

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.thread(target=receive)
receive_thread.start()

write_thread = threading.thread(target=write)
write_thread.start()




def main():#게임을 실행하는 메인 함수
    run = True
    n = Network()
    startPos = n.getPos() #이거는 움직이는 게임을 보고 참고한 거기 때문에 처음 시작 지점(좌표)를 받는 함수->이 함수를


    while run:
        p2Pos = n.send()

#1) 닉네임 정하기 완료 버튼 누르면
# #클라이언트가 매칭 요청 정보를 서버로 전송
def match_req():
    pass
# 서버는 매칭 정보 수령 후, 이전에 매치 요청 보낸 사람이 있는지 확인
#없다면, 대기룸 입장 또는 매칭 중입니다..?네트워크는 print("searching...") / 있다면 매칭 시작 print("match sucssesfully done.")



#2)채팅 기능
#특정 바이트 만큼 입력 받고 서버로 전송해서 양쪽 클라이언트 화면에 모두 뜨도록 하기


#3)클라이언트 A가 캐릭터 선택을 완료하면 서버로 선택된 캐릭터를 서버로 보내고 (print("character 1 selected")) 클라이언트 B에게 그 메시지가 뜨도록 하기.
# (A에는 이미 떠 있으니까 B에만 전송해서 뜨게 하면 됨/클라이언트 A에 뜨는 메시지는 서버를 통해서이면 안됨) (나중에 메시지를 이미지로 대체)
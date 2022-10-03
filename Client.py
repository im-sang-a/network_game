from network import Network
import socket
import threading
import concurrent.futures

#닉네임 입력 및 매칭 하는 화면

nickname = input("choose a nickname: ") #닉네임 입력하는 창

#입력 완료하면 client는 socket 통신 실행
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def match(): #매칭-서버 커넥팅 시도. 되면 채팅 시작. 안되면 아무것도 진행 안되도록.
    try:#클라이언트 접속 시도
        client.connect(('192.168.197.1', 60000)) #IP주소, port  #커넥트
        print("게임에 접속했습니다. 대기 화면으로 이동합니다.")
        return 0

    except:
        #이미 매칭인원이 꽉 차서 접속이 안되는 경우로 나중에 다시 시도해달라는 메시지.
        print("게임이 이미 진행중입니다. 나중에 다시 시도해주세요")
        return 1


#대기 화면 - 채팅 기능
def receive(): #채팅 상에서 메시지를 받는 함수
    while True:
        try:
            message = client.recv(1024).decode('ascii') #서버로부터 1024비트의 data를 받아서 decode
            if message == 'NICK': #만약 메시지가 'NICK'인 경우
                client.send(nickname.encode('ascii')) #클라이언트가 앞서 입력한 닉네임을 서버로 전송
            else: #이미 닉네임이 입력된 경우로, 이 경우 message 내용은 다른 클라이언트가 서버로 보낸 메시지 => message 출력
                print(message)

        except: #받은 정보가 없으면 에러 발생. client 연결 해제
            print("An error occurred!")
            client.close()
            break

def write(): #채팅 상에서 메시지를 입력해서 서버로 메시지 내용을 전송하는 함수
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

#리시브 함수 실행
#멀티 스레드

#return 값을 얻기 위해서 아래 코드로 바꿈.
#참고: #https://rateye.tistory.com/880
with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(match)
    return_value = future.result() #return 값

# match_thread = threading.Thread(target=match)#매칭 시작.
# match_thread.start()

#return_value가 1이면, 반환 받은 값이 1이면(연결 된 경우) 아래 채팅 스레드 모두 실행
if return_value == 0: #여기 실수. 0인데 1로 해버림. 그래서 충돌해서 계속 winerror 10054떴었음
    # 채팅 - 메시지를 받는 스레드
    receive_thread = threading.Thread(target=receive)  # target 안에는 함수를 넣어서 실행
    receive_thread.start()

    # 채팅 - 메시지를 작성하는 스레드
    write_thread = threading.Thread(target=write)
    write_thread.start()


#->채팅 기능 실행 완료





# def main():#게임을 실행하는 메인 함수
#     run = True
#     n = Network()
#     startPos = n.getPos() #이거는 움직이는 게임을 보고 참고한 거기 때문에 처음 시작 지점(좌표)를 받는 함수->이 함수를
#
#
#     while run:
#         p2Pos = n.send()
#
# #1) 닉네임 정하기 완료 버튼 누르면
# # #클라이언트가 매칭 요청 정보를 서버로 전송
# def match_req():
#     pass
# 서버는 매칭 정보 수령 후, 이전에 매치 요청 보낸 사람이 있는지 확인
#없다면, 대기룸 입장 또는 매칭 중입니다..?네트워크는 print("searching...") / 있다면 매칭 시작 print("match sucssesfully done.")



#2)채팅 기능
#특정 바이트 만큼 입력 받고 서버로 전송해서 양쪽 클라이언트 화면에 모두 뜨도록 하기


#3)클라이언트 A가 캐릭터 선택을 완료하면 서버로 선택된 캐릭터를 서버로 보내고 (print("character 1 selected")) 클라이언트 B에게 그 메시지가 뜨도록 하기.
# (A에는 이미 떠 있으니까 B에만 전송해서 뜨게 하면 됨/클라이언트 A에 뜨는 메시지는 서버를 통해서이면 안됨) (나중에 메시지를 이미지로 대체)
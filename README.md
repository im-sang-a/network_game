# network_game

network 개발 참고
https://www.techwithtim.net/tutorials/python-online-game-tutorial/server/

IPv4 주소 커밋 되지 않게 주의하기

server.py 파일 실행 후 백그라운드에 종료되지 않은 상태에 두고 다른 파일 실행하기


채팅 개발 참고
https://youtu.be/3UOyky9sEQY

#네트워크 1주차 수정필요한 부분
  1)한 컴퓨터에서 서버를 실행시키고 같은 와이파이/LAN에 연결된 다른 컴퓨터에서 클라이언트를 실행시키면 작동하는지 확인 필요.
     -> 안된다면, PORT 번호 차단된 건지 확인해보기(192.168.1.xxx->IP 주소는 이거여야 함)
     https://stackoverflow.com/questions/61135576/connect-multiple-computers-with-sockets-python
     -> ![image](https://user-images.githubusercontent.com/67996426/194000185-22a3d8bc-1ace-4962-8b46-d5631d3880de.png)
     ->https://m.blog.naver.com/heennavi1004/222051331011 여기 참고. 파이썬 TCP/IP 소켓 통신 

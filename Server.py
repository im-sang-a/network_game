import socket

HOST = ''
PORT = 60000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('서버가 시작되었습니다.')
    conn, addr = s.accept()


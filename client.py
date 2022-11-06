# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import socket
import threading
from tkinter import *
from tkinter import PhotoImage
from time import sleep

#새로운 프레임 띄우기
def openFrame(frame):
    frame.tkraise()

def name_select():
    result = tkinter.simpledialog.askstring("제목", "닉네임을 입력하세요")
    global your_name
    your_name = str(result)
    my_name.set(your_name)
    if your_name.encode().isalpha() == False:
        tk.messagebox.showerror(
            title="ERROR!", message="영어로 닉네임을 입력하세요."
        )
        name_select()
    else:
        lbl_your_name["text"] = "당신의 닉네임: " + your_name
        connect_to_server(your_name)
        openFrame(frame2)

#이미지선택
a = None
def character_select1(e):
    global a
    a = image1

def character_select2(e):
    global a
    a = image2

def character_select3(e):
    global a
    a = image3

def character_select4(e):
    global a
    a = image4

def select_ok(e):
    select_char_can.configure(image = a)

#채팅 입력한 거 화면에 보이게
def chat_send():
    message = chat_input.get()
    chat_space.insert(END, '\n' + message)
    chat_input.delete(0, 'end')

def game_logic(you, opponent):
    winner = ""
    rock = "rock"
    paper = "paper"
    scissors = "scissors"
    player0 = "you"
    player1 = "opponent"

    if you == opponent:
        winner = "draw"
    elif you == rock:
        if opponent == paper:
            winner = player1
        else:
            winner = player0
    elif you == scissors:
        if opponent == rock:
            winner = player1
        else:
            winner = player0
    elif you == paper:
        if opponent == scissors:
            winner = player1
        else:
            winner = player0
    return winner

def enable_disable_buttons(todo):
    if todo == "disable":
        btn_rock.config(state=tk.DISABLED)
        btn_paper.config(state=tk.DISABLED)
        btn_scissors.config(state=tk.DISABLED)
    else:
        btn_rock.config(state=tk.NORMAL)
        btn_paper.config(state=tk.NORMAL)
        btn_scissors.config(state=tk.NORMAL)

def count_down(my_timer, nothing):
    global game_round
    if game_round <= TOTAL_NO_OF_ROUNDS:
        game_round = game_round + 1

    lbl_game_round["text"] = "Game " + str(game_round) + " round 가 시작되었습니다."

    while my_timer > 0:
        my_timer = my_timer - 1
        print("게임 타이머: " + str(my_timer))
        lbl_timer["text"] = my_timer
        sleep(1)

    enable_disable_buttons("enable")
    lbl_round["text"] = "Round - " + str(game_round)
    lbl_final_result["text"] = " "

def choice(arg):
    global your_choice, client, game_round
    your_choice = arg
    lbl_your_choice["text"] = "당신의 선택: " + your_choice

    if client:
        dataToSend = "Game_Round" + str(game_round) + your_choice
        client.send(dataToSend.encode())
        enable_disable_buttons("disable")


def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, your_name
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name.encode())  # 연결 후 서버에게 메세지 보냄

        # 서버로부터 메세지를 계속 수신하기 위해 스레드 시작
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(
            title="ERROR!!!",
            message="host와 연결 할 수 없습니다. "
            + HOST_ADDR
            + " on port: "
            + str(HOST_PORT)
            + " 연결 할 수 없습니다. 다시 시도해주세요. "
        )


def receive_message_from_server(sck, m):
    global your_name, opponent_name, game_round
    global your_choice, opponent_choice, your_score, opponent_score
    # final_result = ""
    # color = ""

    while True:
        from_server = str(sck.recv(4096).decode())

        if not from_server:
            break

        if from_server.startswith("welcome"):
            if from_server == "welcome1":
                lbl_welcome["text"] = (
                    " 환영합니다! " + your_name + "님 상대방을 기다려주세요."
                )
            elif from_server == "welcome2":
                lbl_welcome["text"] = (
                    " 환영합니다! " + your_name + "님 상대방을 기다려주세요."
                )
            lbl_line_server.pack()

        elif from_server.startswith("opponent_name$"):
            opponent_name = from_server.replace("opponent_name$", "")
            lbl_opponent_name["text"] = "상대방 닉네임: " + opponent_name
            # op_name = str(opponent_name)
            # opp_name.set(op_name)
            top_frame.pack()
            middle_frame.pack()
            openFrame(frame3)

            # 두 명의 사용자 연결되어 게임 시작 준비 완료
            threading._start_new_thread(count_down, (game_timer, ""))
            lbl_welcome.config(state=tk.DISABLED)
            lbl_line_server.config(state=tk.DISABLED)

        elif from_server.startswith("$opponent_choice"):
            # 서버에서 상대방 선택
            opponent_choice = from_server.replace("$opponent_choice", "")

            # 누가 이겼는지 결과
            who_wins = game_logic(your_choice, opponent_choice)
            round_result = " "
            if who_wins == "you":
                your_score = your_score + 1
                round_result = "이겼습니다."
                # final_result = "(당신이 선공입니다!!!)"
                # color = "green"
            elif who_wins == "opponent":
                opponent_score = opponent_score + 1
                round_result = "졌습니다."
                # final_result = "(당신이 방어입니다!!!)"
                # color = "red"
            else:
                round_result = "무승부"
                # final_result = "(무승부!!!)"
                # color = "black"
                # lbl_opponent_choice["text"] = "상대방의 선택: " + opponent_choice
                # lbl_result["text"] = "결과: " + round_result
                # lbl_game_round["text"] = "다시 선택해주세요."
                # enable_disable_buttons('')
                # continue

            # GUI 업데이트
            lbl_opponent_choice["text"] = "상대방의 선택: " + opponent_choice
            lbl_result["text"] = "결과: " + round_result

            # 마지막 라운드 결과
            if game_round == TOTAL_NO_OF_ROUNDS:
                # compute final result
                final_result = ""
                color = ""

                if your_score > opponent_score:
                    final_result = "(당신이 이겼습니다!!!)"
                    color = "green"
                elif your_score < opponent_score:
                    final_result = "(당신이 졌습니다!!!)"
                    color = "red"
                else:
                    final_result = "(무승부!!!)"
                    color = "black"
                    # sleep(2)
                    # game_logic(your_choice, opponent_choice)


                lbl_final_result["text"] = (
                    "잠시후 결과창으로 이동합니다!!!"
                )
                lbl_final_result.config(foreground=color)
                enable_disable_buttons("disable")

                sleep(3)
                openFrame(frame5)

                result = tk.Label(frame5, text =  "최종결과: "
                    + str(your_score)
                    + " - "
                    + str(opponent_score)
                    + " "
                    + final_result)
                result.place(x = 315, y= 350)

                game_round = 0
                your_score = 0
                opponent_score = 0

            threading._start_new_thread(count_down, (game_timer, ""))
    sck.close()


'**************************게임창 띄우기******************************'
window=tk.Tk()
window.title("참참참 게임")
window.geometry("700x700")

global my_name, opp_name
my_name = StringVar()
opp_name = StringVar()

#프레임 정의
frame1=tk.Frame(window) #기본 프레임
frame2=tk.Frame(window) #닉네임 정하고 매칭 시작후 방 들어가는 화면
frame3=tk.Frame(window) #대기방
frame4=tk.Frame(window) #가위바위보 창
frame5=tk.Frame(window) #참참참 게임
frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=0, sticky="nsew")
frame3.grid(row=0, column=0, sticky="nsew")
frame4.grid(row=0, column=0, sticky="nsew")
frame5.grid(row=0, column=0, sticky="nsew")


#이미지
image1=PhotoImage(file="image/image1.gif")
image2=PhotoImage(file="image/image2.gif")
image3=PhotoImage(file="image/image3.gif")
image4=PhotoImage(file="image/image4.gif")
playbt=PhotoImage(file="image/start.gif")




#frame1(게임 첫 화면)
game_st=tk.Button(frame1,image=playbt,command = name_select)
game_st.pack(padx=300,pady=500)

#frame2(매칭방)
input_nickname_bt=tk.Label(frame2,text="대기중...")
input_nickname_bt.place(x = 315, y= 350)

#frame3(대기방)
#선택 이미지 표시
select_char_can = tk.Label(frame3, width =150, height = 150)
select_char_can.place(x=50, y=50)
select_char_user=tk.Label(frame3, textvariable= my_name)
select_char_user.place(x=70,y=10)
select_anchar_user=tk.Label(frame3,textvariable= opp_name)
select_anchar_user.place(x= 250,y=10)


#캐릭터 선택 버튼
char_select_br = tk.Button(frame3, text = "캐릭터 선택")
char_select_br.place(x =200,y=660)
#캐릭터 버튼 배치
char_image1 = tk.Button(frame3,image=image1, width = 200, height = 200)
char_image2 = tk.Button(frame3,image=image2, width = 200, height = 200)
char_image3 = tk.Button(frame3,image=image3, width = 200, height = 200)
char_image4 = tk.Button(frame3,image=image4, width = 200, height = 200)
char_image1.place(x=25,y=240)
char_image2.place(x=235,y=440)
char_image3.place(x=25,y=440)
char_image4.place(x=235,y=240)
char_image1.bind('<Button>', character_select1)
char_image2.bind('<Button>', character_select2)
char_image3.bind('<Button>', character_select3)
char_image4.bind('<Button>', character_select4)
char_select_br.bind('<Button>', select_ok)


#채팅 보여질 공간 (Label에서 Text로 변경)
chat_space = tk.Text(frame3, width = 30, height =35)
chat_space.place(x= 460, y=30)

#채팅입력 하는곳
chat_input = tk.Entry(frame3)
# chat_input.bind("<Return>",chat_send)
chat_input.place(x = 460, y = 500,width=155,height=22)

#전송 버튼
chat_br = tk.Button(frame3, text = " 전송 ", command = chat_send)
chat_br.place(x =630,y=495)

#가위바위보 게임시작 버튼
chamcham_st_bt= tk.Button(frame3,image=playbt,command=lambda :openFrame(frame4))
chamcham_st_bt.place(x=500,y=550)

#나가기 버튼
exit_bt = tk.Button(frame5, width =30, height = 30, bg= 'blue', command=quit)
exit_bt.place(x = 550, y= 660)

#대기방 돌아가기
#exit_bt2 = tk.Button(frame5, width =30, height = 30, bg= 'pink', command= lambda :openFrame(frame3))
#exit_bt2.place(x = 500, y= 600)

your_name = ""
opponent_name = ""
game_round = 0
game_timer = 4
your_choice = ""
opponent_choice = ""
TOTAL_NO_OF_ROUNDS = 5
your_score = 0
opponent_score = 0

# 네트워크 클라이언트
client = None
HOST_ADDR = "localhost"
# HOST_ADDR = "localhost"
HOST_PORT = 8080

top_message_frame = tk.Frame(frame4)
lbl_line = tk.Label(
    top_message_frame,
    text="***********************************************************",
).pack()
lbl_welcome = tk.Label(top_message_frame, text="")
lbl_welcome.pack()
lbl_line_server = tk.Label(
    top_message_frame,
    text="***********************************************************",
)
lbl_line_server.pack_forget()
top_message_frame.pack(side=tk.TOP)

top_frame = tk.Frame(frame4)
top_left_frame = tk.Frame(
    top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1
)
lbl_your_name = tk.Label(
    top_left_frame, text="당신의 닉네임: " + your_name, font="Helvetica 11 bold"
)
lbl_opponent_name = tk.Label(top_left_frame, text="상대방 닉네임: " + opponent_name)
lbl_your_name.grid(row=0, column=0, padx=5, pady=8)
lbl_opponent_name.grid(row=1, column=0, padx=5, pady=8)
top_left_frame.pack(side=tk.LEFT, padx=(10, 10))


top_right_frame = tk.Frame(
    top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1
)
lbl_game_round = tk.Label(
    top_right_frame,
    text="Game round (x)",
    foreground="blue",
    font="Helvetica 14 bold",
)
lbl_timer = tk.Label(
    top_right_frame, text=" ", font="Helvetica 24 bold", foreground="blue"
)
lbl_game_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))

top_frame.pack_forget()

middle_frame = tk.Frame(frame4)

lbl_line = tk.Label(
    middle_frame, text="***********************************************************"
).pack()
lbl_line = tk.Label(
    middle_frame, text="**** GAME LOG ****", font="Helvetica 13 bold", foreground="blue"
).pack()
lbl_line = tk.Label(
    middle_frame, text="***********************************************************"
).pack()

round_frame = tk.Frame(middle_frame)
lbl_round = tk.Label(round_frame, text="Round")
lbl_round.pack()
lbl_your_choice = tk.Label(
    round_frame, text="당신의 선택: " + "None", font="Helvetica 13 bold"
)
lbl_your_choice.pack()
lbl_opponent_choice = tk.Label(round_frame, text="상대방 선택: " + "None")
lbl_opponent_choice.pack()
lbl_result = tk.Label(
    round_frame, text=" ", foreground="blue", font="Helvetica 14 bold"
)
lbl_result.pack()
round_frame.pack(side=tk.TOP)

final_frame = tk.Frame(middle_frame)
lbl_line = tk.Label(
    final_frame, text="***********************************************************"
).pack()
lbl_final_result = tk.Label(
    final_frame, text=" ", font="Helvetica 13 bold", foreground="blue"
)
lbl_final_result.pack()
lbl_line = tk.Label(
    final_frame, text="***********************************************************"
).pack()
final_frame.pack(side=tk.TOP)

middle_frame.pack_forget()

button_frame = tk.Frame(frame4)
button_frame.pack(side=tk.BOTTOM)
photo_rock = PhotoImage(file="image/rock.gif")
photo_paper = PhotoImage(file="image/paper.gif")
photo_scissors = PhotoImage(file="image/scissors.gif")

btn_rock = tk.Button(
    frame4,
    text="주먹",
    command=lambda: choice("rock"),
    state=tk.DISABLED,
    image=photo_rock,
)
btn_paper = tk.Button(
    frame4,
    text="보",
    command=lambda: choice("paper"),
    state=tk.DISABLED,
    image=photo_paper,
)
btn_scissors = tk.Button(
    frame4,
    text="가위",
    command=lambda: choice("scissors"),
    state=tk.DISABLED,
    image=photo_scissors,
)

btn_rock.place(x=250, y=450)
btn_paper.place(x=320, y=450)
btn_scissors.place(x=390, y=450)

openFrame(frame1)
window.mainloop()

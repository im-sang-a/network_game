# -*- coding: euc-kr -*-
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import socket
from time import sleep
import threading

# 메인 게임 창
window_main = tk.Tk()
window_main.title("Game Client")
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
HOST_ADDR = "192.168.16.1"
HOST_PORT = 8080


top_welcome_frame = tk.Frame(window_main)
lbl_name = tk.Label(top_welcome_frame, text="Name:")
lbl_name.pack(side=tk.LEFT)
ent_name = tk.Entry(top_welcome_frame)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top_welcome_frame, text="입장", command=lambda: connect())
btn_connect.pack(side=tk.LEFT)
top_welcome_frame.pack(side=tk.TOP)

top_message_frame = tk.Frame(window_main)
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


top_frame = tk.Frame(window_main)
top_left_frame = tk.Frame(
    top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1
)
lbl_your_name = tk.Label(
    top_left_frame, text="당신의 닉네임: " + your_name, font="Helvetica 13 bold"
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

middle_frame = tk.Frame(window_main)

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

button_frame = tk.Frame(window_main)
photo_rock = PhotoImage(file="image/rock.gif")
photo_paper = PhotoImage(file="image/paper.gif")
photo_scissors = PhotoImage(file="image/scissors.gif")

btn_rock = tk.Button(
    button_frame,
    text="주먹",
    command=lambda: choice("rock"),
    state=tk.DISABLED,
    image=photo_rock,
)
btn_paper = tk.Button(
    button_frame,
    text="보",
    command=lambda: choice("paper"),
    state=tk.DISABLED,
    image=photo_paper,
)
btn_scissors = tk.Button(
    button_frame,
    text="가위",
    command=lambda: choice("scissors"),
    state=tk.DISABLED,
    image=photo_scissors,
)
btn_rock.grid(row=0, column=0)
btn_paper.grid(row=0, column=1)
btn_scissors.grid(row=0, column=2)
button_frame.pack(side=tk.BOTTOM)


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


def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(
            title="ERROR!", message="영어로 닉네임을 입력하세요."
        )
    else:
        your_name = ent_name.get()
        lbl_your_name["text"] = "당신의 닉네임: " + your_name
        connect_to_server(your_name)


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

        # 위젯 비활성화
        btn_connect.config(state=tk.DISABLED)
        ent_name.config(state=tk.DISABLED)
        lbl_name.config(state=tk.DISABLED)
        enable_disable_buttons("disable")

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
            top_frame.pack()
            middle_frame.pack()

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
            elif who_wins == "opponent":
                opponent_score = opponent_score + 1
                round_result = "졌습니다."
            else:
                round_result = "무승부"

            # GUI 업데이트
            lbl_opponent_choice["text"] = "상대방의 선택: " + opponent_choice
            lbl_result["text"] = "결과: " + round_result

            # 마지막 라운드 결과
            if game_round == TOTAL_NO_OF_ROUNDS:
                # compute final result
                final_result = ""
                color = ""

                if your_score > opponent_score:
                    final_result = "(당신이 선공입니다!!!)"
                    color = "green"
                elif your_score < opponent_score:
                    final_result = "(당신이 방어입니다!!!)"
                    color = "red"
                else:
                    final_result = "(무승부!!!)"
                    color = "black"

                lbl_final_result["text"] = (
                    "최종결과: "
                    + str(your_score)
                    + " - "
                    + str(opponent_score)
                    + " "
                    + final_result
                )
                lbl_final_result.config(foreground=color)

                enable_disable_buttons("disable")
                game_round = 0
                your_score = 0
                opponent_score = 0

            # 타이머 시작
            threading._start_new_thread(count_down, (game_timer, ""))

    sck.close()


window_main.mainloop()
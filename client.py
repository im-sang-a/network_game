import tkinter
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *

#새로운 프레임 띄우기
def openFrame(frame):
    frame.tkraise()

#닉네임 입력 완료 버튼 눌렀을 때->닉네임 서버로 보내서 비교하기
def click_entrancebutton():
    openFrame(frame3)


def name_select():
    result = tkinter.simpledialog.askstring("제목", "닉네임을 입력하세요")
    # 매칭 완료 및 실패->함수 사용해서 매칭에 성공한다면 다음 프레임으로 전환
    openFrame(frame2)
    print(result)

#참참참 시작
def cham_start():
    pass

#이미지선택
def character_select():
    pass

#채팅 입력한 거 화면에 보이게
def chat_send(e):
    chat_space.config(text = chat_input.get())

#게임창 띄우기
window=tkinter.Tk()
window.title("참참참 게임")
window.geometry("700x700")

frame1=tkinter.Frame(window,bg="red") #기본 프레임
frame2=tkinter.Frame(window,bg="yellow") #두번째 프레임(닉네임 정하고 매칭 시작후 방 들어가는 화면)
frame3=tkinter.Frame(window,bg="green") #세번째 프레임(대기방)

l_frame3=tkinter.Frame(frame3,bg="pink") #대기방에서 쓸 공간 나눠보기
r_frame3=tkinter.Frame(frame3,bg="white")


frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=0, sticky="nsew")
frame3.grid(row=0, column=0, sticky="nsew")
l_frame3.pack(side=tkinter.LEFT,fill="both",expand=True)
r_frame3.pack(side=tkinter.RIGHT,fill="both",expand=True)

#frame1 게임 시작 버튼
game_st=tkinter.Button(frame1,bg='white',text="게임 시작",command = name_select)
game_st.pack(padx=300,pady=500)

#frame2
input_nickname_bt=tkinter.Button(frame2,bg="white",text="방 입장",command=click_entrancebutton)
input_nickname_bt.place(x = 315, y= 350)

#frame3

#캐릭터 선택 버튼
char_select_br = tkinter.Button(l_frame3, text = "캐릭터 선택", command = character_select)
char_select_br.place(x = 125,y= 260)

#캐릭터 이미지
char_image = tkinter.Canvas(l_frame3, width = 150, height = 150)
char_image.place(x = 90, y = 100)

#채팅 보여질 공간
chat_space = tkinter.Label(r_frame3, width = 35, height = 30)
chat_space.place(x= 80, y= 0)

#채팅입력 하는곳
chat_input = tkinter.Entry(r_frame3)
chat_input.bind("<Return>",chat_send)
chat_input.place(x = 80, y = 470)

#전송 버튼
chat_br = tkinter.Button(r_frame3, text = "전송", command = chat_send)
chat_br.place(x = 230,y= 465)

#게임시작 버튼
chamcham_st_bt= tkinter.Button(r_frame3,bg="white",text="게임 준비",command= cham_start)
chamcham_st_bt.place(x = 250,y=650)

openFrame(frame1)
window.mainloop()
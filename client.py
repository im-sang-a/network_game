import tkinter
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *
from PIL import ImageTk,Image

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

#채팅 입력한 거 화면에 보이게 (인터넷 참고해서 변경)
def chat_send(e):
    message = chat_input.get()
    chat_space.insert(END, '\n' + message)


#게임창 띄우기
window=tkinter.Tk()
window.title("참참참 게임")
window.geometry("700x700")
window.resizable(False, False)

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

#frame1(게임 첫 화면)
game_st=tkinter.Button(frame1,bg='white',text="게임 시작",command = name_select)
game_st.pack(padx=300,pady=500)

#frame2(매칭방)
input_nickname_bt=tkinter.Button(frame2,bg="white",text="방 입장",command=click_entrancebutton)
input_nickname_bt.place(x = 315, y= 350)

#frame3(대기방)
frame3_cha=LabelFrame(l_frame3,text="캐릭터 선택창")
frame3_cha.pack(fill="both",expand=True)
frame3_chat=LabelFrame(r_frame3,text="채팅창")
frame3_chat.pack(fill="both",expand=True)
#캐릭터 선택 버튼
char_select_br = tkinter.Button(l_frame3, text = "캐릭터 선택", command = character_select)
char_select_br.place(x = 125,y= 400)

#캐릭터 이미지
image1=Image.open("image/image1.jpg")
image1=image1.resize((200,200))
image1=ImageTk.PhotoImage(image1)
image2=Image.open("image/image2.jpg")
image2=image2.resize((200,200))
image2=ImageTk.PhotoImage(image2)
image3=Image.open("image/image3.jpg")
image3=image3.resize((200,200))
image3=ImageTk.PhotoImage(image3)
image4=Image.open("image/image4.jpg")
image4=image4.resize((200,200))
image4=ImageTk.PhotoImage(image4)


char_image1 = tkinter.Button(frame3_cha,image=image1, width = 130, height = 130)
char_image2 = tkinter.Button(frame3_cha,image=image2, width = 130, height = 130)
char_image3 = tkinter.Button(frame3_cha,image=image3, width = 130, height = 130)
char_image4 = tkinter.Button(frame3_cha,image=image4, width = 130, height = 130)
char_image1.place(x = 20, y= 20)
char_image2.place( x=  160, y= 20)
char_image3.place(x= 20, y = 190)
char_image4.place(x= 160, y= 190)

#채팅 보여질 공간 (Label에서 Text로 변경)
chat_space = tkinter.Text(r_frame3, width = 35, height = 30)
chat_space.place(x= 50, y=30)

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
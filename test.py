import tkinter
from tkinter import *

##버튼 눌렀을때 처리
#def click_stbutton():
#    new_window=tkinter.Toplevel()
#    new_window.title("게임 대기방")
#    new_window.geometry("800x800")

#새로운 프레임 띄우기
def openFrame(frame):
    frame.tkraise()

#게임창 띄우기
window=tkinter.Tk()
window.title("참참참 게임")
window.geometry("700x700")

frame1=tkinter.Frame(window) #기본 프레임
frame2=tkinter.Frame(window) #두번째 프레임

frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=0, sticky="nsew")

#버튼 생성하기
game_st=tkinter.Button(frame1,bg='white',text="게임 시작",command=lambda:[openFrame(frame2)])
game_st.pack(padx=325,pady=500)

openFrame(frame1)
window.mainloop()

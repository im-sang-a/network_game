import tkinter
from tkinter import *

#버튼 눌렀을때 처리
def click_stbutton():



#게임창 띄우기
window=Tk()
window.title("참참참 게임")
window.geometry("700x700")

#버튼 생성하기
game_st=tkinter.Button(window,bg='white',text="게임 시작",command=click_stbutton())
game_st.place(x=320,y=450)

window.mainloop()

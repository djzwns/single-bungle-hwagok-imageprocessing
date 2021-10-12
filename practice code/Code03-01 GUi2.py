# import tkinter
# window = tkinter.Tk()
# button1 = tkinter.Button()

# c++ namespace 와 비슷
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *

## function
def openMenu():
    global window, label2
    # messagebox.showinfo("파일", "열기를 선택함")
    fullname = askopenfilename(parent=window, filetypes=(("raw 파일", "*.raw"), ("모든 파일", "*.*")))
    label2.configure(text=fullname)


def addImage():
    global label1
    value = askinteger("제목", "내용", minvalue=-255, maxvalue=255)
    label1.configure(text=str(value))


window = Tk()
window.title("GUI 연습2")
window.geometry("500x300")

mainMenu = Menu(window) # 빈 메뉴 바
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="file", menu=fileMenu)
fileMenu.add_command(label="Open", command=openMenu)
fileMenu.add_command(label="Save", command=None)
fileMenu.add_separator()
fileMenu.add_command(label="Close", command=None)

imageMenu = Menu(mainMenu)
mainMenu.add_cascade(label="영상처리", menu=imageMenu)
imageMenu.add_command(label="밝게/어둡게", command=addImage)
imageMenu.add_command(label="반전", command=None)
imageMenu.add_command(label="흑백", command=None)
imageMenu.add_command(label="미러", command=None)

label1 = Label(window, text="요기1", font=("궁서체", 30), fg="blue", bg="yellow")
label1.pack()

label2 = Label(window, text="요기2", font=("궁서체", 30), fg="blue", bg="magenta")
label2.pack()

window.mainloop()

# GUI: Graphical User Interface
# TUI: Text User Interface
# MFC: C, C++, WinAPI --> MFC

# tkinter : window 창을 제공하는 python library
from tkinter import *
from tkinter import messagebox

# function
def clickButton():
    #messagebox.showinfo("title", "asdasdasd")
    label2.configure(text="hello world")

window = Tk()

## 여기에 화면을 구성하고 처리
window.title("Image")
window.geometry("300x400")
window.resizable(width=False, height=False)

label1 = Label(window, text="hello world")
label1.pack()

label2 = Label(window, text="dlrow olleh", font=("궁서체", 30), fg="blue", bg="yellow")
label2.pack()

button1 = Button(window, text="click me", fg="red", command=clickButton)
button1.pack()

photo = PhotoImage(file="../images/crayon_orig.png")
label3 = Label(window, image=photo)
label3.pack()

window.mainloop()

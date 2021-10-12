from tkinter import *


def click():
    label1.config(text="clicked", font=("궁서체", 20), fg="blue")


window = Tk()
window.title("Quiz02 복습3번")
window.geometry("300x400")
window.resizable(False, False)

label1 = Label(window, text="label1")
label1.pack()

button = Button(window, text="button click", command=click)
button.pack()

radioVar = IntVar()
radio1 = Radiobutton(window, text="radio1", value=1, variable=radioVar)
radio1.pack()
radio2 = Radiobutton(window, text="radio2", value=2, variable=radioVar)
radio2.pack()

check = Checkbutton(window, text="check1")
check.pack()

photo = PhotoImage(file="../images/crayon_orig.png")
label2 = Label(window, image=photo)
label2.pack()

window.mainloop()
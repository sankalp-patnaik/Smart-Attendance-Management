import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3
import sqlite3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

engine = pyttsx3.init()
engine.say("Welcome! to the face recognition attandance Management system")
# engine.say("Please browse through your options..")
engine.runAndWait()


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()
# Database initialization
def create_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

create_db()
def register_user(username, password):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    conn.close()
def login_user(username, password):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user
def signup():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        register_user(username, password)
    else:
        messagebox.showerror("Error", "Please fill in both fields.")
def login():
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        messagebox.showerror("Error", "Please fill in both fields.")
    else:
        user = login_user(username, password)
        if user:
            messagebox.showinfo("Success", "Login successful!")
            open_attendance_management()
        else:
            messagebox.showerror("Error", "Invalid credentials!")


# D:\2024\Project\Attendance-Management-system-using-face-recognition-master\attendance.py
haarcasecade_path = "D:\\2024\\ProjectAttendance\\AMSP\\haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "D:\\2024\\ProjectAttendance\\AMSP\\TrainingImageLabel\\Trainner.yml"
)
trainimage_path = "D:\\2024\\ProjectAttendance\\AMSP\\TrainingImage"
studentdetail_path = (
    "D:\\2024\\ProjectAttendance\\AMSP\\StudentDetails\\studentdetails.csv"
)
attendance_path = "D:\\2024\\ProjectAttendance\\AMSP\\Attendance"

def open_attendance_management():
    window.deiconify()
    login_window.withdraw()

window = Tk()
window.title("Face recognizer")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="#222831")
window.withdraw()

# Create login window
login_window = tk.Toplevel()
login_window.title("Login System")
login_window.geometry("1280x720")
login_window.configure(background="#222831")
# bg="#222831", fg="#F5DD61", font=("Arial", 12)

tk.Label(login_window, text="Username", bg="#222831", fg="#F5DD61",font=("times", 20, " bold ")).place(x=640,y=200)
entry_username = tk.Entry(login_window,font=("Arial", 12), bg="#393E46", fg="#EEEEEE", insertbackground="#EEEEEE", highlightthickness=2, highlightcolor="#00ADB5")
entry_username.pack()
entry_username.place(x=600,y=260)


tk.Label(login_window, text="Password", bg="#222831", fg="#F5DD61",font=("times", 20, " bold ")).place(x=640,y=300)
entry_password = tk.Entry(login_window, show="*",font=("Arial", 12), bg="#393E46", fg="#EEEEEE", insertbackground="#EEEEEE", highlightthickness=2, highlightcolor="#00ADB5")
entry_password.pack()
entry_password.place(x=600,y=360)

tk.Button(login_window, text="Signup", command=signup,
    font=("times new roman", 16),
    fg="#F31559",
    height=1,
    width=6,
    highlightthickness=2, highlightcolor="#00ADB5"
).place(x=600, y=430)
tk.Button(login_window, text="Login", command=login,
    font=("times new roman", 16),
    fg="#F31559",
    height=1,
    width=6,
    highlightthickness=2, highlightcolor="#00ADB5"
).place(x=700, y=430)
tk.Button(
    login_window,
    text="EXIT",
    bd=10,
    command=quit,
    font=("times new roman", 16),
    bg="black",
    fg="#F31559",
    height=2,
    width=17,
).place(x=580, y=500)


# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="black")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="#E1F0DA",
        bg="black",
        font=("times", 20, " bold "),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="#E1F0DA",
        bg="black",
        width=9,
        height=1,
        activebackground="Red",
        font=("times", 20, " bold "),
    ).place(x=110, y=50)


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


logo = Image.open("UI_Image/rvsLogo.png")
logo = logo.resize((50, 47), Image.ANTIALIAS)
logo1 = ImageTk.PhotoImage(logo)
titl = tk.Label(window, bg="black", relief=RIDGE, bd=10, font=("arial", 35))
titl.pack(fill=X)
l1 = tk.Label(window, image=logo1, bg="white",)
l1.place(x=400, y=10) #x=470

titl = tk.Label(
    window, text="RVS College of Engineering & Technology !!", bg="black", fg="white", font=("arial", 20),
)
titl.place(x=480, y=12)

a = tk.Label(
    window,
    text="Welcome to the Face Recognition Based\nAttendance Management System",
    bg="#161A30",
    fg="#FCF5ED",
    bd=10,
    font=("arial", 35),
)
a.pack()

ri = Image.open("UI_Image/register.png")
r = ImageTk.PhotoImage(ri)
label1 = Label(window, image=r)
label1.image = r
label1.place(x=100, y=270)

ai = Image.open("UI_Image/attendance.png")
a = ImageTk.PhotoImage(ai)
label2 = Label(window, image=a)
label2.image = a
label2.place(x=980, y=270)

vi = Image.open("UI_Image/verifyy.png")
v = ImageTk.PhotoImage(vi)
label3 = Label(window, image=v)
label3.image = v
label3.place(x=600, y=270)


def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#222831")
    ImageUI.resizable(0, 0)
    titl = tk.Label(ImageUI, bg="black", relief=RIDGE, bd=10, font=("arial", 35))
    titl.pack(fill=X)
    # image and title
    titl = tk.Label(
        ImageUI, text="Register Your Face", bg="black", fg="#E1F0DA", font=("arial", 30),
    )
    titl.place(x=270, y=12)

    # heading
    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="black",
        fg="#F5DD61",
        bd=10,
        font=("arial", 24),
    )
    a.place(x=280, y=75)

    # ER no
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=10,
        height=2,
        bg="black",
        fg="#F5DD61",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 12),
    )
    lbl1.place(x=120, y=130)
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="black",
        fg="#F5DD61",
        relief=RIDGE,
        font=("times", 25, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="black",
        fg="#F5DD61",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 12),
    )
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="black",
        fg="#F5DD61",
        relief=RIDGE,
        font=("times", 25, "bold"),
    )
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="black",
        fg="#F5DD61",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 12),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="black",
        fg="#F5DD61",
        relief=RIDGE,
        font=("times", 12, "bold"),
    )
    message.place(x=250, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # take Image button
    # image
    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("times new roman", 18),
        bg="black",
        fg="#F5DD61",
        height=2,
        width=12,
        relief=RIDGE,
    )
    takeImg.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # train Image function call
    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("times new roman", 18),
        bg="black",
        fg="#F5DD61",
        height=2,
        width=12,
        relief=RIDGE,
    )
    trainImg.place(x=360, y=350)


r = tk.Button(
    window,
    text="Register a new student",
    command=TakeImageUI,
    bd=10,
    font=("times new roman", 16),
    bg="black",
    fg="#F5DD61",
    height=2,
    width=17,
)
r.place(x=100, y=520)


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


r = tk.Button(
    window,
    text="Take Attendance",
    command=automatic_attedance,
    bd=10,
    font=("times new roman", 16),
    bg="black",
    fg="#F5DD61",
    height=2,
    width=17,
)
r.place(x=600, y=520)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


r = tk.Button(
    window,
    text="View Attendance",
    command=view_attendance,
    bd=10,
    font=("times new roman", 16),
    bg="black",
    fg="#F5DD61",
    height=2,
    width=17,
)
r.place(x=1000, y=520)
r = tk.Button(
    window,
    text="EXIT",
    bd=10,
    command=quit,
    font=("times new roman", 16),
    bg="black",
    fg="#F31559",
    height=2,
    width=17,
)
r.place(x=600, y=660)

window.mainloop()

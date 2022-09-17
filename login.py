from tkinter import *
from tkinter import messagebox
import pymysql
import pyttsx3
import speech_recognition as sr
from PIL import Image, ImageTk


def talk(text):
    """This method is used for command given to program"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def compose_email():
    """This method is used for destroying login page so that dashboard page can run"""
    root.destroy()


def dashboard():
    import dashBoard


class Login:

    def __init__(self, root):
        self.root = root
        self.root.title("Login Form")
        self.root.geometry("1920x800+0+0")
        self.root.config(bg="white")

        # Background Image
        self.bg = Image.open("a7.jpg").resize((1920, 800), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.bg)
        bg = Label(self.root, image=self.photo)
        bg.pack()

        # login frame
        self.front = Image.open("a6.jpg").resize((500, 400), Image.ANTIALIAS)
        self.photo1 = ImageTk.PhotoImage(self.front)

        label_front = Label(self.root, image=self.photo1)
        title = Label(self.root, text="Sign In", font=("times new roman", 26, "bold"), bg="#C1CECE", fg="green")
        email_name = Label(self.root, text="Email/Username", font=("times new roman", 18, "bold"),
                           bd=0, bg="white", fg="blue")
        pass_name = Label(self.root, text="Password", font=("times new roman", 18, "bold"), bg="white", fg="blue")

        label_front.place(x=480, y=150)
        title.place(x=640, y=168, width=200)
        email_name.place(x=500, y=260, width=200)
        pass_name.place(x=500, y=360)

        # Entry box variable with voice command
        talk("Now, We are on the login page")
        talk("Please Speak your email")
        self.entry_email = StringVar(self.root, self.get_info())
        talk("Please speak your password")
        self.entry_pass = StringVar(self.root, self.get_info())
        talk("Speak login")

        # Condition for login
        value = self.get_info()
        if 'login' == value:
            self.login1()

        # These are all the entry box
        e_value = Entry(self.root, textvariable=self.entry_email, font=('times new roman,', 15, 'bold'), bg='lightgray')
        pass_value = Entry(self.root, textvariable=self.entry_pass, font=('times new roman,', 15, 'bold'),
                           bg='lightgray')
        btn_login = Button(self.root, text="Login", fg="white", bg="purple", command=self.login1,
                           font=("times new roman", 18, "bold"), cursor="hand2")
        or_lable = Label(self.root, text="Or", font=("times new roman", 15, "bold"))
        btn_regi = Button(self.root, text="Register new Account?", bd=0, font=("times new roman", 15, "bold"),
                          cursor="hand2", fg="blue")

        e_value.place(x=500, y=300, width=300)
        pass_value.place(x=500, y=400, width=300)
        btn_login.place(x=500, y=470, width=150)
        or_lable.place(x=680, y=480)
        btn_regi.place(x=740, y=475)

    def get_info(self):
        """This method is used for getting voice commands from the user"""
        listener = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source, duration=1)
                talk("Speak now")
                print('listening...')
                voice = listener.listen(source)
                info = listener.recognize_google(voice)
                print(info.replace(" ", ""))
                return info.lower().replace(" ", "")
        except EXCEPTION as es:
            # messagebox.showerror("Error", f" Error due to {str(es)}", parent=self.root)
            talk("I didn't get you, Can you please speak again")
            self.get_info()

    def login1(self):
        """This method is used for checking login condition is provided correctly or not and also checks
            many conditions"""
        if self.entry_email.get() == "" or self.entry_pass.get() == "":
            talk("All fields are required")
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="registration_data")
                cur = con.cursor()
                cur.execute("select * from rdata where email=%s and password=%s",
                            (self.entry_email.get(), self.entry_pass.get()))
                row = cur.fetchone()
                if row is None:
                    talk("Invalid Username or Password")
                    messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
                else:
                    talk("Email and Password has been matched")
                    messagebox.showinfo("Success", "Login Successfully", parent=self.root)
                    compose_email()
                    dashboard()

                con.close()
            except EXCEPTION as es:
                messagebox.showerror("Error", f" Error due to {str(es)}", parent=self.root)


root = Tk()
obj = Login(root)
root.mainloop()

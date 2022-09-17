from tkinter import *
from tkinter import messagebox
import pymysql
import pyttsx3
import speech_recognition as sr
from PIL import Image, ImageTk


def talk(text):
    """This method is used for command given to program"""
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)
    engine.say(text)
    engine.runAndWait()


def login_window():
    """This method is used for importing login page inside register page"""
    import login


def destroy_register():
    """This method is used for destroying register page so that login page can run"""
    root.destroy()


class Register:
    # Constructor
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Form")
        self.root.geometry("1920x800+0+0")
        self.root.config(bg="white")

        # Background Image
        self.bg = Image.open("a1.jpg").resize((1920, 800), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.bg)
        bg = Label(self.root, image=self.photo)
        bg.place(x=300, y=0)

        # Front image
        self.bg1 = Image.open("a2.jpg").resize((400, 500), Image.ANTIALIAS)
        self.photo1 = ImageTk.PhotoImage(self.bg1)
        front = Label(self.root, image=self.photo1)
        front.place(x=80, y=150)

        # Registration frame
        frame = Frame(self.root, bg="white")
        frame.place(x=485, y=150, width=900, height=503)
        title = Label(frame, text="REGISTER HERE", font=("times new roman", 30, "bold"), bg="white", fg="purple")
        title.place(x=30, y=10)

        # Labels for form
        f_name = Label(frame, text="First Name", font=("times new roman", 15, "bold"), bg="white", fg="blue")
        l_name = Label(frame, text="Last Name", font=("times new roman", 15, "bold"), bg="white", fg="blue")
        email_name = Label(frame, text="Email/Username", font=("times new roman", 15, "bold"), bg="white", fg="blue")
        pass_name = Label(frame, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="blue")
        confir_pass_name = Label(frame, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white",
                                 fg="blue")

        f_name.place(x=30, y=100)
        l_name.place(x=30, y=150)
        email_name.place(x=30, y=200)
        pass_name.place(x=30, y=250)
        confir_pass_name.place(x=30, y=300)

        # Command vise entry box variables
        talk("Now, We are on the Registration page, Provide Each details carefully")
        talk("Please Speak your first name")
        self.entry_fname = StringVar(frame, self.get_info())
        talk("Please Speak your Last name")
        self.entry_lname = StringVar(frame, self.get_info())
        talk("Please Speak your email ID")
        self.entry_email = StringVar(frame, self.get_info())
        talk("Please Speak your Password")
        self.entry_pass = StringVar(frame, self.get_info())
        talk("Please Speak your Password again for confirmation")
        self.entry_conf_pass = StringVar(frame, self.get_info())
        talk("Please Speak register for registration")

        # Condition for register
        value_cont = self.get_info()
        if 'register' == value_cont:
            self.register_data()

        # These are the Entry box
        f_name = Entry(frame, textvariable=self.entry_fname, font=('times new roman,', 15, 'bold'), bg='lightgray')
        l_name = Entry(frame, textvariable=self.entry_lname, font=('times new roman,', 15, 'bold'), bg='lightgray')
        e_value = Entry(frame, textvariable=self.entry_email, font=('times new roman,', 15, 'bold'), bg='lightgray')
        pass_value = Entry(frame, textvariable=self.entry_pass, font=('times new roman,', 15, 'bold'), bg='lightgray')
        conf_pass_value = Entry(frame, textvariable=self.entry_conf_pass, font=('times new roman,', 15, 'bold'),
                                bg='lightgray')
        btn_register = Button(frame, text="Register Now", fg="white", bg="green", font=("times new roman", 18, "bold"),
                              cursor="hand2", command=self.register_data)
        btn_login = Button(self.root, text="Sign In", command='login_window', fg="white", bg="purple",
                           font=("times new roman", 18, "bold"),
                           cursor="hand2")

        f_name.place(x=230, y=100)
        l_name.place(x=230, y=150)
        e_value.place(x=230, y=200)
        pass_value.place(x=230, y=250)
        conf_pass_value.place(x=230, y=300)
        btn_register.place(x=50, y=370, width=370)
        btn_login.place(x=214, y=540, width=150)

    def clear(self):
        """This is clear method used for clear all the entry box once successful submission will be done by user"""
        self.entry_fname.set('')
        self.entry_lname.set('')
        self.entry_email.set('')
        self.entry_pass.set('')
        self.entry_conf_pass.set('')

    def get_info(self):
        listener = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source, duration=1)
                talk("Speak now")
                print('listening...')
                voice = listener.listen(source, timeout=10)
                info = listener.recognize_google(voice)
                print(info)
                return info.lower().replace(" ", "")
        except Exception as es:
            # messagebox.showerror("Error", f" Error due to {str(es)}", parent=self.root)
            talk("I didn't get you, Can you please speak again")
            self.get_info()

    def register_data(self):
        """This method is used for registration of data into the field and for checking whether the entered data
                is filled correctly or not. Also checks embed data into the Database table"""

        if (self.entry_fname.get() == "" or self.entry_lname.get() == "" or
                self.entry_email.get() == "" or self.entry_pass.get() == "" or self.entry_conf_pass == ""):
            talk("All fields are required")
            messagebox.showerror("Error", "All fields are required", parent=self.root)

        elif self.entry_pass.get() != self.entry_conf_pass.get():
            talk("Password And Confirm Password Should Be Same")
            messagebox.showerror("Error", "Password And Confirm Password Should Be Same", parent=self.root)

        else:

            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="registration_data")
                cur = con.cursor()
                cur.execute("select * from rdata where email=%s", self.entry_email.get())
                row = cur.fetchone()
                if row is not None:
                    talk("User Already Exist, Please try with another Email")
                    messagebox.showerror("Error", "User Already Exist, Please try with another Email")
                else:
                    cur.execute("insert into rdata (f_name, l_name, email, password) values (%s,%s,%s,%s)",
                                (self.entry_fname.get(),
                                 self.entry_lname.get(),
                                 self.entry_email.get(),
                                 self.entry_pass.get()))
                    con.commit()
                    con.close()
                    talk("Registered Successfully")
                    messagebox.showinfo("Success", "Register Successfully", parent=self.root)
                    self.clear()
                    destroy_register()
                    login_window()

            except Exception as es:
                messagebox.showerror("Error", f"Error due to : {str(es)}", parent=self.root)


root = Tk()
obj = Register(root)
root.mainloop()

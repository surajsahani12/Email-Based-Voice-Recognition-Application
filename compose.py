import smtplib
import speech_recognition as sr
import pyttsx3
from email.message import EmailMessage

def welcome(self):
    engine = pyttsx3.init()
    engine.say("Do you want to compose email")
    engine.runAndWait()


def emi(self):
    engine = pyttsx3.init()
    engine.say("please enter email for confirmation")
    engine.runAndWait()


def passw(self):
    engine = pyttsx3.init()
    engine.say("please enter password for confirmation")
    engine.runAndWait()


listener = sr.Recognizer()

def get_info(self):
    try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source, duration=5)
                print('listening...')
                voice = listener.listen(source)
                info = listener.recognize_google(voice)
                print(info)
                return info.lower()
    except:
        pass

def get_info1(self):
        listener = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source, duration=1)
                print('listening...')
                voice = listener.listen(source)
                info = listener.recognize_google(voice)
                print(info)
                return info.lower().replace(" ", "")
        except:
            pass


engine = pyttsx3.init()
def talk(self, text):
        engine.say(text)
        engine.runAndWait()

def send_email(self, receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Make sure to give app access in your Google account
    server.login(r,b)
    email = EmailMessage()
    email['From'] = 'Sender_Email'
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)

sender_email_list = {'1':'surajsahani80977@gmail.com', '2':'surajsahani8977@gmail.com', 'tu':'surajsahani8977@gmail.com'}
email_list = {
        'suraj' : 'surajsa@sjcem.edu.in',
        'sushil' : 'sushily@sjcem.edu.in'
    }


def get_email_info(self):
    talk('To whom you want to send mail')
    name = get_info()
    receiver = email_list[name]
    print(receiver)
    talk('What is the subject of your email?')
    subject = get_info()
    talk('Tell me the text in your email')
    message = get_info()
    send_email(receiver, subject, message)
    talk('Hey lazy ass. Your email is sent')
    talk('Do you want to send more email?')
    send_more = get_info()
    if 'yes' in send_more:
        get_email_info()
    else:
        exit()

self.emi()
a = self.get_info1()
r = sender_email_list[a]
print(r)
self.passw()
b = self.get_info1()
self.welcome()
value = get_info()
if 'yes' == value:
    self.get_email_info()




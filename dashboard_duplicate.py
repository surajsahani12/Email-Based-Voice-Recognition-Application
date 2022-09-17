from __future__ import print_function
import smtplib
import time
from email.message import EmailMessage
from tkinter import *
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials




def send_email(receiver, subject, text):
    """This method is used for sending mail in real time"""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Make sure to give app access in your Google account
    server.login('your gmail ', 'your password')
    email = EmailMessage()
    email['From'] = 'Sender_Email'
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(text)
    server.send_message(email)


class DashBoard:
    def __init__(self, root):
        self.root = root
        self.from_name = None
        self.entry_subject = None
        self.entry_to = None
        self.entry_body = None
        self.to_name = None
        self.entry_from = None
        self.to = None
        self.content = []
        self.body = None
        self.root.title("DashBoard")
        self.root.geometry("1920x800+0+0")
        self.root.config(bg="blue")

        # Frame for left side
        self.frame = Frame(self.root, bg='white', highlightbackground='purple', highlightthickness=5).place(x=20, y=50, height=700, width=280)
        self.frame2 = Frame(self.root, bg='white', highlightbackground='gray', highlightthickness=5).place(x=310, y=50, height=700, width=1200)
        self.frame3 = Frame(self.root, bg='white', highlightbackground='red', highlightthickness=5).place(x=450, y=7, height=40, width=900)
        label = Label(self.frame3, text="Welcome to S-Mail Dashboard", bg='white', font=("times new roman", 22, "bold")).place(x=650, y=7, width=500)


        self.email_list = {
            'name1': 'anyofyouremail1',
            'name2': 'anyofyouremail2'
        }

        value = input()
        if 'inbox' == value:
            self.check_email()
        elif 'compose' == value:
            self.compose()
        else:
            exit()
        # self.content = []
        query = input()
        if 'sent' in query:
            self.send_mail()

        # Compose button
        self.comp_btn = Image.open("mail.png").resize((260, 150), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.comp_btn)
        comp = Label(self.frame, image=self.photo, bg='white', bd=0)
        com_btn = Button(image=self.photo, bd=0, bg='white', borderwidth=0, activebackground='white',
                         command=self.compose, cursor='hand2')
        comp.place(x=25, y=70)
        com_btn.place(x=25, y=70)

        # Inbox, sent mail, Trash mail buttons and images
        self.inbox = Image.open("inbox.png").resize((30, 30), Image.ANTIALIAS)
        self.photo1 = ImageTk.PhotoImage(self.inbox)
        in_label = Label(self.frame, image=self.photo1, bg='white')
        inbox_btn = Button(self.frame, text='Inbox', command=self.check_email, bg='white', bd=0,
                           font=("times new roman", 16, "bold"), activebackground='white', cursor='hand2')

        self.sent = Image.open("sent.png").resize((30, 30), Image.ANTIALIAS)
        self.photo2 = ImageTk.PhotoImage(self.sent)
        sent_label = Label(self.frame, image=self.photo2, bg='white')
        sent_btn = Button(self.frame, text='Sent Mail', bg='white', bd=0, font=("times new roman", 16, "bold"),
                          activebackground='white', command=self.send_mail, cursor='hand2')

        self.trash = Image.open("trash_mail.png").resize((30, 30), Image.ANTIALIAS)
        self.photo3 = ImageTk.PhotoImage(self.trash)
        trash_label = Label(self.frame, image=self.photo3, bg='white')
        trash_btn = Button(self.frame, text='Trash Mail', bg='white', bd=0, font=("times new roman", 16, "bold"),
                           activebackground='white', cursor='hand2')

        in_label.place(x=50, y=200)
        inbox_btn.place(x=95, y=200)
        sent_label.place(x=50, y=250)
        sent_btn.place(x=95, y=250)
        trash_label.place(x=50, y=300)
        trash_btn.place(x=95, y=300)

        # Label and ScrollText for Emails
        body_label = Label(self.frame2, text="Emails:", font=("times new roman", 15, "bold"))
        body_label.place(x=350, y=100)
        text_area = scrolledtext.ScrolledText(self.root, wrap=WORD, width=100, height=20, font=("Times New Roman", 15))
        # text_area.place(column=1, pady=140, padx=350)
        text_area.place(x=350 ,y=140)
        self.lst_mails = '\n'.join(self.content)
        text_area.insert(INSERT, self.lst_mails)

    def send_mail(self):
        """Shows basic usage of the Gmail API.
                   Lists the user's Gmail labels.
                   """
        global msg
        cred = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            cred = Credentials.from_authorized_user_file('token.json', self.SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not cred or not cred.valid:
                if cred and cred.expired and cred.refresh_token:
                    cred.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    cred = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(cred.to_json())

            service = build('gmail', 'v1', credentials=cred)

            # # Call the Gmail API
            # results = service.users().labels().list(userId='me').execute()
            # labels = results.get('labels', [])

            # Get messages
            results = service.users().messages().list(userId='me', labelIds=['SENT']).execute()
            messages = results.get('messages', [])

            # if not Messages:
            if not messages:
                print('You have no sent mails.')
            else:
                message_count = 0
                for message in messages:
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                    message_count = message_count + 1
                print("You have " + str(message_count) + " sent mails.")
                new_message_choice = input()
                if 'yes' == new_message_choice:
                    read_number = int(input())
                    for message1 in messages[:read_number]:
                        msg1 = service.users().messages().get(userId='me', id=message1['id']).execute()
                        email_data = msg1['payload']['headers']
                        for values in email_data:
                            name = values["name"]
                            if name == "To":
                                self.to_name = values["value"]
                                print("You sent mail to:-" + self.to_name)
                                time.sleep(1)
                                self.to = msg1['snippet'][:300]
                                self.content.append(self.to)
                                self.content.append(self.to_name)
                                print("  " + msg1['snippet'][:300] + "...")
                                print("\n")
                else:
                   print("See you soon")

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def check_email(self):
        """Shows basic usage of the Gmail API.
            Lists the user's Gmail labels.
            """
        global msg
        cred = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            cred = Credentials.from_authorized_user_file('token.json', self.SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not cred or not cred.valid:
                if cred and cred.expired and cred.refresh_token:
                    cred.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    cred = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(cred.to_json())

            service = build('gmail', 'v1', credentials=cred)

            # # Call the Gmail API
            # results = service.users().labels().list(userId='me').execute()
            # labels = results.get('labels', [])

            # Get messages
            results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
            messages = results.get('messages', [])

            # if not labels:
            if not messages:
                print('You have no new message.')
            else:
                message_count = 0
                for message in messages:
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                    message_count = message_count + 1
                print("You have " + str(message_count) + " unread message.")
                new_message_choice = input()
                if 'yes' == new_message_choice:
                    print("Please speak number of messages do you want me to read")
                    read_number = int(input())
                    for message1 in messages[:read_number]:
                        msg1 = service.users().messages().get(userId='me', id=message1['id']).execute()
                        email_data = msg1['payload']['headers']
                        for values in email_data:
                            name = values["name"]
                            if name == "From":
                                self.from_name = values["value"]
                                print("You have new messages from:-" + self.from_name)
                                time.sleep(1)
                                self.body = msg1['snippet'][:30]
                                self.content.append(self.body)
                                self.content.append(self.from_name)
                                print(self.content)
                                print("  " + msg1['snippet'][:30] + "...")
                                print("\n")
                else:
                    print("See you soon")

    def compose(self):
        new = Toplevel(self.root)
        new.geometry("500x400+1000+300")
        new.config(bg='white')
        new.title("Compose")

        from_label = Label(new, text="From", font=("times new roman", 14, "bold"))
        to_label = Label(new, text="To", font=("times new roman", 14, "bold"))
        subject_label = Label(new, text="Subject", font=("times new roman", 14, "bold"))
        body_label = Label(new, text="Body:", font=("times new roman", 14, "bold"))

        from_label.place(x=30, y=20)
        to_label.place(x=30, y=60)
        subject_label.place(x=30, y=100)
        body_label.place(x=30, y=140)

        self.entry_from = StringVar(self.root, 'surajsahani80977@gmail.com')
        entry_from_value = Entry(new, textvariable=self.entry_from, font=("times new roman", 15, "italic"),
                                 borderwidth=2, relief=SUNKEN)


        self.entry_to = StringVar()
        entry_to_value = Entry(new, textvariable=self.entry_to, font=("times new roman", 15, "italic"),
                               borderwidth=2, relief=SUNKEN)

        self.entry_subject = StringVar()
        entry_sub_value = Entry(new, textvariable=self.entry_subject, font=("times new roman", 15, "italic"),
                                borderwidth=2, relief=SUNKEN)

        self.entry_body = StringVar()
        entry_body_value = Entry(new, textvariable=self.entry_body, font=("times new roman", 15, "bold"),
                                 borderwidth=2, relief=SUNKEN)

        send_btn = Button(new, text='Send', command=send_email, font=("times new roman", 14, "bold"),
                          activebackground='white', cursor='hand2')

        entry_from_value.place(x=100, y=20, width=300, height=30)
        entry_to_value.place(x=100, y=60, width=400, height=30)
        entry_sub_value.place(x=100, y=100, width=400, height=30)
        entry_body_value.place(x=100, y=140, width=400, height=200)
        send_btn.place(x=430, y=350)
        # send_email(receiver, subject, text)
        # send_more = input()
        # if 'yes' in send_more:
        #     self.__init__(root)
        # # else:
        #     exit()



root = Tk()
dash = DashBoard(root)
root.mainloop()

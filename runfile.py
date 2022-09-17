import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import playsound as playsound
from googletrans import Translator


def question(user_val):
    text = gTTS(text=user_val, lang='hi')
    playsound.playsound('user1.mp3')


def speak_Now(user_val):
    text = gTTS(text=user_val, lang='hi')
    playsound.playsound('user2.mp3')


def speak_Again(user_val):
    text = gTTS(text=user_val, lang='hi')
    playsound.playsound('user3.mp3')


def speak_again(user_val):
    text = gTTS(text=user_val, lang='hi')
    playsound.playsound('user6.mp3')


def app_Closed(user_val):
    text = gTTS(text=user_val, lang='hi')
    playsound.playsound('user4.mp3')


def respeak(user_val):
    text = gTTS(text=user_val, lang='hi')
    # text.save('user7.mp3')
    playsound.playsound('user7.mp3')


def register_window():
    import register


def login_window():
    import login


def trans(value):
    translator = Translator()
    translated_text = translator.translate(value, src='hi', dest='en')
    speech = str(translated_text.text).lower()
    print(speech)
    return speech


def talk(text):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[2].id)
    engine.say(text)
    engine.runAndWait()


def get_info():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            speak_Now(" Speak now")
            print("Listening...")
            voice = listener.listen(source)
            # listener.adjust_for_ambient_noise(source, duration=3)
            info = listener.recognize_google(voice, language='hi-In')
            # talk(info)
            print(info)
            return info.lower()
    except Exception as es:
        respeak("Kripaya karke phir se boliye")
        get_info()


def get_info_eng():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            speak_Now(" Speak now")
            print("Listening...")
            voice = listener.listen(source)
            # listener.adjust_for_ambient_noise(source, duration=3)
            info = listener.recognize_google(voice)
            # talk(info)
            print(info)
            return info.lower()
    except Exception as es:
        talk("I didn't get you, Can you please speak again")
        get_info_eng()


talk(" Welcome to Voice based Email system for visually Impaired people")
talk(" Choose languages, Hindi or English")
language = get_info_eng()
if 'hindi' in language:
    question(" Aap registration karna chahenge yaa login karna chahenge yaa application band karna chahenge")
    count = 0
    count1 = 0
    value = get_info()
    while value is None:
        count1 += 1
        speak_again(" Phir se boliye")
        value = get_info()
        value = value
        if count1 == 3:
            app_Closed(" application band ho gayaa")
            exit()
        else:
            continue
    else:
        while 'close' not in trans(value):
            if 'register' in trans(value):
                register_window()
                break
            elif 'log in' in trans(value):
                login_window()
                break
            else:
                count += 1
                speak_Again(" Kreepya karke phir se boliye")
                print(" Please Speak again")
            value = get_info()
            if count == 3:
                app_Closed(" application band ho gaya")
                exit()
            else:
                continue

else:
    talk(" Do you want to registration, login or cancel")
    count = 0
    value = get_info_eng()
    while 'cancel' not in value:
        if 'registration' in value:
            register_window()
            break
        elif 'login' in value:
            login_window()
            break
        else:
            count += 1
            talk(" Can you please, Speak again")
            print(" Please Speak again")
        value = get_info_eng()
        if count == 3:
            app_Closed(" Application has been closed")
            exit()
        else:
            continue


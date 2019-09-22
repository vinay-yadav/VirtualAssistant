'''
Before using this code, make some changes so that it can work better
1.download and import all required packages before running it.
2.In send_email(), provide the email and password (account from which you want to send email)in account and password respectively, all in lower letters
3.Add name and email id's (of recipient) in 'emails' dictionary.
'''

import pyttsx3      # pip install pyttsx3
import pyaudio      # download using google as it gives error using pip
import datetime
import speech_recognition as sr     # pip install speechrecognition
import wikipedia    # pip install wikipedia
import webbrowser   # pip install webbrowser
import os
import smtplib      # pip install smtplib
import random
import time


engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 190)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def ext_check(path):
    ext = os.path.splitext(path)
    if ext[1] == '.mp3':
        return True


def gen(low, up):
    num = random.randrange(low, up)
    return num


def greet_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak('Good morning sir')
    elif 12 <= hour < 16:
        speak('Good afternoon sir')
    else:
        speak('Good evening sir')

    speak("I'm Jarvis, how may I help you")


def facts():
    num = gen(1, 7)
    if num is 1:
        speak("Snakes can help predict earthquakes.")
    elif num is 2:
        speak("A flock of crows is known as a murder")
    elif num is 3:
        speak("29th May is officially put a pillow on your fridge day")
    elif num is 4:
        speak("Cherophobia is an irrational fear of fun or happiness")
    elif num is 5:
        speak("Bananas are curved because they towards the sun")
    else:
        speak("During your life time, you will produce enough saliva to fill two swimming pools")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print('You said : ', query)

    except Exception as e:
        print(e)
        print('say that again please')
        speak('apologize sir, say that again please')
        return 'None'
    return query


emails = {'name_1': 'email_address_1', 'name_2': 'email_address_2'}


def send_email(to, content):
    account = os.environ.get('account_id')      # provide sender account's email_id
    password = os.environ.get('account_pass')   # provide sender account's passsword
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(user=account, password=password)
    server.sendmail(account, to, content)
    server.close()


if __name__ == '__main__':
    greet_me()
    while True:
        query = take_command().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak('According to wikipedia')
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open('youtube.com')

        elif 'open google' in query:
            webbrowser.open('google.com')

        elif 'open stackoverflow' in query:
            webbrowser.open('stackoverflow.com')

        elif 'play music' in query:
            speak('Playing music right away')
            music_dir = 'PATH'                  # provide the path of your music folder
            songs = os.listdir(music_dir)
            # print(len(songs))
            while True:
                num = gen(0, len(songs))
                song = songs[num]
                file = os.path.join(music_dir, song)
                # print(file)
                check = ext_check(file)
                if check:
                    os.startfile(file)
                    break

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"sir, the time is {strTime}")

        elif 'who made you' in query:
            speak('My master Mr.Vinay, made me for his assistance and I am happy to help him.')

        elif 'open vlc' in query:
            file_path = 'vlc.exe'   # provide the application path
            os.startfile(file_path)

        elif 'send email' in query:
            speak('To whom should I send?')
            receiver = take_command().lower()
            if receiver in emails:
                to = emails[receiver]
                try:
                    speak('what should I say?')
                    content = take_command()
                    send_email(to, content)
                    speak('Email has been sent!')
                except Exception as e:
                    print(e)
                    speak('Sorry sir but having trouble in sending mail')

            else:
                speak('Sorry sir but this person is not in your mailing list. '
                      'But you can send email by entering email id manually.')
                speak('Do you want to mail send email with custom email id?')
                decision = take_command().lower()
                if 'yes' in decision:
                    speak('Please, enter their email id sir')
                    to = input('Email: ').lower()
                    try:
                        speak('what should I say?')
                        content = take_command()
                        send_email(to, content)
                        speak('Email has been sent!')
                    except Exception as e:
                        print(e)
                        speak('Sorry sir but having trouble in sending mail')
                else:
                    speak('no problem boss')

        elif 'who are you' in query:
            os.startfile('jarvis.mp3')
            time.sleep(26)

        elif 'how are you' in query:
            speak("I'm doing great, thanks for asking. what can I help you with")

        elif 'talk to me' in query:
            num = gen(1, 6)
            if num is 1:
                speak("That's my favourite thing to do")

            elif num is 2:
                speak("For sure. Want to hear some weird facts?")
                decision = take_command().lower()
                if 'yes' in decision:
                    facts()
                else:
                    speak('No problem')

            elif num is 3:
                speak("Ok, you have my full attention")

            elif num is 4:
                speak('Sure, I like talking to you')

            else:
                speak("I'd love to talk. How are you doing today")
                take_command()
                speak('Glad to hear it. Can I do anything for you?')

        elif 'facts' in query:
            facts()

        elif 'goodbye jarvis' in query:
            speak('Bye sir, have a nice day')
            exit()

        else:
            speak("Apologize sir but I can't do this yet")

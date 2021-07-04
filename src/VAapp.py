# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 21:16:30 2021

@author: Greekshith
"""
import datetime
import os
import tkinter as tk
import webbrowser
from tkinter.scrolledtext import ScrolledText

import pyjokes
import pyttsx3
import speech_recognition as sr
import wikipedia
from ecapture import ecapture as ec

# the dictionary below has been intialized based on app locations in my computer
# locations must be changed if you need to open apps on another computer
# new apps can be added too, with key value pairs as names(or alternative names you may use) and their respective locations

cmd_dict = {
    'MSTEAMS': 'C:\\Users\\greek\\AppData\\Local\\Microsoft\\Teams\\Update.exe --processStart \"Teams.exe\"',
    'MICROSOFT TEAMS': 'C:\\Users\\greek\\AppData\\Local\\Microsoft\\Teams\\Update.exe --processStart \"Teams.exe\"',
    'TEAMS': 'C:\\Users\\greek\\AppData\\Local\\Microsoft\\Teams\\Update.exe --processStart \"Teams.exe\"',
    'CHROME': '"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"',
    'GOOGLE': '"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"',
    'BRAVE': '"C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"',
    'MSEDGE': '"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"',
    'MICROSOFT EDGE': '"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"',
    'APEX LEGENDS': '"D:\\Program Files (x86)\\Origin Games\\Apex\\r5apex.exe"',
    'BATTLE.NET': '"D:\\Battle.net\\Battle.net Launcher.exe"',
    'COD': '"D:\\Call of Duty Modern Warfare\\Modern Warfare Launcher.exe"',
    'CODW': '"D:\\Call of Duty Modern Warfare\\Modern Warfare Launcher.exe"',
    'MINDSTORMS': '"D:\\Program Files (x86)\\LEGO Software\\LEGO MINDSTORMS EV3 Home Edition\\MindstormsEV3.exe"',
    'LEGO MINDSTORMS': '"D:\\Program Files (x86)\\LEGO Software\\LEGO MINDSTORMS EV3 Home Edition\\MindstormsEV3.exe"',
    'MICMUTE': '"C:\\Program Files (x86)\\MicMute\\mic_mute.exe"',
    'VALORANT': '"C:\\Riot Games\\Riot Client\\RiotClientServices.exe" --launch-product=valorant --launch-patchline=live',
    'NOTE': 'Notepad',
    'NOTES': 'Notepad',
    'NOTEPAD': 'Notepad',
    'EDITOR': 'Notepad',
    'MS STORE': 'start ms-windows-store:',
    'MYSQL': '"C:\\Program Files\\MySQL\\MySQL Workbench 8.0 CE\\MySQLWorkbench.exe"',
    'ORIGIN': '"D:\\Origin\\Origin.exe"',
    'OUTLOOK': 'outlook',
    'POWERPOINT': 'powerpnt',
    'WORD': 'winword'
}


class VAapp():
    opindex = 1.0
    root = None
    interaction_mode = None
    voice_exit = False

    def __init__(self):
        self.opindex = 1.0
        self.root = None

    def build(self):
        # creating the GUI
        self.root = tk.Tk()
        self.root.title('Gideon')
        self.root.geometry("400x500")

        frame = tk.Frame(self.root, background="blue")
        frame1 = tk.Frame(frame, background="#a2d5c6")
        frame2 = tk.Frame(frame, background="#077b8a")
        frame3 = tk.Frame(frame, background="gray")
        frame3left = tk.Frame(frame3, background="#322e2f")
        frame3right = tk.Frame(frame3, background="#322e2f")

        frame.pack(fill='both', expand=True)

        frame1.pack(fill='both', expand=True)
        frame1.place(relheight=0.7, relwidth=1)

        frame2.pack(fill='both', expand=True)
        frame2.place(relheight=0.15, relwidth=1, relx=0, rely=0.7)

        frame3.pack(fill='both', expand=True)
        frame3.place(relheight=0.15, relwidth=1, relx=0, rely=0.85)

        frame3left.pack(fill='both', expand=True)
        frame3left.place(relheight=1, relwidth=0.7)

        frame3right.pack(fill='both', expand=True)
        frame3right.place(relheight=1, relwidth=0.3, relx=0.7, rely=0)

        micbtn = tk.Button(frame2, width=20, height=3,
                           text='RECORD VOICE', command=self.voiceinp)
        micbtn.pack(fill='none', expand=False, side='top')
        micbtn.place(relx=0.5, rely=0.5, anchor="c")

        self.input_user = tk.StringVar()
        self.msgbox = tk.Entry(frame3left, text=self.input_user)
        self.msgbox.pack(fill='both', expand=True, padx=10, pady=10)

        enterbtn = tk.Button(frame3right, text='Send', command=self.keyinp)
        enterbtn.pack(fill='both', expand=True, padx=10, pady=10)

        self.opbox = ScrolledText(frame1)
        self.opbox.pack(fill='none', expand=False, side='top')
        self.opbox.place(relheight=0.8, relwidth=1, rely=0.1)

    def run(self):
        self.opbox.after(0, self.wishMe())
        self.root.mainloop()

    def keyinp(self):
        """
        this function takes the input from the message box
        and then it uses it to perform commands based on users input
        """
        user_get = self.msgbox.get()
        self.input_user.set('')
        self.opindex = self.opbox.index(tk.END)
        self.opbox.insert(self.opindex, "USER:" + user_get + '\n' + '\n')
        self.opbox.update_idletasks()
        self.text_interaction(user_get)

    def voiceinp(self):
        """
        this function takes the voice input after pressing the record button
        and then it uses it to perform commands based on users input
        """
        user_get = self.takeCommandvoice()
        self.opindex = self.opbox.index(tk.END)
        self.opbox.insert(self.opindex, "USER:" + user_get + '\n' + '\n')
        self.opbox.update_idletasks()
        while True:
            self.voice_interaction(user_get)
            if self.voice_exit:
                self.bot_response('In text mode...')
                pyttsx3.speak('In text mode')
                self.voice_exit = False
                break
            else:
                user_get = self.takeCommandvoice()

    def bot_response(self, message):
        """
        this function displays the VA's responses
        """
        bot_response = "GIDEON: " + message + '\n' + '\n'
        self.opindex = self.opbox.index(tk.END)
        self.opbox.insert(self.opindex, bot_response)
        self.opbox.see(tk.END)
        self.opbox.update_idletasks()

    def wishMe(self):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            self.bot_response("Good Morning Sir !")
            pyttsx3.speak("Good Morning Sir !")

        elif hour >= 12 and hour < 18:
            self.bot_response("Good Afternoon Sir !")
            pyttsx3.speak("Good Afternoon Sir !")

        else:
            self.bot_response("Good Evening Sir !")
            pyttsx3.speak("Good Evening Sir !")

        self.bot_response("I am your personal assistant, Gideon")
        pyttsx3.speak("I am your personal assistant, Gideon")

    def takeCommandvoice(self):
        """
        initializing the speech recognition
        """
        r = sr.Recognizer()
        """
        using microphone as source
        """
        with sr.Microphone() as source:
            self.bot_response("Listening...")
            self.opbox.update_idletasks()
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            self.bot_response("Recognizing...")
            """
            using recognize_google for speech to text conversion
            can be replaced with other commands like recognize_sphinx if needed
            """
            a = r.recognize_google(audio, language='en-in')
            self.bot_response(f"User said: {a}\n")
            self.opbox.update_idletasks()
        except Exception as e:
            print("Printing Exception here ")
            print(e)
            self.bot_response("Unable to Recognize your voice.")
            return "None"
        return a

    def searchresult(self, a):
        b = ''
        p = ['SEE IF YOU CAN FIND ANYTHING ABOUT',
             'SEARCH THE WEB FOR', 'LOOK UP FOR', 'WHAT IS', 'SEARCH FOR', 'SEARCH']
        for i in p:
            if (i in a):
                b = a.replace(i, '')
                break
        self.bot_response('loading results')
        pyttsx3.speak('loading results')
        """
        searched will open in default browser
        """
        webbrowser.open("https://duckduckgo.com/?q=" + b)

    def openapp(self, a):
        found = False
        for key, value in cmd_dict.items():
            if key in a:
                found = True
                pyttsx3.speak("Opening " + key)
                self.bot_response(value)
                os.system(value)
        if not found:
            pyttsx3.speak(a)
            self.bot_response("Is Invalid,Please Try Again")
            pyttsx3.speak("is Invalid,Please try again")

    def tellday(self):
        day = datetime.datetime.today().weekday() + 1
        Day_dict = {1: 'Monday', 2: 'Tuesday',
                    3: 'Wednesday', 4: 'Thursday',
                    5: 'Friday', 6: 'Saturday',
                    7: 'Sunday'}

        if day in Day_dict.keys():
            self.bot_response(Day_dict[day])
            pyttsx3.speak("The day is " + str(Day_dict[day]))

    def telltime(self):
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        self.bot_response(strTime)
        pyttsx3.speak(f"Sir, the time is {strTime}")

    def text_interaction(self, user_get):
        global text_exit, default_mode
        a = user_get
        default_mode = 'text'
        a = a.upper()

        if (self.interaction_mode == 'TAKENOTE'):
            noted = user_get
            file = open("file1.txt", "w")
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            file.write(strTime)
            file.write(" :-  \n")
            file.write(noted)
            file.close()
            self.bot_response('file saved, note taken')
            self.interaction_mode = None

        elif ('SWITCH TO VOICE' in a) or ('SWAP TO VOICE' in a) or ('USE VOICE' in a):
            default_mode = 'voice'
            self.bot_response('In voice mode... click on record to begin')

        elif ('DONT' in a) or ('NEVERMIND' == a) or ('NO' == a) or ("EXIT" in a) or ("QUIT" in a) or ("CLOSE" in a):
            pyttsx3.speak("okay, exiting")
            text_exit = True

        elif ('SOLVE MATH' in a):
            webbrowser.open("https://www.wolframalpha.com/")

        elif ('TODAYS DATE' in a) or ('WHAT DAY IS IT' in a):
            self.tellday()

        elif ('WHATS THE TIME' in a) or ('TIME' in a):
            self.telltime()

        elif ('WHERE IS' in a):
            a = a.replace("WHERE IS", "")
            location = a
            self.bot_response("User asked to Locate")
            self.bot_response(location)
            webbrowser.open("https://www.google.com/maps/place/" + location)

        elif ('JOKE' in a) or ('TELL ME A JOKE' in a):
            jok = pyjokes.get_joke('en', 'neutral')
            self.bot_response(jok)

        elif ('TAKE A NOTE' in a) or ('NOTE THIS DOWN' in a):
            self.bot_response('What should i note down sir?')
            self.interaction_mode = 'TAKENOTE'

        elif ("SHOW NOTE" in a):
            pyttsx3.speak("Showing Notes")
            file = open("file1.txt", "r")
            self.bot_response(file.read())
            file.close()

        elif ('TAKE A PHOTO' in a) or ('TAKE A PICTURE' in a) or ('CLICK A PICTURE' in a):
            ec.capture(0, "Gideon Camera ", False)

        elif ('SEARCH IN WIKIPEDIA FOR' in a) or ('SEARCH WIKIPEDIA FOR' in a):
            ltemp = ['SEARCH IN WIKIPEDIA FOR', 'SEARCH WIKIPEDIA FOR']
            for i in ltemp:
                if i in a:
                    query = a.replace(i, '')
            ltemp = []
            pyttsx3.speak("Checking the wikipedia ")
            result = wikipedia.summary(query, sentences=4)
            pyttsx3.speak("According to wikipedia")
            self.bot_response(result)
            pyttsx3.speak(result)

        elif ('SEARCH' in a) or ('FIND ANYTHING' in a) or ('LOOK UP' in a) or ('WHAT IS' in a):
            self.searchresult(a)

        elif ('WHAT\'S YOUR NAME' in a) or ('TELL ME YOUR NAME' in a):
            self.bot_response('My name is Gideon')
            pyttsx3.speak('My name is Gideon')

        elif ('HEY GIDEON' in a):
            self.bot_response('How may i help you sir?')
            pyttsx3.speak('how may i help you sir')

        else:
            self.openapp(a)

    def voice_interaction(self, user_get):
        global default_mode
        default_mode = 'voice'
        a = user_get
        a = a.upper()

        if ('SWITCH TO TEXT' in a) or ('SWAP TO TEXT' in a) or ('USE TEXT' in a):
            default_mode = 'text'
            self.bot_response('In text mode... enter query in box below')
            self.voice_exit = True

        elif ('DON\'T' in a) or ('NEVERMIND' == a) or ('NO' == a) or ("EXIT" in a) or ("QUIT" in a) or ("CLOSE" in a):
            pyttsx3.speak("okay, exiting")
            self.voice_exit = True

        elif ('SOLVE MATH' in a):
            webbrowser.open("https://www.wolframalpha.com/")

        elif ('TODAYS DATE' in a) or ('WHAT DAY IS IT' in a):
            self.tellday()

        elif ('WHATS THE TIME' in a) or ('TIME' in a):
            self.telltime()

        elif ('WHERE IS' in a):
            a = a.replace("WHERE IS", "")
            pyttsx3.speak("User asked to Locate")
            pyttsx3.speak(a)
            webbrowser.open("https://www.google.com/maps/place/" + a)

        elif ('TELL ME A JOKE' in a) or ('JOKE' in a):
            jok = pyjokes.get_joke('en', 'neutral')
            self.bot_response(jok)
            pyttsx3.speak(jok)

        elif ('TAKE A NOTE' in a) or ('NOTE THIS DOWN' in a):
            self.bot_response('what should i note down sir')
            pyttsx3.speak('what should i note down sir')
            noted = self.takeCommandvoice()
            file = open("file1.txt", "w")
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            file.write(strTime)
            file.write(" :-  \n")
            file.write(noted)
            file.close()
            self.bot_response('file saved, note taken')
            pyttsx3.speak('note taken')

        elif ("SHOW NOTE" in a):
            pyttsx3.speak("Showing Notes")
            file = open("file1.txt", "r")
            self.bot_response(file.read())
            file.close()

        elif ('TAKE A PHOTO' in a) or ('TAKE A PICTURE' in a) or ('CLICK A PICTURE' in a):
            ec.capture(0, "Gideon Camera ", False)

        elif ('SEARCH IN WIKIPEDIA FOR' in a) or ('SEARCH WIKIPEDIA FOR' in a):
            ltemp = ['SEARCH IN WIKIPEDIA FOR', 'SEARCH WIKIPEDIA FOR']
            for i in ltemp:
                if i in a:
                    query = a.replace(i, '')
            ltemp = []
            pyttsx3.speak("Checking the wikipedia ")
            result = wikipedia.summary(query, sentences=4)
            pyttsx3.speak("According to wikipedia")
            self.bot_response(result)
            pyttsx3.speak(result)

        elif ('SEARCH' in a) or ('FIND ANYTHING' in a) or ('LOOK UP' in a) or ('WHAT IS' in a):
            self.searchresult(a)

        elif ('WHAT\'S YOUR NAME' in a) or ('TELL ME YOUR NAME' in a):
            self.bot_response('My name is Gideon')
            pyttsx3.speak('My name is Gideon')

        elif ('HEY GIDEON' in a):
            """
            the pyttsx3 module doesn't recognize the word gideon
            """
            pyttsx3.speak('how may i help you sir')

        else:
            self.openapp(a)

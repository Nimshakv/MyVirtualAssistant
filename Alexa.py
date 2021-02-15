import speech_recognition as sr
import pyttsx3 as pt
import pyaudio
import pywhatkit as kit
import datetime
from datetime import date


class Alexa:
    def __init__(self):
        self.engine = pt.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        kit.playonyt("hello")

    def start(self):
        self.wish_me()
        self.talk('What can I do for you')

        while True:
            command = self.listen()
            if command is not None:
                self.process_command(command)

    def wish_me(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.talk("Hello,Good Morning")
            print("Hello,Good Morning")
        elif 12 <= hour < 18:
            self.talk("Hello,Good Afternoon")
            print("Hello,Good Afternoon")
        else:
            self.talk("Hello,Good Evening")
            print("Hello,Good Evening")

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language='en-in')
            print(command)
            command = command.lower()
            if 'geezer' in command:
                command = command.replace('alexa', '')
                return command
        except sr.UnknownValueError:
            self.talk('Pardon, please try that again')
        except sr.RequestError as e:
            self.talk('Pardon, please try that again')
        return None

    def process_command(self, command):
        print(command)
        if 'play' in command:
            print(command)
            song = command.replace('play', '')
            self.talk(f'you want me to play {song} in youtube. Is that correct?')
            if self.is_yes():
                print(command)
                self.talk(f'playing {command}')
                kit.playonyt(command)
            else:
                self.talk('Oh Oh! Please try that again.')
                self.listen()

        elif 'time' in command:
            time = datetime.datetime.now()
            print(type(time))
            time = time.strftime("%H:%M:%S")
            self.talk(f'Current time is {time}')

        elif 'date' in command:
            today = date.today()
            self.talk(f'Today is {today}')

        elif 'search' in command:
            command = command.replace('search', '')
            kit.search(command)

        # if 'wikipedia' in command:

    def is_yes(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language='en-in')
            print(command)
            command = command.lower()
            if 'yes' in command:
                return True
        except sr.UnknownValueError:
            self.talk('Pardon, please try that again')
        except sr.RequestError as e:
            self.talk('Pardon, please try that again')
        return False

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":
    ax = Alexa()
    # ax.start()
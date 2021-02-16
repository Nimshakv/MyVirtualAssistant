import speech_recognition as sr
import pyttsx3 as pt
import pyaudio
import pywhatkit as kit
import datetime
from datetime import date
import wikipedia
import webbrowser
from urllib.request import urlopen
import constants
import re
import random


class VirtualAssistant:
    def __init__(self):
        self.speech_recognizer = sr.Recognizer()
        self.engine = pt.init()

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)

    def start(self):
        self.wish_me()
        self.talk(constants.FIRST_QUESTION)
        self.take_command()

    def take_command(self):
        while True:
            command = self.listen()
            self.process_command(command)

    def listen(self):
        with sr.Microphone() as source:
            print("Say something!")
            self.speech_recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.speech_recognizer.listen(source)
        try:
            command = self.speech_recognizer.recognize_google(audio, language='en-in')
        except sr.UnknownValueError:
            command = self.listen()
        except sr.RequestError as e:
            command = self.listen()
        return command

    def is_yes(self):
        with sr.Microphone() as source:
            self.speech_recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.speech_recognizer.listen(source)
        try:
            command = self.speech_recognizer.recognize_google(audio, language='en-in')
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

    def wish_me(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.talk(constants.HELLO + constants.GOOD_MORNING)
        elif 12 <= hour < 18:
            self.talk(constants.HELLO + constants.GOOD_AFTERNOON)
        else:
            self.talk(constants.HELLO + constants.GOOD_EVENING)

    def process_command(self, command):
        print(command)

        # random questions
        if constants.HELLO or constants.HI or constants.HEY in command:
            self.talk(constants.HELLO)
        elif constants.ARE_YOU_THERE in command:
            self.talk(constants.AM_HERE)

        # tasks
        elif constants.PLAY in command:
            song = command.replace(constants.PLAY, '')
            self.talk(f'you want me to play {song} in youtube. Am I right?')
            if self.is_yes():
                self.talk(f'playing {command}')
                kit.playonyt(command)
            else:
                self.talk('Oh Oh! Please try that again.')
                command_2 = self.listen()
                if command_2 is not None:
                    self.process_command(command_2)

        elif 'time' in command:
            time_now = datetime.datetime.now().strftime("%H:%M:%S")
            self.talk(f'Current time is {time_now}')

        elif 'date' in command:
            today = date.today()
            self.talk(f'Today is {today}')

        elif 'search' in command:
            command = command.replace('search', '')
            kit.search(command)

        elif 'wikipedia' in command:
            self.talk('Searching Wikipedia...')
            statement = command.replace("wikipedia", "").replace("search", "").replace("about", "").replace("in", "")\
                               .replace('according to', '').replace('what is', '')
            self.talk(f'you want me to search about {statement} in wikipedia. Am I right?')
            if self.is_yes():
                results = wikipedia.summary(statement, sentences=3, auto_suggest=False, redirect=True)
                self.talk("According to Wikipedia")
                self.talk(results)
            else:
                self.talk('Oh Am sorry. Try that again')
                command_2 = self.listen()
                if command_2 is not None:
                    self.process_command(command_2)

        elif 'open youtube' in command:
            webbrowser.open_new_tab("https://www.youtube.com")
            self.talk("youtube is open now")
            # time.sleep(5)

        elif 'open google' in command:
            webbrowser.open_new_tab("https://www.google.com")
            self.talk("Google chrome is open now")
            # time.sleep(5)

        elif 'open gmail' in command:
            webbrowser.open_new_tab("gmail.com")
            self.talk("Google Mail open now")
            # time.sleep(5)

        elif command in constants.RANDOM_QUESTIONS:
            self.talk('I cannot answer that')

        else:
            error = random.choice(constants.ERRORS)
            self.talk(error)


if __name__ == "__main__":
    va = VirtualAssistant()
    # va.start()
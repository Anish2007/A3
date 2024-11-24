import os
import webbrowser
import openai
import pyttsx3
import speech_recognition as sr
import datetime
from config import apikey

chatStr = ""

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\nJarvis: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response["choices"][0]["text"].strip()
        say(answer)
        chatStr += f"{answer}\n"
        return answer
    except Exception as e:
        say("An error occurred while communicating with OpenAI.")
        print(f"Error: {e}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Error recognizing speech:", e)
            return "Some error occurred. Sorry from Jarvis."

if __name__ == '__main__':
    print("Welcome to Jarvis A.I")
    say("Jarvis A.I")
    while True:
        query = takeCommand().lower()

        # Open websites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])

        # Play music
        if "play music" in query:
            musicPath = "C:\\Users\\YourUsername\\Music\\downfall-21371.mp3"
            os.startfile(musicPath)

        # Tell time
        elif "the time" in query:
            now = datetime.datetime.now()
            hour = now.strftime("%H")
            minute = now.strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes.")

        # Chat with OpenAI
        elif "using artificial intelligence" in query:
            chat(query)

        # Quit
        elif "jarvis quit" in query:
            say("Goodbye, Sir.")
            exit()

        # Reset chat
        elif "reset chat" in query:
            chatStr = ""
            say("Chat history reset.")

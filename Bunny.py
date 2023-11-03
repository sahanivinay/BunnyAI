import os.path
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pygame
import openai


apikey = "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"


chatStr = ""


def chat(query_prompt):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Vinay:{query_prompt}\n Bunny: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('write')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5  # to hold for listening we can remove or change this
        audio = r.listen(source)
        try:  # try for query that doesn't get recognized
            print("Recognizing...")
            speech = r.recognize_google(audio, language="en-in")
            print(f"User said: {speech}")
            return speech
        except Exception as e:
            return "Some Error Occurred. Sorry from Bunny"


if __name__ == '__main__':
    pygame.mixer.init()  # Initialize the pygame mixer
    pygame.mixer.music.load("Hukum.mp3")  # Replace with the actual path to your music file
    print('PyCharm')
    say("Hello, I am Bunny A.I.")
    while True:
        print("Listening...")
        query = take_command()
        songs = [["Hukum", "Hukum.mp3"], ["Humdard", "Humdard.mp3"]]
        for song in songs:
            if f"Play {song[0]}".lower() in query.lower():
                say(f"Playing {song[0]} Boss...")
                # Replace the file path with your music file
                pygame.mixer.music.load(song[1])
                pygame.mixer.music.play()

            elif "Stop music".lower() in query.lower():
                pygame.mixer.music.stop()
                say("Music stopped, Boss!")

        sites = [["YouTube", "https://www.youtube.com"], ["WikiPedia", "https://www.wikipedia.com"],
                 ["Google", "https://www.google.com"], ["Instagram", "https://www.instagram.com"]]
        for site in sites:
            # todo : Add a feature to open websites
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Boss...")
                webbrowser.open(site[1])
                say(query)
        # todo : Add a feature to know current time
        if "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Boss, the time is {hour} and {minute}")

        elif "Write".lower() in query.lower():
            ai(prompt=query)

        elif "Bunny quit".lower() in query.lower():
            say("Bye Boss!")
            exit()
        elif "Reset chat".lower() in query.lower():
            chatStr = ""
            say("Chat reset Boss!")
            say(query)

        else:
            chat(query)

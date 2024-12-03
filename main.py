import os
import webbrowser
import openai
import datetime
import random
import speech_recognition as sr
from config import apikey

# Global chat history
chatStr = ""

# Function to handle OpenAI Chat API
def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"Rushabh: {query}\nJarvis: "
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response["choices"][0]["message"]["content"]
        say(reply)
        chatStr += f"{reply}\n"
        return reply
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        say("There was an issue processing your request.")
        return "Error in API request."

# Function to handle tasks for "Steve"
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt}\n*************************\n\n"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response["choices"][0]["message"]["content"]
        text += reply

        # Ensure folder exists
        if not os.path.exists("Jarvis Files"):
            os.mkdir("Jarvis Files")

        # Generate a valid filename
        sanitized_prompt = ''.join(c if c.isalnum() else '_' for c in prompt)[:50]
        filename = f"Jarvis Files/{sanitized_prompt}.txt"

        # Write response to file
        with open(filename, "w") as f:
            f.write(text)
        print(f"Response saved to {filename}")
        say("Response has been saved successfully.")
    except Exception as e:
        print(f"Error with OpenAI API or file operation: {e}")
        say("There was an issue processing your request.")

# Function to speak text
def say(text):
    os.system(f'say "{text}"')

# Function to capture audio commands
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(f"Error recognizing speech: {e}")
            return "Some Error Occurred. Sorry from Jarvis"

# Function to open websites
def openWebsite(query):
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "bbc": "https://www.bbc.co.uk",
        "skysports": "https://www.skysports.com",
        "pokerstars": "https://www.pokerstars.uk",
        "stackoverflow": "https://stackoverflow.com",
        "linkedin": "https://www.linkedin.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "netflix": "https://www.netflix.com",
        "amazon": "https://www.amazon.com"
    }

    for key, value in websites.items():
        if f"open {key}" in query.lower():
            say(f"Opening {key}...")
            webbrowser.open(value)
            return True
    return False

# Main execution
if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis is ready")
    while True:
        query = takeCommand()

        if "open" in query.lower():
            if not openWebsite(query):
                say("Sorry, I couldn't find the website in my list.")

        elif "the time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"The time is {hour} hours and {minute} minutes.")
        elif "open facetime" in query.lower():
            os.system("open /System/Applications/FaceTime.app")
            say("Opening FaceTime")

        elif "open camera" in query.lower():
            os.system("open /System/Applications/Photos.app")
            say("Opening Camera")

        elif "open music" in query.lower():
            os.system("open /System/Applications/Spotify.app")
            say("Opening Spotify")

        elif "open calculator" in query.lower():
            os.system("open /System/Applications/Calculator.app")
            say("Opening Calculator")

        elif "Open Notes" in query.lower():
            os.system("open /System/Applications/Notes.app")
            say("Opening Notes")

        elif "Github" in query.lower():
            os.system("open /System/Applications/GitHub.app")
            say("Opening Github")

        elif "open terminal" in query.lower():
            os.system("open /System/Applications/Utilities/Terminal.app")
            say("Opening Terminal")

        elif "Python" in query.lower():
            os.system("open /System/Applications/JetBrains Toolbox.app")
            say("Opening PyCharm")

        elif "Discord" in query.lower():
            os.system("open/ System/Applications/Discord.app")
            say("Opening Discord")


        elif "open arc" in query.lower():
            os.system("open /System/Applications/Arc.app")
            say("Opening Arc")

        elif "jarvis quit" in query.lower():
            say("Goodbye, sir!")
            break

        elif "reset chat" in query.lower():
            chatStr = ""
            say("Chat history reset.")

        elif "steve" in query.lower():
            # Send the command to Steve and save it to Jarvis Files
            ai(prompt=query)

        else:
            chat(query)

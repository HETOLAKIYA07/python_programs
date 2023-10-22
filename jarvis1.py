##########################################################
#                                                        #
#               develop by:- olakiya het                 #
#               email:- olakiyahet@gmail.com             #
#               github:- HETOLAKIYA007                   #            
##########################################################



import speech_recognition as sr
import pyttsx3
import webbrowser
import pyautogui
import os
import smtplib


from dotenv import load_dotenv



def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    
def get_password():
    speak("Please enter the password to access Jarvis.")
    user_input = listen()
    return user_input
    
def open_email():
    speak("Opening a new window for composing an email.")
    webbrowser.open("https://mail.google.com/mail/u/0/?fs=1&tf=cm&source=mailto&su=")

def listen():
    recognizer = sr.Recognizer()
    microphone_index = 0
    while True:
        with sr.Microphone(device_index=microphone_index) as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source)  # No timeout, keep listening indefinitely
                text = recognizer.recognize_google(audio)
                return text.lower()
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand.")
                speak("I'm sorry, I couldn't understand. Please try again.")
            except sr.RequestError as e:
                print(f"Error occurred while processing speech: {e}")
                speak("An error occurred while processing your speech. Please try again.")
    return ""

def close_current_tab():
      pyautogui.hotkey('ctrl', 'w')

def stop_listening():
    speak("Sure, I'll stop listening for commands now.")
    return True

def main():
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the user's password
    correct_password = os.getenv("PASSWORD")
    user_password = get_password()
    
    if user_password != correct_password:
        speak("Incorrect password. Access denied.")
        return

    speak("Access granted. I am your AI assistant. How can I help you?")

    current_search_url = ""  # Variable to store the current search URL

    while True:
        command = listen()

        if "hello" in command:
            speak("Hello. sir how can I assist you?")
        elif "what is your name" in command:
            speak("My name is Jarvis.")
            
        elif "search" in command:
            speak("What do you want me to search for?")
            search_query = listen()
            if search_query:
                current_search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                webbrowser.open(current_search_url)
            else:
                speak("Sorry, I didn't catch that. Please try again.")
                
        elif "open youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com/")
            
        elif "open google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com/")
            
        elif "open email" in command:
            open_email()
        
        elif "close this tab" in command:
            if current_search_url:
                speak("Closing the current tab.")
                close_current_tab()  # Close the current tab using pyautogui
                current_search_url = ""
            else:
                speak("There is no active search tab to close.")
                
        elif "goodbye" in command or "exit" in command:
            speak("Goodbye!")
            break
        
        elif "stop listening" in command:
            if stop_listening():
                break
        else:
            speak("I'm sorry, I can't perform that task right now.")
            
if __name__ == "__main__":
    main()

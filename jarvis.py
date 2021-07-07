# importing libraries
import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pyaudio
import datetime
import wikipedia 
import webbrowser
import os, sys
import smtplib
from boltiot import Sms,Email,Bolt 
import json, time
from chatterbot import ChatBot #chat bot imported
from chatterbot.trainers import ChatterBotCorpusTrainer#to train the chatbot

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
chatbot = ChatBot('Bot') 
trainer = ChatterBotCorpusTrainer(chatbot)#train the chatbot
trainer.train('chatterbot.corpus.english')
bolt_api_key="7999fe36-9865-4595-9665-e59bed7827ea" 
device_id="BOLT13134431"
mybolt = Bolt(bolt_api_key, device_id)
Sid='ACfdee362a6fea2bbf5e48b21b9780edaf'
Auth='b053105ea4c32e737d941127c62e9e96'
From='+12513129372'
Api_mal='7b37ef167e36703185138fd3dfbf921f-87c34c41-a5dc575a'
url='sandboxb9a4f1046eae44748fe62381ae6de518.mailgun.org'
send='adepuakhila9@gmail.com'

def speak(audio): #function to make our system speak out
    engine.say(audio)
    engine.runAndWait()


def wishMe(): #wishes you, when you start based on the time
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am your P A. Please tell me how may I help you")       


def takeCommand():#function to take your command and recognise it
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        speak('Listening..')
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:   
        print("Say that again please...")
        #speak("couldn't recognize")
        return "None"
    return query

def browse(comm): # to browse the website 
    webbrowser.open(comm+".com")
    

def msg(per):# send the message to the verified contact numbers
    try:
        if(per=='me'):
            To='+919701399833'
        elif(per=='meghana'):
            To='+917097414233'
        elif(per=='dilip'):
            To='+919121033345'
        elif(per=='nitish'):
            To='+916305453526'
        else:
            speak('Sorry boss. I am not able to send this message as the contact not found')
            return 0;
        sms = Sms(Sid,Auth,To,From)
        speak('What is the content of message')
        content=takeCommand()
        while content=="None":
            speak("Please repeat")
            content=takeCommand()
        response = sms.send_sms(content)
        print("Response received from Twilio is: " + str(response))
        print("Status of SMS at Twilio is :" + str(response.status))
        speak('message sent')
    except Exception as e:
        print(e)
        speak("Sorry boss. I am not able to send this message")

def mail(per):# to send emails to verified mail ids
    try:
        if(per=='me'):
            recep='adepuakhila9@gmail.com'
        elif(per=='meghana'):
            recep='meghana.koratpally@gmail.com'            
        elif(per=='dilip'):
            recep='dk15679@gmail.com'
        elif(per=='nitish'):
            recep='nitishmurki76@gmail.com'            
        else:
            speak('Sorry boss. I am not able to send this email as mail is not verified')
            return 0;        
        mailer = Email(Api_mal,url,send,recep)
        speak('What is the content of message')
        content=takeCommand()
        while content=="None":
            speak("Please repeat")
            content=takeCommand()
        response = mailer.send_email('This is mini',content)
        response_text = json.loads(response.text)
        speak("Response received from Mailgun is: " + str(response_text['message']))
        #speak('Email sent')
    except Exception as e:
        print(e)
        speak("Sorry boss. I am not able to send this Email")
    

def note(i):#takes down the note and save it in a foldeer
    try:
        speak('creating a notes')
        fd = os.open( 'C:\\Users\\RAJU\\Desktop\\mini\\new'+i+'txt', os.O_RDWR|os.O_CREAT )
        speak('starting notes')
        speak('Please say me what to note')
        content='HI'
        while content!='exit':
            content=takeCommand()
            if content=='None':
                continue
            os.write(fd,str.encode(content))
            os.write(fd,str.encode('\n'))
        os.close(fd)
    except Exception as e:
        print(e)
        speak("Sorry boss. Coludn't make a note please try again")

def wiki(query):#function for wikipedia search
    try:
        speak('Searching Wikipedia...')
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except Exception as e:
        speak("Coludn't search it")
def greet(query):
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<17:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")
    speak(query)
    speak("How are you")
    #speak("I am damn, tell me how can I help you")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'wiki' in query: #einstein wikipedia
            query = query.replace("wiki", "")  
            wiki(query)
        elif 'wikipedia' in query: #einstein wikipedia
            query = query.replace("wikipedia", "")  
            wiki(query)
        elif 'greet' in query:
            query=query.replace("greet","")
            greet(query)
        elif 'hello' in query:
            print("Hello sir!")
            speak('Hello sir, Tell me how can I help you')
        elif 'how are you' in query:
            speak('I am good How can I help you')
        elif '.com'in query:#open google.com
            query = query.replace("open", "")
            browse(query)
        elif 'on' in query:#home automation
            mybolt.digitalWrite(0,'HIGH')
        elif 'off' in query:#turon off light
            mybolt.digitalWrite(0, 'LOW')           
        elif 'send message' in query:#send message to me(send message to megana)
            query = query.replace("send message to ", "")
            z=msg(query)            
        elif 'send email' in query:#send email to me(send email to megana)
            query = query.replace("send email to ", "")
            z=mail(query)
        elif 'note' in query:#take note
            note(4)
        elif 'the time' in query:# what is the time # tell me the time
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")            
        elif 'open file' in query:#open file
            path ='C:\\Users\\RAJU\\Desktop\\mini'
            os.startfile(path)            
        elif 'quit' in query:
            print("quiting..! Thank you for your time")
            speak("quiting..! Thank you for your time")
            break
        elif 'shutdown' in query:
            speak('Do you really want to shutdown')
            reply=takeCommand()
            if 'yes' in reply:
                os.system('shutdown /s /t 1')
            else:
                continue
        elif 'restart' in query:
            speak('Do you really want to restart')
            reply=takeCommand()
            if 'yes' in reply:
                os.system('shutdown /r /t 1')
            else:
                continue
        elif 'log out' in query:
            speak('Do you really want to log out')
            reply=takeCommand()
            if 'yes' in reply:
                os.system('shutdown -1')
            else:
                continue    
        elif 'none' in query:
            print('repeat')
        else:
            reply=chatbot.get_response(query)
            speak(reply)
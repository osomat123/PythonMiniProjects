import os
import pyttsx3
import json
import speech_recognition as sr

def getApps():
    
    try:
        with open("apps.json","r") as read_file:
            strApps = read_file.read()
            apps = eval(json.loads(strApps))
        
    except FileNotFoundError:
        
        apps = {}

        for (path,app,file) in os.walk('/Applications'):
            if path.endswith('.app') and path.count('.app') == 1:
                app = path[1:].split('/')[-1].replace('.app','')  # Get app name
                path = path.replace(' ','\ ') # Set app path
                apps[app] = path

        for (path,app,file) in os.walk('/System/Applications'):
            if path.endswith('.app') and path.count('.app') == 1:
                app = path[1:].split('/')[-1].replace('.app','') # Get app name
                path = path.replace(' ','\ ') # Set app path
                apps[app] = path
                
        with open("apps.json",'w') as file:
            file.write(json.dumps(str(apps)))
            
    try:
        with open("nicknames.json","r") as read_file:
            strApps = read_file.read()
            nicks = eval(json.loads(strApps))
            apps.update(nicks)
            
    except FileNotFoundError:
        pass
    
    return apps


def addNick(nick,longApp):
    
    flag = 0
    
    with open("apps.json","r") as read_file:
        strApps = read_file.read()
        apps = eval(json.loads(strApps))
        
    try:
        with open("nicknames.json","r") as read_file:
            strApps = read_file.read()
            nicks = eval(json.loads(strApps))
            
    except FileNotFoundError:
        nicks = {}
        
    newNicks = nicks
    
    for app in apps.keys():
        if app.upper() == longApp:
            nicks[nick] = apps[app]
            flag = 1
            break
    
    if flag ==0:
        return False
    
    with open("nicknames.json",'w') as file:
        file.write(json.dumps(str(newNicks)))
    
    return True


def get_speech():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Speak Now...")
        audio = r.listen(source)
        print("Processing...")
        
    return r.recognize_google(audio)


def search_google(voice):
    query = voice.replace(" ","+").strip()
    url = "https://www.google.com/search?q="+query
    webbrowser.get().open_new(url)

print("Initializing...\n")
valid = ['RUN','OPEN','EXECUTE','BYE','EXIT','QUIT','ADD NICKNAME','HELP','STOP','CIAO']
apps = getApps()

print("Welcome to Py Assistant")
print("How can I help?\n")
pyttsx3.speak("Welcome to Py Assistant....How can I help?")

print("Let me know if you need help\n")
pyttsx3.speak("Let me know if you need help")

while True:
    
    input("Press Enter and start speaking...")
    print()
    voice = get_speech()
    print('You said "',voice,'"')
    
    query = voice.upper()
    appFound = 0
    commandValid = 0
    
    for command in valid:
        if command in query:
            commandValid = 1
            break
    
    if commandValid == 0:
        
        print('Searching google for',voice)
        pyttsx3.speak('Searching google for '+ voice)
        search_google(voice)
        continue
    
    if "HELP" in query:
        f = open("help.txt",'r')
        print(f.read())
        f.close()
        continue
        
    if ("BYE" == query) or ("EXIT" == query) or ("QUIT" == query) or ('STOP' == query) or ('CIAO' == query):
        print("Bye!\n")
        pyttsx3.speak("Bye.")
        break
        
    if 'ADD NICKNAME'in query:
        names = [i.strip() for i in query.split('FOR')]
        nick = names[0][13:]
        longApp = names[1]
        
        if nick in apps:
            print("Nickname already exists. Give another nickname.\n")
            pyttsx3.speak("Nickname already exists. Give another nickname")
            continue
        
        ret = addNick(nick,longApp)
        
        if ret == True:
            with open("nicknames.json","r") as read_file:
                strApps = read_file.read()
                nicks = eval(json.loads(strApps))
                
            apps.update(nicks)
                
            print("Nickname added.\n")
            pyttsx3.speak("Nickname added.")
            appFound = 1
            
    if ('RUN' in query) or ('OPEN' in query) or ('EXECUTE' in query):
        for app in apps.keys():
            if app.upper() in query:
                command = 'open '+apps[app]
                print("Sure!\nOpening "+app+" ...\n")
                pyttsx3.speak("Sure.....Opening "+app)
                os.system(command)
                appFound = 1
                break        

    if appFound == 0:
        print('Application not found. Try Again!\n')
        pyttsx3.speak("Application not found. Try Again!")
        
    os.system('clear')
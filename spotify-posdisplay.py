import serial
import os
import time
import base64
import json
import spotipy
import spotipy.util as util
import atexit
from dotenv import load_dotenv
load_dotenv()

# env vars
port = os.getenv('SERIAL_LINE')
username = os.getenv('SPOTIFY_USERNAME')
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# internal vars - do not mess with
cachedstatus = "not"
forcerefresh = False

# pole display interface functions

def write(txt):
    try:
        ser = serial.Serial(port)
        ser.write(b"" + str.encode(txt))
        ser.close()
    except serial.SerialException as e:
        print("failed writing to display:", e)

def scroll(txt):
    try:
        ser = serial.Serial(port)
        ser.write(b'\x05' + str.encode(txt) + b'\x0D')
        ser.close()
    except serial.SerialException as e:
        print("failed writing to display:", e)

def scroll2(txt):
    try:
        ser = serial.Serial(port)
        ser.write(b'\x1B' + b'\x06' + str.encode(txt) + b'\x0D')
        ser.close()
    except serial.SerialException as e:
        print("failed writing to display:", e)

def clr():
    try:
        ser = serial.Serial(port)
        ser.write(b'\x1F')
        ser.close()
    except serial.SerialException as e:
        print("failed writing to display:", e)

def enablecursor():
    try:
        ser = serial.Serial(port)
        ser.write(b'\x13')
        ser.close()
    except serial.SerialException as e:
        print("failed writing to display:", e)

def disablecursor():
    try:
        ser = serial.Serial(port)
        ser.write(b'\x14')
        ser.close()
    except serial.SerialException as e:
        print("failed writing to display:", e)

def newline():
    try:
        ser = serial.Serial(port)
        ser.write(b'\x12')
        ser.write(b'\x0A')
        ser.write(b'\x0D')
        ser.close()
    except serial.SerialException as e:
        print("failed writing to display:", e)

# spotify functions

def getnowplaying():
    scope = 'user-read-currently-playing'

    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri="https://www.w3schools.com/action_page.php")

    spotify = spotipy.Spotify(auth=token)
    current_track = spotify.current_user_playing_track()
    return current_track

def getartists(song):
    artist_names = [artist['name'] for artist in song['item']['artists']]
    artist_string = ", ".join(artist_names)
    return artist_string

# main functions

def exit_handler():
    print("exiting script...")
    clr()

def getsongstatus():
    if playing == True:
        return "> NOW PLAYING"
    elif playing == False:
        return "|| PAUSED"
    elif playing == None:
        return "[] STOPPED"
    
def checkifhasplaypaused():
    global forcerefresh
    global cachedstatus
    if playing != checkcachedstatus():
        print("cache not equal, returned " + str(checkcachedstatus()), "although playing is " + str(playing))
        if playing == True:
            cachedstatus = "yes"
            forcerefresh = True
        elif playing == False:
            cachedstatus = "no"
            forcerefresh = True
        elif playing == None:
            cachedstatus = "not"
            forcerefresh = True
        print("updated cachedstatus to " + cachedstatus)

def checkcachedstatus():
    global cachedstatus
    print("!! cachedstatus is " + cachedstatus)
    if cachedstatus == "yes":
        return True
    elif cachedstatus == "no":
        return False
    elif cachedstatus == "not":
        return None

def cycle():
    print("running!")
    disablecursor()
    write("Initializing...")
    global notfirst
    notfirst = False
    global currentsong
    global playing
    global forcerefresh
    forcerefresh = False
    if type(getnowplaying()) != type(None):
        currentsong = "" + str(getnowplaying()['item']['name'])
    else:
        currentsong = None
    while True:
        if type(getnowplaying()) != type(None):
            if getnowplaying()['is_playing'] == True:
                print("is playing")
                playing = True
            elif getnowplaying()['is_playing'] == False:
                print("is paused")
                playing = False
            else:
                print("is neither playing or paused")
                playing = None
            print("not none, instead " + str(type(getnowplaying())))
            checkifhasplaypaused()
            print("forcerefresh is " + str(forcerefresh))
            if currentsong != getnowplaying()['item']['name'] or notfirst==False or forcerefresh==True:
                print("refreshing")
                print(notfirst)
                print(getnowplaying()['item']['name'])
                notfirst = True
                forcerefresh = False
                currentsong = "" + str(getnowplaying()['item']['name'])
                print(str(len(str(getartists(getnowplaying()) + " - " + getnowplaying()['item']['name']))))
                if len(str(getartists(getnowplaying()) + " - " + getnowplaying()['item']['name'])) > 44:
                    print("max chars, cannot write to display")
                    clr()
                    write(getsongstatus())
                    newline()
                    write("(max chars)")
                elif len(str(getartists(getnowplaying()) + " - " + getnowplaying()['item']['name'])) > 19:
                    print("scroll mode")
                    clr()
                    write(getsongstatus())
                    newline()
                    scroll2(getartists(getnowplaying()) + " - " + getnowplaying()['item']['name'])
                else:
                    print("no scroll")
                    clr()
                    write(getsongstatus())
                    newline()
                    write(getartists(getnowplaying()) + " - " + getnowplaying()['item']['name'])
        else:
            currentsong = None
            print("player not open")
            clr()
            write("[] STOPPED")
        time.sleep(5)
        print("reloading")

atexit.register(exit_handler)
clr()
cycle()

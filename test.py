import asyncio
import datetime
import pymongo, dns
from pymongo import MongoClient
from colorama import Fore, Back, Style
import pyautogui
import socket 
import subprocess
import datetime
import threading
import base64
import zmq
import time
import win32api, win32con
import keyboard
import os 
import sys
from os import remove
from sys import argv
import cv2
import numpy as np


#If this doesnt work just make a recording with mouse movement when loading into raid and loop it(Ez way)
#Run in seperate threads to find out what screen you are in, and to update current log

dbClient = MongoClient(
    "mongodb+srv://D1P:D1P9812@hokuspokusdb.gehgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = dbClient["ElonWare"]
elonware_db = db["EW-Logins"]

#Getting hwid and ip
try:
  fetched_hwid = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
  fetched_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
except Exception as e:
  pyautogui.alert(f'Error while fetching ip/hwid:\n\n{e}')
  sys.exit()

#Connecting to server

context = zmq.Context()
print("[+]Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5421064")
print("[+]Connected to server")
os.system('cls')

#Make a hwid check to  make sure they match

current_screen  = 'None'
desired_kd = 0
version = '0.1'
current_log = 'None'
ping = '0'

#Next button
nextButton_x, nextButton_y = 954,939

#Main screen
nextButton1_x, nextButton1_y = 925,645

#Early termination 
nextButton2_x, nextButton2_y = 950,975

loading_screens = ['characterChoosing','redText','insuranceScreen','LFGScreen', 'killList', 'raidStats', 'expGained', 'characterHeal']
next_screens = ['characterChoosing','redText','insuranceScreen','LFGScreen']

#def uninstall():
  #remove(argv[0])


async def startup():  
  first_raid = True
  current_screen = 'startup'
  
  #Printing logging message
  print('KD WARE - SERVER VERSION:')
  key = input('[+]Key:\n')

  #Checking if key is in database/check if right hwid
  if elonware_db.count_documents({"key": f"{key}"}) > 0:
    for dbFind in elonware_db.find({"key":key}):
      expirationDate = (dbFind["expirationDate"])
      first_login = dbFind["first_login"]
      hwid = dbFind['hwid']
      ip = dbFind['ip']
      
    #Logging ip and hwid  
    if first_login == 'True':
      elonware_db.update_one(
        {"key": f"{key}"},
        {"$set":{"hwid":f"{fetched_hwid}", "ip":f"{fetched_ip}","first_login":"False"}}
      )
      pyautogui.alert('Restart program to continue')
      sys.exit()
      
    if str(fetched_ip) == str(ip) and str(fetched_hwid) == str(hwid):
    
      #Checking if key is expired
      if datetime.datetime.now() > datetime.datetime.strptime(str(expirationDate), "%Y-%m-%d %H:%M:%S.%f"):
        pyautogui.alert('Key expired')
        uninstall()
        return
        #Take away costumer role in discord
      else:pass
      
      pyautogui.alert('Successfully logged in!')
      await main_screen(fetched_ip,fetched_hwid)
      
    else:
      print(hwid, fetched_hwid)
      pyautogui.alert('HWID missmatch')
      uninstall()
      
  else:
    pyautogui.alert('Key not valid')
    remove(argv[0])

async def main_screen(fetched_ip,fetched_hwid):
  os.system('cls')
  current_screen = 'main_screen'
  
	#Printing main menu
  print('KD WARE - SERVER VERSION:')
  print(f'Ip: {fetched_ip}')
  print(f'HWID: {fetched_hwid}')
  print('[+]Toggle')
  input('')
  await click_next()

def click(x,y):
    print('clicking')
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

async def click_next():
    while True:
        currentScreen = await get_screen()
        print('Getting ready to click')
        
        if currentScreen == 'loadingScreen':
          pyautogui.press('space')
          time.sleep(1)

        elif currentScreen == 'mapChoosing':
          #Clicking interchange
          win32api.SetCursorPos((783,446))
          win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,783,446,0,0)
          win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,783,446,0,0)

          time.sleep(0.3)

          #Clicking next 
          x,y = nextButton_x, nextButton_y
          click(x,y)

        elif currentScreen == 'mainMenu':
          x,y = nextButton1_x, nextButton1_y
          click(x,y)
        
        elif currentScreen in loading_screens: 
          x,y = nextButton_x, nextButton_y
          click(x,y)
            
        elif currentScreen == 'earlyTermination':
          x,y = nextButton2_x, nextButton2_y
          click(x,y)
        
        else:
            await asyncio.sleep(1)

async def update():
  while True:
    os.system('cls')
    print(Fore.RED + custom_fig.renderText('KD WARE'))
    print(f'[+]Ping - {ping}')
    print(f'[+]Current screen - {current_screen}')
    await asyncio.sleep(1)


async def get_screen():
    #Writing down current time
    now = datetime.datetime.now()
    
    #Taking screenshot // Insert area 
    img = pyautogui.screenshot('template.jpeg',region=(497, 0, 800, 800))
    img = open("template.jpeg", 'rb')

    #Sending picture to server
    print('Sending picture to server')
    bytes = bytearray(img.read())
    strng = base64.b64encode(bytes)
    socket.send(strng)
    img.close()
    
    reply = socket.recv()
    current_screen = reply.decode()
    print(current_screen) 
    
    
    #Checking how long it took
    ping = str(datetime.datetime.now() - now)
    print(datetime.datetime.now() - now)
    return current_screen

keyboard.on_press_key("p", lambda _:os._exit(0))
x = threading.Thread(target=update)
asyncio.run(startup())



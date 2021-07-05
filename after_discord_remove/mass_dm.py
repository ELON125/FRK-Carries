import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord.ext.commands import has_permissions
import time
import json
from discord.utils import get
from discord_components import DiscordComponents, Button, ButtonStyle
import chat_exporter
import io
import datetime
import pymongo,dns
from pymongo import MongoClient
from pyautogui import *
import pyautogui
import keyboard

x, y = 125, 186
x1,y1 = 789,123
x2,y2 = 437, 260
x3,y3 = 1376,264
x4,y4 = 201,127
x5,y5 = 757,451
x6,y6 = 742,505
x7,y7 = 436, 988

ids = '/bojo#3977/Sammmm#0660/mAtoe#0901/ELON#7282/UWish#2560/boonk#3999/!ttaM#9072/adm1#0161/gazzx#3986/Joee#5607/Dogdog#9388/ODaZzJO#4338/olly#7777/Exrorius#9999/Poe#0666/bean#0486/Talo#3649/$UPER$#4518/tapy#9599/Klenzy#0001/flapjack#3996/𝘬4#0001/ℜ𝔢𝔩𝔞𝔵𝔢𝔯#0666/NKinsella1#0001/OnioN#7456/dev1l#5975/KingOfKeks#1620/T£KO^#0001/Exastiity#4553/trilkan#1111/TheStonedpanda(EU)#9452/Water#6669/abyss#3173/!!!!taki0.420#6969/minuxfn#8712/victor!#4121/ηautic#8006/Bulgie#2032/razzle#3069/markeymrk#2149/KeithGalloway#2726/Xøtic#5908/-pepto-#4739/J!p#1880/mysuncast#2036/Havoc#6362/highcarbs#1313/SAMMY#2843/Hzwly#1532/!Jitt#2003/Whoq#0001/trevorven#5426/--#3037/Sparta#7343/FaanN게이#8159/BENJI^#7191/VinnyEU#6737/ChingCh0ng#3345/Zer0#0106/Backs#6666/prome#2114/Botman#7647/MDALE#3054/!Lep#0001/stitch#7777/!Mi$ty#5433/LucKyy#7211/leems#1929/Luroah#0352/ᵒⁱˡ#0001/NLT_Savage#1297/Rouzik#3122/Tachy#3578/Stalin#0388/Strohbz#1366/Amathyst#0001/KristySisneros#3479/Archie.#0001/AcV#2993/birdboy#4928/j0rdan#1337/SweetBrown#2107/Exlipsics#3855/Boo#5765/Scopess^#0002/penguin#5043/GB#2432/wendigo.#9230/JCL#7974/FlushedAwayRat#9254/Johncumman#5521/uWu#3197/Leon#1337/Cody#9619/Risk_BTW#5088/DrinkEnergetic#8579/Hmoney#8888/Anziety#2312/Falco#1273/gggggggg#0666/Sn1perDude#8522/!jakub#1111/Bearr#7475/!Vinny#0001/!dvx#0001/Luna悟#6077/iamperkins#3962/JustAlex#0420/nash#2222/calzone#7777/brightboi#9958/.2137gruby#2137/Coasttoid#7306/GG!#0619/Cunker#2425/LowkeyCharms#1111/Cobraman151#9029/Atlas#7200/Tag#3682/Akurah#0905/EkaterinaAbramov#1387/Tyse#7404/mackblack123#5410/25cents#1648/arq#7798/gwel*#1388/_SEABASS#9665/Res.#0001/bumpkin#5479/dog1#3591/stevepolaris#1497/!Ca!i#8888/SacrificialPact#8256/PimpChimp#6403/legacy#3921/FrOoZzY♛#3368/MemberCount#7205/heu#0930/silvias13#5148/GOAT#8690/uoshua#1355/straik#4630/bigboy7foru#6157/Moody#7460/acez#4444/[PXA]Zuhny#9999/Suave#4412/✞𝑂𝑎𝑘𝑧✞#6246/toby#7628/jEsUs#9175/OfficerScentral#9966/Dyno#3861/Mason#0253/OLLI£☄#0666/$aat#4444/Safe#3410/Dudley#3106/Carl-bot#1536/nano-neurax#0395/mDubz#7286/WoolfofAllStreets#9343/Toree.#5488/Koi#9392/skiderino#5502/GerberMaster#1624/Brav06gd#0006/Patrik#1013/charnuslayer#3582/TheBigBadWolf55#7977/BouffFajita#4600/DonOtto#2711/卡勒姆#6135/Umbra#1323/Akame#8833/FL$P#1827/SerbianChad#4014/harpost#0442/Biggs#0766/wok#3639/&lt;EoT&gt;HalfGallon#0001/Troosh#8364/DTREKT#0056/Banshee#7709/!Lynx#8631/Marksman#6730/jaqq.#8982/Crack#9335/d1mast4#7866/DISBOARD#2760/IHACK#1511/elli0tt#0001/Dexter#2243/Rustyy💫#9383/Sammalz#6402/Gokuo#2375/RC#2164/JoshClient💫🕊#3791/InviteTracker#0478/!Fishy💫#9999/razz#0907/Gem#7413/osmun#8008/YungSteen#3721/KeeN#0509/Mood$🔌#0893/Davemode#5647/Climberr#8855/John.#5610/(1)Bean#7777/.brennon#7053/DonePardon#0007/Alfie#1116/Marcus1#0489/Zythos#5810/ｋｉｌｌａ#5072/Clostros#7258/Jared.#6969/Khanyounot#5773/vanugenththe5th#9417/para#4418/!"AwM^#3646/GiveawayBot#2381/will_#4262/TheDudeX#0990/Eoka#9762/nick#1962/wwa#0001/Waffles#3610/Dakar#1153/skero#2978/potato.#9800/soohe#7968/Arqz#1111/FofikPofik(Вован)#1051/Fluxid22#6575/Nakama#3715/I_Pariah_I#7443/Rythm#3722/zoZo#0240/C0N0R#0386/kem#9262/LurkingLary#0803/A_Stackz#8429/ManHut#7657/Certiorari#8811/tuntum#1208/Zandd#9195/ddd2v#4230/Ramses#0001/!Brooko97^#1689/R1DO#7536/MaoZedong#6314/maxxx.#0666/Benz#2222/pep£££#9177/UKJC#6779/KRAXI#7719/ReaperK17#0001/BizzyZ#5309/M1L0#3672/splivvs#1686/CardDecline#0001/xBrokenX#5010/Geo23#8870/PapaNoname#6969/Cal#7670/L3gend#0001/Odeling#2312/l5LAVl#0001/Knaller#0001/nabiix#2672/maxx#1898/Nulle#0001/.cloudz#0001/Rat#4306/retytim#1000/TicketTool#4843/KRF-Tickets#4758/Leeyam#8195/opzz#0795/ChodeFuck#2078/Leakzzy#1151/Enko#3732/Dam3Dolla#3721/Chapo#0798/VZNRY#2538/Zoieisbae#2597/Capmcrunch#5605/bojo#3977/KRF#0001/Sammmm#0660/mAtoe#0901/mAtoe#0901'

print(pyautogui.position())
counter = 0
dm_list = ''
num = 0

for member in ids.split("/"):
    print(member) # needs to be
    print(counter)
    if counter > 20:
        print(dm_list)
        counter = 0
        inv_file = open(f'{num}.txt', "w+", encoding='utf-8')
        inv_file.write(dm_list)
        dm_list = ''
        num +=1
    else:
        dm_list = dm_list + '\n' + member
        counter +=1



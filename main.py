from random import random, choice
import sys
from math import ceil
title = choice([
"SIGMA GRINDSET I: Fear not poverty. Poverty is the bitter soil in which sweet desire blossoms.",
"SIGMA GRINDSET II: Fortune despises the idle man. Stasis is death. Always move forward.",
"SIGMA GRINDSET III: Be envious. Covet. Then take what you desire.",
"SIGMA GRINDSET IV: Deception is the sword of wisdom. Be wise.",
"SIGMA GRINDSET V: Beware the idle man who would lull you back into idleness.",
"SIGMA GRINDSET VI: Contentment is idleness. Desire inspires action. Nurture all desires.",
"SIGMA GRINDSET VII: Money begets money.",
"SIGMA GRINDSET VIII: Charity is power. More charity is more power.",
"SIGMA GRINDSET IX: Shun sentimentality. It is a weakness that binds the idle man.",
"SIGMA GRINDSET X: Fulfill desire and others will follow.",


"This is a journey into money...", ###doin` up the house
"shitty warframe market warframe checking tool for checking prices of warframes for a game called warframe.",
"i forgor",
"Also try Destiny 2!                                                       wait no actually dont please I beg of you",
"How To Get Platinum FAST in Warframe 2023 - In Depth Guide (no)",
"EXPLOIT THESE AND GET TONS OF FREE PLATINUM FAST & EASY IN WARFRAME NOW! | 2023 (no)",
"apogus",
"ez plat hack (riven mafia hates him!)",
"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
"rv/pv is a good clan trust me      Source: bro just trust me"
])
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleTitleW(title)
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
import requests,json
from time import sleep

warframe = ["ash",
            "atlas",
            "banshee",
            "baruuk",
            "chroma",
            "ember",
            "equinox",
            "frost",
            "gara",
            "garuda",
            "harrow",
            "hildryn",
            "hydroid",
            "inaros",
            "ivara",
            "khora",
            "limbo",
            "loki",
            "mag",
            "mesa",
            "mirage",
            "nekros",
            "nezha",
            "nidus",
            "nova",
            "nyx",
            "oberon",
            "octavia",
            "revenant",
            "rhino",
            "saryn",
            "titania",
            "trinity",
            "valkyr",
            "vauban",
            "volt",
            "wukong",
            "zephyr"
            ]
warframealtsuffix = ["khora",
                    "revenant",
                    "baruuk",
                    "hildryn"
                    ]
            
prices = { 'set':{
                "Online":[],
                "Ingame":[]},
            'blueprint':{
                "Online":[],
                "Ingame":[]},
            'systems':{
                "Online":[],
                "Ingame":[]},
            'chassis':{
                "Online":[],                          
                "Ingame":[]},                          
           'neuroptics':{
                "Online":[],
                "Ingame":[]},
           'investment':{
                "Online":[],
                "Ingame":[]},
           'grofit':{
                "Online":[],
                "Ingame":[]},
           }
         
###pulling stuff from warframe market, if fails it retries
def wfmget(part_suffix, warframeID, try_number=1):
    try:
        rWFMget = requests.get(f"https://api.warframe.market/v1/items/{warframe[warframeID]}_prime_{part_suffix}/orders").json()  ##https://warframe.market/api_docs
    except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
        sleep(2**try_number + random()*0.01) #exponential backoff
        return wfmget(part_suffix, warframeID, try_number=try_number+1)
    else:
        return rWFMget['payload']['orders']

def progress_bar(currentProgress, part_suffix, total=37):
    global warframe
    percentage = 100 * (currentProgress / float(total))
    bar = '█' * int(percentage) + '-' * ceil((100 - int(percentage)))
    filler = ' ' * (20 - len(part_suffix) - 6)
    sys.stdout.write("\033[F\033[F")
    print(f"Checking {part_suffix}(s)...{filler}Status: {warframe[currentProgress].title()} Prime         \n|{bar}| {currentProgress}/{total}     ")
    
    if currentProgress == total:
        sys.stdout.write("\033[F\033[F")
        print(f"Checking {part_suffix}(s)...{filler}Status: Done!                                \n|{bar}| {currentProgress}/{total}     ")
        print(f"\n\n")
def chkprice(part_suffix):
    
    global prices
    global warframe
    global warframealtsuffix
    
    
    for warframeID in range(0,len(warframe)):
        
        progress_bar(warframeID,part_suffix)
        
        ###patch , newer warframes have an extra "_blueprint" for some reason
        for warframealtID in range(0,len(warframealtsuffix)):
            if warframe[warframeID] in warframealtsuffix[warframealtID] and part_suffix in ('chassis','systems','neuroptics'):
                part_suffix += "_blueprint"
        
        
        rWFMget = wfmget(part_suffix,warframeID)

        ###filtering out what we need, and throwing away the unneeded
        priceIngame = []
        for orderID in range(0,len(rWFMget)):
            if rWFMget[orderID]['order_type'] == 'sell' and rWFMget[orderID]['user']['status'] == 'ingame':
                priceIngame.append(rWFMget[orderID]['platinum'])
                
        try: priceIngame = min(priceIngame)
        except ValueError: priceIngame = 0 ##If it don't exist , make it 0 so the script doesnt die
        priceOnline = []
        for orderID in range(0,len(rWFMget)):
            if rWFMget[orderID]['order_type'] == 'sell' and rWFMget[orderID]['user']['status'] == 'online':
                priceOnline.append(rWFMget[orderID]['platinum'])
                
        try: priceOnline = min(priceOnline)
        except ValueError: priceOnline = 0 ##If it don't exist , make it 0 so the script doesnt die
        
        ###another patch because whooooops , apparently adding _blueprint results in a KeyError :clueless:
        
        if part_suffix in ('chassis_blueprint','systems_blueprint','neuroptics_blueprint'):
                part_suffix = part_suffix[:-10] ### if we have _blueprint , we remove em 
       # f"\033[38;2;203;186;238m{prices['Ingame'][warframeID]}\033[0m | \033[38;2;155;255;155m{prices['Online'][warframeID]}\033[0m" ##ANSI color coding
        
        prices[part_suffix]['Online'].append(priceOnline)
        prices[part_suffix]['Ingame'].append(priceIngame)
        
    
###actually getting the prices

chkprice('set')
chkprice('blueprint')
chkprice('chassis')
chkprice('systems')
chkprice('neuroptics')

###calculating "investment" and "return"

for warframeID in range(0,len(warframe)):
    prices['investment']['Online'].append(prices['blueprint']['Online'][warframeID]+prices['chassis']['Online'][warframeID]+prices['systems']['Online'][warframeID]+prices['neuroptics']['Online'][warframeID])
    prices['investment']['Ingame'].append(prices['blueprint']['Ingame'][warframeID]+prices['chassis']['Ingame'][warframeID]+prices['systems']['Ingame'][warframeID]+prices['neuroptics']['Ingame'][warframeID])
    
    prices['grofit']['Online'].append(prices['set']['Online'][warframeID]-prices['investment']['Online'][warframeID])
    prices['grofit']['Ingame'].append(prices['set']['Ingame'][warframeID]-prices['investment']['Ingame'][warframeID])
    
###printing out the info
from prettytable import PrettyTable

wfmtable = PrettyTable()
print("\033[38;2;203;186;238mONLINE IN GAME\033[0m  \033[38;2;155;255;155mONLINE\033[0m")
wfmtable.field_names = ["Prime","Blueprint","Systems","Chassis","Neuroptics","Set","Investment","Grofit"] ### grofitingame is used for sorting then removed
for warframeID in range(0,len(warframe)):
    sortID = prices['grofit']['Ingame'].index(max(prices['grofit']['Ingame'])) ###weird shit but it works and it works efficiently i think
    wfmtable.add_row([warframe[sortID].title(), 
                    f"\033[38;2;203;186;238m{prices['blueprint']['Ingame'][sortID]}\033[0m  \033[38;2;155;255;155m{prices['blueprint']['Online'][sortID]}\033[0m",
                    f"\033[38;2;203;186;238m{prices['systems']['Ingame'][sortID]}\033[0m  \033[38;2;155;255;155m{prices['systems']['Online'][sortID]}\033[0m",
                    f"\033[38;2;203;186;238m{prices['chassis']['Ingame'][sortID]}\033[0m  \033[38;2;155;255;155m{prices['chassis']['Online'][sortID]}\033[0m",
                    f"\033[38;2;203;186;238m{prices['neuroptics']['Ingame'][sortID]}\033[0m   \033[38;2;155;255;155m{prices['neuroptics']['Online'][sortID]}\033[0m",
                    f"\033[38;2;203;186;238m{prices['set']['Ingame'][sortID]}\033[0m   \033[38;2;155;255;155m{prices['set']['Online'][sortID]}\033[0m",
                    f"\033[38;2;203;186;238m{prices['investment']['Ingame'][sortID]}\033[0m   \033[38;2;155;255;155m{prices['investment']['Online'][sortID]}\033[0m",
                    f"\033[38;2;203;186;238m{prices['grofit']['Ingame'][sortID]}   \033[0m\033[38;2;155;255;155m{prices['grofit']['Online'][sortID]}\033[0m"
                    ])
    prices['grofit']['Ingame'][sortID] = min(prices['grofit']['Ingame'])-1 

print(wfmtable)

input("")

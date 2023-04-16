import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("nexus' shitty emone tool (GET RICH FAST NOT CLICKBAIT 100%")
import requests,json
from time import sleep
from random import random
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
            
prices = { 'set':[],
           'blueprint':[],
           'systems':[],
           'chassis':[],
           'neuroptics':[],
           'investment':[],
           'return':[]
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
    bar = '█' * int(percentage) + '-' * (100 - int(percentage))
    
    
    print(f"Checking {part_suffix}(s)...     Current warframe: {warframe[currentProgress].title()} Prime\n\r|{bar}| {currentProgress}\{total}\r")
    sys.stdout.write("\033[F")
###im gonna need to do this shit ..4 times so im gonna yeet the entire thing into a func and pass the params that change.
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
        minprice = []
        for orderID in range(0,len(rWFMget)):
            if rWFMget[orderID]['order_type'] == 'sell' and rWFMget[orderID]['user']['status'] == 'ingame':
                minprice.append(rWFMget[orderID]['platinum'])
                
        
        minprice = min(minprice)
        
        ###another patch because whooooops , apparently adding _blueprint results in a KeyError :clueless:
        
        if part_suffix in ('chassis_blueprint','systems_blueprint','neuroptics_blueprint'):
                part_suffix = part_suffix[:-10] ### if we have _blueprint , we remove em 
                
        prices[part_suffix].append(minprice)
        
    
###actually getting the prices

chkprice('set')
chkprice('blueprint')
chkprice('chassis')
chkprice('systems')
chkprice('neuroptics')

###calculating "investment" and "return"

for warframeID in range(0,len(warframe)):
    prices['investment'].append(prices['blueprint'][warframeID]+prices['chassis'][warframeID]+prices['systems'][warframeID]+prices['neuroptics'][warframeID])
    
    prices['return'].append(prices['set'][warframeID]-prices['investment'][warframeID])
    
###printing out the info


###|| Warframe || blueprint | systems | chassis | neuroptics || set | investment | return ||

from prettytable import PrettyTable

wfmtable = PrettyTable()

wfmtable.field_names = ["warframe","blueprint","systems","chassis","neuroptics","set","Investment","grofit"]
for warframeID in range(0,len(warframe)):
    wfmtable.add_row([warframe[warframeID],prices['blueprint'][warframeID],prices['systems'][warframeID],prices['chassis'][warframeID],prices['neuroptics'][warframeID],prices['set'][warframeID],prices['investment'][warframeID],prices['return'][warframeID]])
print(wfmtable)

dont_close_blyat = input("press anythin to close mate")
import time as pytime
import os
import random
from datetime import datetime

from tqdm import tqdm
from bypass_cryptoAPI import *
from bypass_tempmailAPI import *

# for i in tqdm.tqdm(range(800 * 12), desc="[+] Downloading"):
#     key = getrandomkey()
#     headers = {'X-CoinAPI-Key' : key}
#     url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/history?period_id=1HRS&time_start=' + time
#     response = requests.get(url, headers=headers)
#     if "error" in response.text:
#         print(response.text)
#         print("[-] Key is destroyed", key)
#         keys.remove(key)
#         print("[+] Trying next key")
#         continue

#     with open("data.json", "a") as file:
#         file.write(response.text)
            
    
#     a = json.loads(response.text)    
#     time = a[-1]["time_period_end"]
#     print(time.split("-")[0])
#     records += len(a)

def readKeys(filename:str) -> list:
    keys = []
    with open(filename, "r") as file:
        key = file.readline().strip('\n')
        while len(key) > 0:
            keys.append(key)
            key = file.readline().strip('\n')

    return keys


def validateKeys(api:CryptoAPI, keys:list, required:int=50) -> list:
    valid = []
    nonvalid = []
    for index in tqdm(range(len(keys)), desc="[+] Validating keys"):
        key = keys[index]
        if api.CheckKeyStatus(key):
            valid.append(key)
            with open("valid-keys.txt", "a") as file:
                file.write(key + "\n")
            continue

        nonvalid.append(key)

    if len(valid) < required:
        raise Exception()
    
    return valid

def getKeys(api, minkey:int) -> list:
    # get all the validated keys
    print("[+] Checking for valid keys")
    validated = readKeys("valid-keys.txt")
    if(len(validated) >= minkey):
        return validated
    
    print("[+] Checking for non-valid keys")
    nonvalid = readKeys("keys.txt")
    if((len(validated) + len(nonvalid)) >= minkey):
        print("[+] Validating non-valid keys")
        try:
            nonvalid = validateKeys(api, nonvalid, minkey)
        except Exception as e:
            print("[-] Could not validate enough keys, wait till keys are registered")
            exit()

        return validated + nonvalid
    
    raise Exception()
    


def getRandomKey(keys:list) -> str:
    if len(keys) == 0:
        raise Exception()
    
    index = random.randint(0, len(keys) - 1)
    return keys[index]

def getTimeFromData(csv:str) -> str:
    return csv.split(",")[0]

def getTime()->str:
    if not os.path.exists('./data.csv'):
        return '2016-01-01T00:00:00'

    with open("./data.csv", "r") as file:
        data = file.readlines()
        if len(data) > 0:
            time = getTimeFromData(data[-1])
            return time

    return '2016-01-01T00:00:00'

def convertToCsv(object:list) -> list:
    l = []
    for item in object:
        d = ""
        for value in item.values():
            d += str(value) + ","
        l.append(d)
    return l

def writeList(file, csv:list):
    for i in csv:
        file.write(i + "\n")

def calculateTimeSpan(p1, p2):
    pass

def getlocaltime():
    t = datetime.now()
    return t.strftime("%H:%M:%S")

def Update(start:float, interval:int) -> float:
    if (start - pytime.perf_counter() < interval):
        return start
    
    print(f"[i] {getlocaltime()} update message")

    return pytime.perf_counter()



# Options
MIN_KEYS = 50 # the minimum amount of keys needed to start the bot
BUFFER = 1 * 60 * 24 * 356 # one year buffer
PERIOD = 500 

def main() -> None:
    # Create objects
    api = CryptoAPI()

    # Step 1: Get the keys
    try:
        keys = getKeys(api, MIN_KEYS)
    except Exception as e:
        print("[-] Not enough keys to start bot, pls run keygen.py to generate the keys")
    
    print(f"[+] {len(keys)} keys validated")

    # Step 2: Check current data file
    time = getTime()
    print("[+] Starting from ", time)
    
    # Step 3: Download and append new data
    file = open("./data.csv", "a")
    update = pytime.perf_counter()
    active = True

    for i in tqdm(range(PERIOD), desc="[+] Downloading data"):
        update = Update(update, 2)
        k = getRandomKey(keys)
        try:
            # get data
            data = api.GetData(k, time)
            data = convertToCsv(data)
            
            # write data to file
            writeList(file, data)

            # update time
            time = getTimeFromData(data[-1])

        except CryptoAPIRequestError as e:
            # try new key
            print(f"[i] Key {k} broke")
            keys.remove(k)
            continue

        except Exception as e:
            file.close()
            print(e)
            print("[-] Error while downloading data")
            return
        
        except KeyboardInterrupt as e:
            print("[+] Quitting bot")
            


if __name__ == "__main__":
    main()
from ctypes import addressof
from fnmatch import fnmatch
import time as pytime
import os
import random
from datetime import datetime

from tqdm import tqdm
from bypass_cryptoAPI import *
from bypass_tempmailAPI import *

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

def getTime(file)->str:
    if not os.path.exists(file):
        return '2016-01-01T00:00:00'

    with open(file, "r") as file:
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

def Update(start:float, interval:int, message:str) -> float:
    if (pytime.perf_counter() - start < interval):
        return start
    
    print(f"[i] {getlocaltime()} {message}")

    return pytime.perf_counter()

def CheckData(object:list) -> bool:
    # list is empty, already on latest data
    if len(object) == 0:
        return False
    return True

def DateToInt(date:str)-> datetime:
    d,t = date.split("T")
    year, month, day = d.split("-")
    hour, min, sec = t.split(":")
    return datetime(int(year), int(month), int(day), int(hour), int(min))
    

def VerifyData(filename:str) -> bool:
    # open file
    prev = 0
    with open(filename, "r") as file:
        lines = file.readlines()
        for index in tqdm(range(len(lines)), desc="[+] Verifying data!!!"):
            line = lines[index]
            
            # get date
            d = line.split(",")[0]
            d = DateToInt(d)
            # skip first one
            if prev == 0:
                prev = d
                continue

            if d <= prev:
                return False
            
    
    return True


def add_record(line:str, record:list, buffersize:int) -> list:
    # remove first one
    if(len(record) >= buffersize):
        record.pop(0)
    
    record.append(line)
    return record

def check_record(line:str, record:list) -> bool:
    if line in record:
        return False

    return True 

def checkfilename(name):
    return name in os.listdir()


# Options
MIN_KEYS = 50 # the minimum amount of keys needed to start the bot
BUFFER = 1 * 60 * 24 * 356 # one year buffer
PERIOD = 5000 
RECORD_SIZE = 50
SYMBOL_ID = "BINANCE_SPOT_ETH_USDT"
PERIOD_ID = "5MIN"

def main() -> None:

    fname = f"{SYMBOL_ID}.csv"
    if checkfilename(fname):
        # verify old data
        if not VerifyData(fname):
            print("[-] ERROR: Data is not fully structured")
            exit()

    # Create objects
    api = CryptoAPI()

    # Step 1: Get the keys
    try:
        keys = getKeys(api, MIN_KEYS)
    except Exception as e:
        print("[-] Not enough keys to start bot, pls run keygen.py to generate the keys")
    
    print(f"[+] {len(keys)} keys validated")

    # Step 2: Check current data file
    time = getTime(fname)
    print("[+] Starting from ", time)
    
    # Step 3: Download and append new data
    file = open(fname, "a")
    update = pytime.perf_counter()
    active = True

    record_buffer = []

    for i in tqdm(range(PERIOD), desc=f"[+] Downloading data"):
        update = Update(update, 10, f"Time: {time}")
        k = getRandomKey(keys)
        try:
            # get data
            data = api.GetData(k, time, SYMBOL_ID, PERIOD_ID)

            # check data
            if not CheckData(data):
                print("[+] Downloaded all the data...quitting")
                exit()

            # get json data in csv format
            data = convertToCsv(data)
            
            # Check if data no already in file -> avoid duplicates
            if not check_record(data, record_buffer):
                continue

            # add line to buffer
            record_buffer = add_record(data, record_buffer, RECORD_SIZE)
            
            # write data to file
            writeList(file, data)

            # update time
            n = getTimeFromData(data[-1])
            if n == time:
                print("[+] Data up to date")
                exit()
            
            time = n

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
            exit()
            


if __name__ == "__main__":
    main()

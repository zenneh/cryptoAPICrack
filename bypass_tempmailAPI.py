import requests
import json
import urllib
import time
import re

class TMailAccount:
    def __init__(self, address):
        self.address= address
        self.login, self.domain = address.split("@")


class TMail():
    
    def __init__(self):
        self.api = "https://www.1secmail.com/api/v1/?"
        self.C_GENERATEMAILBOX = "genRandomMailbox"
        self.C_GETMESSAGES = "getMessages"
        self.C_READMESSAGE = "readMessage"

    def GetRandomMail(self, count=1):
        parameters = {
            "action":self.C_GENERATEMAILBOX,
            "count": str(count)
        }
        url = self.api + urllib.parse.urlencode(parameters)
        r = requests.get(url)
        accounts = []
        for user in json.loads(r.text):
            accounts.append(TMailAccount(user))

        return accounts

    def GetMailBox(self, account:TMailAccount):
        parameters = {
            "action":self.C_GETMESSAGES,
            "login": account.login,
            "domain": account.domain
        }
        url = self.api + urllib.parse.urlencode(parameters)
        r = requests.get(url)
        return json.loads(r.text)

    def ReadMessage(self, account, message):
        parameters = {
            "action":self.C_READMESSAGE,
            "login": account.login,
            "domain": account.domain,
            "id": message["id"]
        }
        url = self.api + urllib.parse.urlencode(parameters)
        r = requests.get(url)
        return json.loads(r.text)

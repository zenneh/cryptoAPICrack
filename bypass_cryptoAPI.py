from pypasser import reCaptchaV3
import requests
import json
import time
import urllib

class CryptoAPIRequestError(Exception):
    pass

class CryptoAPI:

    def __init__(self):
        self.header = {
            "Host": "www.coinapi.io",
            "Origin": "https://www.coinapi.io",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5"
        }

    def RequestKey(self, mail):

        # 1: getting captcha token
        anchor = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LemQuAUAAAAAGWCfov5kLghlSM5708-A3VbBoxb&co=aHR0cHM6Ly93d3cuY29pbmFwaS5pbzo0NDM.&hl=en&v=g9jXH0OtfQet-V0Aewq23c7K&size=invisible&cb=xg1hnz6zsld6"
        reCaptcha_response = reCaptchaV3(anchor)
        e = json.dumps(reCaptcha_response)

        # 2: make key request
        # payload
        data = {
            "email": mail,
            "name":"test",
            "title":"test",
            "companysize":"1000+",
            "recaptha3token": e,
            "e": ""
        }

        # make request
        r = requests.post("https://www.coinapi.io/www/freeplan", headers=self.header, data=json.dumps(data))

        # Check for valid request
        data = json.loads(r.text)
        if data["status"] != None:
            if data["status"] == "OK":
                return True
        
        print(r.text)
        return False
    
    # return json list of prices
    def GetData(self, key, time, symbol_id, period_id="5MIN") -> list:
        url = f'https://rest.coinapi.io/v1/ohlcv/{symbol_id}/history?period_id={period_id}&time_start={time}'
        header = {"X-CoinAPI-Key": key}

        r = requests.get(url, headers=header)
        if "error" in r.text:
            raise CryptoAPIRequestError
        
        return json.loads(r.text)
    
    def CheckKeyStatus(self, key) -> bool:
        header = {'X-CoinAPI-Key' : key,
            "Accept": "application/json",
            "Accept-Encoding": "deflate, gzip"
        }
        parameters = {
            "apikey": key
        }
        url = "https://rest.coinapi.io/v1/exchangerate/BTC?" + urllib.parse.urlencode(parameters)

        r = requests.get(url, headers=header)
        if "error" in r.text:
            return False

        return True

        

            


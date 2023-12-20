import json
import time
import tools
from request import http

clear_t = tools.next_day()
srap_count = 0


def game_captcha(gt: str, challenge: str):
    return get_validate(gt,challenge,'https://webstatic.mihoyo.com/')



def bbs_captcha(gt: str, challenge: str):
    return get_validate(gt,challenge,'https://app.mihoyo.com/')

def get_validate(gt: str, challenge: str, referer: str):
    def srap(gt: str, challenge: str):
        global srap_count
        req = http.post("http://gs.srap.link:8087/getvalidate", json={
            "gt": gt,
            "challenge": challenge
        }, timeout=120)
        print(req.text)
        if req.status_code != 200:
            return "many request"
        data = req.json()
        if data["status"] == "success":
            if data["data"]["result"] == "success":
                srap_count += 1
                return data["data"]["validate"]
            elif "many request" in data["data"]["msg"]:
                srap_count = 30
                return "many request"
        return None
    
    def rrocr(gt: str, challenge: str, referer: str):
        app_key = ""
        if app_key == "":
            return None
        req = http.post("http://api.rrocr.com/api/recognize.html", data={
            "appkey": app_key,
            "referer": referer,
            "gt": gt,
            "challenge": challenge
        }, timeout=60)
        print(req.text)
        data = req.json()
        if data["status"] == 0:
            return data["data"]["validate"]
        return None
    
    def fxxkmys(gt: str, challenge: str):
        token = ""
        if token == "":
            return None
        req = http.get("http://api.fuckmys.tk/geetest", params={
            "token": token,
            "gt": gt,
            "challenge": challenge
        }, timeout=60)
        print(req.text)
        data = req.json()
        if data["code"] == 0:
            return data["data"]["validate"]
        return None
    
    clear_ajax()
    if srap_count < 30:
        r = srap(gt,challenge)
        if r != "many request":
            return r
        r = fxxkmys(gt,challenge)
        if r is not None:
            return r
    return rrocr(gt,challenge,referer)


def clear_ajax():
    global clear_t
    global srap_count
    if int(time.time()) >= clear_t:
        srap_count = 0
        clear_t = tools.next_day()

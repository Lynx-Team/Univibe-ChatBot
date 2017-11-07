import json
import requests
import time
import urllib

#"416840082:AAEtRo9zN67iYCu9rt815OIMohIdwmCPbbo"
#"495392477:AAF6ebL1x3bpLKaJqn-t3vP9nNSDHQSvurM"
TOKEN = "416840082:AAEtRo9zN67iYCu9rt815OIMohIdwmCPbbo"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def getUrl(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def getJson(url):
    content = getUrl(url)
    js = json.loads(content)
    return js

def getUpdates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = getJson(url)
    return js

def getLastUpdateId(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def createAnswer(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        sendMessage(text, chat)

def sendMessage(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    getUrl(url)


def main():
    last_update_id = None
    while True:
        updates = getUpdates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = getLastUpdateId(updates) + 1
            createAnswer(updates)
        time.sleep(0.5)


#if __name__ == '__main__':
#    main()
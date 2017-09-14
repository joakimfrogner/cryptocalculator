import json
import requests
import sys
import datetime
import os
import shutil

from pprint import pprint

def setup():
    apilayer_key = input("Enter apilayer key: ")
    input_filename = "coindata.json"

    with open("settings.py", "w") as f:
        f.write("apilayer_key = \"{}\"\n".format(apilayer_key))
        f.write("input_file = \"{}\"".format(input_filename))

    shutil.copyfile("templates/coindata_template.json", input_filename)

if not os.path.isfile("settings.py"):
    setup()

from settings import *

def get_coins():
    url = "https://api.coinmarketcap.com/v1/ticker/"
    
    try:
        data = json.loads(requests.get(url).text)
    except:
        return False

    return [[x["name"], x["id"], x["symbol"], x["price_usd"]] for x in data]

def get_price(coin):
    coins = get_coins()

    try:
        price = [x[3] for x in coins if (x[2] == coin)][0]
    except:
        return False

    return float(price)

def convert(amount, after, before="USD"):
    try:
        data = json.loads(
            requests.get("http://apilayer.net/api/live?access_key={}&currencies=USD,{}&format=1".format(apilayer_key, after)).text)

        total = amount * float(data["quotes"]["USD{}".format(after)])

        return total
    except Exception as e:
        return False

def get_prices(coinlist, spent, conv="USD"):
    total = 0
    amounts = []    

    for coin in coinlist:
        price = get_price(coin["symbol"])
        amount = float(coin["amount"])

        sell_price = price * amount
        amounts.append([coin["symbol"], amount, "USD" + ": " + str(sell_price)])
        total += sell_price

    if conv != "USD": 
        converted = convert(total, conv)
        if converted:
            total = converted
        else:
            exit("No such currency {}".format(conv))

    return total, spent, conv, amounts

def get_log():
    with open(input_file) as f:
        data = json.loads(f.read())
        return data["log"]

if __name__ == '__main__':
    with open(input_file, "r+") as f:
        data = json.loads(f.read())
        total, spent, conv, amounts = get_prices(data["amounts"], data["total_spent"], conv=data["conv"])
        
        found_today = False

        for log in data["log"]["data"]:
            if str(datetime.date.today()) == log["date"]:
                log["spent"] = spent
                log["if_sold"] = str(int(total))
                found_today = True

        if not found_today:
            data["log"]["data"].append({ "spent": spent, "if_sold": str(int(total)) })

        f.seek(0)
        json.dump(data, f)
        f.truncate()

        if len(sys.argv) > 1 and sys.argv[1] == "-d":
            print("Total spent:       {} {}".format(conv, spent))
            print("Total if sold now: {} {}".format(conv, int(total)))
            print("Gained:            {} {}".format(conv, int(total) - int(spent)))
            print("----------------------------")
            pprint(amounts)
            input()

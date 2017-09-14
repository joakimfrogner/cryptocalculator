import datetime
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.dates import DateFormatter
from matplotlib import pyplot as plt

from settings import *
from calculate import *

def plot():
    data = get_log()
    log = data["data"]
    conv = data["conv"]
    
    x = [datetime.datetime.strptime(x["date"], "%Y-%m-%d").date() for x in log]
    y_spent = [x["spent"] for x in log]
    y_if_sold = [x["if_sold"] for x in log]
    #y_gained = [int(x["if_sold"]) - int(x["spent"]) for x in log]

    fig, ax = plt.subplots()
    ax.plot(x, y_spent, label="Invested ({})".format(conv))
    ax.plot(x, y_if_sold, label="If sold now ({})".format(conv))
    #ax.plot(x, y_gained, label="Gained ({})".format(conv))

    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))

    plt.xlabel("Date")
    plt.ylabel("Invested ({})".format(conv))
    plt.title("Data for investment in cryptocurrencies")
    plt.legend()
    
    plt.show()
    

if __name__ == '__main__':
    plot()

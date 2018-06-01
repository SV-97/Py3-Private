
from subprocess import check_output
from subprocess import call
from time import time, sleep, localtime, mktime
from datetime import datetime
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime as dt

plt.xkcd()

def main():
    start = time()
    log = open("Log.txt","a+")
    # function to ping a server and write the time it takes to answer into a file
    # in:   address - IP address to ping
    def ping(address="8.8.8.8"): 
        line = check_output("ping -n {number_of_pings} {address}".format(number_of_pings = "1", address = address), shell=True).decode("cp437")
        lines = line.split("\n")
        start_of_time = lines[2].find("Zeit")+len("Zeit=")
        delay = ""
        for digit in lines[2][start_of_time:]:
            if digit.isalpha():
                break
            else:
                delay += digit
        log.write(str(delay) + " at " + str(time()) + "\n")

    def plot(x,y,address="8.8.8.8"):
        plt.plot(x,y, linewidth = 2, label = address)
        plt.ylabel("Response time in ms") # label the y axis
        plt.xlabel("Timestamp") # label the x axis
        plt.legend() # show a small window with the label assigned in plot + the colour of the line

    
    ping()
    x = []
    y = []
    xstamp = []
    log.seek(0)
    for line in log.readlines():
        line = line.rstrip("\n")
        cx = float(line[line.find(" at ")+len(" at "):])
        xstamp.append(cx)
        cy = int(line[:line.find(" at ")])
        cx = localtime(cx)
        cx = datetime.fromtimestamp(mktime(cx))
        x.append(cx)
        y.append(cy)
    
    plot(x,y)
    
    plt.show()
    log.close()
    end = time()
    runtime = end - start #make function go at least seconds
    if (runtime) <= 20:
        sleep(5-runtime)
    plt.close()
    main()

main()
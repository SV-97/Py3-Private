
from subprocess import check_output
from subprocess import call
from multiprocessing import Process
from time import time, sleep, localtime, mktime
from datetime import datetime
from multiprocessing import Pool
import matplotlib.animation as animation
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime as dt

def pltshow():
    log = open("Log.txt","r")
    plt.xkcd()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    def plot(i,address="8.8.8.8"):
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
            ax.clear()
            ax.plot(x,y, linewidth = 2, label = address)
            plt.ylabel("Response time in ms") # label the y axis
            plt.xlabel("Timestamp") # label the x axis
            fig.legend() # show a small window with the label assigned in plot + the colour of the line
            plt.draw()

    ani = animation.FuncAnimation(fig,plot,interval = 1000)
    plt.show()

if __name__ == '__main__':
    p = Process(target=pltshow)

    def main():
        start = time()
        log = open("Log.txt","a")
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
    
        ping()
        log.close()
        end = time()
        runtime = end - start #make function go at least seconds
        if (runtime) <= 300:
            sleep(300-runtime)
        main()

    
    p.start()
    main()

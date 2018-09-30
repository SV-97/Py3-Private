import os
import re

path = os.path.dirname(__file__)
files = os.listdir(path)
day_files = re.findall(r"Day[0-9]+", "".join(files))
max_ = max([int(x[3:]) for x in day_files])

with open(path + "/Day" + str(max_+1), "w") as f:
    f.write("")

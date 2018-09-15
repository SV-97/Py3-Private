import os

path = os.path.dirname(__file__)

with open(__file__, "r+") as file:
    copy = file.readlines()
    file.seek(0)
    copy[-1] = copy[-1].replace("the_auto_list = [", 'the_auto_list = ["auto_entry", ')
    file.writelines(copy)
    file.truncate()
the_auto_list = []
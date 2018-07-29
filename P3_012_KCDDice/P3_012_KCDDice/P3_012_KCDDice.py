import random
import collections

#config
winningscore = 2000
numberofdice = 6
startingplayer = "random"
basepoints = {1:100,2:0,3:0,4:0,5:50,6:0}
#end config

priority = 0
while priority == 0:
    priority = random.Random().randint(-1,1) if startingplayer == "random" else (1 if startingplayer == "1" else -1) # randomize starting player

ews = []
for eyes, points in basepoints.items():
    if points != 0:
        ews.append(eyes)

class Die:
    def __init__(self):
        self.rnd = random.Random()
    def shuffle(self):
        self.val = self.rnd.randint(1,6)

class Player:
    def __init__(self,name):
        self.score = 0
        self.dice = [Die() for i in range(numberofdice)]
        self.name = name

def shuffle(dice):
    for die in dice:
        die.shuffle()


def turn(player):
    global priority 
    print("\nNew Turn - {} - {} points".format(player.name, player.score))
    turnscore = 0
    dice = player.dice #not sliced; no copy
    # if player chose to continue
    c = True
    while c == True:
        shuffle(dice)
        vals = [die.val for die in dice]
        print(vals)
        quantities = collections.Counter(vals) # quantity each number of eyes got rolled
        # check if there are any possible scores
        scored = False
        for eyes, quant in quantities.items():
            if quant >= 3:
                scored = True
            else:
                if eyes in ews:
                    if quant > 0:
                        scored = True
        if scored == False:
            print("Nothing to score")
            priority = -priority
            return

        # read which dice are to be scored
        invalid = True 
        while invalid == True:
            dicetoscore = collections.Counter(map(int,list(input("Enter dice to score: ").replace(" ", "")))) # seperated by whitespaces            invalid = False
            for eyes,quant in dicetoscore.items():
                if quant > quantities[eyes]:
                    print("Invalid input")
                    invalid = True
                else:
                    invalid = False
        # calculate score
        numberofremoveddice = 0
        noscore = False
        for eyes,quant in dicetoscore.items():
            if quant >= 3:
                if eyes == 1:
                    turnscore += 1000*(quant-2)
                else:
                    turnscore += eyes*100*(quant-2)
            else:
                a = basepoints[eyes]*quant
                noscore = True if a <= 0 else False # set turnscore to 0 if part of combination yields 0
                turnscore += a
            numberofremoveddice += quant
        if noscore == True:
            print("Scored 0!")
            priority = -priority
            return

        c = True if input("Current turnscore is {}. Shuffle again? y/n ".format(turnscore)) == "y" else False
        dice = dice[:len(dice)-numberofremoveddice] if len(dice) - numberofremoveddice != 0 else player.dice[:]
    player.score += turnscore
    priority = -priority

p1 = Player("Player 1")
p2 = Player("Player 2")
while p1.score < winningscore and p2.score < winningscore:
    if priority >= 0:
        turn(p1)
    if priority < 0:
        turn(p2)

winner, loser = (p1,p2) if p1.score > p2.score else (p2,p1)
print("\n{} won with {} points!\n".format(winner.name, winner.score))
print("The loser had {} points\n".format(loser.score))
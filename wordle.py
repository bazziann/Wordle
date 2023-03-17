import os
import random
import re
import time

# Utility functions

# Terminal color escape sequence
colors = {"black":"\033[0;30m", "red": "\033[0;31m", "green": "\033[0;32m", "yellow": "\033[0;33m", "cyan": "\033[0;36m", "white": "\033[0;37m", "reset": "\033[0m"}
def color(col):
    return colors[col]

def drawTable(workspace, isEnd=False):
    os.system("clear")
    print(color("red") + "                      W O R D L E  in  P Y T H O N \n\n" + color("reset"))
    rowSep = "       +" + ("---+" * 5)
    line = 0
    if isEnd:
        helpText = [workspace["info"]]
    else:
        helpText = []
        for line in help:
            helpText.append(line)
        helpText.append(" ")
        for line in workspace["keyboard"]:
            helpText.append(line)
    n = 0
    for row in workspace["rows"]:
        toPrint = rowSep
        if n < len(helpText):
            toPrint += helpText[n]
        toPrint += "\n"
        n += 1
        toPrint += "       " + row
        if n < len(helpText):
            toPrint += helpText[n]
        n += 1
        print(toPrint)
    print(rowSep)

def isValid(workspace, word):
    if len(word) != 5:
        print(color("red") + "   Word must have 5 letters!" + color('reset'))
        return False
    if word not in validWords:
        print(color("red") + "   That word does not exist!" + color('reset'))
        return False
    if word in workspace["guessList"]:
        print(color("red") + "   You already tried that word." + color('reset'))
        return False
    return True

def prompt(displayPrompt):
    print(color("yellow") + displayPrompt + ">>" + color("green"), end="")
    response = input().strip()
    print(color("reset"))
    return response

def updateKeyboard(workspace, inp):
    chars = [*inp]
    for char in chars:
        if workspace["answer"].find(char) == -1:
            c = color("red")
        else:
            c = color("cyan")
        r = color("reset")
        for i in range(len(workspace["keyboard"])):
            workspace["keyboard"][i] = workspace["keyboard"][i].replace(char, c + char + r)

def check(workspace, inp):
    workspace["gotIt"] = (workspace["answer"] == inp)
    chars_inp = [*inp]
    workspace["guess"] = chars_inp
    workspace["guessList"].append(inp)
    chars_answer = [*workspace["answer"]]
    colored_chars = []
    for n in range(5):
        c = chars_inp[n]
        exp = workspace["answer"][n]
        if c == exp:
            col = color("green")
        elif c in workspace["answer"]:
            col = color("yellow")
        else:
            col = color("reset")
        colored_chars.append(col + c + color("reset"))

    workspace["show"] = "| " + " | ".join(colored_chars) + " |"

# Save data is persisted to file
saves = "scores";   # path to savefile
scores = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "Wins":0,"Fails":0,"Streak":0,"Longest Streak":0,"gametime":0}

def savescores():
    fh = open(saves, "w")
    for key in scores.keys():
        fh.write(f"{key} = {int(scores[key])}\n")
    fh.close()

# Read save file
if os.path.exists(saves):  
    lines = open(saves, "r").read().strip().split("\n")
    for line in lines:  
        values = line.split("=")
        scores[values[0]] = int(values[1])

# Read words from dictionary file
if os.path.exists("words"):
    source = "words"
else:
    source = "/usr/share/dict/words"

validWords = set()
words = open(source, "r").read().strip().split("\n")
for word in words:
    if re.search(r"^[a-z]{5}$", word):
        validWords.add(word)

help = [
    "   Try and guess a 5 letter word in 6 moves"," ",
    color("green") + "   Green " + color("reset") + "  = Right letter in right place",
    color("yellow") + "   Yellow " + color("reset") + " = Right letter in wrong place",
    "   Keyboard " + color("red") + " Red " + color("reset") + " = letter not found in word", 
    "   Keyboard " + color("cyan") + " Cyan " + color("reset") + "= letter found in word",
    "   Enter 'Q' to quit.",
]

# Main game loop
while True:
    # Keep track of how long it takes user to solve
    startTime = time.time()
    
    workspace = {
        "goes": 0,
        "guess":"",
        "gotIt": False,
        "guessList":[],
        "keyboard": [
            "    q  w  e  r  t  y  u  i  o  p ",
            "      a  s  d  f  g  h  j  k  l ",
            "        z  x  c  v  b  n  m ",
        ],
        "answer": random.choice(tuple(validWords)),
        "info": "",
        "rows": [],
    }
    for i in range(6):
        workspace["rows"].append("|" + "   |"*5)
    
    while not workspace["gotIt"]:
        workspace["goes"] += 1
        drawTable(workspace)
        while True:
            inp = input(f"   Guess {(workspace['goes'])}: ")
            if inp == "Q":
                exit()
            if isValid(workspace, inp):
                break
        updateKeyboard(workspace, inp) #color keyboard
        check(workspace, inp) #check for match
        workspace["rows"][workspace["goes"]-1] = workspace["show"] 
        workspace["guess"] = "" #reset guess

        if workspace["goes"] == 6:
            break
    scores["gametime"] = time.time() - startTime
    if workspace["gotIt"]:
        workspace["info"] = color("green") + "        **WELL DONE**" + color("reset") + "   Got it in " + str(workspace["goes"]) + " goes in " + str(scores["gametime"]) + " secs"
        scores["Wins"] += 1
        scores["Streak"] += 1
        if scores["Longest Streak"] < scores["Streak"]:
            scores["Longest Streak"] = scores["Streak"]
    else:
        workspace["info"] = color("red") + "     Failed!! answer was " + color("reset") + workspace["answer"]
        scores["Fails"] += 1
        scores["Streak"] = 0

    drawTable(workspace, True)
    savescores()

    inp = input(f"   Want another game? Y/N: ")
    if inp == "N":
        break
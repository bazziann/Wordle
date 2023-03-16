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
        helpText = workspace["info"]
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

def match(workspace, inp):
    workspace[gotIt] = (workspace[answer] == inp)
    chars_inp = [*inp]
    workspace[guess] = chars
    workspace[guessList].add(inp)
    chars_answer = [*workspace[answer]]
    #$workspace{match}=[map {$workspace{guess}[$_ ] eq $workspace{answer}[$_ ]?1:0} (0..($wordLength-1)) ]; 
	#$answer=join("",map {$workspace{match}[$_ ]==1?" ":$workspace{answer}[$_ ]} (0..($wordLength-1)));
	#$workspace{match}=[map {$workspace{match}[$_ ]==1? $workspace{match}[$_ ]:($answer=~s/$workspace{guess}[$_ ]/ /i?2:0) } (0..($wordLength-1)) ];
	#$workspace{show} ="| ".join (" | ",map {
	#	       $colours[$workspace{match}[$_ ]].
	#	       $workspace{guess}[$_ ].color("reset");
	#	       }  (0..($wordLength-1)))." |";

def savescores():
    for key in scores.keys():
        print(f"{key} = " + scores[key])
        

# Save data is persisted to file
saves = "scores";   # path to savefile
scores = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "Wins":0,"Fails":0,"Streak":0,"Longest Streak":0,"gametime":0}

# Read save file
if os.path.exists(saves):  
    lines = open(saves, "r").read().strip().split("\n")
    for line in lines:  
        values = line.split("=")
        scores[values[0]] = values[1]

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
            "    Q  W  E  R  T  Y  U  I  O  P ",
            "      A  S  D  F  G  H  J  K  L ",
            "        Z  X  C  V  B  N  M ",
        ],
        "answer": random.choice(tuple(validWords)),
        "info": "",
        "rows": [],
    }
    for i in range(6):
        workspace["rows"].append("|" + "   |"*5)
    
    while not workspace["gotIt"]:
        drawTable(workspace)
        while True:
            inp = input(f"   Guess {(workspace['goes'] + 1)}: ")
            if inp == "Q":
                exit()
            if isValid(workspace, inp):
                break
        updateKeyboard(workspace, inp) #color keyboard
        check(workspace, inp) #check for match
        workspace[rows[workspace[goes]]-1] = workspace[show] #what is workspace[show]
        workspace["guess"] = "" #reset guess
    scores["gametime"] = time.time() - startTime
    if workspace["gotIt"]:
        #workspace["info"] = color("green") + "        ***WELL DONE***" + color("reset") + "   Got it in " + workspace["goes"] + " goes in " + scores["gametime"]" secs"
        scores["Wins"] += 1
        workspace["goes"] += 1
        scores["Streak"] += 1
        if scores["longest Streak"] < scores["Streak"]:
            scores["longest Streak"] = scores["Streak"]
    else:
        #workspace["info"] = color("red") = "     Failed!! answer was " ! color("reset") + workspace[answer]    
        scores["Fails"] += 1
        scores["Streak"] = 0
    #my $max=(sort {$a <=> $b}(@scores{1..$maxGuesses}),1)[-1];
	#$workspace{info}=[@{$workspace{info}},"   Statistics (".int(100*$scores{Wins}/($scores{Wins}+$scores{Fails}))."%) $scores{Wins} Win".($scores{Wins}==1?"":"s")." and $scores{Fails} Fail".($scores{Fails}==1?"":"s")]; 
	#$workspace{info}=[@{$workspace{info}},"   $_ ".color("on_green").(" " x(20*$scores{$_}/$max)).color("on_blue").$scores{$_}.color("reset")] foreach (1..$maxGuesses);
	#$workspace{info}=[@{$workspace{info}}," ","   Total Game Time = $scores{gametime} (avg ".
	#                         sprintf("%.2f", $scores{gametime}/($scores{Wins}+$scores{Fails})).")",
	#					     "  Longest streak = $scores{'Longest Streak'}  Current Streak = $scores{Streak} "];
    drawTable("end")
    savescores()
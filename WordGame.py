import random

from time import *
import threading

#list comprehension to generate grid
grid = [[ '_' for _ in range(5)] for _ in range(4)]
#this is the new grid that will replenish letters if a proper word is inputted
newGrid = [[ '_' for _ in range(5)] for _ in range(4)]

scoreList = []

def main():
    global grid
    generateGrid()
    printGrid(grid)
    decision = showMenu()


    
    while (decision != "quit"): #this is not possible, but will quit if they press 3, so wouldn't come here
        if(decision=="play"):
            score = play()
            print("Your score is "+ str(score) +".\n")
            checkRoundScore(score)
            generateGrid()
        elif(decision=="scores"):
            if (len(scoreList) == 0):
                print("\nThere are no High Scores at the moment.")
            else: # got a score that isn't 0
                highScores()

        sleep(1)
        print("\n\nYou can still play!")
        begOfPlay = False
        decision = showMenu()

def showMenu(): #shows the menu and returns play, scores, or exits
    menu = int(input(
        
"""
Game Menu:
1 - to play
2 - to see the high scores
3 - to quit

your choice: """))

    
    while (menu != 3):
        if menu == 1:
            return "play"
        elif menu == 2:
            return "scores"
        else:
            print("That was an invaild input, try again.")
            menu = int(input(
        
"""
Game Menu:
1 - to play
2 - to see the high scores
3 - to quit

your choice: """))
    exit(0)

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def generateGrid():      #creates a grid with random letters  
    for x in range(4):
        for y in range(5):
            grid[x][y] = random.choice(alphabet)

def printGrid(grid): #prints the generated grid without brackets or commas
    print()
    for i in range(4):
        print(' '.join(grid[i])) #prints 4 letters without any commas or brackets    
    print()
        
def play(): #returns the score for that round
    score = 0

    #countdown is a function below
    countDownThread = threading.Thread(target = countDown) #sets up timer to be able to run while other code is running
    countDownThread.start()

    while timer > 0: #will only run the code while timer has more than 0 secs

        printGrid(grid)
        word = input("Write a word using letters in the grid:") #ALWAYS LETS YOU WRITE A WORD EVEN IF PAST TIME
        onBoard = checkForLetter(word)#saves as true or false
        inDict = checkDict(word)#saves as true or false
        
        if (onBoard == True and inDict == True): 
            copyGrid(grid, newGrid)
            score = score + len(word)
        else:
            print("That word does not meet the criteria. Try again.")

    
    #print("out of the while loop")
    print("\nTimes up!\n")
    return score

def copyGrid(copyTo, copyFrom):
    for x in range(4):
        for y in range(5):
            copyTo[x][y] = copyFrom[x][y]

def checkForLetter(word): #returns True or False
    wordList = [] #list of all the letters in the input
    for l in word:
        wordList.append(l)

    #sets newGrid to grid without same reference point #will also clear the previous changes from a board where the word was rejected
    for x in range(4):
        for y in range(5):
            newGrid[x][y] = grid[x][y]

    
    for x in range(4):
        for y in range(5):
            for l in wordList: #checks each letter on grid with each letter in wordList to see if it's the same
                if (grid[x][y] == l):
                    newGrid[x][y] = random.choice(alphabet) #if it is the same, that letter gets switched out for a new random letter
                    wordList.remove(l) #the letter that was on the board is removed from wordList



    if len(wordList) == 0: #if all the letters were in the list and therefore removed

        return True
    
    elif (len(wordList) >= 0):
        return False
    
    printGrid(newGrid)
    
def checkDict(word):
    userWord = word
    userWord.lower()

    #will only check dictionary if it's more than 3 letters
    if (len(userWord) < 3):
        return False

    file = "Dictionary.txt"

    infile=open(file,'r') 
    dictWords=[line.strip() for line in infile]
    infile.close()


    for dw in dictWords:
        if (userWord == dw):
            return True
    #will only come here if none returned true        
    return False


def checkRoundScore(score): #sorts and chops off end, and if highscore will append

    global scoreList
    
    becameHighScore = False

    if (score == 0):
        print("Sorry, but that was not a high score.")
        return
    
    if (len(scoreList) == 0):
        smallestScoreList = [0, 0]
    else:
        smallestScoreList = min(scoreList)
    
    smallestScore = smallestScoreList[0]
    
    if ((len(scoreList) < 10) or (score > smallestScore)): #compares score to the smallest score
        organizeHighscores(score)
        becameHighScore = True

    elif(score < scoreList[0][0]):
        print("Sorry, but that was not a high score.")
        
    
    if (becameHighScore == True): #if they have a new score
        highScores() #prints the high scores #scoreList
        
def organizeHighscores(score):
    global scoreList
    
    print("Congrats!! You got a high score!")
    playerName = input("What is your name?\t")
    playerName = playerName.title()
    scoreList.append([score, playerName])

    scoreList.sort(reverse = True)#reverse = True
    scoreList = scoreList [:10]
    
def highScores():
    global scoreList

    print("\nHigh Scores:")
    for playerAndScore in scoreList:
        print("{},\t{}".format(playerAndScore[1], playerAndScore[0]))
    
def countDown():
    global timer
    
    timer = 20

    for t in range(20):
        timer = timer - 1
        sleep(1)
        
        
main()
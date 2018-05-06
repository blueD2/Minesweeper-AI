#A command line version of Minesweeper
import random
import re
import time
import config
from string import ascii_lowercase

#GRID NUMBERS
#Bomb: -4
#Wall: -3
#Unclicked: -1
#Flag: -2

class Minesweeper:
    def __init__(self):
        dumb = 1

    def setupgrid(self, gridsize, start, numberofmines):
        emptygrid = [[-1 for i in range(gridsize)] for i in range(gridsize)]

        mines = self.getmines(emptygrid, start, numberofmines)

        for i, j in mines:
            emptygrid[i][j] = -4

        grid = self.getnumbers(emptygrid)

        return (grid, mines)


    #def showgrid(grid):
    #    gridsize = len(grid)
    #
    #    horizontal = '   ' + (4 * gridsize * '-') + '-'
    #
    #    # Print top column letters
    #    toplabel = '     '
    #
    #    for i in ascii_lowercase[:gridsize]:
    #        toplabel = toplabel + i + '   '
    #
    #    print(toplabel + '\n' + horizontal)
    #
    #    # Print left row numbers
    #    for idx, i in enumerate(grid):
    #        row = '{0:2} |'.format(idx + 1)
    #
    #        for j in i:
    #            row = row + ' ' + j + ' |'
    #
    #        print(row + '\n' + horizontal)
    #
     #   print('')


    def getrandomcell(self, grid):
        gridsize = len(grid)

        a = random.randint(0, gridsize - 1)
        b = random.randint(0, gridsize - 1)

        return (a, b)


    def getneighbors(self, grid, rowno, colno):
        gridsize = len(grid)
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                    neighbors.append((rowno + i, colno + j))

        return neighbors


    def getmines(self, grid, start, numberofmines):
        mines = []
        neighbors = self.getneighbors(grid, *start)

        for i in range(numberofmines):
            cell = self.getrandomcell(grid)
            while cell == start or cell in mines or cell in neighbors:
                cell = self.getrandomcell(grid)
            mines.append(cell)

        return mines


    def getnumbers(self, grid):
        for rowno, row in enumerate(grid):
            for colno, cell in enumerate(row):
                if cell != -4:
                    # Gets the values of the neighbors
                    values = [grid[r][c] for r, c in self.getneighbors(grid,rowno, colno)]

                    # Counts how many are mines
                    grid[rowno][colno] = values.count(-4)

        return grid


    #def showcells(grid, currgrid, rowno, colno):
    #    # Exit function if the cell was already shown
    #    if currgrid[rowno][colno] != ' ':
    #        return
    #
    #    # Show current cell
    #    currgrid[rowno][colno] = grid[rowno][colno]
    #
    #    # Get the neighbors if the cell is empty
    #    if grid[rowno][colno] == '0':
    #        for r, c in getneighbors(grid, rowno, colno):
    #            # Repeat function for each neighbor that doesn't have a flag
    #            if currgrid[r][c] != 'F':
    #                showcells(grid, currgrid, r, c)

    def guessClear(self, grid, currgrid, r, c):
        if currgrid[r][c] != -1:
            return

        currgrid[r][c] = grid[r][c]

        if grid[r][c] == 0:
            for r, c in self.getneighbors(grid, r, c):
                # Repeat function for each neighbor that doesn't have a flag
                if currgrid[r][c] != -2:
                    self.guessClear(grid, currgrid, r, c)


    #def playagain():
    #    choice = input('Play again? (y/n): ')
    #
    #    return choice.lower() == 'y'


    #def parseinput(inputstring, gridsize, helpmessage):
    #    cell = ()
    #    flag = False
    #    message = "Invalid cell. " + helpmessage
    #
    #    pattern = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[gridsize - 1])
    #    validinput = re.match(pattern, inputstring)
    #
    #    if inputstring == 'help':
    #        message = helpmessage
    #
    #    elif validinput:
    #        rowno = int(validinput.group(2)) - 1
    #        colno = ascii_lowercase.index(validinput.group(1))
    #        flag = bool(validinput.group(3))
    #
    #        if -1 < rowno < gridsize:
    #            cell = (rowno, colno)
    #            message = ''
    #
    #    return {'cell': cell, 'flag': flag, 'message': message}

    def move(self, ann, currgrid, numFlags, numberofmines):
        highestCell = ()
        highestP = -1
        lowestCell = ()
        lowestP = 2
        for r, rvalue in enumerate(currgrid):
            for c, cvalue in enumerate(rvalue):
                if(cvalue == -1):
                    inputs = self.getregion(currgrid, r, c)
                    p = ann.evaluate(inputs)
                    #if (p[0] < .05 and numFlags < numberofmines): #probably a bomb
                    #    return {'cell': (r, c), 'flag': True}
                    if (p[0] > highestP):
                        highestP = p[0]
                        highestCell = (r, c)
                    if (p[0] < lowestP):
                        lowestP = p[0]
                        lowestCell = (r, c)
        highDiff = 1 - highestP
        lowDiff = lowestP
        if(numFlags < numberofmines and highestP > .975 and highDiff < lowDiff):
            return {'cell': highestCell, 'flag': True}
        return {'cell': lowestCell, 'flag': False}

    def getregion(self, currgrid, r, c):
        gridsize = len(currgrid)
        inputs = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (i==0 and j==0):
                    continue
                elif -1 < (r + i) < gridsize and -1 < (c + j) < gridsize:
                    inputs.append(currgrid[r + i][c + j])
                else:
                    inputs.append(-3)
        return inputs


    def calcscore(self, currgrid, grid, won, display):
        score = 0
        correctflags = 0
        incorrectflags = 0
        spacescleared = 0
        for rowno, row in enumerate(currgrid):
            for colno, cell in enumerate(row):
                if cell == -2:
                    if grid[rowno][colno] == -4:
                        score = score + 20
                        correctflags = correctflags + 1
                    else:
                        score = score - 10
                        incorrectflags = incorrectflags + 1
                else:
                    if won or cell != -1:
                        score = score + 1
                        spacescleared = spacescleared + 1
        if display:
            print("Correct flags: " + str(correctflags) + " Incorrect flags: " + str(incorrectflags) + " Spaces cleared: " + str(spacescleared))
            print("Score: " + str(score))
        return score

    def playgame(self,ann,display):
        gridsize = config.board['width']
        numberofmines = config.board['bombs']
        isDead = False

        currgrid = [[-1 for i in range(gridsize)] for i in range(gridsize)]

        grid = []
        flags = []
        #starttime = 0

        #helpmessage = ("Type the column followed by the row (eg. a5). To put or remove a flag, add 'f' to the cell (eg. a5f).")

        #showgrid(currgrid)
        #print(helpmessage + " Type 'help' to show this message again. *notices bulge* oWo what's this?\n")

        while True:
            minesleft = numberofmines - len(flags) 
            #prompt = input('Enter the cell ({} mines left): '.format(minesleft))
            #result = parseinput(prompt, gridsize, helpmessage + '\n')
            result = self.move(ann, currgrid, len(flags), numberofmines)

            #message = result['message']
            cell = result['cell']

            if cell:
                #print('\n\n')
                rowno, colno = cell
                currcell = currgrid[rowno][colno]
                flag = result['flag']

                if not grid:
                    grid, mines = self.setupgrid(gridsize, cell, numberofmines)
                #if not starttime:
                    #starttime = time.time()

                if flag:
                    # Add a flag if the cell is empty
                    if currcell == -1:
                        currgrid[rowno][colno] = -2
                        flags.append(cell)
                    # Remove the flag if there is one
                    #elif currcell == 'F':
                    #    currgrid[rowno][colno] = ' '
                    #    flags.remove(cell)
                    else:
                        raise Exception("Tried to put a flag in nonempty square")

                # If there is a flag there, show a message
                elif cell in flags:
                    raise Exception("Tried to click a flag")

                elif grid[rowno][colno] == -4:
                    #print('RIP\n')
                    #showgrid(grid)
                    #if playagain():
                        #playgame()
                    return self.calcscore(currgrid, grid, False, display)

                elif currcell == -1:
                    self.guessClear(grid, currgrid, rowno, colno)

                else:
                    raise Exception("Tried to click a revealed square")

                if set(flags) == set(mines):
                    #minutes, seconds = divmod(int(time.time() - starttime), 60)
                    
                    #showgrid(grid)
                    #if playagain():
                        #playgame()
                    return self.calcscore(currgrid, grid, True, display)

            #showgrid(currgrid)
            #print(message)

    #playgame()




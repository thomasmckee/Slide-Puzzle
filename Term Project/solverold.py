import math
import random
import copy

def mDist(board):
    totalDist = 0
    L = int(math.sqrt(len(board)))
    for i in range(int(L**2)):
        cX, cY = i % L, i // L
        fX, fY = board[i] % L, board[i] // L
        dX, dY = abs(cX-fX), abs(cY - fY)
        totalDist += (dX+dY)
    return totalDist

def nDisp(board):
    totalDisp = 0
    L = int(math.sqrt(len(board)))
    for i in range(int(L**2)):
        if i != board[i]:
            score = 1
            totalDisp += score
    return totalDisp
    
def getScore(board):
    return mDist(board) + nDisp(board)

def isLegalMove(move, L):
    for i in move:
        if i < 0 or i >= L:
            return False
    return True

def getMoves(board):
    finalMoves = []
    L = int(math.sqrt(len(board)))
    zI = board.index(L**2-1)
    zX, zY = zI % L, zI // L
    testMoves = [[zX+1, zY], [zX-1, zY], [zX, zY+1], [zX, zY-1]]
    for move in testMoves:
        if isLegalMove(move, L):
            finalMoves.append(move)
    return finalMoves

def makeMove(board, move, L):
    copyBoard = copy.deepcopy(board)
    zI = copyBoard.index(L**2-1)
    moveI = move[0] + L*move[1]
    copyBoard[zI], copyBoard[moveI] = copyBoard[moveI], copyBoard[zI]
    return copyBoard

def solvedBoard(board):
    return board == list(range(len(board)))

def depthSearchWrapper(board, depth):
    def depthSearch(board, depth, tempList = []):
        L = int(math.sqrt(len(board)))
        if solvedBoard(board):
            return tempList
        if depth == 0:
            if getScore(board) < minScore[1]:
                m = [tempList, getScore(board)]
        else:
            for move in getMoves(board):
                tempList.append(move)
                newBoard = makeMove(board, move, L)
                depthSearch(newBoard, depth - 1, tempList)
    depthSearch(board, depth)
    return minScore[0]

def solve(board, seenList = []):
    seenList.append(board)
    L = int(math.sqrt(len(board)))
    if solvedBoard(board):
        return True
    minScore = [[], 10000]
    for newBoard in depthSearchWrapper(board, 5):
        if newBoard in seenList:
            continue
        score = getScore(newBoard)
        if score < minScore[1]:
            minScore = [newBoard, score]
    printBoard(board)
    print(minScore[1])
    solve(minScore[0], seenList)

#ignore rest

def changeBoard(board):
    newBoard = copy.deepcopy(board)
    for i in range(len(newBoard)):
        if newBoard[i] == 8:
            newBoard[i] = 0
        else:
            newBoard[i] += 1
    return [newBoard[:3], newBoard[3:6], newBoard[6:]]

def make2dList(rows, cols, value):
    a=[]
    for row in range(rows): a += [[value]*cols]
    return a

def makeBoard(n):
    board = createBoard(n)
    newBoard = changeBoard(board)
    while not isValidBoard2(newBoard):
        board = createBoard(n)
        newBoard = changeBoard2(board)
    return board

def createBoard(n):
    values = list(range(0, n**2))
    board = [0]*(n**2)
    for i in range(len(board)):
        valIndex = random.randint(0, len(values)-1)
        board[i] = values[valIndex]
        values.remove(values[valIndex])
    return board

#Information about valid board states taken from this website:
#https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
def isValidBoard(board):
    newBoard = changeBoard(board)
    return isValidBoard2(newBoard)

def printBoard(board):
    print(board[:3])
    print(board[3:6])
    print(board[6:9])
    print('------------')
    
def isValidBoard2(board):
    newLst = flattenList(board)
    inversions = 0
    for i in range(len(newLst)):
        check = newLst[i:]
        for j in check:
            if newLst[i] > j and j != 0:
                inversions += 1
    if len(board) % 2 == 1:
        if inversions % 2 == 0:
            return True
    elif len(board) % 2 == 0:
        if (newLst.index(0)//len(board)) % 2 == 0:
            if inversions % 2 == 1:
                return True
        elif (newLst.index(0)//len(board)) % 2 == 1:
            if inversions % 2 == 0:
                return True
    return False

def testBoard():
    for i in range(10):
        board = makeBoard(3)
        newBoard = changeBoard(board)
        if isValidBoard2(newBoard):
            return(board)
        else:
            print(1)

def make2dList(rows, cols, value):
    a=[]
    for row in range(rows): a += [[value]*cols]
    return a

def flattenList(lst):
    newLst = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            newLst.append(lst[i][j])
    return newLst

def isValidBoard(board):
    L = int(math.sqrt(len(board)))
    inversions = 0
    for i in range(len(board)):
        if i == L**2-1:
            continue 
        check = board[i:]
        for j in check:
            if board[i] > j:
                inversions += 1
    if len(board) % 2 == 1:
        if inversions % 2 == 0:
            return True
    elif len(board) % 2 == 0:
        if (board.index(L**2-1)//L) % 2 == 0:
            if inversions % 2 == 1:
                return True
        elif (board.index(L**2-1)//L) % 2 == 1:
            if inversions % 2 == 0:
                return True
    return False

def changeBoard2(board):
    newBoard = copy.deepcopy(board)
    for i in range(len(newBoard)):
        if newBoard[i] == 15:
            newBoard[i] = 0
        else:
            newBoard[i] += 1
    return [newBoard[:4], newBoard[4:8], newBoard[8:12], newBoard[12:]]
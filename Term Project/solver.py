import math
import copy
import time
import cProfile

'''
This solver implements the A* search algorithm to find the optimal solution
of a slide puzzle. Originally, it was going to be used to used to solve a
4x4 puzzle, but that requires and iterative-deepening A* algorithm and a 
heursitic function more complex than manhattan distance to run in reasonable 
time. Overall, it seemed to be outside the scope of this class, and definitely
beyond my personal skill.

For that reason, I chose to reduce the size of the image puzzle in the project
to 3x3. Even so, for particularly difficult 3x3 boards, the solver may still 
take minutes to find the optimal path. Most boards will find the optimal path
in under 20 seconds, however.

It is worth noting that whenever it finds a path, it will always be the optimal 
one. Although its functionality is limited, the solver still correctly 
implements the algorithm.
'''

#Making move on board
def makeMove(board, move):
    L = int(math.sqrt(len(board)))
    copyBoard = copy.copy(board)
    zI = copyBoard.index(L**2-1)
    #Calculating move index in 1D list based off of x/y coords
    moveI = move[0] + L*move[1]
    copyBoard[zI], copyBoard[moveI] = copyBoard[moveI], copyBoard[zI]
    return copyBoard

#Function to find the board based off of the given path
def makeMoves(board, path):
    newBoard = copy.copy(board)
    for move in path:
        newBoard = makeMove(newBoard, move)
    return newBoard

def mDist(board): #Calculating manhattan distance of board
    totalDist = 0
    L = int(math.sqrt(len(board)))
    for i in range(L**2):
        #Finding sum of differences between x and y coordinates
        if board[i] == (L**2 - 1):
            continue
        cX, cY = i % L, i // L
        fX, fY = board[i] % L, board[i] // L
        dX, dY = abs(cX-fX), abs(cY - fY)
        totalDist += (dX+dY)
    return totalDist
    
def nDisp(board):
    score = 0
    for i in range(len(board)):
        if i != board[i]:
            score += 1
    return score

def getLegalMoves(board):
    finalMoves = []
    L = int(math.sqrt(len(board)))
    #Finding the coordinates of the blank
    zI = board.index(L**2-1)
    zX, zY = zI % L, zI // L
    #Finding possible moves from that blank
    testMoves = [[zX+1, zY], [zX-1, zY], [zX, zY+1], [zX, zY-1]]
    for move in testMoves:
        if isLegalMove(move, L):
            finalMoves.append(move)
    return finalMoves

def isLegalMove(move, L):
    #Move is legal if on board
    for i in move:
        if i < 0 or i >= L:
            return False
    return True

def solve(board):
    visited = 0
    seen = []
    queue = [] #List of paths, where a path is a sequence of moves
    for move in getLegalMoves(board): #Getting initial paths and seen boards
        queue.append([move])
        newBoard = makeMove(board, move)
        seen.append(newBoard)
    seen.append(board)
    def search(queue, board, visited):
        bestScore = math.inf
        bestSteps = 0
        bestPath = None
        for path in queue:
            #Score based off of A* = estimated distance to finish + current cost
            dist = mDist(makeMoves(board, path))
            steps = len(path)
            score = dist + steps
            #Checking if solved
            if dist == 0:
                return path
            #Finding best path that has not already been expanded
            #In case of a tie, prefer path that is longer
            if score == bestScore:
                if steps > bestSteps:
                    bestScore = score
                    bestPath = path
                    bestSteps = steps
            if score < bestScore:
                bestScore = score
                bestPath = path
                bestSteps = steps
        visited += 1
        #Removing the path since it is going to be expanded
        queue.remove(bestPath)
        bestPathBoard = makeMoves(board, bestPath)
        #Expanding the path
        for move in getLegalMoves(bestPathBoard):
            newPath = bestPath + [move]
            newPathBoard = makeMoves(board, newPath)
            #because unique paths can lead to common boards, checking if same
            #boards exist in seen
            if newPathBoard not in seen:
                seen.append(newPathBoard)
                queue.append(newPath)
        #Recursing
        return search(queue, board, visited)
    return search(queue, board, visited)

#This function copied from 15-112 website
def callWithLargeStack(f,*args):
    import sys
    import threading
    threading.stack_size(2**27)  # 64MB stack
    sys.setrecursionlimit(2**27) # will hit 64MB stack limit first
    # need new thread to get the redefined stack size
    def wrappedFn(resultWrapper): resultWrapper[0] = f(*args)
    resultWrapper = [None]
    #thread = threading.Thread(target=f, args=args)
    thread = threading.Thread(target=wrappedFn, args=[resultWrapper])
    thread.start()
    thread.join()
    return resultWrapper[0]


#Some random test stuff 
'''
t1 = time.time()
print(callWithLargeStack(solve,[7, 2, 8, 1, 5, 6, 0, 3, 4]))
t2 = time.time()
print('Time: %0.2f'%(t2-t1))
'''
#print(solve([8, 0, 7, 1, 5, 6, 2, 3, 4]))
#830267145
#018267345
#271354860 the bad one
#831746250 the worse one

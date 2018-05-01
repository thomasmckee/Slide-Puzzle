import math
import copy

# Depth First Search - Finds the best score within a certain depth
# Original approach wasn't ideal since deepcopy requires you copy way too much stuff
# Pure recursive approach is much more efficient and harder to mess up
#
# Takes in: Board, Depth to go to
# Returns: Tuple of (bestBoard, hueristic, moveList)
def dfs(board, depth):
    # Base case: return this when depths
    if (depth == 0):
        return (board, getScore(board), [])
    # What if this board is solved? Don't force it to make a move if mDist is 0
    if (getScore(board) == 0):
        return (board, 0, [])
    # Now try to find the best move
    # Get what moves can be made
    possible = getLegalMoves(board)
    # Evaluate best move
    bestMove = None
    bestResult = (None, math.inf, None)
    for move in possible:
        newboard = makeMove(board, move)
        result = dfs(newboard, depth - 1)
        if (result[1] < bestResult[1]):
            bestMove = move
            bestResult = result
        if bestResult[1] == 0:
            break
    # add the move that was made to the move history (at the front of the list)
    bestResult[2].insert(0, bestMove)
    return bestResult

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
    score = 0
    for i in range(len(board)):
        if i != board[i]:
            score += 1
    return score

def getScore(board):
    return mDist(board) + nDisp(board)

def makeMove(board, move):
    L = int(math.sqrt(len(board)))
    copyBoard = copy.copy(board)
    zI = copyBoard.index(L**2-1)
    moveI = move[0] + L*move[1]
    copyBoard[zI], copyBoard[moveI] = copyBoard[moveI], copyBoard[zI]
    return copyBoard

def getLegalMoves(board):
    finalMoves = []
    L = int(math.sqrt(len(board)))
    zI = board.index(L**2-1)
    zX, zY = zI % L, zI // L
    testMoves = [[zX+1, zY], [zX-1, zY], [zX, zY+1], [zX, zY-1]]
    for move in testMoves:
        if isLegalMove(move, L):
            finalMoves.append(move)
    return finalMoves

def isLegalMove(move, L):
    for i in move:
        if i < 0 or i >= L:
            return False
    return True

def solve(board):
    moves = []
    solved = False
    depth = 2
    while solved == False:
        result = dfs(board, depth)
        board  = result[0]
        solved = result[1] == 0
        moves += result[2]
        depth += 1
        printBoard2(board)
    print(len(moves))
    return moves

def printBoard(board):
    print(board[:4])
    print(board[4:8])
    print(board[8:12])
    print(board[12:])
    print('------------')

def printBoard2(board):
    print(board[:3])
    print(board[3:6])
    print(board[6:])
    print('---------')

def maxSwap(board):
    L = len(board)
    moves = 0
    while board != list(range(L)):
        bI = board.index(L-1)
        bNI = board.index(bI)
        board[bI], board[bNI] = board[bNI], board[bI]
        moves += 1
    return moves

solve([8, 0, 7, 1, 5, 6, 2, 3, 4])

#[7, 2, 8, 1, 5, 6, 0, 3, 4]
#[8, 0, 7, 1, 5, 6, 2, 3, 4]
#[8, 0, 1, 6, 7, 3, 2, 5, 4]
#[4, 6, 8, 0, 1, 5, 3, 2, 7]
#[1, 6, 0, 2, 4, 3, 7, 5, 8]
#[7, 2, 0, 6, 3, 5, 1, 4, 8]

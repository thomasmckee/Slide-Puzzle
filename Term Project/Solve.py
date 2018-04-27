import math
import copy

class Solve(object):
    def init(self):
        self.minScore = [[], 1000]
        self.moveList = []
        self.move = []
        self.depth = 0

    def depthSearchWrapper(self, board, depth):
        def depthSearch(board, depth):
            L = int(math.sqrt(len(board)))
            if self.solvedBoard(board):
                return self.moveList 
            if depth == 0:
                if self.getScore(board) < self.minScore[1]:
                    self.minScore = [self.moveList, self.getScore(board)]
            else:
                for move in self.getMoves(board):
                    self.depth += 1
                    self.moveList.append(move)
                    newBoard = self.makeMove(board, move, L)
                    depthSearch(newBoard, depth - 1)
        depthSearch(board, depth)
        print(self.minScore[0])

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
        return Solve.mDist(board) + Solve.nDisp(board)
    
    def solvedBoard(board):
        return board == list(range(len(board)))
    
    def getMoves(board):
        finalMoves = []
        L = int(math.sqrt(len(board)))
        zI = board.index(L**2-1)
        zX, zY = zI % L, zI // L
        testMoves = [[zX+1, zY], [zX-1, zY], [zX, zY+1], [zX, zY-1]]
        for move in testMoves:
            if Solve.isLegalMove(move, L):
                finalMoves.append(move)
        return finalMoves
    
    def makeMove(board, move, L):
        copyBoard = copy.deepcopy(board)
        zI = copyBoard.index(L**2-1)
        moveI = move[0] + L*move[1]
        copyBoard[zI], copyBoard[moveI] = copyBoard[moveI], copyBoard[zI]
        return copyBoard
    
    def isLegalMove(move, L):
        for i in move:
            if i < 0 or i >= L:
                return False
        return True

Solve.init(Solve)
Solve.depthSearchWrapper(Solve, [7, 2, 8, 1, 5, 6, 0, 3, 4], 5)
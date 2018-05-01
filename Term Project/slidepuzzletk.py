import random
from tkinter import *
import time

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

def makeBoard(n):
    board = createBoard(n)
    while not isValidBoard(board):
        board = createBoard(n)
    return board

def createBoard(n):
    values = list(range(0, n**2))
    board = make2dList(n, n, 0)
    for i in range(len(board)):
        for j in range(len(board)):
            valIndex = random.randint(0, len(values)-1)
            board[i][j] = values[valIndex]
            values.remove(values[valIndex])
    return board

#Information about valid board states taken from this website:
#https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
def isValidBoard(board):
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

def endBoard(n):
    lst = list(range(n**2))
    lst.pop(0)
    lst.append(0)
    return lst

def init(data):
    data.time1 = time.time()
    data.time2 = 0
    data.n = 4
    #data.board = makeBoard(data.n)
    data.board = [[5, 8, 0, 2], [15, 14, 12, 7], [9, 6, 10, 13], [11, 3, 4, 1]]

    data.boardLst = flattenList(data.board)
    data.endBoard = endBoard(data.n)
    data.moves = 0
    data.mainMenu = True
    data.GameOver = False
    data.practiceMenu = False
    data.practice = False

def mousePressedMenu(event, data):
    if data.mainMenu:
        rxPrac, rxPrac2, ryPrac, ryPrac2 = 2/5, 3/5, 7/10, 8/10
        xminPrac, xmaxPrac = data.width*rxPrac, data.width*rxPrac2
        yminPrac, ymaxPrac = data.height*ryPrac, data.height*ryPrac2
        if xminPrac < event.x < xmaxPrac and yminPrac < event.y < ymaxPrac:
            data.practiceMenu = True
            data.mainMenu = False
    return

def mousePressedPracticeMenu(event, data):
    w, h = data.width, data.height
    r1, r2 = .45, .55
    th1, th2, th3, th4 = .48, .43, .52, .57
    tw1, tw2, tw3 = .57, .61, .65
    w1, w2, h1, h2, t1 = .4, .6, .6, .7, .65
    xMin, xMax, yMin, yMax = w*tw1, w*tw3, h*th2, h*th1
    yMin2, yMax2 = w*th3, w*th4
    xMin3, xMax3, yMin3, yMax3 = w*w1, w*w2, h*h1, h*h2
    if xMin < event.x < xMax and yMin < event.y < yMax:
        if data.n < 10:
            data.n += 1
            data.board = makeBoard(data.n)
            data.endBoard = endBoard(data.n)
    elif xMin < event.x < xMax and yMin2 < event.y < yMax2:
        if data.n > 3:
            data.n -= 1
            data.board = makeBoard(data.n)
            data.endBoard = endBoard(data.n)
    elif xMin3 < event.x < xMax3 and yMin3 < event.y < yMax3:
        data.practiceMenu = False
        data.practice = True

def mousePressed(event, data):
    if event.x < 0 or event.x > data.width:
        return
    if event.y < 0 or event.y > data.height:
        return
    if data.mainMenu:
        mousePressedMenu(event, data)
    if data.practiceMenu:
        mousePressedPracticeMenu(event, data)
        return
    if data.GameOver:
        return
    board = data.board
    x = int(event.x//(data.width/data.n))
    y = int(event.y//(data.height/data.n))
    for i in range(data.n):
        for j in range(data.n):
            if data.board[i][j] == 0:
                zXI = j
                zYI = i
    if abs(x - zXI) + abs(y - zYI) < 2:
        board[y][x], board[zYI][zXI] = board[zYI][zXI], board[y][x]
        data.boardLst = flattenList(data.board)
        data.board = board
        data.moves += 1
    if data.boardLst == data.endBoard:
        data.GameOver = True
        data.practice = False
        data.time2 = time.time()


def keyPressed(event, data):
    if data.GameOver:
        if event.keysym in 'Rr':
            init(data)

def drawMenu(canvas, data):
    r1, r2, r3, r4, r5, r6 = 1/4, 7/10, 8/10, 2/5, 3/5, 3/4
    canvas.create_text(data.width/2, data.height*r1, anchor = CENTER,
    text = 'Sliding Puzzle Game', font = 'Helvetica 24')
    canvas.create_rectangle(data.width*r4, data.height*r2, data.width*r5,
    data.height*r3)
    canvas.create_text(data.width/2, data.height*r6, anchor = CENTER,
    text = 'Practice', font = 'Helvetica 14')

def drawPracticeMenu(canvas, data):
    r1, r2 = .45, .55
    th1, th2, th3, th4 = .48, .43, .52, .57
    tw1, tw2, tw3 = .57, .61, .65
    w1, w2, h1, h2, t1, t2 = .4, .6, .6, .7, .65, .4
    canvas.create_rectangle(data.width*r1, data.height*r1, data.width*r2,
    data.height*r2)
    canvas.create_text(data.width/2, data.height/2, anchor = CENTER,
    text = data.n, font = 'Helvetica 20')
    canvas.create_polygon(data.width*tw1, data.height*th1, data.width*tw2,
    data.height*th2, data.width*tw3, data.height*th1)
    canvas.create_polygon(data.width*tw1, data.height*th3, data.width*tw2,
    data.height*th4, data.width*tw3, data.height*th3)
    canvas.create_rectangle(data.width*w1, data.height*h1, data.width*w2,
    data.height*h2)
    canvas.create_text(data.width/2, data.height*t1, anchor = CENTER,
    text = 'Continue', font = 'Helvetica 14')
    canvas.create_text(data.width/2, data.height*t2, anchor = CENTER,
    text = 'Board Size:', font = 'Helvetica 14')
    
def drawBoard(canvas, data):
    for i in range(data.n):
        for j in range(data.n):
            if data.board[i][j] == 0:
                canvas.create_rectangle(j*(data.width/data.n), 
                i*(data.height/data.n),(j+1)*(data.width/data.n),
                (i+1)*(data.height/data.n), fill = 'black')
            canvas.create_rectangle(j*(data.width/data.n), 
            i*(data.height/data.n),(j+1)*(data.width/data.n),
            (i+1)*(data.height/data.n), width = 2)
            canvas.create_text((j+.5)*(data.width/data.n),
            (i+.5)*(data.height/data.n), text = data.board[i][j],
            font = 'Helvetica %d'%(data.width // (data.n*5)))

def drawEnd(canvas, data):
    r1, r2, r3, r4, r5, r6 = 1/3, 2/3, 2/5, 7/15, 8/15, 3/5
    canvas.create_rectangle(0, data.height*r1, data.width,
    data.height*r2, fill = 'blue')
    canvas.create_text(data.width/2, data.height*r3, anchor = CENTER,
    text = 'You Win!')
    canvas.create_text(data.width/2, data.height*r4, anchor = CENTER,
    text = 'This round took %d moves'%data.moves)
    canvas.create_text(data.width/2, data.height*r5, anchor = CENTER,
    text = 'and %0.2f seconds'%(data.time2 - data.time1))
    canvas.create_text(data.width/2, data.height*r6, anchor = CENTER,
    text = 'Press R to Return to Main Menu')

def redrawAll(canvas, data):
    if data.mainMenu:
        drawMenu(canvas, data)
        return
    if data.practiceMenu:
        drawPracticeMenu(canvas, data)
        return
    if data.practice:
        drawBoard(canvas, data)
    elif data.GameOver:
        drawEnd(canvas, data)

def run(width=500, height=500):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
run()

#solve([8, 3, 7, 6, 0, 4, 2, 5, 1])
from tkinter import *
from tkinter import messagebox
import random

root= Tk()
root.title("Minesweeper")

rows=10
columns=10
mines=10
board=[]
buttons=[]
gameover= False

colors= ['#FFFFFF', '#0000FF', '#008200', "#FF0000", '#000084', '#840000']


def menu():
    menubar= Menu(root)
    menusize= Menu(root, tearoff=0)
    menusize.add_command(label="Beginner: 8X8 (16 Mines)", command=lambda: grid(10,10,10))
    menusize.add_command(label="Intermediate: 10X10 (20 Mines)", command=lambda: grid(20,20,40))
    menusize.add_command(label="Advanced: 20X20 (40 Mines)", command=lambda: grid(30,30,50))

    menubar.add_cascade(label="Size", menu=menusize)
    menubar.add_command(label="Quit", command=lambda: root.destroy())
    root.config(menu=menubar)

def grid(r,c,m):
    global rows, columns, mines
    rows= r
    columns= c
    mines= m
    restart()

def field():
    global rows, columns, mines, board
    board=[]
    for i in range(0, rows):
        board.append([])
        for j in range(0, columns):
            board[i].append(0)
    for _ in range(0, mines):
        i= random.randint(0, rows-1)
        j= random.randint(0, columns-1)
        while board[i][j]== -1:
            i= random.randint(0, rows-1)
            j= random.randint(0, columns-1)
        board[i][j]= -1
        if i!=0:
            if j!=0:
                if board[i-1][j-1]!= -1:
                    board[i-1][j-1]= int(board[i-1][j-1]) + 1
            if board[i-1][j]!= -1:
                board[i-1][j]= int(board[i-1][j])+ 1
            if j!= columns-1:
                if board[i-1][j+1]!= -1:
                    board[i-1][j+1]= int(board[i-1][j+1])+ 1
        if j!= 0:
            if board[i][j-1]!= -1:
                board[i][j-1]= int(board[i][j-1])+ 1
        if j!= columns-1:
            if board[i][j+1]!= -1:
                board[i][j+1]= int(board[i][j+1])+ 1
        if i!= rows-1:
            if j!= 0:
                if board[i+1][j-1]!= -1:
                    board[i+1][j-1]= int(board[i+1][j-1])+ 1
            if board[i+1][j]!= -1:
                board[i+1][j]= int(board[i+1][j])+ 1
            if j!= columns-1:
                if board[i+1][j+1]!= -1:
                    board[i+1][j+1]= int(board[i+1][j+1])+ 1

def box():
    global rows, columns, buttons
    Btn= Button(root, text="Restart", command=restart, cursor='hand2').grid(row=0, column=0, columnspan=columns, sticky=N+W+E+S)
    buttons= []
    for i in range(0, rows):
        buttons.append([])
        for j in range(0, columns):
            b= Button(root, text=" ", width=2, command=lambda i=i, j=j: click(i,j))
            b.bind("<Button-3>", lambda e, i=i, j=j: r_click(i,j))
            b.grid(row=i+1, column=j, sticky=N+W+E+S)
            buttons[i].append(b)

def restart():
    global gameover
    gameover= False
    for i in root.winfo_children():
        if type(i)!= Menu:
            i.destroy()
    box()
    field()

def click(i,j):
    global board, buttons, colors, gameover, rows, columns
    if gameover:
        return
    buttons[i][j]["text"]= str(board[i][j])
    if board[i][j]== -1:
        buttons[i][j]["text"]= "@"
        buttons[i][j].config(background='red', disabledforeground='black')
        gameover= True
        messagebox.showinfo("Game Over", "You Lost.")
        for i in range(0, rows):
            for j in range(columns):
                if board[i][j]== -1:
                    buttons[i][j]["text"]= "@"
    else:
        buttons[i][j].config(disabledforeground= colors[board[i][j]])
    if board[i][j]== 0:
        buttons[i][j]["text"]= " "
        auto(i,j)
    buttons[i][j]['state']= 'disabled'
    buttons[i][j].config(relief= SUNKEN)
    win()

def auto(i,j):
    global board, buttons, colors, rows, columns
    if buttons[i][j]["state"]== "disabled":
        return
    if board[i][j]!= 0:
        buttons[i][j]["text"]= str(board[i][j])
    else:
        buttons[i][j]["text"]=" "
    buttons[i][j].config(disabledforeground= colors[board[i][j]])
    buttons[i][j].config(relief=SUNKEN)
    buttons[i][j]["state"]= "disabled"
    if board[i][j]== 0:
        if i!= 0 and j!= 0:
            auto(i-1, j-1)
        if i!= 0:
            auto(i-1, j)
        if i!= 0 and j!= columns-1:
            auto(i-1, j+1)
        if j!= 0:
            auto(i, j-1)
        if j!= columns-1:
            auto(i, j+1)
        if i!= rows-1 and j!= 0:
            auto(i+1, j-1)
        if i!= rows-1:
            auto(i+1, j)
        if i!= rows-1 and j!= columns-1:
            auto(i+1, j+1)

def r_click(i,j):
    global buttons
    if gameover:
        return
    if buttons[i][j]["text"]== "?‍‍":
        buttons[i][j]["text"]= " "
        buttons[i][j]["state"]= "normal"
    elif buttons[i][j]["text"]==" " and  buttons[i][j]["state"]== "normal":
        buttons[i][j]["text"]= "?‍‍"
        buttons[i][j]["state"]= "disabled"

def win():
    global buttons, board, rows, columns
    win= True
    for i in range(0, rows):
        for j in range(0, columns):
            if buttons[i][j]!= -1 and buttons[i][j]["state"]== "normal":
                win= False
    if win:
        messagebox.showinfo("Game Over", "You won.")

menu()
box()
field()
root.mainloop()
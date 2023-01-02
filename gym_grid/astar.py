import pygame, sys, random, math
from tkinter import messagebox, Tk
import time


size = (width, height) = 1168, 608

pygame.init()

win = pygame.display.set_mode(size)

clock = pygame.time.Clock()

cols, rows = 73, 38


grid = []
openSet, closeSet = [], []
path = []

w = 16
h = 16

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        # if random.randint(0, 100) < 20:
        #     self.wall = True
        
    def show(self, win, col):
        if self.wall == True:
            col = (0, 0, 0)
        pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))
    
    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])
        #Add Diagonals
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])


def clickWall(pos, state):
    i = pos[0] 
    j = pos[1]
    grid[i][j].wall = state

            
def heuristics(a, b):
    return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2)


for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

start = grid[0][0]
#end = grid[cols - cols//2][rows - cols//4]
end = grid[72][37]

openSet.append(start)

import json

def json2list(name):
    with open("../gym_grid/data/coordinates_{}.json".format(name), "r") as fp:
        data = json.load(fp)
        return data

def close():
    pygame.quit()
    sys.exit()

def runAstar():
    flag = False
    noflag = True
    startflag = False
    w_x = json2list("X")
    w_y = json2list("Y")
    counter = 0
    while True:
        for t in range(len(w_x)):
            clickWall([w_x[t] - 1, w_y[t] - 1], True)

        #if event.key == pygame.K_RETURN:
        startflag = True

        if startflag:
            if len(openSet) > 0:
                winner = 0
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[winner].f:
                        winner = i

                current = openSet[winner]
                
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        print("Done")
                        
                    elif flag:
                        continue

                if flag == False:
                    openSet.remove(current)
                    closeSet.append(current)

                    for neighbor in current.neighbors:
                        if neighbor in closeSet or neighbor.wall:
                            continue
                        tempG = current.g + 1

                        newPath = False
                        if neighbor in openSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            openSet.append(neighbor)
                        
                        if newPath:
                            neighbor.h = heuristics(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current

            else:
                if noflag:
                    print("no solution")
                    noflag = False
                    return False

        win.fill((0, 20, 20)) # Grid çizgileri
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (255, 255, 255)) # background
                # print(len(path), len(openSet), len(closeSet))
                if flag and spot in path:
                    counter += 1
                    print(counter)
                    spot.show(win, (255, 255, 0))

                elif spot in closeSet:
                    spot.show(win, (255, 0, 0))
                elif spot in openSet:
                    spot.show(win, (0, 255, 0))
                try:
                    if spot == end:
                        spot.show(win, (0, 120, 255))
                except Exception:
                    pass


                
        pygame.display.flip()
        time.sleep(0.1)
        if counter == len(path) and counter > 0:
            print("reset")
            return True
        
        
    




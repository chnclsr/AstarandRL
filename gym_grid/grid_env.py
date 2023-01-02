import os.path
from .astar import runAstar
import pygame
from pygame.locals import *
import time
import numpy as np
from .constants import *
import json
# import gym
# from gym import spaces
from .player import Player
from .objects import Wall, IDMap, Target

class GridEnv:
    def __init__(self, timeStep=100, randomWalls=False, controlAstar=False):
        pygame.init()
        self.w = ScreenW
        self.h = ScreenH
        self.y_limit  = (self.h // grid_height) - 2
        self.x_limit = (self.w // grid_width) - 2
        self.gridMap = []
        self.left = h_step_len
        self.top = v_step_len
        self.width = grid_width
        self.height = grid_height
        self.screen = None
        self.action_space = 8
        self.observartion_space = (self.x_limit, self.y_limit)
        self.player = None
        self.target = None
        self.walls = []
        self.gameExit = None
        self.timeStepLimit = timeStep
        self.timeStep = None
        self.numWallBlock = 150
        self.reset_timer = 0
        self.randomWalls = randomWalls
        self.wall_coordinates_X = []
        self.wall_coordinates_Y = []
        self.Astar = controlAstar
        self.goal = 100


    def getMap(self):
        for i in range(1, self.y_limit+1):
            for j in range(1, self.x_limit+1):
                box = IDMap()
                box.x = j
                box.y = i
                box.ID = "N" # W:wall, N:nothing, A:agent, T:target
                self.gridMap.append(box)


    def getState(self):
        state = np.zeros([self.x_limit, self.y_limit])
        for ff in [[d.x, d.y] for d in self.walls]:
            state[ff[0] - 1, ff[1] - 1] = 1 # add walls pos.

        state[self.player.x - 1, self.player.y - 1] = 1 # add agent pos.
        state[self.target.x - 1, self.target.y - 1] = 1 # add target pos.
        return state


    def getReward(self):
        def calDistanceReward():
            pre_distance = np.sqrt((self.pre_x - self.target.x) ** 2 + (self.pre_y - self.target.y) ** 2)
            curr_distance = np.sqrt((self.player.x - self.target.x) ** 2 + (self.player.y - self.target.y) ** 2)
            distanceReward = -(curr_distance - pre_distance) / np.sqrt(2)
            # print(distanceReward, curr_distance, pre_distance)
            return distanceReward
        reward = 0
        reward += self.goal
        reward -= self.player.reward
        reward += calDistanceReward()
        reward -= 0.01 # timestep
        return reward


    def getTerminate(self):
        done = False
        if self.player.x == self.target.x and self.player.y == self.target.y:
            done = True
            self.goal = 10
        return done

    def step(self, action):
        self.pre_x = self.player.x
        self.pre_y = self.player.y
        self.player.move(str(action))
        done = self.getTerminate()
        state = self.getState()
        info = None
        reward = self.getReward()
        self.timeStep += 1
        # print("timestep {}".format(self.timeStep))

        if self.timeStep == self.timeStepLimit:
            done = True
        return state, reward, done, info

    def reset(self):
        def _initialize():
            self.gameExit = False
            self.timeStep = 0
            self.goal = 0
            self.screen = pygame.display.set_mode((self.w, self.h))
            self.player = None
            self.getPlayer()  # get agent
            self.pre_x = self.player.x
            self.pre_y = self.player.y
            self.getTarget()
            if self.reset_timer == 0:
                self.gridMap = []
                self.getMap()
                self.walls = []
                self.getWalls()
                # A* algorithm to control env has a solution
                # ---- A* --------------
                if self.Astar:
                    out = runAstar()
                    while not out: # out is False means there is no solution for this map conditions, continue if has a solutuion
                        self.gridMap = []
                        self.getMap()
                        self.walls = []
                        self.getWalls()
                        out = runAstar()
                # ----------------------
        _initialize()
        self.reset_timer += 1
        self.player.gridIDs = self.gridMap
        state = self.getState()
        return state

    def getWalls(self):
        if self.randomWalls:
            for i in range(self.numWallBlock):
                x = np.random.randint(1, self.x_limit, 1)[0] # referans for other 3 block
                y = np.random.randint(1, self.y_limit, 1)[0]

                x1 = x + 1 # left side
                y1 = y

                x2 = x + 1 # left and down side
                y2 = y + 1

                x3 = x # down side
                y3 = y + 1

                w_list = [[x,y], [x1,y1], [x2,y2], [x3,y3]]
                for X in w_list:
                    w = Wall()
                    a, b = X[0], X[1]
                    if (a == self.player.x and b == self.player.y) or (a == self.target.x and b == self.target.y): # oyuncu ya da hedef üzerine duvar gelemez
                        continue
                    ID = self.gridMap[a + ((b - 1) * self.x_limit - 1)].ID
                    if not ID == "W": # controller
                        self.gridMap[a + ((b-1) * self.x_limit - 1)].ID = "W"
                        w.x = self.gridMap[a + ((b-1) * self.x_limit - 1)].x
                        w.y = self.gridMap[a + ((b-1) * self.x_limit - 1)].y
                        self.walls.append(w)
                        self.wall_coordinates_X.append(w.x)
                        self.wall_coordinates_Y.append(w.y)
            self.list2json(self.wall_coordinates_X, "X")
            self.list2json(self.wall_coordinates_Y, "Y")
            print(len(self.walls))
        else:
            self.wall_coordinates_X = self.json2list("X")
            self.wall_coordinates_Y = self.json2list("Y")
            for i in range(len(self.wall_coordinates_X)):
                w = Wall()
                self.walls.append(w)
                w.x = self.wall_coordinates_X[i]
                w.y = self.wall_coordinates_Y[i]
                self.gridMap[w.x + ((w.y - 1) * self.x_limit - 1)].ID = "W"


    def list2json(self, data, name):
        with open("../gym_grid/data/coordinates_{}.json".format(name), "w") as fp:
            json.dump(data, fp)

    def json2list(self, name):
        with open("../gym_grid/data/coordinates_{}.json".format(name), "r") as fp:
            data = json.load(fp)
            return data

    def getTarget(self):
        self.target = Target()
        self.target.x = self.player.x_limit
        self.target.y = self.player.y_limit

    def getPlayer(self):
        self.player = Player()
        self.player.x_limit = self.x_limit
        self.player.y_limit = self.y_limit
        self.player.numAction = self.action_space
        self.player.screen = self.screen
        self.player.left = self.left
        self.player.top = self.top
        self.player.width = self.width
        self.player.height = self.height

    def draw_grid(self):
        self.screen.fill(WHITE)
        for y in range(self.height, self.h, self.height): #horizontal lines
            pygame.draw.line(self.screen, BLACK, (self.width, y), (self.w - self.width, y), 1)
        for x in range(self.width, self.w, self.width): #vertical lines
            pygame.draw.line(self.screen, BLACK, (x, self.height), (x, self.h - self.height), 1)

    def draw_target(self):
        pygame.draw.rect(self.screen, [0, 255, 0],
                         [self.target.x * self.width, self.target.y * self.player.height, self.player.width,
                          self.player.height], 0)

    def draw_agent(self):
        # print(self.player.x, self.player.y)
        pygame.draw.rect(self.screen, [0, 0, 255], [self.player.x * self.width, self.player.y * self.player.height, self.player.width, self.player.height], 0)

    def draw_walls(self):
        for wall in self.walls:
            pygame.draw.rect(self.screen, [0, 0, 0], [wall.x * self.width, wall.y * self.player.height, self.player.width, self.player.height], 0)

    def render(self):
        self.draw_grid()
        self.draw_agent()
        self.draw_target()
        self.draw_walls()
        # draw_target()
        pygame.display.flip()
        time.sleep(0.001)

    def close(self):
        pygame.quit()



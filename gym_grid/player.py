from .constants import *
import numpy as np

class Player:
    def __init__(self):
        self.y_limit = None
        self.x_limit = (ScreenW // grid_width) - 2
        self.x = 1 #np.random.randint(2, self.x_limit, 1)[0]
        self.y = 1 #np.random.randint(2, self.y_limit, 1)[0]

        self.screen = None
        self.left = None
        self.top = None
        self.height = None
        self.width = None
        self.gridIDs = None
        self.numAction = None
        self.reward = 0
        self.on_y_limit = False



    def selectAction(self):
        action = np.random.choice(range(self.numAction), p=[1 / self.numAction] * self.numAction)
        return action

    def controlWall(self, target_x, target_y):
        ID = self.gridIDs[target_x + ((target_y - 1) * self.x_limit - 1)].ID
        if ID == "N":
            return False
        else:
            print("! wall")
            return True

    def moveDown(self, half=False):
        if self.y < self.y_limit:
            if not half:# çarpraz aksiyon mu
                target_y = self.y + 1
                target_x = self.x
                if not self.controlWall(target_x, target_y):
                    self.y += 1
                    self.top -= 16
                    self.on_y_limit = False
            elif half and (not self.x == self.x_limit and not self.x == 1): # çarpraz aksiyonsa duvar olsa da hareket eder
                self.y += 1
                self.top -= 16
                self.on_y_limit = False
        else:
            self.on_y_limit = True

    def moveUp(self, half=False):
        if self.y > 1:
            if not half: # çarpraz aksiyon mu
                target_y = self.y - 1
                target_x = self.x
                if not self.controlWall(target_x, target_y):
                    self.y -= 1
                    self.top += 16
                    self.on_y_limit = False
            elif half and (not self.x == self.x_limit and not self.x == 1):
                self.y -= 1
                self.top += 16
                self.on_y_limit = False
        else:
            self.on_y_limit = True


    def moveRight(self, afterUP=True, half=False):
        if self.x < self.x_limit:
            target_x = self.x + 1
            target_y = self.y

            if not self.controlWall(target_x, target_y) and not self.on_y_limit and not half:
                self.x += 1
                self.left += 16

            elif not self.controlWall(target_x, target_y) and not self.on_y_limit and half:
                self.x += 1
                self.left += 16

            elif afterUP == True and half and not self.on_y_limit: #up aksiyonunu geri al
                self.y += 1
                self.top -= 16

            elif afterUP == False and half and not self.on_y_limit: # down aksiyonunu geri al
                self.y -= 1
                self.top += 16

    def moveLeft(self, afterUP=True, half=False):
        if self.x > 1:
            target_x = self.x - 1
            target_y = self.y

            if not self.controlWall(target_x, target_y) and not self.on_y_limit and not half:
                self.x -= 1
                self.left -= 16

            elif not self.controlWall(target_x, target_y) and not self.on_y_limit and half:
                self.x -= 1
                self.left -= 16

            elif afterUP == True and half and not self.on_y_limit:
                self.y += 1
                self.top -= 16

            elif afterUP == False and half and not self.on_y_limit: # down aksiyonunu geri al
                self.y -= 1
                self.top += 16

    def move(self, action):
        self.reward = 0

        if action == "0":
            self.moveDown()

        elif action == "1":
            self.moveUp()

        elif action == "2":
            self.moveLeft()

        elif action == "3":
            self.moveRight()

        elif action == "4":
            self.moveDown(half=True)
            self.moveRight(afterUP=False, half=True)

        elif action == "5":
            self.moveDown(half=True)
            self.moveLeft(afterUP=False, half=True)

        elif action == "6":
            self.moveUp(half=True)
            self.moveLeft(afterUP=True, half=True)

        elif action == "7":
            self.moveUp(half=True)
            self.moveRight(afterUP=True, half=True)



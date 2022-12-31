class Target:
    def __init__(self):
        self.x = None
        self.y = None


class Wall(Target):
    def __init__(self):
        super().__init__()


class IDMap:
    def __init__(self):
        self.ID = None
        self.x = None
        self.y = None
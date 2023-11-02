from pygame.locals import *
from _typeshed import Incomplete

class FlappyBird:
    isRobot: bool
    isRender: bool
    isOpenHitmaskFile: bool
    isLearning: bool
    FPS: int
    SCREENWIDTH: int
    SCREENHEIGHT: int
    PIPEGAPSIZE: int
    BASEY: Incomplete
    IM_WIDTH: int
    IM_HEIGTH: int
    PIPE: Incomplete
    PLAYER: Incomplete
    BASE: Incomplete
    BACKGROUND: Incomplete
    MESSAGE: Incomplete
    def __init__(self) -> None: ...
    PLAYERS_LIST: Incomplete
    BACKGROUNDS_LIST: Incomplete
    PIPES_LIST: Incomplete
    def initMainData(self): ...
    def main(self) -> None: ...
    def showWelcomeAnimation(self): ...
    score: int
    playerIndexGen: Incomplete
    basex: Incomplete
    baseShift: Incomplete
    newPipe1: Incomplete
    newPipe2: Incomplete
    upperPipes: Incomplete
    lowerPipes: Incomplete
    pipeVelX: int
    playerVelY: int
    playerMaxVelY: int
    playerMinVelY: int
    playerAccY: int
    playerRot: int
    playerVelRot: int
    playerRotThr: int
    playerFlapAcc: int
    playerFlapped: bool
    def initMainGameData(self, movementInfo) -> None: ...
    crashTest: Incomplete
    playerIndex: Incomplete
    visibleRot: Incomplete
    def mainGame(self, action: int = ...): ...
    def play(self) -> None: ...
    HITMASKS: Incomplete
    def reset(self, isRender: bool = ...): ...
    def step(self, action): ...
    def is_terminal(self): ...
    def creatHismasksFile(self) -> None: ...
    def showGameOverScreen(self, crashInfo) -> None: ...
    def showScore(self, score) -> None: ...
    def checkCrash(self, player, upperPipes, lowerPipes): ...
    def pixelCollision(self, rect1, rect2, hitmask1, hitmask2): ...
    def getRandomPipe(self): ...
    def playerShm(self, playerShm) -> None: ...
    def getHitmask(self, image): ...

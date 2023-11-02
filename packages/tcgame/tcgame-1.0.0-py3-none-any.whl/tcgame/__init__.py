from tcgame.envs.path_finding import PathFinding
from tcgame.envs.path_finding_2d import Maze
from tcgame.envs.finding import Finding

from tcgame.agents.agent import QLearning


ENV_FINDING = 'finding'
ENV_PATH_FINDING = 'path_finding'
ENV_PATH_FINDING_2D = 'path_finding_2d'
ENV_FLAPPYBIRD = 'flappybird'

def getGameEnv(gameName):
    if gameName == ENV_FINDING:
        return Finding()
    if gameName == ENV_PATH_FINDING:
        return PathFinding()
    if gameName == ENV_PATH_FINDING_2D:
        return Maze()
    if gameName == ENV_FLAPPYBIRD:
        from tcgame.envs.flappy import FlappyBird
        return FlappyBird()

def getFindingAgent(n_states=None, actions=None):
    if n_states is not None:
        if actions is not None:
            return QLearning(n_states, actions)
        return QLearning(n_states)
    return QLearning()
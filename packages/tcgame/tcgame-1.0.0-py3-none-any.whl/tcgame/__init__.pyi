from _typeshed import Incomplete
from tcgame.agents.agent import QLearning as QLearning
from tcgame.envs.finding import Finding as Finding
from tcgame.envs.path_finding import PathFinding as PathFinding
from tcgame.envs.path_finding_2d import Maze as Maze
from tcgame.envs.flappy import FlappyBird


ENV_FINDING: str
ENV_PATH_FINDING: str
ENV_PATH_FINDING_2D: str
ENV_FLAPPYBIRD: str

def getGameEnv(gameName: str) -> (None | Finding | PathFinding | Maze | FlappyBird): ...
def getFindingAgent(n_states: Incomplete | None = ..., actions: Incomplete | None = ...) -> QLearning: ...

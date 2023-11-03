from _typeshed import Incomplete

class QLearning:
    actions: Incomplete
    alpha: Incomplete
    gamma: Incomplete
    epsilon: Incomplete
    q_table: Incomplete
    def __init__(self, n_states: int = ..., actions=..., learning_rate: float = ..., reward_decay: float = ..., e_greedy: float = ...) -> None: ...
    def choose_action(self, state): ...
    def learn(self, s, a, r, s_) -> None: ...

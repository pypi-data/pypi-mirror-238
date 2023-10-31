from _typeshed import Incomplete
from optilog.encoders.pb import IncrementalEncoder as IncrementalEncoder
from optilog.solvers.sat import Cadical as Cadical, Glucose41 as Glucose41

def sink(*args, **kwargs) -> None: ...

class LinearMaxSat:
    formula: Incomplete
    num_vars: Incomplete
    solver: Incomplete
    verbose: Incomplete
    weights: Incomplete
    opt_callback_func: Incomplete
    not_decide_vars: Incomplete
    decide_card_vars: Incomplete
    prev_model_: Incomplete
    def __init__(self, formula, solver: Incomplete | None = ..., opt_callback_func: Incomplete | None = ..., seed: int = ..., not_decide_vars=..., decide_card_vars: bool = ..., verbose: bool = ...) -> None: ...
    block_vars: Incomplete
    best_model_: Incomplete
    best_cost: Incomplete
    def solve(self, assumptions=..., timeout: Incomplete | None = ..., intermediate_timeout: Incomplete | None = ...): ...
    def get_model(self): ...

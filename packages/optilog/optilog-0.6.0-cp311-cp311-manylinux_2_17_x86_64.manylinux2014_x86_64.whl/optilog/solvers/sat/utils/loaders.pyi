from typing import List, NamedTuple, Optional

class SatSolverOutput(NamedTuple):
    model: Optional[List[int]]
    sat: Optional[str]
    def verify_on(self, formula) -> None: ...

class MaxSatSolverOutput(NamedTuple):
    model: Optional[List[int]]
    sat: Optional[str]
    cost: Optional[int]
    def verify_on(self, formula) -> None: ...

def load_sat_output(path, model_format) -> None: ...
def load_maxsat_output(path, model_format) -> None: ...

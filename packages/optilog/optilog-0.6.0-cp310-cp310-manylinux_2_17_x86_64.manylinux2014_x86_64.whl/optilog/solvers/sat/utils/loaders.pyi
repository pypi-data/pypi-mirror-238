from optilog.formulas import WCNF as WCNF
from optilog.internalutils import general_parser as general_parser
from typing import List, NamedTuple, Optional

class SatSolverOutput(NamedTuple):
    model: Optional[List[int]]
    sat: Optional[str]
    def verify_on(self, formula): ...

class MaxSatSolverOutput(NamedTuple):
    model: Optional[List[int]]
    sat: Optional[str]
    cost: Optional[int]
    def verify_on(self, formula): ...

def load_sat_output(path, model_format): ...
def load_maxsat_output(path, model_format): ...

from _typeshed import Incomplete
from collections.abc import Generator
from optilog.sat import CNF as CNF
from optilog.tuning import Transformer as Transformer
from optilog.tuning.encode_transformers.opb_parser import OPBPArser as OPBPArser

class PBEncoderTransformer:
    comparator: Incomplete
    pbenc: Incomplete
    amoenc: Incomplete
    amkenc: Incomplete
    @staticmethod
    def run(input_data) -> Generator[Incomplete, Incomplete, None]: ...
    @staticmethod
    def get_params(args): ...
    @staticmethod
    def get_conditions(args):
        """
        # Conditionals:
        child_name | condition [&&,||] condition ...

        # Condition Operators:
        # parent_x [<, >] parent_x_value (if parameter type is ordinal, integer or real)
        # parent_x [==,!=] parent_x_value (if parameter type is categorical, ordinal or integer)
        # parent_x in {parent_x_value1, parent_x_value2,...}
        """

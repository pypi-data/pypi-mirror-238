from _typeshed import Incomplete
from collections.abc import Generator
from optilog.sat import CNF as CNF, Encoder as Encoder
from optilog.tuning import Transformer as Transformer
from optilog.tuning.encode_transformers.opb_parser import OPBPArser as OPBPArser

class optilogEncoderTransformer(Transformer):
    card_enc: str
    def __init__(self, args) -> None: ...
    def run(self, cfg, seed, instance): ...
    pb_enc: Incomplete
    def lazy_run(self, cfg, seed, instance) -> Generator[Incomplete, Incomplete, None]: ...
    @staticmethod
    def get_params(args): ...

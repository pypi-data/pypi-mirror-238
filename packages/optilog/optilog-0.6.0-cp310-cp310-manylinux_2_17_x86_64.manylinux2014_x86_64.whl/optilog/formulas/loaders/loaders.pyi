from optilog.formulas import QCNF as QCNF, QCNFException as QCNFException
from pathlib import Path
from typing import Union

def load_qcnf(file_path: Union[str, Path]) -> QCNF:
    """Loads a QCNF DIMACS [#qcnf]_ into a :py:class:`optilog.formulas.QCNF` object and returns it.

    :param path: The path of a qcnf in DIMACS format.
    """

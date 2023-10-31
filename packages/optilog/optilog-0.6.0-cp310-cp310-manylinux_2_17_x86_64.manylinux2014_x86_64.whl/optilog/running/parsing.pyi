import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from typing import Optional, Type, Union

class CastingTag:
    type: Incomplete
    def __init__(self, type_) -> None: ...
    def serialize(self): ...
    def numpy_type(self): ...
    def cast(self, e): ...
    @staticmethod
    def deserialize(type): ...

class Tag(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def serialize(self): ...
    @abstractmethod
    def match(self, line): ...
    def numpy_type(self): ...
    @staticmethod
    def deserialize(d): ...

class StandardTag(Tag):
    timestamp: Incomplete
    save_history: Incomplete
    def __init__(self, expression, timestamp, save_history, type) -> None: ...
    def numpy_type(self): ...
    def serialize(self): ...
    def match(self, line): ...
    @staticmethod
    def deserialize(d): ...

class ModelTag(Tag):
    timestamp: Incomplete
    save_history: Incomplete
    model_format: Incomplete
    model_carry: Incomplete
    def __init__(self, model_format, timestamp, save_history) -> None: ...
    def match(self, line): ...
    def serialize(self): ...
    @staticmethod
    def deserialize(d): ...

class ParsingInfo:
    """Creates a blank Parsing Info with no parsing tags.
    """
    tags: Incomplete
    def __init__(self) -> None: ...
    @staticmethod
    def from_template(output_format: str = ..., model_format: str = ...) -> ParsingInfo:
        """
        Generates a ParsingInfo instance with the most common parsing filters for SAT/MaxSAT experiments.

        The parameter `output_format` parses the Solution Status status line ('s SATISFIABLE' etc.) on a filter called `sat`. Additionally, in `maxsat` mode we also parse the Solution Cost Line ('o 13') on a filter called `cost`.
        The parameter `model_format` parses the Solution Values on a filter called `model`. The 'standard' format expects decimal digits (v 1 -2 3 -4), while the 'binary' format expects a binary output (v 1010).

        All the filters are added with a timestamp but no history.
        The `cost` filter is cast to integer and the `model` filter is parsed to a list of decimal integers.

        :param output_format: Accepts {'sat', 'maxsat', None} as options. Specifies the Solution Status and Solution Cost Line filters.
        :param model_format: Accepts {'standard', 'binary', None} as options. Specifies the format of the model to be parsed. If it is None, models won't be parsed, which may improve performance.
        :returns: A ParsingInfo instance with configured filters
        """
    def add_filter(self, name: str, expression: str, timestamp: bool = ..., save_history: bool = ..., cast_to: Optional[Type[Union[int, float]]] = ...):
        '''
        Adds a filter to parse on the logs.
        The `name` of the filter will be added as a column on the pandas DataFrame.
        The `expression` *must* have a matching group (surrounded by parentheses).
        If the `timestamp` parameter is set to true, a new column called "time_{name}" will be added to the dataframe with the timestamp in miliseconds.
        By the default, only the last match of each filter is logged. But if you want to have access to all the matches, enable `save_history`, which will save the history of all the parsed values as a list.
        If the `cast_to` parameter is assigned a numeric type, the matched value of the filter will be casted while parsing the logs.

        :param name: Name of the filter tag
        :param expression: Matching regex with at least one group 
        :param timestamp: Whether or not to include the timestamp. The possible values are False for no timestamp, True for all the timestamps, cpu for only the cpu timestamps, and wall for only the wall timestamps.
        :param save_history: Whether or not to save the history of all the matches.
        :param cast_to: Accepts {None, int, float}. Specifies whether the match should be casted
        '''
    def serialize(self): ...
    @staticmethod
    def deserialize(d): ...
    def copy(self): ...
    def merge_with(self, other): ...

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import *  # type: ignore

from . import common


@dataclass
class RevelError(Exception, ABC):
    """Base class for all Revel exceptions."""

    @property
    @abstractmethod
    def message(self) -> str:
        """The error message."""
        raise NotImplementedError


@dataclass
class NoOptionGivenError(RevelError):
    """Raised when the user doesn't specify a command."""

    available_commands: List[str]

    @property
    def message(self) -> str:
        return f"Please specify a command. Available commands are {common.comma_separated_list(self.available_commands, 'and', '`')}."


@dataclass
class NoSuchOptionError(RevelError):
    """Raised when the user passes an invalid option."""

    entered_command: str
    available_commands: List[str]

    @property
    def message(self) -> str:
        return f"`{self.entered_command}` is not a valid option."


@dataclass
class AmbiguousOptionError(RevelError):
    """Raised when the user passes an ambiguous option."""

    entered_command: str
    matching_commands: List[str]
    available_commands: List[str]

    @property
    def message(self) -> str:
        return f"`{self.entered_command}` is ambiguous. It could refer to {common.comma_separated_list(self.matching_commands, 'or', '`')}."


class ArgumentError(RevelError):
    """
    Raised when attempting to call a function with invalid arguments. The
    message is human-readable and meant to be directly passed to the user
    """

    def __init__(self, message: str):
        self._message = message

    @property
    def message(self) -> str:
        return self._message

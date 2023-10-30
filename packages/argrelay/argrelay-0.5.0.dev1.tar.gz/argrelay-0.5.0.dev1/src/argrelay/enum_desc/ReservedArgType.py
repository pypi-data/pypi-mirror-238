from enum import Enum, auto


# TODO: TODO_66_66_75_78: Rename to `ReservedPropType` (or `ReservedPropName`?) - see term dictionary.
class ReservedArgType(Enum):
    EnvelopeClass = auto()
    FuncId = auto()
    ArgType = auto()
    ArgValue = auto()
    HelpHint = auto()

from enum import Enum, auto


# TODO: Remove this completely - this is obsoleted by FS_26_43_73_72 func tree.
# TODO: TODO_66_66_75_78: Rename to `GlobalPropType` (or `GlobalPropName`?) - see term dictionary.
class GlobalArgType(Enum):
    FunctionCategory = auto()
    """
    A way to separate functions in different "buckets".

    For example:
    *   "internal" provided by `argrelay` for various built-in and support functions
    *   "external" provided by plugins for domain-specific
    """

    ActionType = auto()
    """
    Specifies what function does. For example: "goto", "list", ...
    """

    ObjectSelector = auto()
    """
    Specifies what kind of objects a function works with. For example: "host", "service", ...
    """

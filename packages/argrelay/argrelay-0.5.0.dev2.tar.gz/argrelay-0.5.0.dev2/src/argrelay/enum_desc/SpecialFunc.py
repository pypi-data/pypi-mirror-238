from enum import Enum, auto


class SpecialFunc(Enum):
    """
    See also: FS_80_45_89_81 / integrated functions
    """

    # TODO: rename to intercept_invocation_func (two words min + func postfix):
    intercept_func = auto()
    """
    Implements FS_88_66_66_73 intercept func.
    """

    # TODO: rename to print_help_func (two words min + func postfix):
    help_func = auto()
    """
    Implements FS_71_87_33_52 help hint.
    """

    echo_args_func = auto()
    """
    Implements FS_43_50_57_71 echo args func.
    """

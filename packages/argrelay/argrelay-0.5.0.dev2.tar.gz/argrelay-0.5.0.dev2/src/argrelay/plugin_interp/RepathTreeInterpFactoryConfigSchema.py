from copy import deepcopy

from marshmallow import RAISE, fields

from argrelay.misc_helper.TypeDesc import TypeDesc
from argrelay.plugin_interp.FuncArgsInterpFactoryConfigSchema import (
    FuncArgsInterpFactoryConfigSchema,
    func_args_interp_config_desc,
)

repath_tree_ = "repath_tree"

class RepathTreeInterpFactoryConfigSchema(FuncArgsInterpFactoryConfigSchema):
    class Meta:
        unknown = RAISE
        strict = True

    # This is a tree (`dict`) of arbitrary depth with `list[str]` leaves.
    # Ideally, this should be defined as nested `dict`,
    # but it is unknown how to do it in marshmallow.
    # Implements FS_91_88_07_23 repath tree.
    repath_tree = fields.Raw(
        required = True,
    )

_re_tree_interp_config_example = deepcopy(func_args_interp_config_desc.dict_example)
_re_tree_interp_config_example.update({
    repath_tree_: [
        "relay_demo",
    ],
})

repath_tree_interp_config_desc = TypeDesc(
    dict_schema = RepathTreeInterpFactoryConfigSchema(),
    ref_name = RepathTreeInterpFactoryConfigSchema.__name__,
    dict_example = _re_tree_interp_config_example,
    default_file_path = "",
)

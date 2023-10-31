from argrelay.plugin_interp.AbstractInterp import AbstractInterp
from argrelay.plugin_interp.FuncTreeInterpFactory import FuncTreeInterpFactory
from argrelay.plugin_interp.RepathTreeInterp import RepathTreeInterp
from argrelay.plugin_interp.RepathTreeInterpFactoryConfigSchema import (
    repath_tree_interp_config_desc,
    repath_tree_,
)
from argrelay.plugin_interp.TreeWalker import TreeWalker
from argrelay.runtime_context.InterpContext import InterpContext


class RepathTreeInterpFactory(FuncTreeInterpFactory):
    """
    Implements FS_91_88_07_23 repath tree.
    """

    def __init__(
        self,
        plugin_instance_id: str,
        config_dict: dict,
    ):
        super().__init__(
            plugin_instance_id,
            config_dict,
        )
        # FS_91_88_07_23 repath tree
        tree_walker: TreeWalker = TreeWalker(
            "repath",
            self.config_dict[repath_tree_],
        )
        self.paths_to_repath: dict[tuple[str, ...], tuple[str, ...]] = tree_walker.build_paths_to_paths()

    def validate_config(
        self,
    ):
        repath_tree_interp_config_desc.validate_dict(self.config_dict)


    def create_interp(
        self,
        interp_ctx: InterpContext,
    ) -> AbstractInterp:
        return RepathTreeInterp(
            self.plugin_instance_id,
            self.tree_path_config_dict[interp_ctx.interp_tree_context.interp_tree_path],
            interp_ctx,
            self.func_paths,
            self.paths_to_repath,
        )

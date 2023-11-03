try:
    from aim._core.storage import treeutils
except ModuleNotFoundError:
    # lookup the aimos package
    from aimos._core.storage import treeutils

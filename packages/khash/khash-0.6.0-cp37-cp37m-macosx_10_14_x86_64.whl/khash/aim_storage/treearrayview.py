try:
    from aim._core.storage.treearrayview import TreeArrayView
except ModuleNotFoundError:
    # lookup the aimos package
    from aimos._core.storage.treearrayview import TreeArrayView

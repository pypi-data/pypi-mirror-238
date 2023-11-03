try:
    from aim._core.storage.embedded.prefixcontainer import PrefixContainer
except ModuleNotFoundError:
    # lookup the aimos package
    from aimos._core.storage.prefixview import PrefixView as PrefixContainer

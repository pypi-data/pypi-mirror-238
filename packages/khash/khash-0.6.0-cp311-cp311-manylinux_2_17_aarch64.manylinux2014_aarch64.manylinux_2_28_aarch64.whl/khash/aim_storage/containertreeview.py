try:
    from aim._core.storage.embedded.containertreeview import ContainerTreeView
except ModuleNotFoundError:
    # lookup the aimos package
    from aimos._core.storage.containertreeview import ContainerTreeView

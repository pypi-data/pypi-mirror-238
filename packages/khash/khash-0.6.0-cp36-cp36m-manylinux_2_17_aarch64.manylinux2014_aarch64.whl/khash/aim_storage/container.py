try:
    from aim._core.storage.embedded.container import (
        Container,
        ContainerItemsIterator,
        ContainerKey,
        ContainerValue
    )
except ModuleNotFoundError:
    # lookup the aimos package
    from aimos._core.storage.container import (
        Container,
        ContainerItemsIterator,
        ContainerKey,
        ContainerValue
    )

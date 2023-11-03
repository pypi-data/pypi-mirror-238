from amsdal_models.schemas.loaders.base import TransactionsLoaderBase as TransactionsLoaderBase
from collections.abc import Iterator
from pathlib import Path

class CliTransactionsLoader(TransactionsLoaderBase):
    def __init__(self, app_root: Path) -> None: ...
    def iter_transactions(self) -> Iterator[Path]: ...

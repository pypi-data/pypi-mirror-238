from collections.abc import Sequence
from typing import Optional

from atoti._docs_utils import (
    STANDARD_EXTERNAL_TABLE_OPTIONS_KWARGS as _STANDARD_EXTERNAL_TABLE_OPTIONS_KWARGS,
)
from atoti.directquery._clustering_columns_parameter import (
    CLUSTERING_COLUMNS_PARAMETER as _CLUSTERING_COLUMNS_PARAMETER,
)
from atoti.directquery._external_table_options import ExternalTableOptions
from atoti_core import doc

from .table import ClickhouseTable


class ClickhouseTableOptions(ExternalTableOptions[ClickhouseTable]):
    @doc(**_STANDARD_EXTERNAL_TABLE_OPTIONS_KWARGS)
    def __init__(
        self,
        *,
        clustering_columns: Sequence[str] = (),
        keys: Optional[Sequence[str]] = None
    ) -> None:
        """Additional options about the external table to create.

        Args:
            {clustering_columns}
            {keys}
        """
        super().__init__(
            keys=keys,
            options={
                _CLUSTERING_COLUMNS_PARAMETER: clustering_columns
                if clustering_columns
                else None
            },
        )

from typing import Any, Optional, Tuple

from pyspark.sql.functions import col

from pyspark.sql import DataFrame

from sefazetllib import Builder, field
from sefazetllib.transform.Transform import Transform

@Builder
class DataFrameFilterRangeTransform(Transform):
    df: Optional[DataFrame] = None
    reference: str = field(default="")
    output: str = field(default="")
    column_name: str = field(default="")
    start: Any = field(default="")
    end: Any = field(default="")

    def execute(self) -> Tuple[str, DataFrame]:
        df_range = self.df
        if self.column_name != "":
            if self.start != "":
                df_range = df_range.filter((col(self.column_name) >= self.start))
            if self.end != "":
                df_range = df_range.filter((col(self.column_name) < self.end))
        return (
            self.output,
            df_range,
        )
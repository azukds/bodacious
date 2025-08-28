from typing import List

import polars as pl
import polars.selectors as cs

def mean_impute_nulls(train_df: pl.DataFrame, columns = None, drop_nulls = True, drop_nans = True) -> List[pl.Expr]:

    col_expr = pl.col(columns) if columns else cs.numeric()

    if drop_nulls: col_expr = col_expr.drop_nulls()
    if drop_nans: col_expr = col_expr.drop_nans()

    mean_vals = train_df.lazy().select(col_expr.mean()).collect().to_dict()

    return [pl.col(key).fill_null(val) for (key, val) in mean_vals.items()]
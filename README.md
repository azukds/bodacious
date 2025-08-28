[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![stability-alpha](https://img.shields.io/badge/stability-alpha-f4d03f.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#alpha)

THIS PROJECT IS IN ALPHA

I'm just playing with some ideas. Maybe it'll become something?

# bodacious

_Surfer slang:_

> extremely good, extremely great

A fresh approach to tabular feature engineering for machine learning pipelines.

Construct your, potentially stateful, polars expressions using bodacious functions before
using them in plain polars [contexts](https://docs.pola.rs/user-guide/concepts/expressions-and-contexts/#contexts). You
could even [export them as plain json](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.meta.serialize.html#polars.Expr.meta.serialize) 
for use in the future before loading them back in and applying them independently of bodacious (they are just plain old polars expressions).

## Example

```python
import bodacious.imputers as bd

from palmerpenguins import load_penguins
import polars as pl

penguins_pl = pl.DataFrame(load_penguins())

mean_imputation_exprs = bd.mean_impute_nulls(train_df = penguins_pl, columns=None)


print("State from 'train_df' is captured as part of the polars expression:")
print(mean_imputation_exprs)

print("Unmodified frame:")
print(penguins_pl)

print("Null values imputed:")
print(penguins_pl.with_columns(mean_imputation_exprs))
```

```terminal
State from 'train_df' is captured as part of the polars expression:
[<Expr ['col("bill_length_mm").fill_nul…'] at 0x7766D40C20D0>, <Expr ['col("bill_depth_mm").fill_null…'] at 0x7766D40C2110>, <Expr ['col("flipper_length_mm").fill_…'] at 0x7766D40C2150>, <Expr ['col("body_mass_g").fill_null([…'] at 0x7766D40C2190>, <Expr ['col("year").fill_null([Series[…'] at 0x7766D40C21D0>]

Unmodified frame:
shape: (344, 8)
┌───────────┬───────────┬──────────────┬──────────────┬──────────────┬─────────────┬────────┬──────┐
│ species   ┆ island    ┆ bill_length_ ┆ bill_depth_m ┆ flipper_leng ┆ body_mass_g ┆ sex    ┆ year │
│ ---       ┆ ---       ┆ mm           ┆ m            ┆ th_mm        ┆ ---         ┆ ---    ┆ ---  │
│ str       ┆ str       ┆ ---          ┆ ---          ┆ ---          ┆ f64         ┆ str    ┆ i64  │
│           ┆           ┆ f64          ┆ f64          ┆ f64          ┆             ┆        ┆      │
╞═══════════╪═══════════╪══════════════╪══════════════╪══════════════╪═════════════╪════════╪══════╡
│ Adelie    ┆ Torgersen ┆ 39.1         ┆ 18.7         ┆ 181.0        ┆ 3750.0      ┆ male   ┆ 2007 │
│ Adelie    ┆ Torgersen ┆ 39.5         ┆ 17.4         ┆ 186.0        ┆ 3800.0      ┆ female ┆ 2007 │
│ Adelie    ┆ Torgersen ┆ 40.3         ┆ 18.0         ┆ 195.0        ┆ 3250.0      ┆ female ┆ 2007 │
│ Adelie    ┆ Torgersen ┆ null         ┆ null         ┆ null         ┆ null        ┆ null   ┆ 2007 │
│ Adelie    ┆ Torgersen ┆ 36.7         ┆ 19.3         ┆ 193.0        ┆ 3450.0      ┆ female ┆ 2007 │
│ …         ┆ …         ┆ …            ┆ …            ┆ …            ┆ …           ┆ …      ┆ …    │
│ Chinstrap ┆ Dream     ┆ 55.8         ┆ 19.8         ┆ 207.0        ┆ 4000.0      ┆ male   ┆ 2009 │
│ Chinstrap ┆ Dream     ┆ 43.5         ┆ 18.1         ┆ 202.0        ┆ 3400.0      ┆ female ┆ 2009 │
│ Chinstrap ┆ Dream     ┆ 49.6         ┆ 18.2         ┆ 193.0        ┆ 3775.0      ┆ male   ┆ 2009 │
│ Chinstrap ┆ Dream     ┆ 50.8         ┆ 19.0         ┆ 210.0        ┆ 4100.0      ┆ male   ┆ 2009 │
│ Chinstrap ┆ Dream     ┆ 50.2         ┆ 18.7         ┆ 198.0        ┆ 3775.0      ┆ female ┆ 2009 │
└───────────┴───────────┴──────────────┴──────────────┴──────────────┴─────────────┴────────┴──────┘

Null values imputed:
shape: (344, 8)
┌───────────┬───────────┬──────────────┬─────────────┬─────────────┬─────────────┬────────┬────────┐
│ species   ┆ island    ┆ bill_length_ ┆ bill_depth_ ┆ flipper_len ┆ body_mass_g ┆ sex    ┆ year   │
│ ---       ┆ ---       ┆ mm           ┆ mm          ┆ gth_mm      ┆ ---         ┆ ---    ┆ ---    │
│ str       ┆ str       ┆ ---          ┆ ---         ┆ ---         ┆ f64         ┆ str    ┆ f64    │
│           ┆           ┆ f64          ┆ f64         ┆ f64         ┆             ┆        ┆        │
╞═══════════╪═══════════╪══════════════╪═════════════╪═════════════╪═════════════╪════════╪════════╡
│ Adelie    ┆ Torgersen ┆ 39.1         ┆ 18.7        ┆ 181.0       ┆ 3750.0      ┆ male   ┆ 2007.0 │
│ Adelie    ┆ Torgersen ┆ 39.5         ┆ 17.4        ┆ 186.0       ┆ 3800.0      ┆ female ┆ 2007.0 │
│ Adelie    ┆ Torgersen ┆ 40.3         ┆ 18.0        ┆ 195.0       ┆ 3250.0      ┆ female ┆ 2007.0 │
│ Adelie    ┆ Torgersen ┆ 43.92193     ┆ 17.15117    ┆ 200.915205  ┆ 4201.754386 ┆ null   ┆ 2007.0 │
│ Adelie    ┆ Torgersen ┆ 36.7         ┆ 19.3        ┆ 193.0       ┆ 3450.0      ┆ female ┆ 2007.0 │
│ …         ┆ …         ┆ …            ┆ …           ┆ …           ┆ …           ┆ …      ┆ …      │
│ Chinstrap ┆ Dream     ┆ 55.8         ┆ 19.8        ┆ 207.0       ┆ 4000.0      ┆ male   ┆ 2009.0 │
│ Chinstrap ┆ Dream     ┆ 43.5         ┆ 18.1        ┆ 202.0       ┆ 3400.0      ┆ female ┆ 2009.0 │
│ Chinstrap ┆ Dream     ┆ 49.6         ┆ 18.2        ┆ 193.0       ┆ 3775.0      ┆ male   ┆ 2009.0 │
│ Chinstrap ┆ Dream     ┆ 50.8         ┆ 19.0        ┆ 210.0       ┆ 4100.0      ┆ male   ┆ 2009.0 │
│ Chinstrap ┆ Dream     ┆ 50.2         ┆ 18.7        ┆ 198.0       ┆ 3775.0      ┆ female ┆ 2009.0 │
└───────────┴───────────┴──────────────┴─────────────┴─────────────┴─────────────┴────────┴────────┘
```




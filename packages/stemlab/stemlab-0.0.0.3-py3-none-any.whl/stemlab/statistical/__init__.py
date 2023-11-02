from .anova import anov
from .categorical import category
from .dataframes import dframe_lower
from .core import corr_tpvalue
from .descriptive import (
    unique_cat, freq_tables, mode_series, mode_freq, tabstat, tabstat_series,
    desc_stats
)
from .nonparametric import nonp
from .regresslinear import reglinear
from .sampledatasets import data_random, dataset_random, datasets
from .ttests import ttest, ttest_stats
from .wrangle import (
    relocate, insert, dframe_split, outliers, outliers_replace, scale, 
    dframe_labels, stack_cols, unstack_cols, df_order_by_list, multindex_reset,
    drop_contains, na_replace
)
from .ztests import ztest
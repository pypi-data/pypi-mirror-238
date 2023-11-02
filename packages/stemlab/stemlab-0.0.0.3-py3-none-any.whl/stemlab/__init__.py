'''
Stemlab is a Python library for performing mathematical computations.
It aims to become a first choice library for trainers and students
in Science, Technology, Engineering and Mathematics.

See the webpage for more information and documentation:

https://stemlab.org

'''

import sys
if sys.version_info < (3, 6):
    raise ImportError('Stemlab requires installation of Python version 3.6 or above.')
del sys

__version__ = '0.0.1'
__author__ = 'John Indika'
__credits__ = 'STEM Research'

from .calculus import (
    # diffintegration
    diff_parametric, 
    # nonlinear
    roots_nonlinear,
    # numericaldiff
    diff_richardson, 
    # numericalintegration
    int_cotes, int_cotes_data, int_composite, int_composite_data, int_romberg, 
    int_glegendre,
    # odes
    int_odes,
    # vector
    parametric_form, int_line, int_vector, int_surface,
)

from .core import (
    # array_like
    relax_parameter, quote_rational, matrix_inverse, to_listuple, abrange, 
    is_diff_constant, join_list, case_list, is_len_equal, is_iterable, 
    list_to_dict, dict_subset, table_na,
    # base
    plural_sing, strip_all, chars_replace, pm_sign, partial_chars, rand_string,
    # htmlatex
    latex_display, matrix_to_eqtns, dframe_color, dframe_to_html,
    # plotting
    interpolation_plot,
    # symbolic
    is_symexpr, expr_constant, simplify_expr, poly_terms, remove_zeros, 
    sympify_input, lambdify_expr, get_expr_vars
)

from .core.files import write_html, view_html

from .statistical import(
    # anova
    anov,
    # categorical
    category,
    # core
    corr_tpvalue,
    # dataframes
    dframe_lower,
    # descriptive
    unique_cat, freq_tables, mode_series, mode_freq, tabstat, tabstat_series,
    desc_stats,
    # nonparametric
    nonp,
    # regresslinear
    reglinear,
    # sampledatasets
    data_random, dataset_random, datasets,
    # ttests
    ttest, ttest_stats,
    # wrangle
    relocate, insert, dframe_split, outliers, outliers_replace, scale, 
    dframe_labels, stack_cols, unstack_cols, df_order_by_list, multindex_reset,
    drop_contains, na_replace,
    # ztests
    ztest
)
from .datasets import read_dataset, show_datasets, save_data
from .interpolation import interpolate
from .linearalgebra import (
    # iterative techniques
    solve_linear
)

#===========================================================================#
#                                                                           #
# STEM RESEARCH :: Technology for Innovation :: https://stemlab.org         #
#																			#
#===========================================================================#
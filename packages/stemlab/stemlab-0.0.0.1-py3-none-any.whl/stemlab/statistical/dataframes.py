from pandas import DataFrame, Series
from numpy import nan, triu_indices
from typing import Literal

def column_latex(col_latex=True) -> Literal['$', '']:
    """
    Whether or not to use latex in columns (i.e. add $ signs).
    """
    if col_latex is True:
        dollar_symbol = '$'
    else:
        dollar_symbol = ''

    return dollar_symbol

def dframe_lower(data, k=1, decimals=None) -> DataFrame:
    """
    Return the lower or upper triangle.
    """
    M = DataFrame(data).values
    M[triu_indices(M.shape[0], k)] = nan
    dframe = DataFrame(
        data=M,
        index=data.columns,
        columns=data.index
    ).fillna('')
    if decimals is not None:
        try:
            dframe = dframe.round(decimals)
        except:
            pass

    return dframe

def series_name(data, n=1):
    """
    Get Series name.
    """
    if isinstance(data, Series):
        return data.name.capitalize()
    return f'Sample {n}'
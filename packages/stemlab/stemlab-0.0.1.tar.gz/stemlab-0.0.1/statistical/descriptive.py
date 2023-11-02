from pandas import Series, DataFrame, crosstab
from numpy import round, array, ndarray, zeros, nan, std, mean
from ..core.errors import IterableError, PandifyError, SerifyError
from ..core.arraylike import is_iterable
from ..statistical.wrangle import dframe_labels
from ..core.validate import val_listitems

def unique_cat(data, columns='object', dict_cat=False) -> None:
    """
    ```

    Return unique categories for specified columns in a DataFrame.
    
    Parameter
    ---------
    data : {list, tuple, ndarray, Series, DataFrame}
        Data whose with distinct categories.
    columns : {str, list, tuple, ndarray, Series}, default='object'
        Column(s) whose categories we need. If object, then all columns with 
        object data type are considered.
    dict_cat: bool, default=False
        If True, then a dictionary of the unique categories for each of the
        specified columns will be shown. Otherwise, results will be displayed
        on the screen.
    
    Returns
    -------
    {dict_values, None}
    
    Examples
    --------
    >>> 

    ```
    """
    if not isinstance(data, DataFrame):
        try:
            dframe = DataFrame(data).applymap(lambda col: str(col))
        except:
            raise IterableError(par_name='data', string_=False, user_input=data)
    else:
        if columns == 'object':
            dframe = data.select_dtypes(include = ['object'])
        elif isinstance(columns, (str, list, tuple, ndarray, Series)):
            dframe = data[columns]
        
    if dict_cat:
        dict_values = {}
        for col in dframe.columns:
            dict_values.update({col: dframe[col].unique()})
        return dict_values
    else:
        dframe = DataFrame(dframe)
        for col in dframe.columns:
            print(f'{col}\n{"-" * len(col)}')
            print(f'{dframe[col].unique()[:50].tolist()}\n')
        return None
    
def _proportions(freq_table, dim):

    if dim == "rows":
        freq_table = freq_table.div(freq_table["Total"], axis=0)
    elif dim == "columns":
        freq_table = freq_table / freq_table.loc["Total"]
    elif dim == "both":
        freq_table = freq_table / freq_table.loc["Total", "Total"]
    else:
        raise ValueError(f"{dim} is an invalid option for 'dim'")

    return freq_table

def freq_tables(
        data, 
        col_names, 
        cells="counts(percent)", 
        dim="rows", 
        columns=None, 
        index=None, 
        decimals=2, 
        per_decimals=0
):
    """
    ```

    One way and two way frequency tables.

    Parameters
    ----------
    data : {DataFrame, Series, list, tuple, ndarray}
        xxx
    col_names : xxx
        xxx
    cells : {counts, percent, proportions, counts(percent)}, 
        default=counts(percent)
        xxx
    dim : {rows, columns, both}, default='rows'
        xxx
    columns : {list, tuple, ndarray, Series}, default=None
        xxx
    index : {list, tuple, ndarray, Series}, default=None
        xxx
    decimals : int, default=2
        xxx
    per_decimals : int, default=0
        xxx
        
    Returns
    -------

    Examples
    --------
    >> 
    ```
    """
    try:
        dframe = DataFrame(data)
    except:
        raise IterableError(par_name='data', user_input=data)

    if isinstance(col_names, str):
        col_names = [col_names]

    if not isinstance(col_names, (tuple, list)):
        raise TypeError(
            f"'{col_names} must be a list with at most two elements "
            f"represent the variables to be tabulated, got {type(col_names)}"
        )

    if len(col_names) > 2:
        raise Exception(
            f"'col_names' must have atmost 2 elements, got {len(col_names)}"
        )

    for col_name in col_names:
        if col_name not in dframe.columns:
            raise Exception(
                f"{col_name} is not one of the columns of the dataset"
            )

    if len(col_names) == 1: # one way frequency table
        if "co" in cells or "Fr" in cells:
            cells = "Frequency"
        freq_table = crosstab(
            dframe[col_names[0]], 
            columns="Frequency", 
            margins=True, 
            margins_name="Total"
        )
        row_names = list(freq_table.index)
        freq_values = freq_table.values
        result = DataFrame(
            freq_values[:, 0], index=row_names, columns=["Frequency"]
        )
        if "pr" in cells:
            cells = "proportions"
            percent_prop = freq_values[:, 0] / sum(freq_values[-1:, 0])
        elif "pe" in cells:
            cells = "percent"
            percent_prop = (
                freq_values[:, 0] / sum(freq_values[-1:, 0]) * 100
            )
        else:
            percent_prop = freq_values[:, 0]
        cum_percent = [percent_prop[0].tolist()]
        for k in range(1, len(percent_prop)):
            cum_percent.append(cum_percent[k - 1] + percent_prop[k])
        cum_percent[-1] = nan
        if "co" not in cells:
            result[f"{cells.capitalize()}"] = percent_prop
        result[f"Cum. {cells.capitalize()}"] = cum_percent
        try:
            result = result.round(decimals)
            if "Fr" in cells:
                result["Cum. Frequency"] = [
                    int(value) for value in result["Cum. Frequency"][:-1]
                ] + [""]
        except:
            pass
        dframe = result
    else: # two-way frequency table
        freq_table = crosstab(
            index=dframe[col_names[0]],
            columns=dframe[col_names[1]],
            margins=True,
            margins_name="Total",
        )
        row_names = list(freq_table.index)
        col_names = list(freq_table.columns)
        if "pr" in cells:
            freq_table = _proportions(freq_table, dim)
        elif cells == "percent":
            freq_table = _proportions(freq_table, dim) * 100
        elif "(" in cells or ")" in cells or "count(percent)" in cells:
            freq_array = array(freq_table)
            freq_percent = round(
                array(_proportions(freq_table, dim) * 100), decimals
            )
            rows, cols = freq_table.shape
            freq_counts_percent = zeros((rows, cols), dtype=object)
            for row in range(rows):
                for col in range(cols):
                    rowcol_count = round(freq_array[row, col], decimals)
                    if per_decimals == 0:
                        rowcol_percent = int(freq_percent[row, col])
                    else:
                        rowcol_percent = round(freq_percent[row, col], per_decimals)
                    freq_counts_percent[
                        row, col
                    ] = f"{rowcol_count} ({rowcol_percent}%)"
            freq_table = DataFrame(freq_counts_percent)
        else:
            pass

        try:
            freq_table = round(freq_table, decimals)
        except:
            pass

        dframe = DataFrame(
            freq_table.values, index=row_names, columns=col_names
        )
    # row and column names
    try:
        dframe.index = index
    except:
        pass
    try:
        dframe.columns = columns
    except:
        pass
    
    dframe = dframe.round(decimals)

    return dframe

def mode_series(data):
    """
    ```

    Returns the mode and the number of times it appears.

    Parameters:
    ----------
    data : {Series, list, tuple, ndarray}
        An array_like with the values for which we need the mode.
    
    Returns
    -------
    mode_catfreq : tuple
        The mode and how many times it appears, or None if there is no mode.

    Examples
    --------

    ```
    """
    try:
        data = Series(data)
    except:
        raise SerifyError(par_name='data')
    mode_cat = data.mode().values[0]
    mode_table = crosstab(data, columns='Frequency')
    mode_freq = mode_table.sort_values(by='Frequency', ascending=False)
    mode_freq = mode_freq.values[0][0]
    if mode_freq == 1: # there is no mode
        mode_freq = None
        mode_cat = None
    mode_catfreq = (mode_cat, mode_freq)

    return mode_catfreq

def mode_freq(data, columns=[], index_labels=None):
    """
    ```

    Returns the mode and the number of times it appears.

    Parameters:
    ----------
    data : {list, tuple, Series, ndarray, DataFrame}
        Array_like with values/columns for which we need the mode.
    
    Returns
    -------
    dframe_mode : DataFrame
        A DataFrame with the mode and how many times it appears, or None if 
        there is no mode.

    Examples
    --------

    ```
    """
    try:
        dframe = DataFrame(data)
    except:
        raise PandifyError(par_name='data')
    if columns:
        dframe = dframe[columns]
    # apply the series function on the DataFrame columns
    dframe_mode = dframe.apply(lambda col: mode_series(data=col)).T
    dframe_mode.columns = ['Mode', 'Frequency']
    dframe_mode.index = dframe_labels(dframe=dframe_mode, df_labels=index_labels)

    return dframe_mode

def _tabstat_col_names(measures):

    if 'location' in measures:
        col_names = ['N', 'Mean', 'Median']
    elif 'dispersion' in measures:
        col_names = [
            'N', 'Minimum', 'Maximum', 'Range', 'Variance', 'SD', 
            'CV', 'SEM', 'P25', 'P75', 'IQR'
        ]
    elif 'distribution' in measures:
        col_names = ['N', 'Skewness', 'Kurtosis']
    elif measures == 'count':
        col_names = ['N']
    elif measures == 'mean':
        col_names = ['Mean']
    elif measures == 'median':
        col_names = ['Median']
    elif measures == 'minimum':
        col_names = ['Minimum']
    elif measures == 'maximum':
        col_names = ['Maximum']
    elif measures == 'range':
        col_names = ['Range']
    elif measures == 'variance':
        col_names = ['Variance']
    elif measures == 'std':
        col_names = ['SD']
    elif measures == 'sem':
        col_names = ['SEM']
    elif measures == 'q1':
        col_names = ['P25']
    elif measures == 'q3':
        col_names = ['P75']
    elif measures == 'iqr':
        col_names = ['IQR']
    elif measures == 'skewness':
        col_names = ['Skewness']
    elif measures == 'kurtosis':
        col_names = ['Kurtosis']
    
    # user provided multiple statistics
    if is_iterable(array_like=measures, includes_str=False):
        col_names = [measures.title() for measures in measures]
    
    return col_names

def tabstat(dframe, measures='location', index_labels=None, decimals=4):
    """
    ```

    Parameters
    ----------
    data : DataFrame
        xxx
    index_labels : {int, array_like, None}, default=0
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels
        None .............. Will remove the DataFrame index       
        ==============================================================
    measures : {}, default='measures='location'
        xxx
    decimals : int, default=4
        xxx
    
    Returs
    ------
    dframe_stats : DataFrame
        xxx

    Examples
    --------

    ```
    """
    try:
        dframe = DataFrame(dframe)
    except:
        raise PandifyError(par_name='dframe')
    dframe_stats = dframe.apply(lambda col: tabstat_series(
        data=col,
        measures=measures,
        decimals=decimals)
    ).T
    dframe_stats.index = dframe_labels(dframe=dframe_stats, df_labels=index_labels)
    try:
        col_names = _tabstat_col_names(measures=measures)
        if 'Location' in col_names:
            col_names = ['N', 'Mean', 'Median']
        elif 'Dispersion' in col_names:
            col_names = ['N', 'Minimum', 'Maximum', 'Range', 'Variance', 'SD', 
                         'CV', 'SEM', 'P25', 'P75', 'IQR']
        elif 'Distribution' in col_names:
            col_names = ['N', 'Skewness', 'Kurtosis']
        dframe_stats.columns = col_names
    except UnboundLocalError:
        raise ValueError(f"'{measures}' is an invalid value for 'measures'")
    except:
        raise Exception('An unexpected error occurred.')
    
    dframe_stats['N'] = dframe_stats['N'].map(int)
    
    return dframe_stats

def tabstat_series(data, measures='location', decimals=4):
    """
    ```

    Tabulate values of a Series.

    data : {Series, list, tuple, ndarray}
        xxx
    measures : {}, default='measures='location'
        xxx
    decimals : int, default=4
        xxx

    ```
    """
    try:
        data = Series(data)
    except:
        raise SerifyError(par_name='data')
    
    N = data.count()
    mean_ = data.mean(skipna=True)
    median_ = data.median(skipna=True)
    min_ = data.min(skipna=True)
    max_ = data.max(skipna=True)
    range_ = max_ - min_
    var_ = data.var(skipna=True)
    std_ = data.std(skipna=True)
    sem_ = data.sem(skipna=True)
    cv_ = std(data, ddof=1) / mean(data) * 100
    q1_ = data.quantile(0.25)
    q3_ = data.quantile(0.75)
    iqr_ = q3_ - q1_
    skew_ = data.skew(skipna=True)
    kurt_ = data.kurt(skipna=True)
    if 'location' in measures:
        result = [N, mean_, median_]
    elif 'dispersion' in measures:
        result = [N, min_, max_, range_, var_, std_, cv_, sem_, q1_, q3_, iqr_]
    elif 'distribution' in measures:
        result = [N, skew_, kurt_]
    else:
        result = []
        if 'count' in measures:
            result.append(N)
        if 'mean' in measures:
            result.append(mean_)
        if 'median' in measures:
            result.append(median_)
        if 'minimum' in measures:
            result.append(min_)
        if 'maximum' in measures:
            result.append(max_)
        if 'variance' in measures:
            result.append(var_)
        if 'std' in measures:
            result.append(std_)
        if 'sem' in measures:
            result.append(sem_)
        if 'q1' in measures:
            result.append(q1_) 
        if 'q3' in measures:
            result.append(q3_)
        if 'iqr' in measures:
            result.append(iqr_)     
        if 'skewness' in measures:
            result.append(skew_)
        if 'kurtosis' in measures:
            result.append(kurt_)

    result = round(array(result), decimals)
        
    return result

def desc_stats(statistic, conf_level=95, decimals=8):
    """
    ```

    This is ...

    Parameters
    ----------
    statistic : {...}
        This is ...
        =================================================================
        Argument            Description
        =================================================================
        count ............. Number of values
        sum ............... N
        mean .............. N
        median ............ N
        mode .............. N
        min ............... N
        max ............... N
        range ............. N
        p25 ............... N
        p75 ............... N
        percentile ........ N
        variance .......... N
        stdev ............. N
        sem ............... N
        cv ................ N
        iqr ............... N
        skewness .......... N
        kurtosis .......... N
        =================================================================

    Returns
    -------

    Examples
    --------
    >>>

    ```
    """
    valid_stats = [
        'count', 'sum', 'mean', 'median', 'mode',
        'min', 'max', 'range', 'p25', 'p75', 'percentile', 'variance', 
        'stdev', 'sem', 'cv', 'iqr',
        'skewness', 'kurtosis'
    ]

    statistic = val_listitems(
        par_name='statistic', valid_items=valid_stats, user_input=statistic
    )
    
    if statistic == 'count':
        999
    elif statistic == 'sum':
        999
    elif statistic == 'mean':
        999
    elif statistic == 'median':
        999
    elif statistic == 'mode':
        999
    elif statistic == 'min':
        999
    elif statistic == 'max':
        999
    elif statistic == 'range':
        999
    elif statistic == 'p25':
        999
    elif statistic == 'p75':
        999
    elif statistic == 'percentile':
        999
    elif statistic == 'variance':
        999
    elif statistic == 'stdev':
        999
    elif statistic == 'sem':
        999
    elif statistic == 'cv':
        999
    elif statistic == 'iqr':
        999
    elif statistic == 'skewness':
        999
    elif statistic == 'kurtosis':
        999

    return None
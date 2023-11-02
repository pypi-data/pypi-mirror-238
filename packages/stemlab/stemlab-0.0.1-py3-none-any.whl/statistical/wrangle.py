from warnings import warn
from pandas import Series, DataFrame, Categorical, concat
from numpy import array, ndarray, where, arange
from ..core.errors import (
    IterableError, ColumnsLengthError, RowLengthError, NotInValuesError,
    BooleanError, DataFrameError, VectorLengthError, StringError, 
    NotInColumnsError, RequiredError, PandifyError
)
from ..core.arraylike import case_list, join_list, is_iterable
from ..core.base import plural_sing
from ..core.validate import val_string
    
class RelocateInsert:
    def __init__(self, dframe, columns, loc, after):
        self.dframe = dframe
        self.columns = columns
        self.loc = loc
        self.after = after

    def _dframe(self):
        
        if not isinstance(self.dframe, DataFrame):
            raise TypeError(
                f"'dframe' must be {DataFrame}, "
                f"got {type(self.dframe)}"
            )
        return self.dframe

    def _columns(self):
        
        if (not is_iterable(self.columns, includes_str=True) and 
            not isinstance(self.columns, DataFrame)):
            raise IterableError(self.columns, name='columns', string_=True)
        else:
            # convert to list if a string is given
            if not isinstance(self.columns, DataFrame):
                if isinstance(self.columns, str):
                    self.columns = [self.columns]
                else:
                    # just in case it is 2D, then convert to 1D
                    self.columns = array(self.columns).flatten()
        return self.columns

    def _loc(self):

        if not isinstance(self.loc, (str, int)):
            TypeError(f"'loc' must be a string or integer, got {type(self.loc)}")
        return self.loc
    
    def _after(self):

        if not isinstance(self.after, bool):
            raise BooleanError(par_name='after', user_input=self.after)
        return self.after
    
    def _dframe_out(self, column_names):
        
        dframe = DataFrame(self.columns) # just in case it is not a DataFrame
        # check column names
        if column_names is None:
            if isinstance(self.columns, DataFrame):
                # get column names from DataFrame
                column_names = self.columns.columns
            else:
                column_names = [
                    f'Col{index+1}' for index in range(dframe.shape[1])
                ]
        else:
            if isinstance(column_names, str):
                column_names = [column_names]
            
            if not is_iterable:
                raise IterableError(
                    self.column_names,
                    name='column_names'
                )

            if len(column_names) != dframe.shape[1]:
                raise ColumnsLengthError(
                    dframe=dframe, column_names=column_names
                )
        # rename the columns
        try:
            dframe.columns = column_names
        except:
            pass
            
        return dframe
    
    def _get_data(self):
        return (self._dframe(), self._columns(), self._loc(), self._after())

    def _dframe_new(self, column_names=None, relocate_=True):

        if relocate_ is True:
            # drop columns that are being relocated
            dframe_dropped = self.dframe.drop(self.columns, axis=1)
        else:
            dframe_dropped = self.dframe

        if isinstance(self.loc, int):
            col_index = self.loc
        elif is_iterable(self.loc, includes_str=True):
            if is_iterable(self.loc, includes_str=False):
                self.loc = array(self.loc).flatten()[0] # get first element
            try:
                col_index = dframe_dropped.columns.get_loc(self.loc)
                if not isinstance(col_index, int): # there are duplicate cols
                    # get location of first occurance of the duplicated columns
                    if isinstance(col_index, slice):
                        col_index = int(
                            str(col_index).split(',')[0].split('(')[1]
                        )
                    elif isinstance(col_index, ndarray):
                        # get first element of tuple, 
                        # then first element of array, i.e. the [0][0] part
                        col_index = where(col_index==True)[0][0]
            except:
                if self.loc in self.columns:
                    if relocate_: # only needed if relocating, not inserting
                        raise KeyError(
                            f"'loc' cannot be in the column(s) you "
                            "are relocating / inserting."
                        )
                else:
                    raise KeyError(
                        f"'{self.loc}' does not exist in the specified "
                        "DataFrame"
                    )
            if self.after:
                col_index += 1 # so that it comes after the specified column
        else:
            raise TypeError(
                "'loc' must be integer or string, "
                f"got {type(self.loc)}"
            )
        
        # if 'col_index' exceeds the number of columns, 
        # then just put the specified column(s) at the end of the DataFrame
        if abs(col_index) >= dframe_dropped.shape[1]:
            col_index = dframe_dropped.shape[1]
        
        # if negative indices are given, then start from right of the DataFrame
        if col_index < 0:
            col_index = dframe_dropped.shape[1] + col_index+1

        if relocate_ is True:
            if isinstance(self.columns, DataFrame):
                raise TypeError(f"'columns' cannot be a DataFrame")
            dframe_cols = self.dframe[self.columns] # subset the columns
        else: 
            dframe_cols = self._dframe_out(column_names=column_names)
        
        # now put the DataFrames together (concatenate)
        dframe = concat(
            objs=[dframe_dropped.iloc[:, :col_index],
                dframe_cols,
                dframe_dropped.iloc[:, col_index:]],
                axis=1
        )
        
        return dframe

def relocate(dframe, columns_to_relocate, relocate_to=-1, after=True):
    """
    ```

    Relocate column(s) before or after a specified column or at a specified 
    positional index.
    
    Parameters
    ----------
    dframe : DataFrame
        A DataFrame which contains the column(s) to be relocated.
    columns_to_relocate : {list, tuple, ndarray, Series}
        A list, tuple or array with the column(s) in the DataFrame that need 
        be relocated.
    relocate_to : {str, int} , default=-1
        Column name or index where the specified column(s) should be 
        relocated to.
    after : bool, default=True
        If True, specified column(s) will be inserted after the column 
        specified in `relocate_to`. Only used when `relocate_to` is a column 
        name (not index).
    
    Returns
    -------
    dframe : DataFrame
        A DataFrame with columns reordered.

    Examples
    --------
    >>> df = DataFrame(np.random.randint(low=10, high=50, size=(5, 10)), columns=list('BCDDEFGHJD'))
    >>> stm.relocate(dframe=df, columns_to_relocate=['E'], relocate_to='D', after=True)

    ```
    """
    get_data = RelocateInsert(
        dframe=dframe,
        columns=columns_to_relocate,
        loc=relocate_to,
        after=after
    )
    dframe = RelocateInsert(*get_data._get_data())._dframe_new(relocate_=True)

    return dframe

def insert(
        dframe, 
        data_to_insert, 
        column_names=None, 
        insert_at=-1, 
        after=True
):
    """
    ```

    Insert column(s) before or after a specified column or at a specified 
    positional index.
    
    Parameters
    ----------
    dframe : DataFrame
        A DataFrame to which new data should be inserted.
    data_to_insert : {list, tuple, ndarray, Series, DataFrame}
        A list, tuple or array with the data that needs to be inserted.
    insert_at : {str, int} , default=-1
        Column name or index where the data in ``data_to_insert`` should be 
        inserted.
    after : bool, default=True
        If True, specified data will be inserted after the column 
        specified in ``insert_at``. Only used when ``insert_at`` is a column 
        name (not index).
    
    Returns
    -------
    dframe : DataFrame
        A DataFrame with columns reordered.

    Examples
    --------
    >>>

    ```
    """
    get_data = RelocateInsert(
        dframe=dframe,
        columns=data_to_insert,
        loc=insert_at,
        after=after
    )
    dframe = RelocateInsert(*get_data._get_data())._dframe_new(
        column_names, relocate_=False
    )
    
    return dframe

def dframe_labels(dframe, df_labels, col_latex=False, prefix=None, index=True):
    """
    Assign index or column labels (names) to a DataFrame
    """
    # dframe
    if not isinstance(dframe, DataFrame):
        try:
            dframe = DataFrame(dframe)
        except:
            raise PandifyError(par_name='dframe', user_input=dframe)
    
    # index
    if not isinstance(index, bool):
        index = True
    
    # df_labels
    label_cases = ['capitalize', 'title', 'lower', 'upper']
    if df_labels in label_cases:
        df_labels = df_labels.lower()

    if index is True:
        if df_labels in label_cases:
            if df_labels.lower() == 'capitalize':
                df_labels = dframe.index.str.capitalize()
            elif df_labels == 'title':
                df_labels = dframe.index.str.title()
            elif df_labels == 'lower':
                df_labels = dframe.index.str.lower()
            else: # upper
                df_labels = dframe.index.str.upper()
        else:
            if not df_labels and df_labels != 0:
                df_labels = ['' for _ in range(dframe.shape[0])]
            elif is_iterable(array_like=df_labels):
                if dframe.shape[0] != len(df_labels):
                    raise RowLengthError(par_name='index_labels', dframe=dframe)
            elif isinstance(df_labels, int):
                df_labels = arange(
                    start=df_labels,
                    stop=dframe.shape[0] + df_labels
                )
            else:
                df_labels = arange(stop=dframe.shape[0])
    else:
        if df_labels in label_cases:
            if df_labels.lower() == 'capitalize':
                df_labels = dframe.columns.str.capitalize()
            elif df_labels == 'title':
                df_labels = dframe.columns.str.title()
            elif df_labels == 'lower':
                df_labels = dframe.columns.str.lower()
            else: # upper
                df_labels = dframe.columns.str.upper()
        else:
            if not df_labels and df_labels != 0:
                df_labels = ['' for _ in range(dframe.shape[1])]
            elif is_iterable(array_like=df_labels):
                if dframe.shape[1] != len(df_labels):
                    raise ColumnsLengthError(dframe=dframe, col_names='df_labels')
            elif isinstance(df_labels, int):
                df_labels = arange(
                    start=df_labels,
                    stop=dframe.shape[0] + df_labels
                )
            else:
                df_labels = arange(stop=dframe.shape[1])

    if prefix is not None:
        prefix = val_string(par_name='prefix', user_input=prefix)
        df_labels = [f'{prefix}{label}' for label in df_labels]

    if col_latex is True:
        df_labels = [f'${label}$' for label in df_labels]

    return df_labels

def dframe_split(dframe, group_vars) -> dict:
    """
    ```
    
    Split DataFrame

    Parameters
    ----------
    dframe : DataFrame
        A DataFrame that is to be split by specified group variable(s).
    group_vars : {list, tuple, ndarray, Series}
        Categorical variables by which the DataFrame should be split. 

    Returns
    -------
    dict_dframes : Dict
        A dictionary containing the DataFrames.
    
    Examples
    --------
    >>> df = stm.dataset1()
    >>> df = dframe_split(dframe=df, group_vars=['gender'])

    ```
    """
    dict_dframes = {
        key: dframe.loc[value] for key, value in 
        dframe.groupby(group_vars).groups.items()
    }

    return dict_dframes

def df_order_by_list(dframe, column_to_sort, labels_list):
    """
    Sort DataFrame column by list order.
    """
    if not isinstance(dframe, DataFrame):
        raise DataFrameError(par_name='dframe', user_input=dframe)
    
    if not isinstance(column_to_sort, str):
        raise StringError(par_name='column_to_sort', user_input=column_to_sort)
    
    if not is_iterable(labels_list):
        raise IterableError(par_name='label_list', user_input=labels_list)

    dframe = dframe.iloc[
            Categorical(dframe[column_to_sort], labels_list).argsort()
        ]
    
    return dframe

def stack_cols(dframe, columns_to_stack=[], col_labels=None, order_columns=True):
    """
    ```

    Stack columns of a DataFrame.

    Parameters
    ----------
    dframe : DataFrame
        DataFrame with the columns to be stacked.
    columns_to_stack
        Columns whose values are to be stacked into a single column.
    col_names
        Column names for the new DataFrame.

    Return
    ------
    dframe : DataFrame
        A DataFrame with two columns, where the first column contains the
        categories (gotten from column names) and the second contains the 
        values.

    Examples
    --------

    ```
    """
    if not isinstance(dframe, DataFrame):
        raise DataFrameError(par_name='dframe', user_input=dframe)
    df_columns_set = set(dframe.columns) # should be here
    if columns_to_stack:
        if not is_iterable(array_like=columns_to_stack):
            raise IterableError(par_name='columns_to_stack', user_input=columns_to_stack)
        columns_to_stack = array(columns_to_stack).tolist()
        # check that the columns are in the DataFrame
        columns_set = set(columns_to_stack)
        if not columns_set.issubset(df_columns_set):
            not_in_columns = columns_set.difference(df_columns_set)
            not_in_columns = ', '.join(map(str, not_in_columns))
            if len(not_in_columns) == 1:
                not_in_columns = f"'{not_in_columns[0]}' is"
            else:
                not_in_columns = f"'{not_in_columns}' are"
            raise ValueError(
                f"{not_in_columns} not among the DataFrame column names"
            )
    else:
        columns_to_stack = dframe.columns.tolist()
    # extract the column names
    dframe = dframe[columns_to_stack]
    dframe = DataFrame(dframe.stack())\
    .reset_index()\
    .drop('level_0', axis=1)\
    .sort_values(by='level_1')
    if col_labels is None:
        dframe.columns = ['_stack', 'values']
    else:
        if not is_iterable(array_like=col_labels):
            raise IterableError(par_name='col_labels', user_input=col_labels)
        if len(col_labels) != 2:
            raise VectorLengthError(
                par_name='col_labels', 
                n=2, 
                label='exactly', 
                user_input=col_labels
            )
        try:
            dframe.columns = col_labels
        except:
            dframe.columns = ['_stack', 'values']

    if not isinstance(order_columns, bool):
        order_columns = True
    if order_columns is True:
        # sort DataFrame in the way the columns are ordered in the list
        # by default, Pandas will sort in alphabetic order
        dframe = df_order_by_list(
            dframe=dframe, 
            column_to_sort=dframe.columns[0], 
            labels_list=columns_to_stack
        )
    
    dframe.index = range(dframe.shape[0])

    return dframe

def unstack_cols(
        dframe, 
        cat_column, 
        categories=[], 
        values_column='', 
        col_labels=None, 
        order_columns=True
):
    """
    ```

    Stack columns of a DataFrame.

    Parameters
    ----------
    dframe : xxxx
        xxxx
    cat_column : 
        xxxx
    categories : 
        xxxx
    values_column : 
        xxxx
    col_labels
        xxxx
    order_columns : xxxx
        xxxx

    Returns
    -------

    Examples
    --------

    ```
    """
    if not isinstance(dframe, DataFrame):
        raise DataFrameError(par_name='dframe', user_input=dframe)
    # get DataFrame columns, we will need them
    dframe_columns = set(dframe.columns)
    if not is_iterable(cat_column, includes_str=True):
        raise IterableError(par_name='cat_column', user_input=cat_column)
    if not isinstance(cat_column, str):
        if len(cat_column) != 1:
            raise VectorLengthError(
                par_name='cat_column', n=1, user_input=cat_column
            )
        else:
            cat_column = cat_column[0]
    # check that the given column is one of the DataFrame columns
    if cat_column not in dframe_columns:
        raise NotInColumnsError(par_name='cat_column', user_input=cat_column)
    
    # categories
    if categories:
        if not is_iterable(categories):
            raise IterableError(par_name='categories', user_input=categories)
        # get only those categories that are in the `cat_column` column
        categories_set = set(dframe[cat_column]).intersection(categories)
        if len(categories_set) == 0:
            raise ValueError(
                f"'{categories}' does not contain any of the categories "
                f"specified in 'categories'"
            )
        # maintain order or categories, note that `set` did order the 
        # elements alphabetically
        not_found = set(categories).difference(set(dframe[cat_column]))
        if not_found: # if it is not empty
            join_list_ = join_list(
                list_to_join=not_found, 
                delimiter=", ", 
                use_and=True, 
                html_tags=False
            )
            was_were = plural_sing(singular='was', plural='were', n=len(not_found))
            s = plural_sing(singular='', plural='s', n=len(not_found))
            warn(
                f"\nThe value{s} {join_list_} {was_were} not found in the "
                f"column '{cat_column}'"
            )
        categories = [categ for categ in categories if categ in categories_set]
    else:
        # if categories are not given, then use all the categories of the 
        # specified column
        categories = dframe[cat_column].unique()
    categories = array(categories).tolist() # convert to list for convenience
    # values_column
    if not values_column:
        raise RequiredError(par_name='values_column')
    else:
        if not is_iterable(values_column, includes_str=True):
            raise IterableError(
                par_name='values_column', user_input=values_column
            )
        if not isinstance(values_column, str):
            if len(values_column) != 1:
                raise VectorLengthError(
                    par_name='values_column', n=1, user_input=values_column
                )
            else:
                values_column = values_column[0]
    # filter only the two variables from the DataFrame 
    # [cat_column, values_column]
    dframe = dframe.loc[:, [cat_column, values_column]]
    # filter the categories to unstack (filtering is by observations)
    dframe = dframe.loc[dframe[cat_column].isin(categories)]
    # split DataFrame
    df_dict = dframe_split(dframe, group_vars=[cat_column])
    # initialize and concatenate
    dframe = DataFrame()
    for name, df in df_dict.items():
        df = df.iloc[:, [1]]
        df.index = arange(df.shape[0])
        df.columns = [name]
        dframe = concat([dframe, df], axis=1)
    # assign column labels after concatenation
    if col_labels is None: # no columns given
        dframe.columns = df_dict.keys()
    else:
        try:
            dframe.columns = dframe_labels(
                dframe=dframe, df_labels=col_labels, index=False
            )
        except: # if invalid columns, then user original names
            dframe.columns = df_dict.keys()
    
    if not isinstance(order_columns, bool):
        order_columns = True
    if order_columns is True:
        # sort DataFrame in the way the columns are ordered in the list
        # by default, Pandas will sort in alphabetic order
        if col_labels in ['lower', 'upper', 'title', 'capitalize']:
            categories = case_list(list_=categories, case_=col_labels)
        dframe = dframe[categories]

    return dframe

def outliers(data, method='iqr', std=1) -> Series:
    """
    ```

    Returns a vector of outliers in given data.

    Parameters
    ----------
    data : {Series, ndarray, list, tuple}
        A iterable with data values.
    method : iqr or std, default='iqr'
        The method to be used to the outlier bounds.
    std : int, default=1
        Standards deviation from the mean. Only used if ``method='std'``.
    
    Returns
    -------
    data : Series
        A Pandas Series of outliers.

    ```
    """
    data = Series(data).dropna()
    if method not in ['iqr', 'std']:
        raise ValueError(
            f"{method} is an invalid method, "
            "must be 'iqr' or 'std'."
        )
        
    if std not in [1, 2, 3]:
        raise ValueError(f"{std} is an invalid method, must be 1, 2, or 3.")
        
    if method == 'iqr':
        Q1, Q3 = data.quantile([0.25, 0.75])
        IQR = Q3 - Q1
        lower_limit = Q1 - (1.5 * IQR)
        upper_limit = Q3 + (1.5 * IQR)
    else:
        lower_limit = data.mean() - std * data.std()
        upper_limit = data.mean() + std * data.std()
    outliers = data[(data < lower_limit) | (data > upper_limit)].tolist()
            
    return outliers

def outliers_replace(
        data,
        method='iqr',
        std=1,
        replace_with='median'
) -> Series:
    """
    ```

    Returns a vector of outliers in given data.

    Parameters
    ----------
    data : {Series, ndarray, list, tuple}
        A iterable with data values.
    method : iqr or std, default='iqr'
        The method to be used for the outlier bounds.
    std : int, default=1
        Standards deviation from the mean. Only used if method='std'.
    replace_with : {'median', 'mean', int, float}, default='median'
        The value to be used to replace the outlier(s) if any.
    
    Returns
    -------
    outliers : list
        A list of outliers replaced.

    ```
    """
    data = Series(data).dropna()
    if method not in ['iqr', 'std']:
        raise ValueError(f"{method} is an invalid value, " 
                         "must be 'iqr' or 'std'.")
        
    if std not in [1, 2, 3]:
        raise ValueError(f"{std} is an invalid value, must be 1, 2, or 3.")
    
    if isinstance(replace_with, str):
        if replace_with not in ['mean', 'median']:
            raise ValueError(
                f"{replace_with} is an invalid value, must "
                "be 'mean' or 'median'"
            )
        if replace_with == 'mean':
            replace_with = data.mean()
        else:
            replace_with = data.median()
    else:
        if not isinstance(replace_with, (int, float)):
            raise TypeError(
                f"{replace_with} is an invalid value for 'replace_with'"
            )

    if method == 'iqr':
        Q1, Q3 = data.quantile([0.25, 0.75])
        IQR = Q3 - Q1
        lower_limit, upper_limit = Q1 - (1.5 * IQR), Q3 + (1.5 * IQR)
    else:
        lower_limit = data.mean() - std * data.std()
        upper_limit = data.mean() + std * data.std()

    outliers = data[(data < lower_limit) | (data > upper_limit)].tolist()
    data = data.replace(to_replace=outliers, value=replace_with)
            
    return data

def scale(data, method='zscore', ddof=0) -> Series:
    """
    ```

    Scale / adjust values that exist on different scales into a common scale.

    Parameters
    ----------
    data : {Series, ndarray, list, tuple}
        A iterable with data values.
    method : {mas, mmas, zscore}, default='zscore'
        The scaling method to be applied.
    ddof : int, default=0
        Degrees of freedom, used when method='zscore'

    Returns
    -------
    data : Series
        A Series with the scaled values.

    ```
    """
    data = Series(data)
    valid_methods = ['mas', 'mmas', 'zscore']
    if method not in valid_methods:
        raise NotInValuesError(
            par_name='method', valid_args=valid_methods, user_input=method
        )

    if method == 'mas':
        data = data / data.abs().max()
    elif method == 'mmas':
        data = (data - data.min()) / (data.max() - data.min())
    else:
        data = (data - data.mean()) / data.std(ddof=ddof)

    return data

def multindex_reset(dframe, sep=''):
    
    col_labels = dframe.columns.tolist()
    df = DataFrame(col_labels)
    col_labels = df.applymap(str).apply(
        lambda col: sep.join(col), axis=1
    )
    dframe.columns = col_labels.tolist()
    dframe = dframe.reset_index()
    
    return dframe

def drop_contains(dframe, string_, col_names=None, re_index=False, axis=0):
    """
    
    """
    if axis == 1:
        dframe = dframe.drop(
            [col for col in dframe.columns if dframe[col].apply(
                    lambda s: string_ in str(s)
                ).any()
            ],
            axis=1
        )
    else:
        if col_names is None:
            dframe = dframe.select_dtypes('object') # select string variables
            col_names = dframe.columns
        for col_name in col_names:
            dframe = dframe[dframe[col_name].str.contains(string_) == False]
        if re_index:
            dframe.index = range(dframe.shape[0])
        
    return dframe

def na_replace(series, statistic='median'):
    """
    Replace missing values with the mean or median.
    """
    series_na_dropped = series.dropna()
    if statistic == 'median':
        series = series.fillna(value=series_na_dropped.median())
    else:
        series = series.fillna(value=series_na_dropped.mean())
    
    return series
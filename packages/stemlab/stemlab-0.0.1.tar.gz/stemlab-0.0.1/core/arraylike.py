from numpy import (
    ndarray, diag, triu, tril, dot, hstack, repeat, nan, array, float64, 
    append, diff, arange, zeros, round, asarray
)
from numpy.linalg import inv, eigvals, det
from pandas import DataFrame, Series, set_option
from sympy import Matrix, Rational, MutableDenseMatrix, flatten, sympify
from ..core.errors import (
    SingularMatrixError, NumpifyError, IterableError, SympifyError, 
    VectorLengthError, IntegerError
)

def _sympify_input(expr_array, to_matrix=False):
    """
    Converts a string to a symbolic expression.
    """
    try:
        expr_array = sympify(expr_array)
        if to_matrix is True:
            expr_array = Matrix(expr_array)
    except:
        raise SympifyError(par_name='expr_array', user_input=expr_array)
    
    return expr_array
        
def quote_rational(array_values):
    """
    Converts fractions to strings, i.e. encloses them in quotation marks
    """
    array_values = _sympify_input(array_values, to_matrix=True)
    nrow, ncol = Matrix(array_values).shape
    for i in range(nrow):
        for j in range(ncol):
            # isinstance() doesn't work quite well, just use type() == Rational
            if (type(array_values[i][j]) == Rational):  
                array_values[i][j] = str(array_values[i][j])

    return array_values

def relax_parameter(A):
    """
    Calculate the relaxation parameter for SOR method.
    """
    D = diag(diag(A))
    L = tril(A, k = -1)
    U = triu(A, k = 1)
    Tj = dot(inv(D), L + U)
    w = 2 / (1 + (1 - (max(abs(eigvals(Tj)))) ** 2) ** (1/2))

    return w

def matrix_inverse(M, par_name=None):
    """
    ```
    
    Calculate the inverse of a square matrix.

    Parameter
    ---------
    M : array_like
        2D square array.
    par_name
        Name of the 2D square array.

    Returns
    -------


    Examples
    --------
    >> 

    ```
    """
    try:
        m_det = det(M)
    except:
        raise NotImplemented(f"Unable to calculate the determinant of '{par_name}'") 
    if m_det == 0:
        raise SingularMatrixError(par_name=par_name, user_input=M.tolist())
    m_inverse = inv(M)

    return m_inverse


def abrange(a, b, h=1):
    """
    Return evenly spaced values between the interval a and b.

    Parameters
    ----------
    a : int
        Start of the sequence.
    b : int
        End of the sequence.

    Returns
    result : ndarray
        A Numpy array of evenly spaced values between ``a`` and ``b`` inclusive.

    Examples
    --------
    >> import stemlab as stm

    >> abrange(a=10, b=20)
    >> abrange(a=10, b=50, h=3)
    >> abrange(a=50, b=20, h=2)

    """
    result = arange(a, b, h)
    if result[-1] != b:
        result = append(result, b)
    return result

def is_diff_constant(x, decimals=8):
    """
    Check if the difference between consecutive elements of a list is constant.
    """
    return sum(round(diff(x, 2), decimals)) == 0


def join_list(list_to_join, delimiter=", ", use_and=True, html_tags=True):
    """
    Join elements of a list into a single string.
    """
    # list_to_join
    list_to_join = to_listuple(
        array_values=list_to_join, par_name='list_to_join'
    )

    # html_tags
    if not isinstance(html_tags, bool):
        html_tags = True
    
    if html_tags is True:
        html_left_aaa = '<span style="color:#aaa;">'
        html_left_000 = '<span style="color:#000;">'
        html_right = '</span>'
    else:
        html_left_aaa, html_left_000, html_right = [''] * 3
    
    # use_and
    if not isinstance(use_and, bool):
        use_and = True
    
    # delimiter
    if not isinstance(delimiter, str):
        delimiter = ", "

    if len(list_to_join) == 1:
        joined_list = list_to_join[0]
    else:
        if use_and:
            joined_list = f'{delimiter.join(map(str, list_to_join[:-1]))}{html_left_000} and{html_right} {list_to_join[-1]}'
        else:
            joined_list = delimiter.join(map(str, list_to_join))

    joined_list = f'{html_left_aaa}{joined_list}{html_right}'

    return joined_list

def case_list(list_, case_='lower'):
    """
    Change the case of list items.
    """
    if case_ in ['lower', 'upper', 'title', 'capitalize']:
        try:
            if case_ == 'lower':
                list_ = [list_.lower() for list_ in list_]
            elif case_ == 'upper':
                list_ = [list_.upper() for list_ in list_]
            elif case_ == 'title':
                list_ = [list_.title() for list_ in list_]
            else: # capitalize
                list_ = [list_.capitalize() for list_ in list_]
        except Exception as except_error:
            raise Exception(except_error)
        
    return list_

def is_len_equal(x, y):
    """
    Check if ``x`` and ``y`` have the same number of elements.
    """
    return len(x) == len(y)

def is_iterable(array_like, includes_str=False):
    """
    Check if array is iterable.
    """
    data_types = (str, tuple, list, set, ndarray, Series, DataFrame, MutableDenseMatrix)
    if includes_str is False:
        data_types = tuple(data_types[1:])
    if isinstance(array_like, data_types):
        return True
    return False

def list_to_dict(keys_list=None, values_list=[]) -> dict:
    """
    Converts two specified lists to a dictionary.

    Parameters
    ----------
    keys_list : {None, list, tuple, ndarray, Series}, default=None
        The keys of the dicationary to be created.
    values_list : {list, tuple, ndarray, Series}
        The values of the dicationary to be created.

    Returns
    -------
    dict_result : dict
        A dictionary with the values of first list as keys and values of 
        second list as dictionary values.
    
    Examples
    --------
    >>>

    """
    if keys_list is None:
        keys_list = [k for k in len(values_list)]
    keys_list = list(keys_list)
    values_list = list(values_list)
    df = DataFrame([keys_list, values_list], index = ['key', 'value']).T
    dict_result = df.set_index('key')['value'].to_dict()
    
    return dict_result

def dict_subset(dictionary, n=None, sub_from=0, sub_to=5) -> dict:
    """
    Returns a subset of a specified dictionary.

    Parameters
    ----------
    dictionary : Dict
        A dictionary that is to be subset.
    n : int, default=None
        Number of elements to subset.
    
    sub_from : int, default=0
        Starting point of the subset. Used when `n` is None, 
        otherwise it is diregarded.
    
    sub_to : int, default=5
        End point of the subset. Used when `n` is None, 
        otherwise it is diregarded.

    Returns
    -------
    dict_sub : Dict
        The subset of the dictionary.
    
    Examples
    --------
    >>>

    """
    if n is None:
        dict_sub = list(dictionary.keys())[sub_from:sub_to]
    else:
        if n > 0:
            dict_sub = list(dictionary.keys())[:n] # from left
        else:
            dict_sub = list(dictionary.keys())[n:] # from right
        
    dict_sub = {key_val: dictionary.get(key_val, None) for key_val in dict_sub}
    
    return dict_sub

def table_na(data, 
             to_ndarray=True, 
             convert_pd=True, 
             col_names=None, 
             na_label='', 
             decimals=8
):
    """
    Inserts a row with missing values in between two rows or an array.

    Parameters
    ----------
    data: {list, tuple, ndarray, Series}
        The values where we want to insert a row.
    to_ndarray: bool, default=True
        If True, result will be returned as a two dimensional list.
    convert_pd : bool, default=True
        If true, result will be converted to a Pandas DataFrame.
    col_names : {list, tuple, array, Series}, default=None
        Column names of the Pandas DataFrame. Only used when `convert_pd=True`.
    na_label : str, default=''
        The value to be used for the inserted blank rows. 
        Used when `convert_pd = True`.
    decimals : int, default=8
        Number of decimal points in the result.

    Returns
    -------
    result : {DataFrame, 2D Array}
        A DataFrame of a 2D array with the blank rows inserted.

    Examples
    --------
    >> m = [22, 23, 14, 49, 43]
    >> stm.table_na(data = m, to_ndarray = False)
             C1
        1  22.0
        2      
        3  23.0
        4      
        5  14.0
        6      
        7  49.0
        8      
        9  43.0
    >> stm.table_na(data = m, to_ndarray = False, na_label = '-')
             C1
        1  22.0
        2     -
        3  23.0
        4     -
        5  14.0
        6     -
        7  49.0
        8     -
        9  43.0
    >> M = [[28, 17, 16, 37, 46], [21, 39, 19, 29, 30]]
    >> stm.table_na(data = M, to_ndarray = True, 
                    na_label = '-', col_names = ['x', 'y'])
           x	   y
    1	28.0	21.0
    2	   -	   -
    3	17.0	39.0
    4	   -	   -
    5	16.0	19.0
    6	   -	   -
    7	37.0	29.0
    8	   -	   -
    9	46.0	30.0

    """
    L = []
    M = data
    # convert to numpy array just in case it is not
    if not isinstance(M, ndarray):
        try:
            M = array(M).T
            if M.shape[0] == 2 and M.shape[1] > 2:
                M = M.T
        except:
            raise NumpifyError(par_name='M')

    try:
        col_names_count = len(col_names)
    except:
        col_names_count = 0
        col_names = ''

    if col_names_count == 2 and M.shape[1] > 2:
        N = M[:, :2]
    # do not add na row if bc and x1 is in columns
    elif '$b$$c$' in ''.join(col_names) or '_two_columns_' in ''.join(col_names):
        N = M
    else:
        # if the data is not 2D, set array to False so that it uses a list
        try:
            row_count, col_count = M.shape # syntax will crush if it is 1D
        except:
            to_ndarray = False

        if to_ndarray:
            row_count, col_count = M.shape
            if row_count == 2 and col_count > 2:
                M = M.reshape(col_count, row_count)
            row_count, col_count = M.shape
            # row 1
            na = repeat(nan, len(M[:, 0]))
            for i in range(len(M[:, 0])):
                L.append(M[i, 0])
                L.append(na[i])
            L = L[:len(L)-1]
            M1 = array([L]).T
            # from row 2
            M = M[:, 1:]
            row_count, col_count = M.shape
            for i in range(row_count):
                for j in range(col_count):
                    if i < j:
                        M[i, j] = nan
            N = zeros((row_count * 2-1, col_count))
            for j in range(col_count):
                Mi = M[:, j]
                na = repeat(nan, len(Mi))
                L = []
                for i in range(len(Mi)):
                    L.append(Mi[i])
                    L.append(na[i])
                L = L[:len(L)-1]
                LNew = L[j:] + [nan] * j # shift values up
                N[:, j] = LNew
            N = hstack([M1, N])
        else:
            M = M.flatten()
            na = repeat(nan, len(M))
            L = []
            for i in range(len(M)):
                L.append(M[i])
                L.append(na[i])
            N = array([L[:len(L)-1]]).T
        
    result = N

    if convert_pd:
        set_option('display.precision', decimals)
        row_count, col_count = N.shape
        if col_names is None:
            col_names = [f'C{k+1}' for k in range(col_count)]
        
        df = round(result, decimals)
        results_table = array(df, dtype = float64)
        row_names = list(range(1, row_count+1))
        row_names = list(map(lambda x: str(x).replace('nan', ''), row_names))
        try:
            results_table = DataFrame(
                df, index = row_names, columns = col_names
            )
        except:
            results_table = DataFrame(
                df, 
                index = row_names, 
                columns = [f'C{n+1}' for n in range(df.shape[1])]
            )
        result = results_table.fillna(na_label)

    return result


def _val_boolean(user_input, default):
    """
    Validate boolean values. If invalid, then use the default.
    """
    if not isinstance(user_input, bool):
        return default
    return user_input

def to_listuple(array_values,
                includes_str=False,
                to_tuple=False,
                flatten_list=True,
                n=None,
                to_ndarray=False,
                label='exactly',
                par_name='array_values'
):
    """
    Convert an iterable to a list / tuple.
    """
    # array_values
    if not is_iterable(array_values, includes_str=includes_str):
        raise IterableError(
            par_name=par_name, 
            includes_str=includes_str, 
            user_input=array_values
        )
    
    if isinstance(array_values, str):
        array_values = [array_values]
    
    # includes_str, ..., flatten_list
    includes_str = _val_boolean(user_input=includes_str, default=False)
    to_tuple = _val_boolean(user_input=to_tuple, default=True)
    flatten_list = _val_boolean(user_input=flatten_list, default=True)
    to_ndarray = _val_boolean(user_input=to_ndarray, default=False)

    # convert to list/tuple
    try:
        if isinstance(array_values, set):
            array_values = list(set)
        if flatten_list is True:
            array_values = flatten(array_values)
        if to_tuple is True:
            array_values = tuple(array_values)
    except:
        listuple = 'list'
        if to_tuple is True:
            listuple = 'tuple'
        raise ValueError(f"Unable to convert '{par_name}' to a {listuple}")
    
    # check number of elements
    if n is not None:
        if not isinstance(n, int):
            raise IntegerError(par_name='n', user_input=n)
        if len(array_values) != n:
            raise VectorLengthError(
                par_name=par_name, 
                n=n, 
                label=label, 
                user_input=array_values
            )
    
    if to_ndarray:
        array_values = asarray(array_values)

    return array_values

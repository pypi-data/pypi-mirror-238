import calendar
from numpy.random import randint, seed
from numpy import repeat, linspace
from pandas import DataFrame, concat, read_csv
from ..statistical.wrangle import dframe_labels
from ..core.arraylike import is_iterable, abrange
from ..core.symbolic import lambdify_expr
from ..core.errors import InvalidError
from ..datasets import datasets_path

def colsnames(n, blank=False):
    """
    Assign column names to DataFrame.
    """
    if blank is True:
        return ['' for _ in range(n)]
    else:
        return [k+1 for k in range(n)]

def data_random(
        min=10, 
        max=100, 
        nrows=10, 
        ncols=5, 
        col_names=None, 
        index_names=None, 
        rand_seed=None
):
    """
    Generate random data sets.
    """
    try:
        seed(rand_seed)
    except:
        pass
    M = randint(low=min, high=max, size=(nrows, ncols))
    if col_names is None:
        col_names = [f'Col{index}' for index in range(M.shape[1])]
    if isinstance(col_names, str):
        col_names = list(col_names)
    dframe = DataFrame(M)
    # column names
    try:
        dframe.columns = col_names
    except:
        col_names = dframe_labels(dframe=M, col_latex=False, prefix='Col')
        dframe.columns = col_names
    # row names
    try:
        dframe.index = index_names
    except:
        index_names = [f'R{index}' for index in range(1, M.shape[0]+1)]
        dframe.index = index_names

    return dframe

def dataset_random(nrows=10, rand_seed=None, **kwargs):
    """
    Generate a (random) dataset from given columns.

    Parameters
    ----------

    Returns
    -------

    Examples
    --------

    """
    try:
        seed(rand_seed)
    except:
        seed(8765)

    columns_ = kwargs
    if len(columns_) == 0:
        raise ValueError("Specify at least one column to be generated")
    data = DataFrame([])
    for k, v in columns_.items():
        if is_iterable(v):
            M = randint(low=min(v), high=max(v)+1, size=(nrows, 1))
        elif isinstance(v, dict):
            M = repeat(list(v.keys()), list(v.values()))
        elif isinstance(v, int):
            M = randint(low=1, high=abs(v)+1, size=(nrows, 1))
        else:
            raise InvalidError(par_name=k, user_input=v)
        M = DataFrame(M, columns=[k])
        # reshaffle the values, particularly userful for replicate
        M.index = randint(
            low=1, high=M.shape[0] * 10000, size=(1, M.shape[0])
        ).flatten()
        M = M.sort_index()
        M.index = range(M.shape[0])
        data = concat([data, M], axis=1)

    return data

def _data_sales(a=2015, b=2023):

    seed(1234)
    data = randint(low=1000, high=6000, size=(8, 12))
    df_sales = DataFrame(
        data=data,
        index=range(a, b),
        columns = list(calendar.month_abbr)[1:]
    )

    return df_sales

def _data_survey1():

    values = randint(low=12, high=80, size=(10, 4))
    gender = repeat(['Female', 'Male'], [6, 4])
    values = DataFrame(values, columns=['A', 'B', 'C', 'D'])
    gender = DataFrame(gender, columns=['Gender'])
    data = concat([values, gender], axis=1)

    return data

def _data_simpson38(decimals=8):

    x = linspace(0, 1, 9)
    f = lambdify_expr(f='x^2 * exp(-x)', par_name='f')
    data = DataFrame([x, f(x)], index=['x', 'y'], columns=colsnames(len(x)))
    data = data.T.round(decimals)
    
    return data

def _data_boole(decimals=8):

    x = abrange(0, 1.6, .2)
    f = lambdify_expr(f='exp(3 * x) * sin(2 * x)', par_name='f')
    data = DataFrame([x, f(x)], index=['x', 'y'], columns=colsnames(len(x)))
    data = data.T.round(decimals)
    
    return data


def _data_weddle(decimals=8):

    x = linspace(0, .35, 11)
    f = lambdify_expr(f='x * log(x + 1)', par_name='f')
    data = DataFrame([x, f(x)], index=['x', 'y'], columns=colsnames(len(x)))
    data = data.T.round(decimals)
    
    return data

def _income_wide():

    values = [
        [3,75000,76000,77000],
        [1,40000,40500,41000],
        [2,45000,45400,45800]
    ]

    dframe = DataFrame(
        data=values, 
        columns=['id', 'income96', 'income97','income98']
    )

    return dframe

def _income_long():
    values = [
        [1,96,40000],
        [1,97,40500],
        [1,98,41000],
        [2,96,45000],
        [2,97,45400],
        [2,98,45800],
        [3,96,75000],
        [3,97,76000],
        [3,98,77000]
    ]
    dframe = DataFrame(
        data=values, 
        columns=['id', 'year', 'income']
    )

    return dframe

def _kids_wide():

    values = [
        [1,1,2.8,3.4,19,28],
        [1,2,2.9,3.8,21,28],
        [1,3,2.2,2.9,20,23],
        [2,1,2.0,3.2,25,30],
        [2,2,1.8,2.8,20,33],
        [2,3,1.9,2.4,22,33],
        [3,1,2.2,3.3,22,28],
        [3,2,2.3,3.4,20,30],
        [3,3,2.1,2.9,22,31],
    ]
    dframe = DataFrame(
        data=values, 
        columns=[
            'id', 'birth', 'height1', 'height2', 'weight1', 'weight2'
        ]
    )

    return dframe

def _kids_long():
    values = [
        [1,1,1,2.8,19],
        [1,1,2,3.4,28],
        [1,2,1,2.9,21],
        [1,2,2,3.8,28],
        [1,3,1,2.2,20],
        [1,3,2,2.9,23],
        [2,1,1,2.0,25],
        [2,1,2,3.2,30],
        [2,2,1,1.8,20],
        [2,2,2,2.8,33],
        [2,3,1,1.9,22],
        [2,3,2,2.4,33],
        [3,1,1,2.2,22],
        [3,1,2,3.3,28],
        [3,2,1,2.3,20],
        [3,2,2,3.4,30],
        [3,3,1,2.1,22],
        [3,3,2,2.9,31]
    ]
    dframe = DataFrame(
        data=values, 
        columns=['id', 'birth', 'age', 'height', 'weight']
    )

    return dframe

def datasets(id=None):
    """
    Return a dataset.

    Parameter
    ---------
    name : {None, str, int}, default=None
        The name of the dataset.

    Returns
    -------
    df : DataFrame
        The dataset.

    """
    if id == 'sales':
        dframe = _data_sales()
    elif id == 'survey1':
        dframe = _data_survey1()
    elif id == 'simpson38':
        dframe = _data_simpson38()
    elif id == 'boole':
        dframe = _data_boole()
    elif id == 'weddle':
        dframe = _data_weddle()
    elif id == 'income_wide':
        dframe = _income_wide()
    elif id == 'income_long':
        dframe = _income_long()
    elif id == 'kids_wide':
        dframe = _kids_wide()
    elif id == 'kids_long':
        dframe = _kids_long()
    elif id == 'cotes_n8':
        dframe = read_csv(f'{datasets_path()}/csv/cotes_n8.csv')
    else:
        raise InvalidError(par_name='id', user_input=id)

    return dframe

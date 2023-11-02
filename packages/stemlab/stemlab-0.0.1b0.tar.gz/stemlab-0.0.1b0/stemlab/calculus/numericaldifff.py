from pandas import DataFrame
from sympy import Float, sympify
from numpy import nan, float64, ones, round
from ..core.symbolic import lambdify_expr
from ..core.options import display_options
from ..statistical.wrangle import dframe_labels
from ..core.validate import val_decimals, val_numeric, val_boolean
from ..core.htmlatex import dframe_color

methods2 = [
    'Two point backward',
    'Two point forward',
    'Two point centered',
    'Three point backward',
    'Three point forward',
    'Three point midpoint',
    'Three point endpoint',
    'Four point centered',
    'Five point midpoint',
    'Five point endpoint'
]
methods3 = [
    'Three point backward',
    'Three point forward',
    'Three point centered',
    'Four point backward',
    'Four point forward',
    'Five point centered'
]
methods4 = [
    'Four point backward',
    'Four point forward',
    'Four point centered',
    'Five point backward',
    'Five point forward',
    'Six point centered'
]
methods5 = [
    'Five point backward',
    'Five point forward',
    'Five point centered',
    'Six point backward',
    'Six point forward',
    'Seven point centered'
]


def diff_richardson(
        f, x, n=3, h=0.01, col_latex=True, index_labels='default', decimals=12
) -> tuple[DataFrame, Float]:
    """
    ```

    Approximates the first derivative f'(x) at at the point x = x0.  

    Parameters
    ----------
    f : {symbolic, str}
        Expression whose derivative of we seek.
    x : {int, float}
        The value of x at which to find the derivative.
    n : int, default=3
        Number of levels of extrapolation.
    h : {int, float}, default=0.01
        Initial stepsize.
    col_latex : bool, default=True
        If True, column headings will be printed in Latex.
    index_labels : {default, int, array_like, None}, default='default'
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        default ........... System default, or 0, 1, 2, ...
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels     
        ==============================================================
    to_dict : bool, default=False
        If True, return result as a dictionary, otherwise, return a tuple
    decimals : int, default=True
        Number of decimal points.
    
    Returns
    -------
    N : ndarray
        A Numpy array with the values.
    df : DataFrame
        A table used for the calculations.
    result : Float
        The result of integration.

    Examples
    --------
    >> f = '2**x * sin(x)'
    >> x = 1.05
    >> h = 0.4
    >> n = 4
    >> table, result = stm.diff_richardson(f, x, n, h, col_latex=False, index_labels='default', decimals=10)
    >> table
                R1             R2             R3             R4             R5
    -19.4717610403                                                            
    -19.6062230456  -19.651043714                                             
    -19.6368541355 -19.6470644989 -19.6467992179                              
    -19.6443229991 -19.6468126202 -19.6467958283 -19.6467957745               
    -19.6461783707 -19.6467968279 -19.6467957751 -19.6467957743 -19.6467957743
    >> result
    2.2751458417
    
    >> f = '(3/7) * x + exp(x)'
    >> x = 0.0
    >> h = 0.45
    >> n = 4
    >> table, result = stm.diff_richardson(f, x, n, h, col_latex=False, index_labels='default', decimals=10)
    >> table
              R1            R2            R3            R4            R5
    1.4626647995                                                        
    1.4370303118  1.4284854825                                          
    1.4306821388  1.4285660812  1.4285714544                            
    1.4290988558  1.4285710947   1.428571429  1.4285714286              
    1.4287032697  1.4285714077  1.4285714286  1.4285714286  1.4285714286
    >> result
    1.4285714286

    >> f = 'x**3 * cos(x)'
    >> x = 2.3
    >> h = 0.4
    >> n = 4
    >> table, result = stm.diff_richardson(f, x, n, h, col_latex=False, index_labels='default', decimals=10)
    >> table
                R1             R2             R3             R4             R5
    -19.4717610403                                                            
    -19.6062230456  -19.651043714                                             
    -19.6368541355 -19.6470644989 -19.6467992179                              
    -19.6443229991 -19.6468126202 -19.6467958283 -19.6467957745               
    -19.6461783707 -19.6467968279 -19.6467957751 -19.6467957743 -19.6467957743
    >> result
    -19.6467957743
    ```
    """
    display_options()
    f = lambdify_expr(f, univariate=True, par_name='f')
    x = val_numeric(user_input=x, par_name='x')
    x = val_numeric(
        user_input=n, limits=[1, 25], boundary='inclusive', par_name='n'
    )
    h = val_numeric(user_input=h, par_name='h')
    col_latex = val_boolean(user_input=col_latex, default=True)
    if index_labels is None:
        index_labels = 'default'
    decimals = val_decimals(decimals=decimals)

    # begin calculations
    N = nan * ones((n+1, n+1), dtype = float64)
    for i in range(n+1):
        N[i,0] = 0.5 * (f(x+h) - f(x-h)) / h
        p4powerj = 1
        for j in range(1, i+1):
            p4powerj = 4 * p4powerj
            N[i, j] = N[i, j-1] + (N[i, j-1] - N[i-1, j-1]) / (p4powerj - 1)
        h = 0.5 * h
    ncols = N.shape[1]
    if col_latex is True:
        col_names = ['\(R_{(m, \, %s)}\)' %(k+1) for k in range(ncols)]
        row_names = ['\(\\frac{h}{%s}\)' %(2 ** k) for k in range(ncols)]
    else:
        col_names = ['R%s' %(k+1) for k in range(ncols)]
        row_names = ['h/%s' %(2 ** k) for k in range(ncols)]
    N = round(N, decimals)
    dframe = DataFrame(N, columns = col_names).fillna('')
    if index_labels == 'default':
        dframe.index = dframe_labels(dframe=dframe, df_labels=row_names)
    else:
        dframe.index = dframe_labels(dframe=dframe, df_labels=index_labels)
    nrows, ncols = dframe.shape
    dframe = dframe_color(
        dframe=dframe,
        style_indices=[[nrows-1], [ncols-1]],
        values=[],
        operator='',
        rows=[],
        cols=[],
        css_styles='color:blue;font-weight:bold;',
        decimals=decimals,
    )
    result = sympify(N[-1, -1])

    return dframe, result
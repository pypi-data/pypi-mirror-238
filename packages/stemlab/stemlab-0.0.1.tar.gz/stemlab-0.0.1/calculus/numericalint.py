from numpy import (
    ones, float64, nan, round, append, array, linspace, dot, vstack,
    asfarray
)
from scipy.special import roots_legendre
from pandas import DataFrame
from sympy import sympify, Float
from ..core.errors import (
    NumericBtwnError, LowerGEUpperError, IntervalError, LengthDifferError, 
    DifferenceError
)
from ..core.htmlatex import dframe_color
from ..core.symbolic import lambdify_expr
from ..core.arraylike import (
    is_len_equal, is_diff_constant, to_listuple, abrange
)
from ..statistical.wrangle import insert, dframe_labels
from ..statistical.dataframes import column_latex
from ..core.options import display_options
from ..core.validate import val_numeric, val_boolean, val_decimals

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.nquad.html#scipy.integrate.nquad
# https://docs.scipy.org/doc/scipy/reference/integrate.html

def int_cotes(
        f,
        a, 
        b, 
        points=2,
        closed=True,
        style_indices=True,
        col_latex=True, 
        index_labels=1,
        to_dict=False,
        decimals=12
):
    """
    ```

    Integration using Newton cotes methods.

    Parameters
    ----------
    f : {symbolic, str}
        The function to be integrated.
    a : {int, float}
        Lower limit of integration.
    b : {int, float}
        Upper limit of integration.
    points : int, default=2
        Number of points.
    closed : bool, default=True
        If True, then open methods, otherwise closed methods.
    style_indices : bool, True
        If True, a Styler will be returned with some values coloured, 
        otherwise a DataFrame will be returned with no colouring.
    index_labels : {default, int, array_like}, default='default'
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        default ........... System default, or 0, 1, 2, ...
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels
        ==============================================================
    col_latex : bool, default=True
        If True, column headings will be printed in Latex.
    to_dict : bool, default=False
        If True, results will be returned as a dictionary, otherwise it  
        returns a tuple
    decimals : int, default=12
        Number of decimal points.

    Returns
    -------
    dframe : DataFrame Styler
        A DataFrame Styler with used for calculations.
    result
        The approximated area.

    Examples
    --------
    ## Newton-Cotes closed methods
    ## ---------------------------
    >> result_table = []
    >> for n in range(2, 12):
        result = stm.int_cotes(
            f='sin(x)',
            a=0, 
            b=np.pi/4, 
            points=n,
            closed=True, 
            col_latex=True, 
            index_labels=None,
            to_dict=False,
            decimals=12
        )
        display(result[0])
        display(result[1])
        result_table.append([n, result[1]]) 
    >> result_table = pd.DataFrame(result_table, columns=['n', 'area'])
    >> result_table
        n               area
    0   2  0.277680183635000
    1   3  0.292932637840000
    2   4  0.292910702549000
    3   5  0.292893182561000
    4   6  0.292893198409000
    5   7  0.292893218841000
    6   8  0.292893218830000
    7   9  0.292893218813000
    8  10  0.292960243992000
    9  11  0.292893218813000

    ## Newton-Cotes open methods
    ## -------------------------
    >> result_table = []
        for n in range(1, 8):
            result = stm.int_cotes(
                f='sin(x)',
                a=0, 
                b=np.pi/4, 
                points=n,
                closed=False, 
                col_latex=True, 
                index_labels=None,
                to_dict=False,
                decimals=12
            )
            display(result[0])
            display(result[1])
            result_table.append([n, result[1]]) 
    >> result_table = pd.DataFrame(result_table, columns=['n', 'area'])
    >> result_table
       n               area
    0  1  0.300558864942000
    1  2  0.297987542187000
    2  3  0.292858659193000
    3  4  0.292869228136000
    4  5  0.292893292327000
    5  6  0.292893270705000
    6  7  0.292893218723000
    ```
    """
    display_options()
    f = lambdify_expr(f, univariate=True, par_name='f')
    a = val_numeric(user_input=a, par_name='a')
    b = val_numeric(user_input=b, par_name='b')
    if a >= b:
        raise LowerGEUpperError(a='a', b='b')
    closed = val_boolean(user_input=closed, default=True)
    if closed is True:
        minn, maxn = 2, 11
    else:
        minn, maxn = 1, 7
    points = val_numeric(
        user_input=points, 
        to_float=False, 
        limits=[minn, maxn], 
        boundary='inclusive', 
        par_name='points'
    )
    col_latex = val_boolean(user_input=col_latex, default=True)
    if closed is True:
        n = points - 1
        start_row, stop_row = 0, n+1
    else:
        n = points + 1
        start_row, stop_row = 1, n
    h = (b - a)/n
    x = abrange(a, b, h)

    # style_indices
    style_indices = val_boolean(user_input=style_indices, default=True)
    # to_dict
    to_dict = val_boolean(user_input=to_dict, default=False)
    # decimals
    decimals = val_decimals(decimals=decimals)
    
    # https://archive.lib.msu.edu/crcmath/math/math/n/n080.htm
    if closed is True: # Newton-Cotes closed
        if points == 2:
            coefs = [1, 1]
            result = h/2 * dot(f(x), coefs)
        elif points == 3:
            coefs = [1, 4, 1]
            result = h/3 * dot(f(x), coefs)
        elif points == 4:
            coefs = [1, 3]
            coefs = coefs + coefs[::-1]
            result = (3*h/8) * dot(f(x), coefs)
        elif points == 5:
            coefs = [7, 32, 12]
            coefs = coefs + coefs[:-1][::-1]
            result = (2*h/45) * dot(f(x), coefs)
        elif points == 6:
            coefs = [19, 75, 50]
            coefs = coefs + coefs[::-1]
            result = (5*h/288) * dot(f(x), coefs)
        elif points == 7:
            coefs = [41, 216, 27, 272]
            coefs = coefs + coefs[:-1][::-1]
            result = (h/140) * dot(f(x), coefs)
        elif points == 8:
            coefs = [751, 3577, 1323, 2989]
            coefs = coefs + coefs[::-1]
            result = (7*h/17280) * dot(f(x), coefs)
        elif points == 9: ## xxxx CHECK THIS 
            coefs = [989, 5888, -928, 10496, -4540]
            coefs = coefs + coefs[:-1][::-1]
            result = (4*h/14175) * dot(f(x), coefs)
        elif points == 10:
            coefs = [2857, 15741, 1080, 19344, 5788]
            coefs = coefs + coefs[::-1]
            result = (9*h/89600) * dot(f(x), coefs)
        elif points == 11:
            coefs = [16067, 106300, -48525, 272400, -260550, 427368]
            coefs = coefs + coefs[:-1][::-1]
            result = (5*h/299376) * dot(f(x), coefs)
    else: # Newton-Cotes open
        if points == 1:
            coefs = [1]
            result = 2*h * f(x[1])
        elif points == 2:
            coefs = [1, 1]
            result = 3*h/2 * dot(f(x[1:-1]), coefs)
        elif points == 3:
            coefs = [2, -1, 2]
            result = 4*h/3 * dot(f(x[1:-1]), coefs)
        elif points == 4:
            coefs = [11, 1, 1, 11]
            result = 5*h/24 * dot(f(x[1:-1]), coefs)
        elif points == 5:
            coefs = [11, -14, 26, -14, 11]
            result = 6*h/20 * dot(f(x[1:-1]), coefs)
        elif points == 6:
            coefs = [611, -453, 562, 562, -453, 611]
            result = 7/1440*h * dot(f(x[1:-1]), coefs)
        elif points == 7:
            coefs = [460, - 954, 2196, -2459]
            coefs = coefs + coefs[:-1][::-1]
            result = 8/945*h * dot(f(x[1:-1]), coefs)
        coefs = [nan] + coefs + [nan]
    N = vstack([x, coefs, f(x), asfarray(coefs) * f(x)]).T
    col_labels = dframe_labels(
        dframe=N, 
        df_labels=['x', 'k', 'f(x)', 'k f(x)'], 
        col_latex=col_latex, 
        prefix=None, 
        index=False
    )
    if index_labels is None:
        index_labels = 1
    index_labels = dframe_labels(dframe=N, df_labels=index_labels, index=True)
    dframe = DataFrame(N, index=index_labels, columns=col_labels)
    dframe = dframe.round(decimals)#.fillna('-')
    result = sympify(round(result, decimals))
    print(N[:, [0, 2]].tolist())
    # color
    if style_indices is True:
        rows_indices = list(range(start_row, stop_row))
        cols_indices = [3] * (len(rows_indices))
        dframe = dframe_color(
            dframe=dframe,
            style_indices=[rows_indices, cols_indices],
            values=[],
            operator='',
            rows=[],
            cols=[],
            css_styles='color:blue;',
            decimals=decimals,
        )

    result = {'result_table': dframe, 'area': result}
    if to_dict is False:
        result = tuple(result.values())

    return result

def int_cotes_data(
        x,
        y,
        points=8,
        closed=True,
        col_latex=True,
        index_labels=1,
        style_indices=True,
        to_dict=False,
        decimals=12
):
    """
    ```

    Integration using Newton cotes methods.

    Parameters
    ----------
    x : array_like, default=None
        The points corresponding to the ``y`` values.
    y : array_like
        The points to be integrated, synonymous to f(x).
    points : int, default=8
        Number of points.
    closed : bool, default=True
        If True, then open methods, otherwise closed methods.
    style_indices : bool, True
        If True, a Styler will be returned with some values coloured, 
        otherwise a DataFrame will be returned with no colouring.
    index_labels : {default, int, array_like}, default='default'
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        default ........... System default, or 0, 1, 2, ...
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels
        ==============================================================
    col_latex : bool, default=True
        If True, column headings will be printed in Latex.
    to_dict : bool, default=False
        If True, results will be returned as a dictionary, otherwise it  
        returns a tuple
    decimals : int, default=12
        Number of decimal points.

    Returns
    -------
    dframe : DataFrame Styler
        A DataFrame Styler with used for calculations.
    result
        The approximated area.

    Examples
    --------
    >> import stemlab as stm
    >> df = stm.datasets(id='cotes_n8')
    >> x = df['x'].values
    >> y = df['y'].values
    >> table, result = stm.int_cotes_data(x, y, points=8)
    >> table
            $x$     $k$      $f(x)$             $k f(x)$
    1  0.00000000   751.0  0.20000000   150.19999999999999
    2  0.11428571  3577.0  1.30674076  4674.21169852000003
    3  0.22857143  1323.0  1.31892807  1744.94183661000011
    4  0.34285714  2989.0  1.92454430  5752.46291269999983
    5  0.45714286  2989.0  2.99838448  8962.17121072000009
    6  0.57142857  1323.0  3.53789492  4680.63497915999960
    7  0.68571429  3577.0  2.59901184  9296.66535168000155
    8  0.80000000   751.0  0.23200000   174.23200000000000
    >> result
    1.640533271322
    ```
    """
    display_options()
    x = to_listuple(array_values=x, to_ndarray=True, par_name='x')
    y = to_listuple(array_values=y, to_ndarray=True, par_name='y')
    if not is_len_equal(x, y):
        raise LengthDifferError(par_name='x, y', user_input=[x, y])
    if not is_diff_constant(x):
        raise DifferenceError(par_name='x', user_input=x)
    n = len(x)
    h = x[1] - x[0]
    col_latex = val_boolean(user_input=col_latex, default=True)
    closed = val_boolean(user_input=closed, default=True)
    if closed is True:
        minn, maxn = 2, 11
    else:
        minn, maxn = 1, 7
    points = val_numeric(
        user_input=points, 
        to_float=False, 
        limits=[minn, maxn], 
        boundary='inclusive', 
        par_name='points'
    )
    col_latex = val_boolean(user_input=col_latex, default=True)
    if closed is True:
        n = points - 1
        start_row, stop_row = 0, n+1
    else:
        n = points + 1
        start_row, stop_row = 1, n
    h = x[1] - x[0]
    # style_indices
    style_indices = val_boolean(user_input=style_indices, default=True)
    # to_dict
    to_dict = val_boolean(user_input=to_dict, default=False)
    # decimals
    decimals = val_decimals(decimals=decimals)
    
    # https://archive.lib.msu.edu/crcmath/math/math/n/n080.htm
    if closed is True: # Newton-Cotes closed
        if points == 2:
            coefs = [1, 1]
            result = h/2 * dot(y, coefs)
        elif points == 3:
            coefs = [1, 4, 1]
            result = h/3 * dot(y, coefs)
        elif points == 4:
            coefs = [1, 3]
            coefs = coefs + coefs[::-1]
            result = (3*h/8) * dot(y, coefs)
        elif points == 5:
            coefs = [7, 32, 12]
            coefs = coefs + coefs[:-1][::-1]
            result = (2*h/45) * dot(y, coefs)
        elif points == 6:
            coefs = [19, 75, 50]
            coefs = coefs + coefs[::-1]
            result = (5*h/288) * dot(y, coefs)
        elif points == 7:
            coefs = [41, 216, 27, 272]
            coefs = coefs + coefs[:-1][::-1]
            result = (h/140) * dot(y, coefs)
        elif points == 8:
            coefs = [751, 3577, 1323, 2989]
            coefs = coefs + coefs[::-1]
            result = (7*h/17280) * dot(y, coefs)
        elif points == 9: ## xxxx CHECK THIS 
            coefs = [989, 5888, -928, 10496, -4540]
            coefs = coefs + coefs[:-1][::-1]
            result = (4*h/14175) * dot(y, coefs)
        elif points == 10:
            coefs = [2857, 15741, 1080, 19344, 5788]
            coefs = coefs + coefs[::-1]
            result = (9*h/89600) * dot(y, coefs)
        elif points == 11:
            coefs = [16067, 106300, -48525, 272400, -260550, 427368]
            coefs = coefs + coefs[:-1][::-1]
            result = (5*h/299376) * dot(y, coefs)
    else: # Newton-Cotes open
        if points == 1:
            coefs = [1]
            result = 2*h * y[0]
        elif points == 2:
            coefs = [1, 1]
            result = 3*h/2 * dot(y[1:-1], coefs)
        elif points == 3:
            coefs = [2, -1, 2]
            result = 4*h/3 * dot(y[1:-1], coefs)
        elif points == 4:
            coefs = [11, 1, 1, 11]
            result = 5*h/24 * dot(y[1:-1], coefs)
        elif points == 5:
            coefs = [11, -14, 26, -14, 11]
            result = 6*h/20 * dot(y[1:-1], coefs)
        elif points == 6:
            coefs = [611, -453, 562, 562, -453, 611]
            result = 7/1440*h * dot(y[1:-1], coefs)
        elif points == 7:
            coefs = [460, - 954, 2196, -2459]
            coefs = coefs + coefs[:-1][::-1]
            result = 8/945*h * dot(y[1:-1], coefs)
        coefs = [nan] + coefs + [nan]
    N = vstack([x, coefs, y, asfarray(coefs) * y]).T
    col_labels = dframe_labels(
        dframe=N, 
        df_labels=['x', 'k', 'f(x)', 'k f(x)'], 
        col_latex=col_latex, 
        prefix=None, 
        index=False
    )
    if index_labels is None:
        index_labels = 1
    index_labels = dframe_labels(dframe=N, df_labels=index_labels, index=True)
    dframe = DataFrame(N, index=index_labels, columns=col_labels)
    dframe = dframe.round(decimals)#.fillna('-')
    result = sympify(round(result, decimals))

    # color
    if style_indices is True:
        rows_indices = list(range(start_row, stop_row))
        cols_indices = [3] * (len(rows_indices))
        dframe = dframe_color(
            dframe=dframe,
            style_indices=[rows_indices, cols_indices],
            values=[],
            operator='',
            rows=[],
            cols=[],
            css_styles='color:blue;',
            decimals=decimals,
        )

    result = {'result_table': dframe, 'area': result}
    if to_dict is False:
        result = tuple(result.values())

    return result

def int_composite(
        f, 
        a, 
        b, 
        n=None, 
        h=None, 
        method='trapezoidal', 
        col_latex=True, 
        index_labels=None, 
        decimals=12
) -> tuple[DataFrame, Float]:
    """
    ```

    Composite integration given a function.
    
    Parameters
    ----------
    f : {str, symbolic}
        The univariate function to be integrated.
    a : {int, float}
        Lower limit of integration.
    b : {int, float}
        Upper limit of integration.
    n : int, default=None
        Number of points.
    h : {int, float}, default=None
        Stepsize (interval) if ``n=None``. 
    method: {...}, default='trapezoidal'
        The integration method to be applied.
        ==========================================
        Argument        Description
        ==========================================
        trapezoidal     Composite Trapezoidal rule
        simpson13       Composite Simpson 1/3 rule
        simpson38       Composite Simpson 3/8 rule
        boole           Boole's rule
        weddle          Weddle's rule
        ==========================================
    col_latex : bool, default=True
        If True, table headings will be displayed in Latex.
    index_labels : {default, int, array_like, None}, default='default'
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        default ........... System default, or 0, 1, 2, ...
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels
        None .............. Will remove the DataFrame index       
        ==============================================================
    decimals : int, default=12
        Number of decimal points.
    
    Returns
    -------
    df : DataFrame
        A table used for the calculations.
    result : Float
        The result of integration.

    Examples
    --------
    >> f = 'sqrt(x^2 + log(x))'
    >> a, b, n = (1, 1.5, 5)
    >> table, result = stm.int_composite(f, a, b, n, method='trapezoidal', index_labels=None, decimals=12)
    >> table
    $x$          $f(x)$  $k$        $k f(x)$
    1.0  1.000000000000  1.0  1.000000000000
    1.1  1.142501719826  2.0  2.285003439651
    1.2  1.273703873274  2.0  2.547407746549
    1.3  1.397270290412  2.0  2.794540580824
    1.4  1.515411573343  2.0  3.030823146686
    1.5  1.629559789670  1.0  1.629559789670
    >> result
    0.664366735169

    >> f = '(2 * x) / (x^2 - 4)'
    >> a, b, n = (1, 1.6, 8)
    >> table, result = stm.int_composite(f, a, b, n, method='simpson13', index_labels=None, decimals=12)
    >> table
      $x$          $f(x)$  $k$        $k f(x)$
    1.000 -0.666666666667  1.0 -0.666666666667
    1.075 -0.755877829049  4.0 -3.023511316194
    1.150 -0.859010270775  2.0 -1.718020541550
    1.225 -0.980245061265  4.0 -3.920980245061
    1.300 -1.125541125541  2.0 -2.251082251082
    1.375 -1.303703703704  4.0 -5.214814814815
    1.450 -1.528326745718  2.0 -3.056653491436
    1.525 -1.821575214632  4.0 -7.286300858529
    1.600 -2.222222222222  1.0 -2.222222222222
    >> result
    -0.734006310189

    >> f = 'x^2 * exp(-x)'
    >> a, b, n = (0, 1, 8)
    >> table, result = stm.int_composite(f, a, b, n, method='simpson38', index_labels=None, decimals=12)
    >> table
      $x$          $f(x)$  $k$        $k f(x)$
    0.000  0.000000000000  1.0  0.000000000000
    0.125  0.013789014103  3.0  0.041367042309
    0.250  0.048675048942  3.0  0.146025146826
    0.375  0.096650054830  2.0  0.193300109660
    0.500  0.151632664928  3.0  0.454897994784
    0.625  0.209086495515  3.0  0.627259486546
    0.750  0.265706185917  2.0  0.531412371834
    0.875  0.319159983816  3.0  0.957479951449
    1.000  0.367879441171  1.0  0.367879441171
    >> result
    0.155607259902

    >> f = 'exp(3 * x) * sin(2 * x)'
    >> a, b, h = (0, 1.6, .2)
    >> table, result = stm.int_composite(f, a, b, h, method='boole', index_labels=None, decimals=12)
    >> table
    $x$           $f(x)$   $k$          $k f(x)$
    0.0   0.000000000000   7.0    0.000000000000
    0.2   0.709566482737  32.0   22.706127447600
    0.4   2.381706097024  12.0   28.580473164284
    0.6   5.638507893155  32.0  180.432252580973
    0.8  11.018476131760  14.0  154.258665844639
    1.0  18.263727040667  32.0  584.439265301336
    1.2  24.720759839883  12.0  296.649118078601
    1.4  22.339130676084  32.0  714.852181634682
    1.6  -7.093066540184   7.0  -49.651465781286
    result
    17.175703273518

    >> f = 'x * log(x + 1)'
    >> a, b, n = (0, .35, 10)
    >> table, result = stm.int_composite(f, a, b, n, method='weddle', index_labels=None, decimals=12)
    >> table
      $x$          $f(x)$  $k$        $k f(x)$
    0.000  0.000000000000  1.0  0.000000000000
    0.035  0.001204049935  5.0  0.006020249676
    0.070  0.004736105393  1.0  0.004736105393
    0.105  0.010483760172  6.0  0.062902561031
    0.140  0.018343956737  1.0  0.018343956737
    0.175  0.028221925829  5.0  0.141109629147
    0.210  0.040030275518  1.0  0.040030275518
    0.245  0.053688204830  5.0  0.268441024148
    0.280  0.069120821821  1.0  0.069120821821
    0.315  0.086258549673  6.0  0.517551298040
    0.350  0.105036607358  1.0  0.105036607358
    >> result
    0.012949571553
    ```
    """
    display_options()
    f = lambdify_expr(f, univariate=True, par_name='f')
    a = val_numeric(user_input=a, par_name='a')
    b = val_numeric(user_input=b, par_name='b')
    if a >= b:
        raise LowerGEUpperError(a='a', b='b')
    
    if n is None and h is None:
        n = 5
    
    if n is not None and h is not None:
        raise ValueError("Provide 'n' or 'h', not both")

    if n is None:
        h = val_numeric(user_input=h, par_name='h')
        if h >= abs(b - a):
            raise IntervalError(par_name='h', gte=True)
        n = int((b - a) / h)
    else:
        n = val_numeric(user_input=n, to_float=False, par_name='n')
        h = (b - a) / n

    col_latex = val_boolean(user_input=col_latex, default=True)
    decimals = val_decimals(decimals=decimals)
    k1 = 1
    if method == 'boole':
        k1 = 7
    
    N = array([[a, f(a), k1, k1 * f(a)]], dtype=float64)

    # call each of the integration methods
    if method == 'trapezoidal':
        N, result = _trapezoidal(N, f, a, b, n, h, decimals)
    elif method == 'simpson13':
        N, result = _simpson13(N, f, a, b, n, h, decimals)
    elif method == 'simpson38':
        N, result = _simpson38(N, f, a, b, n, h, decimals)
    elif method == 'boole':
        N, result = _boole(N, f, a, b, n, h, decimals)
    elif method == 'weddle':
        N, result = _weddle(N, f, a, b, n, h, decimals)
    else:
        methods = "'trapezoidal', 'simpson13', 'simpson38', 'boole', 'weddle'"
        raise ValueError(f"'method' must be one of {methods}")

    N = append(N, [[b, f(b), k1, k1 * f(b)]], axis=0)
    col_labels = dframe_labels(
        dframe=N,
        df_labels=['x', 'f(x)', 'k', 'k f(x)'],
        col_latex=col_latex,
        prefix=None,
        index=False
    )
    index_labels = dframe_labels(
        dframe=N, df_labels=index_labels, index=True
    )
    dframe = DataFrame(N, index=index_labels, columns=col_labels)
    dframe = dframe.round(decimals).fillna('-')

    return dframe, sympify(result)

def _trapezoidal(N, f, a, b, n, h, decimals):
    """
    Trapezoidal's rule integration given a function and limits of integration.
    """
    x = a
    sum_inner = 0
    for _ in range(1, n):
        x += h
        k = 2
        kfx = k * f(x)
        sum_inner += kfx
        N = append(N, [[x, f(x), k, kfx]], axis=0)
    result = round(0.5 * h * (f(a) + sum_inner + f(b)), decimals)

    return N, result

def _simpson13(N, f, a, b, n, h, decimals):
    """
    Simpson's 1/3 rule integration given a function and limits of integration.
    """
    x = a
    sum_inner = 0
    for m in range(1, n):
        x += h
        if m % 2 == 0:
            k = 2
            kfx = k * f(x)
        else:
            k = 4
            kfx = k * f(x)
        sum_inner += kfx
        N = append(N, [[x, f(x), k, kfx]], axis=0)
    result = round((h/3) * (f(a) + sum_inner + f(b)), decimals)

    return N, result

def _simpson38(N, f, a, b, n, h, decimals):
    """
    Simpson's 3/8 rule integration given a function and limits of integration.
    """
    x = a
    sum_inner = 0
    for m in range(1, n):
        x += h
        if m % 3 == 0:
            k = 2
            kfx = k * f(x)
        else:
            k = 3
            kfx = k * f(x)
        sum_inner += kfx
        N = append(N, [[x, f(x), k, kfx]], axis=0)
    result = round((3/8 * h) * (f(a) + sum_inner + f(b)), decimals)

    return N, result

def _boole(N, f, a, b, n, h, decimals):
    """
    Boole's rule integration given a function and limits of integration.
    """
    x = a
    sum_inner = 0
    for m in range(1, n):
        x += h
        if m % 2 == 1:
            k = 32
            kfx = k * f(x)
        elif m % 4 == 0:
            k = 14
            kfx = k * f(x)
        else:
            k = 12
            kfx = k * f(x)
        sum_inner += kfx
        N = append(N, [[x, f(x), k, kfx]], axis=0)
    result = round((2/45 * h) * (7 * f(a) + sum_inner + 7 * f(b)), decimals)

    return N, result

def _weddle(N, f, a, b, n, h, decimals):
    """
    Weddle's rule integration given a function and limits of integration.
    """
    if n > 13:
        raise ValueError(f"The 'Weddle' method is only available for n <= 13.")
    x = a
    sum_inner = 0
    for m in range(1, n):
        x += h
        if m in [2, 4, 6, 8, 10, 12]:
            k = 1
            kfx = k * f(x)
        elif m in [1, 5, 7, 11]:
            k = 5
            kfx = k * f(x)
        elif m in [3, 9]:
            k = 6
            kfx = k * f(x)
        sum_inner += kfx
        N = append(N, [[x, f(x), k, kfx]], axis=0)
    result = round((3/10 * h) * (f(a) + sum_inner + f(b)), decimals)

    return N, result

def int_composite_data(
        x, 
        y, 
        method='trapezoidal', 
        col_latex=True, 
        index_labels=None, 
        decimals=12
) -> tuple[DataFrame, Float]:
    """
    ```

    Composite integration given data.
    
    Parameters
    ----------
    x : array_like
        The points corresponding to the ``y`` values.
    y : array_like
        The points to be integrated, synonymous to f(x).
    method: {trapezoidal, ..., weddle}, default='trapezoidal'
        The integration method to be applied.
        ==========================================
        Argument        Description
        ==========================================
        trapezoidal     Composite Trapezoidal rule
        simpson13       Composite Simpson 1/3 rule
        simpson38       Composite Simpson 3/8 rule
        boole           Boole's rule
        weddle          Weddle's rule
        ==========================================
    col_latex : bool, default=True
        If True, table headings will be displayed in Latex.
    index_labels : {default, int, array_like, None}, default='default'
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        default ........... System default, or 0, 1, 2, ...
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels
        None .............. Will remove the DataFrame index       
        ==============================================================
    decimals : int, default=12
        Number of decimal points.      

    Returns
    -------
    dframe : DataFrame
        A table used for the calculations.
    result : Float
        The result of integration.

    Examples
    --------
    >> x = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
    >> y = [1.0, 1.14250172, 1.27370387, 1.39727029, 1.51541157, 1.62955979]
    >> table, result = stm.int_composite_data(x, y, method='trapezoidal', index_labels=None, decimals=8)
    >> table
    $x$      $f(x)$  $k$    $k f(x)$
    1.0  1.00000000  1.0  1.00000000
    1.1  1.14250172  2.0  2.28500344
    1.2  1.27370387  2.0  2.54740774
    1.3  1.39727029  2.0  2.79454058
    1.4  1.51541157  2.0  3.03082314
    1.5  1.62955979  1.0  1.62955979
    >> result
    0.6643667345

    >> x = [1.0, 1.075, 1.15, 1.225, 1.3, 1.375, 1.45, 1.525, 1.6]
    >> y = [-0.66666667, -0.75587783, -0.85901027, -0.98024506, -1.12554113, -1.3037037, -1.52832675, -1.82157521, -2.22222222]
    >> table, result = stm.int_composite_data(x, y, method='simpson13', index_labels=None, decimals=8)
    >> table
      $x$      $f(x)$  $k$    $k f(x)$
    1.000 -0.66666667  1.0 -0.66666667
    1.075 -0.75587783  4.0 -3.02351132
    1.150 -0.85901027  2.0 -1.71802054
    1.225 -0.98024506  4.0 -3.92098024
    1.300 -1.12554113  2.0 -2.25108226
    1.375 -1.30370370  4.0 -5.21481480
    1.450 -1.52832675  2.0 -3.05665350
    1.525 -1.82157521  4.0 -7.28630084
    1.600 -2.22222222  1.0 -2.22222222
    >> result
    0.734006310189

    >> x = stm.datasets(id='simpson38')['x'].tolist()
    >> y = stm.datasets(id='simpson38')['y'].tolist()
    >> table, result = stm.int_composite_data(x, y, method='simpson38', index_labels=None, decimals=8)
    >> table
      $x$      $f(x)$  $k$    $k f(x)$
    0.000  0.00000000  1.0  0.00000000
    0.125  0.01378901  3.0  0.04136703
    0.250  0.04867505  3.0  0.14602515
    0.375  0.09665005  2.0  0.19330010
    0.500  0.15163266  3.0  0.45489798
    0.625  0.20908650  3.0  0.62725950
    0.750  0.26570619  2.0  0.53141238
    0.875  0.31915998  3.0  0.95747994
    1.000  0.36787944  1.0  0.36787944
    >> result
    0.15560725875

    >> x = stm.datasets(id='boole')['x'].tolist()
    >> y = stm.datasets(id='boole')['y'].tolist()
    >> table, result = stm.int_composite_data(x, y, method='boole', index_labels=None, decimals=12)
    >> table
    $x$       $f(x)$   $k$      $k f(x)$
    0.0   0.00000000   1.0    0.00000000
    0.2   0.70956648  32.0   22.70612736
    0.4   2.38170610  12.0   28.58047320
    0.6   5.63850789  32.0  180.43225248
    0.8  11.01847613  14.0  154.25866582
    1.0  18.26372704  32.0  584.43926528
    1.2  24.72075984  12.0  296.64911808
    1.4  22.33913068  32.0  714.85218176
    1.6  -7.09306654   1.0   -7.09306654
    >> result
    17.175703272889

    >> x = stm.datasets(id='weddle')['x'].tolist()
    >> y = stm.datasets(id='weddle')['y'].tolist()
    >> table, result = stm.int_composite_data(x, y, method='weddle', index_labels=None, decimals=12)
    >> table
      $x$      $f(x)$  $k$    $k f(x)$
    0.000  0.00000000  1.0  0.00000000
    0.035  0.00120405  5.0  0.00602025
    0.070  0.00473611  1.0  0.00473611
    0.105  0.01048376  6.0  0.06290256
    0.140  0.01834396  1.0  0.01834396
    0.175  0.02822193  5.0  0.14110965
    0.210  0.04003028  1.0  0.04003028
    0.245  0.05368820  5.0  0.26844100
    0.280  0.06912082  1.0  0.06912082
    0.315  0.08625855  6.0  0.51755130
    0.350  0.10503661  1.0  0.10503661
    >> result
    0.01294957167
    ```
    """
    display_options()
    x = to_listuple(array_values=x, to_ndarray=True, par_name='x')
    y = to_listuple(array_values=y, to_ndarray=True, par_name='y')
    if not is_len_equal(x, y):
        raise LengthDifferError(par_name='x, y', user_input=[x, y])
    if not is_diff_constant(x):
        raise DifferenceError(par_name='x', user_input=x)
    n = len(x)
    h = x[1] - x[0]

    col_latex = val_boolean(user_input=col_latex, default=True)

    N = array([[x[0], y[0], 1, y[0]]], dtype=float64)
    # call each of the integration methods
    if method == 'trapezoidal':
        N, result = _trapezoidal_data(N, x, y, n, h, decimals)
    elif method == 'simpson13':
        N, result = _simpson13_data(N, x, y, n, h, decimals)
    elif method == 'simpson38':
        N, result = _simpson38_data(N, x, y, n, h, decimals)
    elif method == 'boole':
        N, result = _boole_data(N, x, y, n, h, decimals)
    elif method == 'weddle':
        N, result = _weddle_data(N, x, y, n, h, decimals)
    else:
        methods = "'trapezoidal', 'simpson13', 'simpson38', 'boole', 'weddle'"
        raise ValueError(f"'method' must be one of {methods}")
    
    N = append(N, [[x[-1], y[-1], 1, y[-1]]], axis=0)
    col_labels = dframe_labels(
        dframe=N, 
        df_labels=['x', 'f(x)', 'k', 'k f(x)'], 
        col_latex=col_latex, 
        prefix=None, 
        index=False
    )
    index_labels = dframe_labels(
        dframe=dframe, df_labels=index_labels, index=True
    )
    dframe = DataFrame(N, index=index_labels, columns=col_labels)
    dframe = dframe.round(decimals).fillna('-')
    result = sympify(result)

    return dframe, result

def _trapezoidal_data(N, x, y, n, h, decimals):
    """ 
    Trapezoidal's rule integration given sample data points.
    """
    sum_inner = 0
    for m in range(1, n-1):
        k = 2
        kfx = k * y[m]
        sum_inner += kfx
        N = append(N, [[x[m], y[m], k, kfx]], axis=0)
    result = round(0.5 * h * (y[0] + sum_inner + y[-1]), decimals)

    return N, result

def _simpson13_data(N, x, y, n, h, decimals):
    """ 
    Simpson's 1/3 rule integration given sample data points.
    """
    sum_inner = 0
    for m in range(1, n-1):
        if m % 2 == 0:
            k = 2
            kfx = k * y[m]
        else:
            k = 4
            kfx = k * y[m]
        sum_inner += kfx
        N = append(N, [[x[m], y[m], k, kfx]], axis=0)
    result = round((h/3) * (y[0] + sum_inner + y[-1]), decimals)

    return N, result

def _simpson38_data(N, x, y, n, h, decimals):
    """ 
    Simpson's 3/8 rule integration given sample data points.
    """
    sum_inner = 0
    for m in range(1, n-1):
        if m % 3 == 0:
            k = 2
            kfx = k * y[m]
        else:
            k = 3
            kfx = k * y[m]
        sum_inner += kfx
        N = append(N, [[x[m], y[m], k, kfx]], axis=0)
    result = round((3/8 * h) * (y[0] + sum_inner + y[-1]), decimals)
    
    return N, result

def _boole_data(N, x, y, n, h, decimals):
    """ 
    Boole's rule integration given sample data points.
    """
    sum_inner = 0
    for m in range(1, n-1):
        if m % 2 == 1:
            k = 32
            kfx = k * y[m]
        elif m % 4 == 0:
            k = 14
            kfx = k * y[m]
        else:
            k = 12
            kfx = k * y[m]
        sum_inner += kfx
        N = append(N, [[x[m], y[m], k, kfx]], axis=0)
    result = round((2/45 * h) * (7 * y[0] + sum_inner + 7 * y[-1]), decimals)
    
    return N, result

def _weddle_data(N, x, y, n, h, decimals):
    """ 
    Weddle's rule integration given sample data points.
    """
    sum_inner = 0
    for m in range(1, n-1):
        if m in [2, 4, 6, 8, 10, 12]:
            k = 1
            kfx = k * y[m]
        elif m in [1, 5, 7, 11]:
            k = 5
            kfx = k * y[m]
        elif m in [3, 9]:
            k = 6
            kfx = k * y[m]
        sum_inner += kfx
        N = append(N, [[x[m], y[m], k, kfx]], axis=0)
    result = round((3/10 * h) * (y[0] + sum_inner + y[-1]), decimals)
    
    return N, result

def _trapezoid(f, a, b, n, decimals=12):
    """
    Trapezoidal integration, used in Romberg integration.
    """
    h = (b - a) / n
    x = linspace(a, b, num=n+1, endpoint=True)
    result = f(a) + 2 * sum(f(x)[1:-1]) + f(b)

    return round(0.5 * h * result, decimals)

def int_romberg(
        f, a, b, n, col_latex=True, index_labels=None, decimals=12
) -> tuple[DataFrame, Float]:
    """
    ```

    Romberg integration.

    Parameters
    ----------
    f : {str, symbolic}
        The univariate function to be integrated.
    a : {int, float}
        Lower limit of integration.
    b : {int, float}
        Upper limit of integration.
    n : int
        Number of points.
    col_latex : bool, default=True
        If True, table headings will be displayed in Latex.
    index_labels : {default, int, array_like, None}, default='default'
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        default ........... System default, or 0, 1, 2, ...
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels
        None .............. Will remove the DataFrame index       
        ==============================================================
    decimals : int, default=12
        Number of decimal points.

    Returns
    -------
    df : DataFrame
        A table used for the calculations.
    result : Float
        The result of integration.

    Examples
    --------

    ```
    """
    display_options()
    col_latex = val_boolean(user_input=col_latex, default=True)
    f = lambdify_expr(f, univariate=True, par_name='f')
    if a >= b:
        raise LowerGEUpperError(a='a', b='b')
    if not isinstance(n, int) or n <= 0:
        raise NumericBtwnError(par_name='n', limits = None, user_input=n)
    # initialize results table
    N = nan * ones((n, n))
    steps = []
    for k in range(n):
        # composite trapezoidal rule for 2^k panels
        steps.append(2**k)
        N[k, 0] = _trapezoid(f, a, b, 2**k)
        # romberg recursive formula
        for j in range(k):
            N[k, j+1] = (4**(j+1) * N[k, j] - N[k-1, j]) / (4**(j+1) - 1)
    col_labels = dframe_labels(dframe=N, col_latex=col_latex, prefix='R_', index=True)
    dframe = DataFrame(N, columns=col_labels).round(decimals).fillna('')
    dframe = insert(dframe, columns_to_insert=steps, column_names='$h$', insert_at=0)
    dframe.index = dframe_labels(dframe=dframe, df_labels=index_labels)
    result = sympify(dframe.iloc[-1, -1])

    return dframe, result

def int_glegendre(
        f, a, b, n=5, col_latex=True, to_dict=False, decimals=12
) -> tuple[DataFrame, Float]:
    """
    ```

    Gauss-Legendre integration.

    Parameters
    ----------
    f : {symbolic, str}
        The function to be integrated.
    a : {int, float}
        Lower limit of integration.
    b : {int, float}
        Upper limit of integration.
    n : int, defaut=5
        Number of points to use.
    index_labels : {default, int, array_like, None}, default='default'
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        default ........... System default, or 0, 1, 2, ...
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels
        None .............. Will remove the DataFrame index       
        ==============================================================
    col_latex : bool, default=True
        If True, column headings will be printed in Latex.
    to_dict : bool, default=False
        If True, results will be returned as a dictionary, otherwise it is a 
        tuple
    decimals : int, default=12
        Number of decimal points.

    Returns
    -------
    df : DataFrame
        A table used for the calculations.
    result : Float
        The result of integration.

    Examples
    --------
    >> f = '(x^2 + 2 * x + 1) / (1 + (x + 1)^4)'
    >> a, b, n = (0, 2, 4)
    >> table, result = stm.int_glegendre(f, a, b, n, decimals=12)
    >> table
         Node $(x_i)$  Weight $(w_i)$        $f(t_i)$    $w_i f(t_i)$
    0 -0.861136311594  0.347854845137  0.483555654740  0.168207177395
    1 -0.339981043585  0.652145154863  0.320661638326  0.209117933785
    2  0.339981043585  0.652145154863  0.176736442540  0.115257814690
    3  0.861136311594  0.347854845137  0.120362156179  0.041868559198
    >> result
    0.534451485068

    >> f = 'exp(-x) * cos(x)'
    >> a, b, n = (0, np.pi/2, 6)
    >> table, result = stm.int_glegendre(f, a, b, n, decimals=12)
    >> table
         Node $(x_i)$  Weight $(w_i)$        $f(t_i)$    $w_i f(t_i)$
    0 -0.932469514203  0.171324492379  0.947010108967  0.162246026197
    1 -0.661209386466  0.360761573048  0.739403072221  0.266748215451
    2 -0.238619186083  0.467913934573  0.454490562638  0.212662467390
    3  0.238619186083  0.467913934573  0.212817476714  0.099580262875
    4  0.661209386466  0.360761573048  0.071327272282  0.025732138950
    5  0.932469514203  0.171324492379  0.011620697401  0.001990910083
    >> result
    0.603939788177

    >> f = 'exp(3 * x) * sin(2 * x)'
    >> a, b, n = (1, 3, 15)
    >> table, result = stm.int_glegendre(f, a, b, n, decimals=6)
    >> table
          Node $(x_i)$  Weight $(w_i)$             $f(t_i)$        $w_i f(t_i)$
    0  -0.987992518020  0.030753241996    18.72009251746500    0.57570353537900
    1  -0.937273392401  0.070366047488    20.60958805522900    1.45021525180500
    2  -0.848206583410  0.107159220467    23.54089125568500    2.52262355606200
    3  -0.724417731360  0.139570677926    25.56049613570100    3.56749577378900
    4  -0.570972172609  0.166269205817    20.35315350236700    3.38410266871000
    5  -0.394151347078  0.186161000016    -8.66212949961100   -1.61255068991200
    6  -0.201194093997  0.198431485327   -97.15376009978399  -19.27836492171400
    7   0.000000000000  0.202578241926  -305.31591759436901  -61.85036181815700
    8   0.201194093997  0.198431485327  -702.56794201301295 -139.41160027685399
    9   0.394151347078  0.186161000016 -1312.34359732972507 -244.30719644292199
    10  0.570972172609  0.166269205817 -2033.82279747745997 -338.16210130907501
    11  0.724417731360  0.139570677926 -2626.24295254265417 -366.54650928516298
    12  0.848206583410  0.107159220467 -2845.35777376225315 -304.90632098656999
    13  0.937273392401  0.070366047488 -2667.53038244886602 -187.70356956736600
    14  0.987992518020  0.030753241996 -2363.60603888629794  -72.68854849735700
    >> result
    -1724.96698300935
    ```
    """
    display_options()
    f = lambdify_expr(f, univariate=True, par_name='f')
    if a >= b:
        raise LowerGEUpperError(a='a', b='b')
    if not isinstance(n, int) or n <= 0:
        raise NumericBtwnError(par_name='n', limits = None, user_input=n)
    col_latex = val_boolean(user_input=col_latex, default=True)
    to_dict = val_boolean(user_input=to_dict, default=False)
    x, w = roots_legendre(n)
    t = 1/2 * (a + b) + 1/2 * (b - a) * x # transformation
    dt = 1/2 * (b - a) # derivative of transformed variable
    result = sympify(round(dt * sum(w * f(t)), decimals))
    # table of weights
    dframe = DataFrame([x, w, f(t), w * f(t)]).T.round(decimals)

    if col_latex is True:
        dframe.columns = ['Node $(x_i)$', 'Weight $(w_i)$', '$f(t_i)$', '$w_i f(t_i)$']
    else:
        dframe.columns = ['Node (xi)', 'Weight (wi)', 'f(ti)', 'wi * f(ti)']

    result = {'result_table': dframe, 'result': result}
    if to_dict is False:
        result = tuple(result.values())
    
    return result
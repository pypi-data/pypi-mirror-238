from numpy import (
    array, nan, linspace, arange, full, repeat, hstack, vstack, diag,
    concatenate, float64, reshape, log, log10, exp, poly1d, polyfit, delete,
    isnan, asarray, asfarray
)
from numpy.linalg import solve
from sympy import (
    sympify, symbols, linear_eq_to_matrix, Poly, Piecewise, lambdify, degree
)
from pandas import DataFrame
from math import factorial
from scipy.interpolate import lagrange, CubicSpline
from sklearn import linear_model
model = linear_model.LinearRegression()
from ..core.arraylike import table_na, to_listuple
from ..core.base import pm_sign
from ..core.symbolic import remove_zeros
from ..core.plotting import interpolation_plot
from ..core.validate import (
    val_boolean, val_decimals, val_listitems, val_numeric, val_string, 
    val_len_equal, val_dflabels
)
from ..statistical.wrangle import dframe_labels
from ..core.htmlatex import dframe_color, latex_display
from ..core.errors import NumpifyError, MaxNError, VectorLengthError

"""
stm.interpolate(
    x, 
    y, 
    x0, 
    method='newton-divided', 
    poly_order=1, 
    expr_variable='x', 
    plot_x0=False, 
    diff_order=0, 
    plot_deriv=False, 
    truncate_terms=1e-16,
    style_indices=True,
    index_labels=1,
    col_labels=None,
    col_latex=True,
    to_dict=False,
    decimals=12, 
    yprime,
    poly_order,
    qs_constraint,
    end_points
    exp_type,
    sat_type,
    )
"""

def _get_indices(N, method):
    """
    Get indices.
    """
    try:
        N = asfarray(N)
    except:
        raise NumpifyError(par_name='N')
    nrows, ncols = table_na(N).shape
    style_indices_list = []
    if method in ['hermite', 'newton-forward', 'newton-divided']:
        for row in range(nrows):
            for col in range(1, ncols):
                if row == col-1:
                    style_indices_list.append([row, col])
    elif method in ['newton-backward']:
        for col in range(1, ncols):
            style_indices_list.append([nrows-col, col])
    else:
        style_indices_list = []
    style_indices_list = asarray(style_indices_list).T.tolist()

    return style_indices_list

def _interpolation_terms(N, x, X0, method, p):
    """
    ```

    Interpolation terms.

    Parameters
    ----------
    N : DataFrame
        A DataFrame with the values.
    x : array_like
        An array_like with the values of `x`.
    x0 : float
        The initial value.
    method : str
        Method of interpolation.
    p : float
        The point
    
    Returns
    ------
    style_indices_list : list
        A 2D list with the array indices.
    poly_approx : str
        A string with the interpolated polynomial.
    ```
    """
    N, n = (N.values, N.shape[1])
    if method == 'gauss-backward':
        terms = [
            '1',
            'p',
            'p * (p+1) / 2',
            '(p-1) * p * (p+1) / 6',
            '(p-1) * p * (p+1) * (p+2) / 24',
            '(p-2) * (p-1) * p * (p+1) * (p+2) / 120'
        ]
        coefficients = [N[p, 1]]
        style_indices_list = [[p, 1]]
        for index in range(1, n-1):
            row = p-1
            if index % 2 == 0:
                row = p
            coefficients.append(N[row, index+1])
            style_indices_list.append([row, index+1])
    elif method == 'gauss-forward':
        terms = [
            '1',
            'p',
            '(p-1) * p / 2',
            '(p-1) * p * (p+1) / 6',
            '(p-1) * (p-2) * p * (p+1) / 24',
            '(p-1) * (p-2) * p * (p+2) * (p+1) / 120'
        ]
        coefficients = [N[p, 1]]
        style_indices_list = [[p, 1]]
        for index in range(1, n-1):
            row = p+1
            if index % 2 == 0:
                row = p
            coefficients.append(N[row, index+1])
            style_indices_list.append([row, index+1])
    elif method == 'stirling':
        terms = [
            '1',
            'p',
            'p**2 / 2',
            'p * (p**2-1**2) / 6',
            'p**2 * (p**2-1**2) / 24',
            'p * (p**2-1**2) * (p**2-2**2) / 120',
            'p**2 * (p**2-1**2) * (p**2-2**2) / 720'
        ]
        style_indices_list = [[p, 1]]
        coefs_backward = []
        for index in range(1, n-1):
            row = p-1
            if index % 2 == 0:
                row = p
            coefs_backward.append(N[row, index+1])
            style_indices_list.append([row, index+1])
        coefs_forward = []
        for index in range(1, n-1):
            row = p+1
            if index % 2 == 0:
                row = p
            coefs_forward.append(N[row, index+1])
            style_indices_list.append([row, index+1])
        # to prevent a missing value from being 
        # include (for even number of points)
        if coefs_backward[-1] == '':
            coefs_backward[-1] = coefs_forward[-1]
        if coefs_forward[-1] == '':
            coefs_forward[-1] = coefs_backward[-1]
        coeff_count = len(coefs_backward)
        coefficients =  [N[p, 1]] + [(coefs_backward[k] + coefs_forward[k])/2 
                                     for k in range(coeff_count)]

    elif method == 'bessel':
        terms = [
            '1',
            '(p-1/2)',
            '( p * (p-1) )/2',
            '( (p-1) * p * (p-1/2) )/6',
            '( (p+1) * p * (p-1) * (p-2) )/24',
            '( (p+1) * p * (p-1/2) * (p-1) * (p-2) )/120'
        ]
        style_indices_list = [[p, 1]]
        coefs_forward = [N[p, 1]]
        for index in range(1, n-1):
            row = p+1
            if index % 2 == 0:
                row = p
            coefs_forward.append(N[row, index+1])
            style_indices_list.append([row, index+1])
        coeff_count = len(coefs_forward)
        style_indices_list_straight = []
        coefs_straight = []
        for col in range(1, coeff_count):
            if col % 2 == 0:
                 coefs_straight.append(0)
            else:
                style_indices_list_straight.append([p+2, col])
                coefs_straight.append(N[p+2, col])
        if len(coefs_forward) > len(coefs_straight):
            coefs_straight += [0] * (len(coefs_forward) - len(coefs_straight))
        if coefs_straight[-1] == 0:
            coefs_straight[-1] = coefs_forward[-1]
        style_indices_list += style_indices_list_straight
        for k in range(coeff_count):
            if k % 2 != 0:
                coefs_straight[k] = coefs_forward[k]
        coefficients = [(coefs_forward[k] + coefs_straight[k])/2 
                        for k in range(coeff_count)]
    elif method == 'laplace-everett':
        terms_q = [
            'q',
            'q * (q**2 - 1**2)/6',
            'q * (q**2 - 1**2) * (q**2 - 2**2)/24',
            'q * (q**2 - 1**2) * (q**2 - 2**2) * (q**2 - 3**2)/120'
        ]
        terms_p = [
            'p',
            'p * (p**2 - 1**2)/6',
            'p * (p**2 - 1**2) * (p**2 - 2**2)/24',
            'p * (p**2 - 1**2) * (p**2 - 2**2) * (p**2 - 3**2)/120'
        ]
        style_indices_list = [[p, 1]]
        coefs_forward = [N[p, 1]]
        for index in range(1, n-1):
            row = p+1
            if index % 2 == 0:
                row = p
            coefs_forward.append(N[row, index+1])
            style_indices_list.append([row, index+1])
        coeff_count = len(coefs_forward)
        style_indices_list_straight = [[p, 1]]
        coefs_straight = []
        for col in range(1, coeff_count):
            if col % 2 == 0:
                 coefs_straight.append(0)
            else:
                style_indices_list_straight.append([p+2, col])
                coefs_straight.append(N[p+2, col])
        style_indices_list += style_indices_list_straight
        # remove the coloring for middle row 
        # (between above and below coloring)
        style_indices_list_new = []
        for value in style_indices_list:
            if value[0] != p+1:
                style_indices_list_new.append(value)
        style_indices_list = style_indices_list_new
        # remove middle coefficients
        coefs_forward_new = []
        coefs_straight_new = []
        for k in range(len(coefs_forward)):
            if k % 2 == 0:
                coefs_forward_new.append(coefs_forward[k])
                coefs_straight_new.append(coefs_straight[k])
        coefficients = coefs_forward_new, coefs_straight_new
    else:
        pass
    if method != 'laplace-everett':
        m = len(coefficients)
        terms = terms[:m]
        terms = [f'{coefficients[k]} * {terms[k]}' for k in range(m)]
        poly_approx = ' + '.join(terms)
    else:
        coefs_q, coefs_p = coefficients
        m = len(coefs_q)
        terms_q = terms_q[:m]
        terms_p = terms_p[:m]
        terms_q = [f'{coefs_q[k]} * {terms_q[k]}' for k in range(m)]
        terms_p = [f'{coefs_p[k]} * {terms_p[k]}' for k in range(m)]
        poly_approx = ' + '.join(terms_q + terms_p)

    p = f'((x {pm_sign(-X0)} {abs(X0)}) / {x[1] - x[0]})'
    q = f'(1-{p})'
    # q applies to laplace-everett
    poly_approx = poly_approx.replace('p', p).replace('q', q)
    style_indices_list = array(style_indices_list).T.tolist()

    return style_indices_list, poly_approx

def _interpolation_p(x, method):
    """
    ```

    Calculates the column indices for p.

    Parameters
    ----------
    x : array_like
        A 2D array with the x values.
    method : str
        Method of interpolation.

    Returns
    -------
    X0
        The initial guess.
    p : float
        The initial value.
    p_col : ndarray
        A 1D array of indices with reference to k.
    ```
    """
    x = to_listuple(x, to_ndarray=True, par_name='x')
    k = len(x[::2]) # exclude the blank values 
    if k %2 == 0:
        methods = ['gauss-forward', 'stirling', 'bessel', 'laplace-everett']
        if method in methods:
            p = k-2
        elif method in ['gauss-backward']:
            p = k
    else:
        p = k-1
    X0 = x[p]
    p_col = table_na(arange(0, len(x)) - p)
        
    return X0, p, p_col

def interpolate(
        x, 
        y, 
        x0, 
        method='newton-divided', 
        expr_variable='x', 
        plot_x0=False, 
        diff_order=0, 
        plot_deriv=False, 
        truncate_terms=1e-16,
        style_indices=True,
        index_labels=1,
        col_labels=None,
        col_latex=True,
        to_dict=False,
        decimals=12, 
        **kwargs
    ):
    """
    ```

    Performs univariate interpolation for a specified method.

    Parameters
    ----------
    x : array_like
        The x-coordinates at which to evaluate the interpolated values.
    y : array_like
        The y-coordinates of the data points, same length as `x`.
    x0 : int, float
        The point at which the interpolation should be performed.
    method : str, optional
        Interpolation method to be implimented. Default will be calculated
        using the `_interpolation()` function.
        =======================================================================
        Method                          Description
        =======================================================================
        Unequally spaced
        ----------------
        straight-line ................. 
        lagrange ......................
        hermite .......................

        Equally spaced data, backward/forward
        -------------------------------------
        newton backward ............... used when x0 is towards the end
        newton forward ................ used when x0 is at the beginning
        gauss-backward ................
        gauss-forward .................

        Equally spaced, central formulas
        --------------------------------
        newton-divided : used when x0 is almost at center
        neville .......................
        stirling ......................
        bessel ........................
        laplace-everett ...............

        Splines
        -------
        linear-splines ................
        quadratic-splines .............
        natural-cubic-splines .........
        clamped-cubic-splines .........
        not-a-knot-splines ............

        Least square methods
        --------------------
        linear-regression .............
        polynomial ....................

        Linearization
        -------------
        exponential ...................
        power .........................
        saturation ....................
        reciprocal ....................
        =======================================================================
    diff_order :  int, default=0
        Order of differentiation. 0 means no differentiation.
    expr_variable : str, default='x'
        Variable to be used in the fitted polynomial.
    plot_x0 : bool, default=True
        If True, the point `x0` will be plotted.
    plot_deriv : bool, default=False
        If True, derivative will be plotted. Will be disregarded if derivative 
        is not specified or it is constant.
    truncate_terms : float, default=1e-16
        Smallest value for which terms should be removed. Terms below this 
        value will not be shown in the polynomial to be displayed.
    style_indices : bool, default=True
        If True, a Styler will be returned with some values coloured, 
        otherwise a DataFrame will be returned with no colouring.
    index_labels : {int, array_like, None}, default=None
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels
        None .............. Will remove the DataFrame index       
        ==============================================================
    col_labels : {int, array_like, None}, default=None
        Same as `index_labels` above.
    col_latex : bool, default=True
        If True, column headings will be printed in Latex.
    to_dict : bool, default=False
        If True, results will be returned as a dictionary, otherwise  
        results are returned as a tuple
    decimals : int, default=12
        Number of decimal points.
    
    **kwargs
    --------
    yprime : array_like
        Points of the first derivative, same length as `x`.
    poly_order : int
        Degree of the fitting polynomial. Required for polynomial 
        interpolation.
    qs_constraint : {int, float}, default=0
        Last equation for quadratic spline. E.g. when qs_constraint = 5, 
        the last equation becomes a0 - 5 = 0. So, just enter a0 - 5.
    end_points : list, tuple, 1D array
        Two endpoints for the clamped-cubic-splines.
    exp_type : str, optional
        Type of exponential function to be applied. Can either be 
        'exp(ax)' or '10^ax'. Default is 'exp(ax)'.
    sat_type : str, optional
        Type of saturation function to be applied. Can either be 
        'ax/(x+b)' or 'x/(ax+b)'. Default is 'ax/(x+b)'.

    Returns
    -------
    result_table : DataFrame
        A DataFrame with the interpolation values.
    poly_approx_eqtn : symbolic
        The interpolation polynomial from the given data points.
    poly_approx_eqtn_value : Float
        The value of the interpolation polynomial at `x0`.
    poly_deriv_eqtn : symbolic
        The nth derivative of the interpolation polynomial.
    poly_deriv_eqtn_value : Float
        Value of the nth derivative of the interpolation polynomial at `x0`.
    image_code : str
        String with the image code.
        
    Examples
    --------
    >> import stemlab as stm
    >> x = np.array([0, 0.78539816, 1.57079633, 2.35619449, 3.14159265])
    >> y = np.array([1, 0.91600365, 0.0872758 , 0.11687946, 0.66613092])
    >> x0 = 1.15
    >> result = stm.interpolate(x, y, x0, expr_variable='x', method='newton-divided', plot_x0=True, diff_order=0, plot_deriv=False, to_dict=True, decimals=12)
    
    >> x = [100, 150, 200, 250, 300, 350, 400]
    >> y = [10.63, 13.03, 15.04, 16.81, 18.42, 19.90, 21.27]
    >> x0 = 160
    >> result = stm.interpolate(x, y, x0, expr_variable='x', method='newton-forward', plot_x0=True, diff_order=0, plot_deriv=False, decimals=12)

    https://s3.us-west-2.amazonaws.com/public.gamelab.fun/dataset/position_salaries.csv
    https://s3.us-west-2.amazonaws.com/public.gamelab.fun/dataset/salary_data.csv
    
    https://atozmath.com/example/CONM/NumeInterPola.aspx?q=F&q1=E1
    https://www.lkouniv.ac.in/site/writereaddata/siteContent/202004032250571912siddharth_bhatt_engg_Interpolation.pdf
    ```
    """
    # x
    x = to_listuple(array_values=x, to_ndarray=True, par_name='x')
    x_values = x.copy()

    n = len(x)
    if n > 25:
        raise MaxNError(par_name='len(x)', user_input=len(x), maxn=25)
    if len(x.shape) == 1:
        ncols = 0
    else:
        ncols = x.shape[1]
    
    # y
    y = to_listuple(array_values=y, to_ndarray=True, par_name='y')
    _ = val_len_equal(x, y) # check number of elements are equal
    
    # x0
    x0 = val_numeric(user_input=x0, par_name='x0')
    if not x0:
        x0 = round((x[1]-x[0]) / 2, decimals)

    # method
    method = method.lower()
    methods = [
        'straight-line', 'lagrange', 'hermite',
        'newton-backward', 'newton-forward',
        'gauss-backward', 'gauss-forward',
        'newton-divided', 'neville', 'stirling', 'bessel', 'laplace-everett',
        'linear-splines', 'quadratic-splines', 'natural-cubic-splines', 
        'clamped-cubic-splines', 'not-a-knot-splines', 
        'linear-regression', 'polynomial', 
        'exponential', 'power', 'saturation', 'reciprocal'
    ]
    method = val_listitems(
        par_name='method', valid_items=methods, user_input=method
    )

    # expr_variable
    expr_variable = val_string(
        par_name='expr_variable', user_input=expr_variable
    )
    if not expr_variable:
        expr_variable = 'x'

    # plot_x0
    plot_x0 = val_boolean(user_input=plot_x0, default=False)

    # diff_order
    diff_order = val_numeric(
        user_input=diff_order, 
        to_float=False,
        limits=[0, 9], 
        boundary='inclusive', 
        par_name='diff_order'
    )
    
    # plot_deriv
    plot_deriv = val_boolean(user_input=plot_deriv, default=False)

    # truncate_terms
    truncate_terms = val_numeric(
        user_input=truncate_terms, 
        limits=[0, .1], 
        boundary='inclusive', 
        par_name='truncate_terms'
    )

    # style_indices
    style_indices = val_boolean(user_input=style_indices, default=True)
    
    # index_labels
    index_labels = val_dflabels(par_name='index_labels', user_input=True)

    # col_labels
    col_labels = val_dflabels(par_name='col_labels', user_input=True)

    # col_latex
    col_latex = val_boolean(user_input=col_latex, default=True)

    # to_dict
    to_dict = val_boolean(user_input=to_dict, default=False)

    # decimals
    decimals = val_decimals(decimals=decimals)
    
    N = full(shape = (n, n+1), fill_value = nan)
    if len(x.shape) == 1:
        N[:, 0] = x
    else:
        N[:, :ncols] = x
    N[:, ncols+1] = y
    
    # get kwargs
    # ----------

    kw_args = kwargs

    # yprime
    if method == 'hermite':
        yprime = kw_args.get('yprime')
        yprime = to_listuple(array_values=yprime, to_ndarray=True, par_name='yprime')

    # poly_order
    if method == 'polynomial':
        poly_order = kw_args.get('poly_order')
        poly_order = val_numeric(
            user_input=poly_order, 
            limits=[1, 25], 
            boundary='inclusive', 
            par_name='poly_order'
        )

    # qs_constraint
    if method == 'quadratic-splines':
        qs_constraint = kw_args.get('qs_constraint')
        if qs_constraint is None:
            qs_constraint = 'a0-0'
        qs_constraint = val_string(
            user_input=qs_constraint, par_name='qs_constraint'
        )

    # end_points
    if method == 'clamped-cubic-splines':
        end_points = kw_args.get('end_points')
        end_points = to_listuple(
            array_values=end_points,
            n=2,
            to_ndarray=True,
            par_name='end_points'
        )
    
    # exp_type
    if method == 'exponential':
        exp_type = kw_args.get('exp_type')
        if exp_type is None:
            exp_type = 'b*exp(ax)'
        exp_type = val_string(par_name='exp_type', user_input=exp_type)
        # check method
        exp_type = exp_type.replace(' ','').lower()
        exp_methods = ['b*exp(ax)', 'b*10^ax', 'ab^x']
        exp_type = val_listitems(
            par_name='exp_type', valid_items=exp_methods, user_input=exp_type
        )

    # sat_type
    if method == 'saturation':
        sat_type = kw_args.get('sat_type')
        if sat_type is None:
            sat_type = 'x/(ax+b)'
        sat_type = val_string(par_name='sat_type', user_input=sat_type)
        # check method
        sat_type = sat_type.replace(' ','').lower()
        sat_methods = ['x/(ax+b)', 'ax/(x+b)']
        sat_type = val_listitems(
            par_name='sat_type', valid_items=sat_methods, user_input=sat_type
        )

    # Unequally spaced
    # ----------------

    if method in 'straight-line':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _straight_line(N, expr_variable)
    
    elif method == 'lagrange':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _lagrange(N, expr_variable)
    
    elif method == 'hermite':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _hermite(N, yprime, expr_variable)

    # Equally spaced data, backward/forward
    # -------------------------------------
        
    elif method == 'newton-backward':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _newton_backward(N, expr_variable)
        
    elif method == 'newton-forward':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _newton_forward(N, expr_variable)
        
    elif method == 'gauss-backward':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _gauss_backward(N, expr_variable)
        
    elif method == 'gauss-forward':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _gauss_forward(N, expr_variable)
        
    # Equally spaced, central formulas
    # --------------------------------
    
    elif method == 'newton-divided':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _newton_divided(N, expr_variable)
        
    elif method == 'neville':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _neville(N, x0, expr_variable)
        
    elif method == 'stirling':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _stirling(N, expr_variable)
        
    elif method == 'bessel':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _bessel(N, expr_variable)
        
    elif method == 'laplace-everett':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _laplace_everett(N, expr_variable)
    
    # Splines
    # -------

    elif method == 'linear-splines':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _linear_splines(N, expr_variable)
    
    elif method == 'quadratic-splines':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _quadratic_splines(N, expr_variable, qs_constraint, truncate_terms)
    
    elif method == 'natural-cubic-splines':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _natural_cubic_splines(N, expr_variable, truncate_terms)

    elif method == 'clamped-cubic-splines':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _clamped_cubic_splines(N, expr_variable, end_points, truncate_terms)
    
    elif method == 'not-a-knot-splines': 
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _not_a_knot_splines(N, expr_variable)
    
    # Least square methods
    # --------------------

    elif method == 'linear-regression':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _linear_regression(N, expr_variable)
    
    elif method == 'polynomial':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _polynomial(N, poly_order, expr_variable)

    # Linearization
    # -------------

    elif method == 'exponential':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _exponential(N, expr_variable, exp_type)
    
    elif method == 'power':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _power(N, expr_variable)
    
    elif method == 'saturation':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _saturation(N, expr_variable, sat_type)
    
    elif method == 'reciprocal':
        N, style_indices_list, poly_approx, col_names, plot, further_analysis = _reciprocal(N, expr_variable)
    else:
        pass

    # create table
    result_table = table_na(
        data=N, 
        to_ndarray=True, 
        convert_pd=True, 
        col_names=col_names, 
        decimals=decimals)
    
    image_code = None
    if further_analysis:
        x = symbols('x')
        poly_approx = sympify(poly_approx).expand()
        poly_approx_x0 = poly_approx.subs(x, x0)
        
        # for display
        poly_approx_exact = poly_approx.subs(x, expr_variable)
        poly_approx_eqtn = poly_approx_exact.evalf(decimals)
        poly_approx_eqtn_value = (
            poly_approx_exact.subs(expr_variable, x0).evalf(decimals)
        )
        # get the number of symbolic variables in the derivative
        try:
            # if not differentiable, this will crush the syntax
            syms_deriv = len(poly_approx.diff(x, diff_order).free_symbols)
        except:
            diff_order = 0
            syms_deriv = 0

        if diff_order != 0 and syms_deriv > 0:
            poly_deriv = poly_approx.diff(x, diff_order)
            poly_deriv_x0 = poly_deriv.subs(x, x0)
            poly_deriv_eqtn = poly_deriv.evalf(decimals).subs(x, expr_variable)
            poly_deriv_eqtn_value = poly_deriv_x0.evalf(decimals)
        else:
            poly_deriv = None
            poly_deriv_eqtn = (
                'Derivative not available, not specified or is constant.'
            )
            poly_deriv_eqtn_value = (
                'Derivative value not available, not specified or is constant.'
            )
        
        if plot:
            poly_linspace = linspace(
                float(min(x_values)), float(max(x_values)), 100
            )
            if method in ['not-a-knot-splines']:
                cubic_spline = CubicSpline(x_values, y, bc_type='not-a-knot')
                poly_approx_linspace = cubic_spline(poly_linspace)
            else:
                # prepare values for plotting
                f = lambdify(x, poly_approx, 'numpy')
                poly_approx_linspace = f(poly_linspace)
            # important since x had been used as a symbolic variable above
            x = x_values.copy()
            image_code = interpolation_plot(
                x, 
                y, 
                x0, 
                poly_approx_x0, 
                poly_linspace, 
                poly_approx_linspace, 
                poly_deriv, 
                expr_variable, 
                method, 
                plot_x0, 
                diff_order, 
                plot_deriv, 
                decimals
            )
    else:
        result_table = result_table
        poly_approx_eqtn = (
            f'No polynomial for {method.capitalize()} interpolation method'
        )
        poly_approx_eqtn_value = poly_approx_eqtn
        poly_deriv_eqtn = 'NA'
        poly_deriv_eqtn_value = 'NA'
    
    # polynomial
    try:
        # will crush if univariate
        poly_approx_eqtn = remove_zeros(
            poly_approx_eqtn, truncate_terms
        ).evalf(decimals)
    except:
        pass
    
    # derivative
    try:
        poly_deriv_eqtn = remove_zeros(
            poly_deriv_eqtn, truncate_terms
        ).evalf(decimals)
    except:
        pass

    # table labels
    col_labels = dframe_labels(
        dframe=N, 
        df_labels=col_names, 
        col_latex=col_latex, 
        prefix=None, 
        index=False
    )
    
    if col_latex is True:
        col_labels = [f'${col_label}$' for col_label in col_labels]
    
    if index_labels is None:
        index_labels = 1
    index_labels = dframe_labels(
        dframe=result_table, df_labels=index_labels, index=True
    )
    dframe = DataFrame(
        data=result_table, index=index_labels, columns=col_labels
    )
    dframe = dframe.round(decimals)

    # color
    if style_indices is True:
        dframe = dframe_color(
            dframe=dframe,
            style_indices=style_indices_list,
            values=[],
            operator='',
            rows=[],
            cols=[],
            css_styles='color:blue;',
            decimals=decimals,
        )
    
    # polynomials
    if 'quadratic' in method:
        poly_degree_fx = 2
        poly_degree_dfx = 1
    elif 'cubic' in method:
        poly_degree_fx = 3
        poly_degree_dfx = 2
    else:
        poly_degree_fx = degree(poly_approx_eqtn)
        poly_degree_dfx = degree(poly_deriv_eqtn)
    poly_approx_eqtn_fx = latex_display(
        lhs=[f'P{poly_degree_fx}({expr_variable})'], 
        rhs=[poly_approx_eqtn], 
        auto_display=False
    )
    poly_approx_eqtn_value_x0 = latex_display(
        lhs=[f'P{poly_degree_fx}({round(x0, decimals)})'], 
        rhs=[poly_approx_eqtn_value], 
        auto_display=False
    )
    
    # derivatives
    if not 'not available' in str(poly_deriv_eqtn):
        poly_deriv_eqtn_dfx = latex_display(
            lhs=[f'P{poly_degree_dfx}({expr_variable})'], 
            rhs=[poly_deriv_eqtn], 
            auto_display=False
        )
        poly_deriv_eqtn_value_x0 = latex_display(
            lhs=[f'P{poly_degree_dfx}({round(x0, decimals)})'], 
            rhs=[poly_deriv_eqtn_value], 
            auto_display=False
        )
    else:
        poly_deriv_eqtn_dfx = poly_deriv_eqtn
        poly_deriv_eqtn_value_x0 = poly_deriv_eqtn_value

    result = {
        'result_table': dframe,
        'equation': poly_approx_eqtn_fx,
        'equation_value': poly_approx_eqtn_value_x0,
        'derivative': poly_deriv_eqtn_dfx,
        'derivative_value': poly_deriv_eqtn_value_x0,
        'image_code': image_code
    }
    if to_dict is False:
        result = tuple(result.values())

    return result

# ------------------------------------------------------------------------------
    # interpolation methods
# ------------------------------------------------------------------------------

# Unequally spaced
# ----------------

def _straight_line(N, expr_variable):

    col_names = [f'{expr_variable}', f'f({expr_variable})_two_columns_']
    x = N[:, 0]
    y = N[:, 1]
    if len(x) != 2:
        raise VectorLengthError(
            par_name='x', n=2, label='exactly', user_input=x
        )
    if len(y) != 2:
        raise VectorLengthError(
            par_name='y', n=2, label='exactly', user_input=y
        )
    m = (y[1] - y[0]) / (x[1] - x[0])
    c = y[0] - m * x[0]
    poly_approx = f'{m} * x + {c}'

    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

def _lagrange(N, expr_variable):

    col_names = [f'{expr_variable}', f'f({expr_variable})_two_columns_']
    x = N[:, 0]
    y = N[:, 1]
    coefs = asfarray(lagrange(x, y))[::-1]
    xs = [f'x**{k}' for k in range(len(coefs)+1)]
    coefs_xs = [f'{coefs[k]} * {xs[k]}' for k in range(len(coefs))]
    poly_approx = sympify(' + '.join(coefs_xs))
    
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

def _hermite(N, yprime, expr_variable):

    nrows, ncols = N.shape
    col_names = [
        f'{expr_variable}', f'f({expr_variable})'
    ] + ['\\text{C}_{%s}' %(k+1) for k in range(2 * ncols-3)]
    x = N[:, 0]
    y = N[:, 1]
    yp = yprime
    z = repeat(nan, 2*nrows)
    Q = full(shape=(2*nrows, 2*nrows), fill_value = nan)
    for i in range(nrows):
        z[2*i] = x[i]
        z[2*i+1] = x[i]
        Q[2*i, 0] = y[i]
        Q[2*i+1, 0] = y[i]
        Q[2*i+1, 1] = yp[i]
        if i != 0:
            Q[2*i, 1] = (Q[2*i, 0] - Q[2*i-1, 0]) / (z[2*i] - z[2*i-1])
    for i in range(2, 2*nrows):
        for j in range(2, i+1):
            Q[i, j] = (Q[i, j-1] - Q[i-1, j-1]) / (z[i] - z[i-j])
    
    # prepare the polynomial
    diag_elements = diag(Q)
    Q11 = diag_elements[0]
    Qii = diag_elements[1:]
    n = len(Qii)+1
    M = [f'(x - {z[0]})']
    for i in range(1, n):
        for j in range(1, i+1):
            fx = f'(x - {z[j]})'
        M.append(f'{M[i-1]} * {fx}')
    M[0] = f'(x - {z[0]})'
    M.insert(0, Q11)
    ff = [Q11]
    for item in range(1, n):
        ff.append(f'{diag_elements[item]} * {M[item]}')
    poly_approx = ' + '.join(map(str, ff)).replace('+ -', '- ')
    N = hstack([z.reshape(-1, 1), Q])
    
    style_indices_list = _get_indices(N, method = 'hermite')
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

# Equally spaced data, backward/forward
# -------------------------------------

def _newton_backward(N, expr_variable):

    nrows, ncols = N.shape
    n = nrows
    col_names = [
        f'{expr_variable}', f'f({expr_variable})'
        ] + ['\\nabla^{%s}f' %(k+1) for k in range(ncols-2)]
    col_names[2] = '\\nabla f'
    ff = str(N[n-1, 1])
    fi = '* p'
    x = N[:, 0]
    for j in range(1, n):
        for k in range(j, n):
            N[k, j+1] = N[k, j] - N[k-1, j]
        if j == 1:
            fi = fi
        else:
            fi = f'{fi} * (p + {j-1})' 
        ff = f'{ff} {pm_sign(N[n-1, j+1])} {abs(N[n-1, j+1])} {fi} / {factorial(j)}'
    p = f'((x {pm_sign(-x[n-1])} {abs(x[n-1])}) / {x[1] - x[0]})'
    poly_approx = ff.replace('p', p)
    
    style_indices_list = _get_indices(N, method = 'newton-backward')
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

def _newton_forward(N, expr_variable):

    nrows, ncols = N.shape
    n = nrows
    col_names = [
        f'{expr_variable}', f'f({expr_variable})'
    ] + ['\\Delta^{%s}f' %(k+1) for k in range(ncols-2)]
    col_names[2] = '\\Delta f'
    ff = str(N[0, 1])
    fi = '* p'
    x = N[:, 0] 
    for j in range(1, n):
        for k in range(j, n):
            N[k, j+1] = N[k, j] - N[k-1, j]
        if j == 1:
            fi = fi
        else:
            fi = f'{fi} * (p - {j-1})'
        ff = f'{ff} {pm_sign(N[j, j+1])} {abs(N[j, j+1])} {fi} / {factorial(j)}'
    p = f'((x {pm_sign(-x[0])} {abs(x[0])}) / {x[1] - x[0]})'
    poly_approx = ff.replace('p', p)
    
    style_indices_list = _get_indices(N, method = 'newton-forward')
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

def _gauss_backward(N, expr_variable):

    method = 'gauss-backward'
    nrows, ncols = N.shape
    col_names = [
        f'{expr_variable}', f'f({expr_variable})'
    ] + ['\\nabla^{%s}f' %(k+1) for k in range(ncols-2)]
    col_names[2] = '\\nabla f'
    x = N[:, 0]
    for j in range(1, nrows):
        for k in range(j, nrows):
            N[k, j+1] = N[k, j] - N[k-1, j]
    M = table_na(N)
    # result = X0, p, p_col
    X0, p, _ = _interpolation_p(M.loc[:, ['C1']], method)

    style_indices_list, poly_approx = _interpolation_terms(M, x, X0, method, p)
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

def _gauss_forward(N, expr_variable):

    method = 'gauss-forward'
    nrows, ncols = N.shape
    col_names = [
        f'{expr_variable}', f'f({expr_variable})'
    ] + ['\\nabla^{%s}f' %(k+1) for k in range(ncols-2)]
    col_names[2] = '\\nabla f'
    x = N[:, 0]
    for j in range(1, nrows):
        for k in range(j, nrows):
            N[k, j+1] = N[k, j] - N[k-1, j]
    M = table_na(N)
    # result = X0, p, p_col
    X0, p, _ = _interpolation_p(M.loc[:, ['C1']], method)

    style_indices_list, poly_approx = _interpolation_terms(M, x, X0, method, p)
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

# Equally spaced, central formulas
# --------------------------------

# https://github.com/cfgnunes/numerical-methods-python/
# https://atozmath.com/example/CONM/NumeInterPola.aspx?q=A&q1=E1
# Best: https://www.lkouniv.ac.in/site/writereaddata/siteContent/202004032250571912siddharth_bhatt_engg_Interpolation.pdf

def _neville(N, x0, expr_variable):

    nrows, ncols = N.shape
    n = nrows
    col_names = [
        f'{expr_variable}', f'f({expr_variable})'
    ] + ['\\text{C}_{%s}' %(k+1) for k in range(ncols-2)]
    x = N[:, 0]
    y = N[:, 1]
    Q = full(shape = (n, n-1), fill_value = nan)
    Q = concatenate((y.reshape(-1, 1), Q), axis=1)
    for i in range(1, n):
        for j in range(1, i+1):
            Q[i, j] = ((x0 - x[i-j]) * Q[i, j-1] - (x0 - x[i]) * Q[i-1, j-1]) / (x[i] - x[i-j])
    N = concatenate((x.reshape(-1, 1), Q), axis=1)
    poly_approx = Q[n-1, n-1]

    style_indices_list = [[n-1], [n]]
    plot = True
    further_analysis = False
    
    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

def _newton_divided(N, expr_variable):

    nrows, ncols = N.shape
    n = nrows
    col_names = [
        f'{expr_variable}', f'f({expr_variable})'
    ] + ['\\text{C}_{%s}' %(k+1) for k in range(ncols-2)]
    ff = str(N[0, 1])
    fi = ''
    x = N[:, 0]
    for j in range(1, n):
        for k in range(j, n):
            N[k, j+1] = (N[k, j] - N[k-1, j]) / (x[k] - x[k-j])

        fi = f'{fi} * (x {pm_sign(-x[j-1])} {abs(x[j-1])})'
        ff = f'{ff} {pm_sign(N[j, j+1])} {abs(N[j, j+1])} {fi}'
    poly_approx = ff

    style_indices_list = _get_indices(N, method = 'newton-divided')
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

def _stirling(N, expr_variable):

    method = 'stirling'
    nrows, ncols = N.shape
    n = nrows
    col_names = [
        f'{expr_variable}', f'f({expr_variable})'
    ] + ['\\text{C}_{%s}' %(k+1) for k in range(ncols-2)]
    x = N[:, 0]
    for j in range(1, n):
        for k in range(j, n):
            N[k, j+1] = N[k, j] - N[k-1, j]
    M = table_na(N)
    # result = X0, p, p_col
    X0, p, _ = _interpolation_p(M.loc[:, ['C1']], method)

    style_indices_list, poly_approx = _interpolation_terms(M, x, X0, method, p)
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

def _bessel(N, expr_variable):

    method = 'bessel'
    nrows, ncols = N.shape
    n = nrows
    col_names = [
        f'{expr_variable}', f'f({expr_variable})'
    ] + ['\\text{C}_{%s}' %(k+1) for k in range(ncols-2)]
    x = N[:, 0]
    for j in range(1, n):
        for k in range(j, n):
            N[k, j+1] = N[k, j] - N[k-1, j]
    M = table_na(N)
    # result = X0, p, p_col
    X0, p, _ = _interpolation_p(M.loc[:, ['C1']], method)

    style_indices_list, poly_approx = _interpolation_terms(M, x, X0, method, p)
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

def _laplace_everett(N, expr_variable):

    method = 'laplace-everett'
    nrows, ncols = N.shape
    n = nrows
    col_names = [
        f'{expr_variable}', f'f({expr_variable})'
    ] + ['\\text{C}_{%s}' %(k+1) for k in range(ncols-2)]
    x = N[:, 0]
    for j in range(1, n):
        for k in range(j, n):
            N[k, j+1] = N[k, j] - N[k-1, j]
    M = table_na(N)
    # result = X0, p, p_col
    X0, p, _ = _interpolation_p(M.loc[:, ['C1']], method)

    style_indices_list, poly_approx = _interpolation_terms(M, x, X0, method, p)
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis

# Splines
# -------

def _linear_splines(N, expr_variable):

    col_names = [f'{expr_variable}', f'f({expr_variable})_two_columns_']
    equations = []
    x = N[:, 0]
    y = N[:, 1]
    n = len(x)
    for i in range(n-1):
        fx = f'{y[i] / (x[i] - x[i+1])} * (x - {x[i+1]}) + {y[i+1] / (x[i+1] - x[i])} * (x - {x[i]})'
        equations.append(sympify(fx))
    x_mid_values = x[1:-1] # exclude the first and last
    x = symbols('x')
    piece_values = [
        (equations[k], x < x_mid_values[k]) for k in range(len(x_mid_values))
    ] + [(equations[-1], True)]
    poly_approx = Piecewise(*piece_values)
    
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
def _quadratic_splines(N, expr_variable, qs_constraint, truncate_terms):

    eqtn_syms = [
        'a0', 'b0', 'c0',
        'a1', 'b1', 'c1', 
        'a2', 'b2', 'c2', 
        'a3', 'b3', 'c3', 
        'a4', 'b4', 'c4', 
        'a5', 'b5', 'c5', 
        'a6', 'b6', 'c6', 
        'a7', 'b7', 'c7', 
        'a8', 'b8', 'c8', 
        'a9', 'b9', 'c9', 
        'a10', 'b10', 'c10', 
        'a11', 'b11', 'c11', 
        'a12', 'b12', 'c12', 
        'a13', 'b13', 'c13', 
        'a14', 'b14', 'c14', 
        'a15', 'b15', 'c15'
    ] 
    nrows, ncols = N.shape
    n = nrows
    col_names = ['{expr_variable}', f'f({expr_variable})'] + ['a', 'b', 'c']
    equations = []
    x = N[:, 0]
    y = N[:, 1]
    for i in range(n-1):
        # move rhs to the left
        fx = f'{x[i]**2} * a{i} + {x[i]} * b{i} + c{i} - {y[i]}'
        equations.append(sympify(fx))
        # move rhs to the left
        fx = f'{x[i+1]**2} * a{i} + {x[i+1]} * b{i} + c{i} - {y[i+1]}'
        equations.append(sympify(fx))         
    for i in range(n-2):
        # rhs is zero
        fx = f'{2 * x[i+1]} * a{i} + b{i} - {2 * x[i+1]} * a{i+1} - b{i+1}'
        equations.append(sympify(fx))
    equations.append(sympify(qs_constraint))
    # convert equations to matrix form
    # * 3 since they are three variables: a, b, c
    A, b = linear_eq_to_matrix(equations, sympify(eqtn_syms[:((n-1) * 3)]))
    A = asfarray(A)
    b = asfarray(b)
    solution_Ab = reshape(solve(A, b), ((n-1), 3))
    x_mid_values = x[1:-1] # exclude the first and last
    x = symbols('x')
    nrows, ncols = solution_Ab.shape
    sol_equations = []
    x_vars = [f'x**{n}' for n in range(ncols-1, -1, -1)]
    for row in range(nrows):
        sol_equations.append(
            sympify(' + '.join(
                [f'{solution_Ab[row, col]} * {x_vars[col]}' for col in range(ncols)]
            ))
        ) 
    piece_values = [
        (remove_zeros(sol_equations[k], truncate_terms), x < x_mid_values[k])
        for k in range(len(x_mid_values))
    ] + [(sol_equations[-1], True)]
    poly_approx = Piecewise(*piece_values)
    na_1column = repeat(nan, ncols).reshape(1, -1)
    solution_Ab_na = vstack([na_1column, solution_Ab])
    N = hstack([N[:, :2], solution_Ab_na])
          
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
def _natural_cubic_splines(N, expr_variable, truncate_terms):

    nrows, ncols = N.shape
    n = nrows
    col_names = [
        f'{expr_variable}',  f'f({expr_variable}) :: a'
    ] + ['b', 'c', 'd']
    x = N[:, 0]
    y = N[:, 1]
    num_points = asfarray(repeat(0, n))
    h = num_points.copy()
    for i in range(n-1):
        h[i] = x[i+1] - x[i]
            
    alpha = num_points.copy()
    for i in range(1, n-1):
        alpha[i] = (3/h[i]) * (y[i+1] - y[i]) - (3/h[i-1]) * (y[i] - y[i-1])   
    l = num_points.copy(); l[0] = 1
    u = num_points.copy(); u[0] = 0
    z = num_points.copy(); z[0] = 0
        
    for i in range(1, n-1):
        l[i] = 2 * (x[i+1] - x[i-1]) - h[i-1] * u[i-1]
        u[i] = h[i]/l[i]
        z[i] = (alpha[i] - h[i-1] * z[i-1])/l[i]
        
    l[-1] = 1
    z[-1] = 0
        
    c = num_points.copy(); c[-1] = 0
    b = num_points.copy()
    d = num_points.copy()
    for j in range(n-2, -1, -1):
        c[j] = z[j] - u[j] * c[j+1]
        b[j] = (y[j+1] - y[j]) / h[j] - h[j] * (c[j+1] + 2 * c[j]) / 3
        d[j] = (c[j+1] - c[j]) / (3 * h[j])
        
    N = vstack([x, y, b, c, d]).T
    M = N[:-1, 1:]
    x_copy = x.copy()
    x_mid_values = x[1:-1]
    x = symbols('x')
    nrows, ncols = M.shape
    sol_equations = []
    for row in range(nrows):
        x_vars = [f'(x - {x_copy[row]})**{n}' for n in range(ncols)]
        fx = ' + '.join(
            [f'{M[row, col]} * {x_vars[col]}' for col in range(ncols)]
        )
        sol_equations.append(sympify(fx)) 
    piece_values = [
        (remove_zeros(sol_equations[k], truncate_terms), x < x_mid_values[k])
        for k in range(len(x_mid_values))
    ] + [(sol_equations[-1], True)]
    poly_approx = Piecewise(*piece_values)

    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
def _clamped_cubic_splines(N, expr_variable, end_points, truncate_terms):

    nrows, ncols = N.shape
    n = nrows
    col_names = [
        f'{expr_variable}', 
        f'f({expr_variable}) :: a'
    ] + ['b', 'c', 'd']
    x = N[:, 0]
    y = N[:, 1]
    end_points = to_listuple(
        array_values=end_points, n=2, to_ndarray=True, par_name='endpoints'
    )
    fp_0, fp_n = end_points
    num_points = repeat(0, n).astype(float64)
    h = num_points.copy()
    for i in range(n-1):
        h[i] = x[i+1] - x[i]
    alpha = num_points.copy()
    alpha[0] = 3 * (y[1] - y[0]) / h[0] - 3 * fp_0
    alpha[-1] = 3 * fp_n - 3 * (y[-1] - y[-2]) / h[-2]
    for i in range(1, n-1):
        alpha[i] = (3/h[i]) * (y[i+1] - y[i]) - (3/h[i-1]) * (y[i] - y[i-1])
    l = num_points.copy()
    l[0] = 2 * h[0]
    u = num_points.copy()
    u[0] = 0.5
    z = num_points.copy()
    z[0] = alpha[0]/l[0]
    for i in range(1, n-1):
        l[i] = 2 * (x[i+1] - x[i-1]) - h[i-1] * u[i-1]
        u[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i-1] * z[i-1]) / l[i]
    l[-1] = h[-2] * (2 - u[-2])
    z[-1] = (alpha[-1] - h[-2] * z[-2]) / l[-1] 
    c = num_points.copy()
    c[-1] = z[-1] 
    b = num_points.copy()
    d = num_points.copy()
    for j in range(n-2, -1, -1):
        c[j] = z[j] - u[j] * c[j+1]
        b[j] = (y[j+1] - y[j]) / h[j] - h[j] * (c[j+1] + 2 * c[j]) / 3
        d[j] = (c[j+1] - c[j]) / (3 * h[j])  
    N = vstack([x, y, b, c, d]).T
    M = N[:-1, 1:]
    x_copy = x.copy()
    x_mid_values = x[1:-1]
    x = symbols('x')
    nrows, ncols = M.shape
    sol_equations = []
    for row in range(nrows):
        x_vars = [f'(x - {x_copy[row]})**{n}' for n in range(ncols)]
        fx = ' + '.join(
            [f'{M[row, col]} * {x_vars[col]}' for col in range(ncols)]
        )
        sol_equations.append(sympify(fx))
    piece_values = [
        (remove_zeros(sol_equations[k], truncate_terms), x < x_mid_values[k]) 
        for k in range(len(x_mid_values))
    ] + [(sol_equations[-1], True)]
    poly_approx = Piecewise(*piece_values)
           
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
def _not_a_knot_splines(N, expr_variable):

    N = N[:, :2]
    col_names = [f'{expr_variable}', f'f({expr_variable})_two_columns_']
    poly_approx = 'NA'
    
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
# Least square methods
# --------------------

def _linear_regression(N, expr_variable):

    # columns with all nan --> index = isnan(arr).any(axis=0) any 
    #  with nan
    index = isnan(N).all(axis = 0)
    # delete the columns with all nan
    N = delete(N, index, axis = 1)
    x = N[:, :N.shape[1]-1]
    y = N[:, -1]
    if len(y.shape) == 1:
        y = y.reshape(-1, 1)
    ncols = x.shape[1]
    if ncols == 1:
        col_names = [
            f'{expr_variable}', f'f({expr_variable})_two_columns_'
        ]
    else:
        col_names = [
            f'{expr_variable}_{k+1}' for k in range(ncols)
        ] + [f'f({expr_variable})_two_columns_']

    model.fit(x, y)
    bi = model.intercept_.tolist() + model.coef_.flatten().tolist()
    xi = [f'x{n}' for n in range(len(bi))]
    bixi = ' + '.join([f'{bi[n]} * {xi[n]}' for n in range(len(bi))])
    bixi = bixi.replace(' ', '').replace('*x0', '')
    if x.shape[1] == 1:
        bixi = bixi.replace('x1', 'x')
    poly_approx = sympify(bixi)
       
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
def _polynomial(N, poly_order, expr_variable):

    col_names = [f'{expr_variable}', f'f({expr_variable})_two_columns_']
    x = N[:, 0]
    y = N[:, 1]
    m = abs(int(poly_order))
    n = len(x)
    poly_order = val_numeric(
        user_input=poly_order, 
        to_float=False, 
        limits=[1, n-1], 
        boundary='inclusive', 
        par_name='poly_order'
    )
    array_coefs = poly1d(polyfit(x, y, m))
    poly_approx = str(Poly(array_coefs, sympify('x')).as_expr())
    
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
#  Linearization
# --------------

def _exponential(N, expr_variable, exp_type):

    col_names = [f'{expr_variable}', f'f({expr_variable})_two_columns_']
    x = N[:, 0]
    y = N[:, 1]
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    if len(y.shape) == 1:
        y = y.reshape(-1, 1)
    if exp_type in ['b*exp(ax)', 'ab^x']:
        y = log(y)
    else:
        y = log10(y)

    model.fit(x, y)
    b0 = model.intercept_[0] # ln b
    b1 = model.coef_[0, 0] # a
    if exp_type == 'b*exp(ax)': # y = b0 exp(b1*x) -->> ln y = ln b0 + b1*x
        b0 = exp(b0)
        bixi = f'{b0} * exp({b1} * x)'
    elif exp_type == 'b*10^ax': # y = b 10^(ax) -->> log10 y = log10 b0 + b1*x
        b0 = 10 ** (b0)
        bixi = f'{b0} * 10 ** ({b1} * x)'
    else:
        b0 = exp(b0)
        b1 = exp(b1)
        bixi = f'{b0} * ({b1})^x'
    poly_approx = sympify(bixi)
    
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
def _power(N, expr_variable):

    col_names = [f'{expr_variable}', f'f({expr_variable})_two_columns_']
    x = N[:, 0]
    y = N[:, 1]
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    if len(y.shape) == 1:
        y = y.reshape(-1, 1)

    x = log(x)
    y = log(y)
    model.fit(x, y) # y = b^(ax) --> ln y = ln b0 + b1 ln x ,
    b0 = model.intercept_[0] # ln b0
    b1 = model.coef_[0, 0] # b1
    b0 = exp(b0)
    bixi = f'{b0} * x ** ({b1})'
    poly_approx = sympify(bixi)
          
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
def _saturation(N, expr_variable, sat_type):

    col_names = [f'{expr_variable}', f'f({expr_variable})_two_columns_']
    x = N[:, 0]
    y = N[:, 1]
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    if len(y.shape) == 1:
        y = y.reshape(-1, 1)
    x = 1/x
    y = 1/y
    
    model.fit(x, y)
    b0 = model.intercept_[0]
    b1 = model.coef_[0, 0]

    # https://web.engr.oregonstate.edu/~webbky/MAE4020_5020_files/Section%207%20Curve%20Fitting.pdf
    if sat_type == 'ax/(x+b)':
        B1 = 1 / b0
        B0 = b1 / b0 # m/c
        bixi = f'{B1} * x / (x + {B0})'
    else:
        bixi = f'x / ({b0} * x + {b1})'
    poly_approx = sympify(bixi)
    
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
def _reciprocal(N, expr_variable):

    col_names = [f'{expr_variable}', f'f({expr_variable})_two_columns_']
    x = N[:, 0]
    y = N[:, 1]
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    if len(y.shape) == 1:
        y = y.reshape(-1, 1)
    y = 1/y

    model.fit(x, y) # y = 1 / (ax + b) --> 1/y = b0 + b1 * x
    b0 = model.intercept_[0] # b0
    b1 = model.coef_[0, 0] # b1
    bixi = f'{1} / ({b1} * x + {b0})'
    poly_approx = sympify(bixi)
        
    style_indices_list = []
    plot = True
    further_analysis = True

    return N, style_indices_list, poly_approx, col_names, plot, further_analysis
    
# p, q = scii.pade(e_exp, 2)
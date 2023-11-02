from math import factorial
from numpy import zeros, append, array, linspace, vstack
from pandas import DataFrame
from sympy import sympify, lambdify, latex, solve
from matplotlib.pyplot import (
    plot, figure, clf, title, xlabel, ylabel, legend, tight_layout
)
from matplotlib.style import context, available
from ..core.errors import (
    NumericBtwnError, FloatError, LowerGEUpperError, SympifyError, 
    VectorLengthError, IntegerError, NotInValuesError
)
from ..core.base import partial_chars
from ..core.arraylike import abrange, to_listuple
from ..core.options import display_options
from ..core.htmlatex import dframe_to_html
from ..core.plotting import figure_encoded

def int_odes(
        method = 'rk4',
        ode_equation='-1.2 * y + 7 * exp(-0.3 * t)',
        exact_solution=None,
        ode_derivs=None,
        ode_system=None,
        method_approx=True,
        start_enter=None,
        start_method='rk4',
        time_span=None,
        initial_y=None,
        stepsize=False,
        step_size=None,
        step_count=10,
        max_iterations=10,
        tolerance=1e-6,
        hmin=None,
        hmax=None,
        show_iters=None,
        to_dict = False,
        col_latex=False,
        decimals=8
):
    """
    Integrate ODEs numerically.

    Parameters
    ----------
    method : {...}, default='rk4'
        The method to be used to integrate the ODE numerically.
        =======================================================================
        Valid value                 Description
        =======================================================================
        'taylor1' ................. Taylor order 1
        'taylor2' ................. Taylor order 2
        'taylor3' ................. Taylor order 3
        'taylor4' ................. Taylor order 4
        'taylor5' ................. Taylor order 5
        'feuler' .................. Explicit Euler
        'meuler' .................. Modified Euler
        'beuler' .................. Implicit Euler
        'rkmidpoint' .............. Midpoint Runge-Kutta
        'rkmeuler' ................ Modified Euler Runge-Kutta
        'r2' ...................... Second order Heun Runge-Kutta
        'heun3' ................... Third order Heun Runge-Kutta
        'n3' ...................... Third order Nystrom Runge-Kutta
        'rk3  ..................... Classical third order Runge-Kutta
        'rk4' ..................... Classical fourth order Runge-Kutta
        'rkm' ..................... Fourth order Runge-Kutta-Mersen
        'rk38' .................... Fourth order Runge-Kutta 3/8
        'rk5' ..................... Classical fifth order Runge-Kutta
        'rkbeuler' ................ Implicit backward Euler Runge-Kutta
        'rktrap' .................. Implicit implicit Trapezoidal Runge-Kutta
        'rk2stage' ................ Implicit 2-stage Gauss-Legendre Runge-Kutta
        'rk3stage' ................ Implicit 3-stage Gauss-Legendre Runge-Kutta
        'rkf' ..................... Adaptive Runge-Kutta-fehlberg
        'rkv' ..................... Adaptive Runge-Kutta-Verner
        'ab2' ..................... Explicit Adam-Bashforth 2 step
        'ab3' ..................... Explicit Adam-Bashforth 3 step
        'ab4' ..................... Explicit Adam-Bashforth 4 step
        'ab5' ..................... Explicit Adam-Bashforth 5 step
        'am2' ..................... Implicit Adam-Moulton 2 step
        'am3' ..................... Implicit Adam-Moulton 3 step
        'am4' ..................... Implicit Adam-Moulton 4 step
        'eheun' ................... Euler-Heun PC
        'abm2' .................... Adam-Bashforth-Moulton 2 step PC
        'abm3' .................... Adam-Bashforth-Moulton 3 step PC
        'abm4' .................... Adam-Bashforth-Moulton 4 step PC
        'abm5' .................... Adam-Bashforth-Moulton 5 step PC
        'ms' ...................... Milne-Simpson PC
        'mms'...................... Modified Milne-Simpson PC
        'hamming' ................. Hammings PC
    ode_equation : {str, symbolic}
        The ODE equation to be integrated numerically.
    time_span : {list, tuple, ndarray}
        Start and end time points (lower and upper limits of integration).
    initial_y : {int, float, list, tuple, ndarray}
        Initial value(s) of the ODE or system of ODEs.
    ode_derivs : {list, tuple}
        A list of derivatives of the ODE equation. Required for Taylor method.
    ode_system : {list, tuple, ndarray}
         A list/tuple of ODEs if integrating a system of ODEs.
    exact_solution : {None, str, symbolic}, default=None
        The exact solution of the ODE.
    method_approx : bool, default=True
        If True, starting values will be approximated using a method specified 
        in ``start_method``.
    start_enter : {list, tuple, ndarray}
        Starting values for multi-step and predictor-corrector method.
    start_method : {'feuler', 'meuler', 'heun3', 'rk4'}, default='rk4'
        Method to be used to approximate the initial values for multi-step and 
        predictor-corrector methods.
    stepsize : bool, default=False
        If True, provide ``step_size``, otherwise provide ``step_count`` below.
    step_size : float, default=None
        The interval (difference between two consecutive time points).
    step_count : int, default=10
        Number of steps (time points).
    max_iterations : int, default=10
        Maximum number of iterations.
    tolerance : float, default=1e-6
        The allowable tolerance.
    hmin : float, default=None
        Minimum value for RKF and RKV methods.
    hmax : float, default=None
        Maximum value for RK-Felhberg and RK-Verner methods.
    show_iters : int, default=None
        Integer representing the number of iterations to be displayed.
        Valid values: None or 1 <= x <= n. If None, then all iterations are 
        displayed.
    to_dict : False
        If True, results will be saved in a dictionary.
    col_latex : bool, default=True
        If True, column headings will be printed in Latex.
    decimals : int, default=8
        Number of decimal points.

    Returns
    -------
    table_df : DataFrame
        A table with the iterative solutions of the integration of ODE(s).
    table_html : str
        HTML code for the above iterative solutions.
    image_html : str
        HTML code for the plotted solution.
    
    if ``to_dict`` is True, the above results are stored in a dictionary.
        
    Examples
    --------
    >> f = 'y - t^2 + 1'
    >> dydx = ['y - t^2 - 2*t + 1', 'y - t^2 - 2*t - 1', 'y - t^2 - 2*t - 1', 'y - t^2 - 2*t - 1']
    >> ft = '(t + 1)^2 - 0.5*exp(t)'
    >> a, b = (0, 2)
    >> y0 = 0.5
    >> h = .2

    ## Taylor order 4

    >> table, figure = stm.int_odes(
        method = 'taylor4',
        ode_equation=f,
        exact_solution=ft,
        time_span=[a, b],
        initial_y=y0,
        ode_derivs=dydx,
        decimals=12
        )
    >> table
        Time (t)  Approximated (yi)  Exact solution(y)  Error: | y - yi |
    0        0.0   0.50000000000000   0.50000000000000   0.00000000000000
    1        0.2   0.82930000000000   0.82929862091992   0.00000137908009
    2        0.4   1.21409102000000   1.21408765117936   0.00000336882064
    3        0.6   1.64894677182800   1.64894059980475   0.00000617202325
    4        0.8   2.12723958711072   2.12722953575377   0.00001005135695
    5        1.0   2.64087443169703   2.64085908577048   0.00001534592656
    6        1.2   3.17996403087476   3.17994153863173   0.00002249224303
    7        1.4   3.73243206731043   3.73240001657766   0.00003205073276
    8        1.6   4.28352852701296   4.28348378780244   0.00004473921051
    9        1.8   4.81523774289362   4.81517626779353   0.00006147510010
    10       2.0   5.30555537917027   5.30547195053467   0.00008342863560

    ## Fourth order Runge-Kutta

    table, figure = stm.int_odes(
        method = 'rk4',
        ode_equation=f,
        exact_solution=ft,
        time_span=[a, b],
        initial_y=y0,
        decimals=12
    )
    >> table
        Time (t)  Approximated (yi)  Exact solution(y)  Error: | y - yi |
    0        0.0   0.50000000000000   0.50000000000000   0.00000000000000
    1        0.2   0.82929333333333   0.82929862091992   0.00000528758658
    2        0.4   1.21407621066667   1.21408765117936   0.00001144051270
    3        0.6   1.64892201704160   1.64894059980475   0.00001858276315
    4        0.8   2.12720268494794   2.12722953575377   0.00002685080582
    5        1.0   2.64082269272875   2.64085908577048   0.00003639304173
    6        1.2   3.17989417023223   3.17994153863173   0.00004736839950
    7        1.4   3.73234007285498   3.73240001657766   0.00005994372268
    8        1.6   4.28340949831841   4.28348378780244   0.00007428948404
    9        1.8   4.81508569457943   4.81517626779353   0.00009057321409
    10       2.0   5.30536300069265   5.30547195053467   0.00010894984202

    ## Adams-Moulton PC with RK4 approximated start values

    >> table, figure = stm.int_odes(
        method = 'am4',
        ode_equation=f,
        exact_solution=ft,
        time_span=[a, b],
        initial_y=y0,
        method_approx=True,
        start_method='rk4',
        decimals=12
    )
    >> table
        Time (t)  Approximated (yi)  Exact solution(y)  Error: | y - yi |
    0        0.0   0.50000000000000   0.50000000000000   0.00000000000000
    1        0.2   0.82929333333333   0.82929862091992   0.00000528758658
    2        0.4   1.21407621066667   1.21408765117936   0.00001144051270
    3        0.6   1.64892201704160   1.64894059980475   0.00001858276315
    4        0.8   2.12720569067661   2.12722953575377   0.00002384507716
    5        1.0   2.64082874144856   2.64085908577048   0.00003034432191
    6        1.2   3.17990290225611   3.17994153863173   0.00003863637561
    7        1.4   3.73235091672886   3.73240001657766   0.00004909984880
    8        1.6   4.28342148841619   4.28348378780244   0.00006229938625
    9        1.8   4.81509733035245   4.81517626779353   0.00007893744107
    10       2.0   5.30537206144074   5.30547195053467   0.00009988909394

    ## Adam-Bashforth PC with exact start values

    >>> start_values = (0.5, 0.829298620919915, 1.2140876511793646, 1.648940599804746)
    >> table, figure = stm.int_odes(
        method = 'ab4',
        ode_equation=f,
        exact_solution=ft,
        time_span=[a, b],
        initial_y=y0,
        method_approx=False,
        start_enter=start_values,
        decimals=12
    )

    ## Runge-Kutta-Felhberb

    >> table, figure = stm.int_odes(
        method = 'rkf',
        ode_equation=f,
        exact_solution=ft,
        time_span=[a, b],
        initial_y=y0,
        hmin=.01,
        hmax=.25,
        tolerance=1e-5,
        decimals=12
    )
    >> table

    ## Systems of equations

    >> 
    """
    dict_methods = {
        'taylor': 'taylor',
        'explicit-euler': 'feuler',
        'modified-euler': 'meuler',
        'implicit-euler': 'beuler',
        'midpoint-runge-kutta': 'rkmidpoint',
        'modified-euler-runge-kutta': 'rkmeuler',
        'second-order-ralston': 'r2',
        'third-order-heun': 'heun3',
        'third-order-nystrom': 'n3',
        'third-order-runge-kutta': 'rk3',
        'fourth-order-runge-kutta': 'rk4',
        'fourth-order-runge-kutta-38': 'rk38',
        'fourth-order-runge-kutta-mersen': 'rkm',
        'fifth-order-runge-kutta': 'rk5',
        'backward-euler': 'rkbeuler',
        'trapezoidal': 'rktrap',
        'two-stage-gauss-legendre': 'rk2stage',
        'three-stage-gauss-legendre': 'rk3stage',
        'adams-bashforth-2-step': 'ab2',
        'adams-bashforth-3-step': 'ab3',
        'adams-bashforth-4-step': 'ab4',
        'adams-bashforth-5-step': 'ab5',
        'adams-moulton-2-step': 'am2',
        'adams-moulton-3-step': 'am3',
        'adams-moulton-4-step': 'am4',
        'euler-heun': 'eheun',
        'adams-bashforth-moulton-2-step': 'abm2',
        'adams-bashforth-moulton-3-step': 'abm3',
        'adams-bashforth-moulton-4-step': 'abm4',
        'adams-bashforth-moulton-5-step': 'abm5',
        'hamming': 'hamming',
        'milne-simpson': 'ms',
        'modified-milne-simpson': 'mms',
        'runge-kutta-fehlberg': 'rkf',
        'runge-kutta-verner': 'rkv',
        'adams-variable-step-size-predictor-corrector': 'avs',
        'extrapolation': 'extra',
        'trapezoidal-with-newton-approximation': 'tn',
        'systems-explicit-euler': 'sfeuler',
        'systems-modified-euler': 'smeuler',
        'systems-third-order-heun': 'sheun3',
        'systems-fourth-order-runge-kutta': 'srk4'
    }

    dict_start = {
        'explicit-euler': 'eeuler',
        'modified-euler': 'meuler',
        'third-order-heun': 'heun3',
        'fourth-order-runge-kutta':'rk4'
    }

    taylor_n = [f'taylor{k+1}' for k in range(5)]
    euler_methods = ['feuler', 'meuler', 'beuler']
    explicit_rk = [
        'rkmidpoint', 'rkmeuler', 'r2', 'heun3', 'n3', 'rk3', 'rk4', 'rk38', 
        'rkm', 'rk5'
    ]
    implicit_rk = ['rkbeuler', 'rktrap', 'rk2stage', 'rk3stage']
    explicit_multistep = ['ab2', 'ab3', 'ab4', 'ab5']
    implicit_multistep = ['am2', 'am3', 'am4']
    predictor_corrector = [
        'eheun', 'abm2','abm3','abm4', 'abm5', 'hamming', 'ms', 'mms'
    ]
    others = ['rkf', 'rkv', 'avs', 'extra', 'tnewton']
    systems_odes = ['sfeuler', 'smeuler', 'sheun3', 'srk4']

    valid_ivp_methods = taylor_n + euler_methods + explicit_rk + \
        implicit_rk + explicit_multistep + implicit_multistep + \
        predictor_corrector + others + systems_odes

    # for app
    dict_methods_app = {v: k for k, v in dict_methods.items()}
    method_app = dict_methods.get(method)
    start_method_app = dict_start.get(start_method)

    display_options()
    # method
    if method not in valid_ivp_methods:
        raise NotInValuesError(
            par_name='method', valid_args=valid_ivp_methods, user_input=method
        )
    
    # show_iters
    if not isinstance(show_iters, int) and show_iters is not None:
        raise IntegerError(par_name='show_iters', user_input=show_iters)
    
    # ode_equation
    try:
        fty = sympify(ode_equation)
        f = lambdify(('t', 'y'), fty, 'numpy')
        f_latex = latex(sympify(ode_equation))
    except:
        raise SympifyError(par_input='ode_equation', user_input=ode_equation)
    
    if method in taylor_n :
        taylor_order = int(method[-1])
        if ode_derivs:
            if isinstance(ode_derivs, str):
                try:
                    ode_derivs = sympify(
                        ode_derivs.replace(' ', '').split(', ')
                    )
                except:
                    raise SympifyError(
                        par_input='ode_derivs', user_input=ode_derivs
                    )
            ode_derivs = to_listuple(ode_derivs, par_name='ode_derivs')
        else:
            derivatives = 'derivative'
            if taylor_order > 1:
                derivatives = 'derivatives'
            raise ValueError(
                f"You must provide {taylor_order} {derivatives} for the "
                f"specified ODE equation, required when 'method=={method}'"
            )
     
    if ode_system:
        if isinstance(ode_system, str):
            try:
                ode_system = sympify(ode_system.replace(' ', '').split(', '))
            except:
                raise SympifyError(user_input=ode_system)
        ode_system = array(to_listuple(ode_system, par_name='ode_system'))
    
    # exact solution is not allowed for systems of equations
    if method in systems_odes:
        if ft: # exact solution
            raise ValueError(
                'A system of equation does not allow the exact solution to be '
                'specified.'
            )
        else:
            if len(ode_system) < 2:
                raise ValueError(
                    f"'ode_system' requires at least 2 ordinary differential "
                    "equations, got 1 equation"
                )
            else:
                # we create a Numpy array of the ODEs
                gf = zeros(0)
                for kth_ode in ode_system:
                    try:
                        g = lambdify((t), sympify(kth_ode), 'numpy')
                        gf = append(gf, g)
                    except Exception as except_error:
                        raise NotImplemented(except_error)

    # exact_solution
    if exact_solution:
        try:
            ft = lambdify('t', sympify(exact_solution), 'numpy')
        except:
            raise SympifyError(user_input=exact_solution)
    else:
        ft = None
    
    # method_approx
    if not isinstance(method_approx, bool):
        method_approx = True

    # time_span
    time_span = to_listuple(time_span, to_ndarray=True, par_name='time_span')
    if len(time_span) == 2:
        if isinstance(time_span[0], (int, float)):
            t0 = time_span[0]
        else:
            raise IntegerError(par_name='time_span [0]', user_input=time_span[0])
        
        if isinstance(time_span[1], (int, float)):
            tf = time_span[1]
        else:
            raise IntegerError(par_name='time_span[1]', user_input=time_span[1])
        
        if t0 >= tf:
            raise LowerGEUpperError(a='t0', b='tf')
    else:
        raise VectorLengthError(
            par_name='time_span', n=2, user_input=time_span
        )
    
    # initial value of y
    if ode_system is None:
        if isinstance(initial_y, (int, float)):
            y0 = initial_y
        else:
            raise IntegerError(par_name='initial_y', user_input=initial_y)
    else: # system of ODEs
        initial_y = to_listuple(initial_y, to_ndarray=True, par_name='initial_y')
    
    # Start step size or interval options
    rkfv = ['rkf', 'rkv']
    if method not in partial_chars(rkfv):
        if stepsize is True:
            if isinstance(step_size, (int, float)):
                h = step_size
                t = abrange(t0, tf, h)
                n = len(t)-1
            else:
                raise NumericBtwnError(
                    par_name='step_size', user_input=step_size
                )
        else:
            if isinstance(step_count, int):
                n = abs(step_count)
                h = float((tf - t0) / n)
                t = linspace(t0, tf, n+1)
            else:
                raise IntegerError(
                    par_name='step_count', user_input=step_count
                )
    else: # adaptive methods
        # hmin
        if not isinstance(hmin, float):
            raise FloatError(par_name='hmin', user_input=hmin)
        
        # hmax
        if not isinstance(hmax, float):
            raise FloatError(par_name='hmax', user_input=hmax)
        
        if hmin >= hmax:
            raise LowerGEUpperError(a='hmin', b='hmax')
        
        # tolerance
        if not isinstance(tolerance, float):
            raise FloatError(par_name='tolerance', user_input=tolerance)
    
    # maximum iterations for Trapezoidal newton method
    if method == 'tnewton':
        if max_iterations:
            if not isinstance(max_iterations, int):
                raise IntegerError(
                    par_name='max_iterations', user_input=max_iterations
                )
            if  1 <= max_iterations <= n:
                N = int(max_iterations)
            else:
                raise NumericBtwnError(
                    par_name='max_iterations', 
                    limits=[1, n], 
                    user_input=max_iterations
                )
        else:
            N = n+1

    y = zeros(n+1)
    y[0] = y0

    # show_iters
    if show_iters is None:
        show_iters = n
    else:
        if show_iters <= n:
            n = show_iters

    if method in predictor_corrector + explicit_multistep + implicit_multistep:
        m = 5
        if method_approx is True:
            if start_method == 'feuler':
                for i in range(m):
                    h = t[i+1] - t[i]
                    y[i+1] = y[i] + h * f(t[i], y[i])
            elif start_method == 'meuler':
                for i in range(m):
                    h = t[i+1] - t[i]
                    k1 = h * f(t[i], y[i])
                    k2 = h * f(t[i] + h, y[i] + k1)
                    y[i+1] = y[i] + (1/2) * (k1 + k2)
            elif start_method == 'heun3':
                for i in range(m):
                    h = t[i+1] - t[i]
                    k1 = h * f(t[i], y[i])
                    k2 = h * f(t[i] + (1/3) * h, y[i] + (1/3) * k1)
                    k3 = h * f(t[i] + (2/3) * h, y[i] + (2/3) * k2)
                    y[i+1] = y[i] + (1/4) * (k1 + 3 *  k3)   
            elif start_method == 'rk4':
                for i in range(m):
                    h = t[i+1] - t[i]
                    k1 = h * f(t[i], y[i])
                    k2 = h * f(t[i] + h/2, y[i] + k1/2)
                    k3 = h * f(t[i] + h/2, y[i] + k2/2)
                    k4 = h * f(t[i] + h, y[i] + k3)
                    y[i+1] = y[i] + 1/6 * (k1 + 2 * k2 + 2 * k3 + k4)
        else:
            start_enter = array(to_listuple(start_enter, par_name='start_enter'))
            # check  each of the methods and number of values given
            y[:len(start_enter)] = start_enter

    # decimal points
    if isinstance(decimals, int):
        if not (0 <= decimals <= 14):
            raise NumericBtwnError(
                par_name='decimals', 
                limits=[0, 14], 
                boundary='inclusive',
                user_input=decimals
            )
    else:
        raise IntegerError(
            par_name='decimals', limits=None, user_input=decimals
        )
    
    if not isinstance(to_dict, bool):
        to_dict = False
    
    if not isinstance(col_latex, bool):
        col_latex = False
    
    # --------------------------------------------------------------------------
        # begin implimenting the methods
    # --------------------------------------------------------------------------

    # taylor
    
    if 'taylor' in method:
        result = _taylor(fty, ode_derivs, taylor_order, y, t, n)

    # euler

    if method == 'feuler':
        result = _feuler(f, t, y, n)

    if method == 'meuler':
        result = _meuler(f, t, y, n)

    if method == 'beuler':
        result = _beuler(f, t, y, n)

    # explicit runge-kutta

    if method == 'rkmidpoint':
        result = _rkmid(f, t, y, n)

    if method == 'rkmeuler':
        result = _rkmeuler(f, t, y, n)

    if method == 'r2':
        result = _ralston2(f, t, y, n)

    if method == 'heun3':
        result = _heun3(f, t, y, n)

    if method == 'n3':
        result = _nystrom3(f, t, y, n)

    if method == 'rk3':
        result = _rk3(f, t, y, n)

    if method == 'rk4':
        result = _rk4(f, t, y, n)

    if method == 'rk38':
        result = _rk38(f, t, y, n)

    if method == 'rkm':
        result = _rkm(f, t, y, n)

    if method == 'rk5':
        result = _rk5(f, t, y, n)

    # implicit runge-kutta

    if method == 'rkbeuler':
        result = _rkbeuler(f, t, y, n)

    if method == 'rktrap':
        result = _rktrap(f, t, y, n)

    if method == 'rk2stage':
        result = _rk2stage(f, t, y, n)

    if method == 'rk3stage':
        result = _rk3stage(f, t, y, n)

    # explicit multi-step

    if method == 'ab2':
        result = _ab2(f, t, y, n)

    if method == 'ab3':
        result = _ab3(f, t, y, n)

    if method == 'ab4':
        result = _ab4(f, t, y, n)

    if method == 'ab5':
        result = _ab5(f, t, y, n)

    # implicit multi-step

    if method == 'am2':
        result = _am2(f, fty, t, y, n)

    if method == 'am3':
        result = _am3(f, fty, t, y, n)

    if method == 'am4':
        result = _am4(f, fty, t, y, n)
    
    # predictor-corrector

    if method == 'eheun':
        result = _eheun(f, t, y, n)

    if method == 'abm2':
        result = _abm2(f, t, y, n)

    if method == 'abm3':
        result = _abm3(f, t, y, n)

    if method == 'abm4':
        result = _abm4(f, t, y, n)

    if method == 'abm5':
        result = _abm5(f, t, y, n)

    if method == 'hamming':
        result = _hamming(f, t, y, n)

    if method == 'ms':
        result = _milne_simpson(f, t, y, n)

    if method == 'mms':
        result = _mm_simpson(f, t, y, n)

    # other methods

    if method == 'rkf':
        result = _rkf(f, t, y, n)

    if method == 'rkv':
        result = _rkv(f, t, y, n)

    if method == 'avs':
        result = _avs(f, t, y, n)

    if method == 'extra':
        result = _extrapolation(f, t, y, n)

    if method == 'tnewton':
        result = _tnewton(f, t, y, n)

    # systems of odes

    if method == 'sfeuler':
        result = _sfeuler(f, t, y, n)

    if method == 'smeuler':
        result = _smeuler(f, t, y, n)

    if method == 'sheun3':
        result = _sheun3(f, t, y, n)

    if method == 'srk4':
        result = _srk4(f, t, y, n)
    
    # Exact solution
    # result is dframe_html
    t_exact, y_exact, dframe_results, dframe_html = _table_results(
        exact_solution, t0, tf, ft, t, y, show_iters, col_latex, decimals
    )
    # Plot figure
    figure_html = plot_odes(
        method,
        exact_solution,
        f_latex,
        t_exact,
        y_exact,
        dframe_results
    )
    
    if to_dict is True:
        result_dict = {
            'dframe_results': dframe_results,
            'dframe_html': dframe_html,
            'figure_html': figure_html
        }
        return result_dict

    return dframe_results, figure_html

def _taylor(fty, ode_derivs, taylor_order, y, t, n):
    taylor_eqtn_derivs = [fty] + ode_derivs
    if taylor_order == 1:
        f1 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[0]), 'numpy')
        for i in range(n):
            h = t[i+1] - t[i]
            d1f = f1(t[i], y[i])
            y[i+1] = y[i] + (h/factorial(1)) * d1f
    elif taylor_order == 2:
        f1 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[0]), 'numpy')
        f2 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[1]), 'numpy')
        for i in range(n):
            h = t[i+1] - t[i]
            d1f = f1(t[i], y[i])
            d2f = f2(t[i], y[i])
            y[i+1] = y[i] + (h/factorial(1)) * d1f + (h**2/factorial(2)) * d2f
    elif taylor_order == 3:
        f1 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[0]), 'numpy')
        f2 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[1]), 'numpy')
        f3 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[2]), 'numpy')
        for i in range(n):
            h = t[i+1] - t[i]
            d1f = f1(t[i], y[i])
            d2f = f2(t[i], y[i])
            d3f = f3(t[i], y[i])
            y[i+1] = y[i] + (h/factorial(1)) * d1f + \
                (h**2/factorial(2)) * d2f + (h**3/factorial(3)) * d3f
    elif taylor_order == 4:
        f1 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[0]), 'numpy')
        f2 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[1]), 'numpy')
        f3 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[2]), 'numpy')
        f4 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[3]), 'numpy')
        for i in range(n):
            h = t[i+1] - t[i]
            d1f = f1(t[i], y[i])
            d2f = f2(t[i], y[i])
            d3f = f3(t[i], y[i])
            d4f = f4(t[i], y[i])
            y[i+1] = (
                y[i] + (h/factorial(1)) * d1f +
                (h**2/factorial(2)) * d2f + (h**3/factorial(3)) * d3f + 
                (h**4/factorial(4)) * d4f
            )
    elif taylor_order == 5:
        f1 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[0]), 'numpy')
        f2 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[1]), 'numpy')
        f3 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[2]), 'numpy')
        f4 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[3]), 'numpy')
        f5 = lambdify(('t', 'y'), sympify(taylor_eqtn_derivs[4]), 'numpy')
        for i in range(n):
            h = t[i+1] - t[i]
            d1f = f1(t[i], y[i])
            d2f = f2(t[i], y[i])
            d3f = f3(t[i], y[i])
            d4f = f4(t[i], y[i])
            d5f = f5(t[i], y[i])
            y[i+1] = (
                y[i] + (h/factorial(1)) * d1f + 
                (h**2/factorial(2)) * d2f + (h**3/factorial(3)) * d3f + 
                (h**4/factorial(4)) * d4f + (h**5/factorial(5)) * d5f
            )

    return y

def _feuler(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        y[i+1] = y[i] + h * f(t[i], y[i])

    return y

def _meuler(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        ynew = y[i] + h * f(t[i], y[i])
        y[i+1] = y[i] + (h/2) * (f(t[i], y[i]) + f(t[i+1], ynew))

    return y

def _beuler(fty, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        fs_symbolic = str(fty).replace('t', '(' + str(t[i+1]) + ')')
        fs_symbolic = fs_symbolic.replace('y', 'y' + str(i))
        fs_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + str(h) + \
            ' * (' + str(fs_symbolic) + '))'
        y[i+1] = solve(fs_symbolic)[0]

    return y

def _rkmid(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h/2, y[i] + k1/2)
        y[i+1] = y[i] + k2

    return y

def _rkmeuler(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h, y[i] + k1)
        y[i+1] = y[i] + (1/2) * (k1 + k2)
        
    return y

def _ralston2(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + (3/4) * h, y[i] + (3/4) * k1)
        y[i+1] = y[i] + (1/3) * (k1 + 2 * k2)

    return y

def _heun3(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + (1/3) * h, y[i] + (1/3) * k1)
        k3 = h * f(t[i] + (2/3) * h, y[i] + (2/3) * k2)
        y[i+1] = y[i] + (1/4) * (k1 + 3 *  k3)

    return y

def _nystrom3(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + 2/3 * h, y[i] + 2/3 * k1)
        k3 = h * f(t[i] + 2/3 * h, y[i] + 2/3 * k2)
        y[i+1] = y[i] + (1/8) * (2 * k1 + 3 * k2 + 3 * k3)

    return y

def _rk3(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h/2, y[i] + 1/2 * k1)
        k3 = h * f(t[i] + h, y[i] - k1 + 2 * k2)
        y[i+1] = y[i] + (1/6) * (k1 + 4 * k2 + k3)

    return y

def _rk4(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h/2, y[i] + k1/2)
        k3 = h * f(t[i] + h/2, y[i] + k2/2)
        k4 = h * f(t[i] + h, y[i] + k3)
        y[i+1] = y[i] + 1/6 * (k1 + 2 * k2 + 2 * k3 + k4)

    return y

def _rk38(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + 1/3 * h, y[i] + 1/3 * k1)
        k3 = h * f(t[i] + 2/3 * h, y[i] - 1/3 * k1 + k2)
        k4 = h * f(t[i] + h, y[i] + k1 - k2 + k3)
        y[i+1] = y[i] + (1/8) * (k1 + 3 * k2 + 3 * k3 + k4)

    return y

def _rkm(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h/3, y[i] + k1/3)
        k3 = h * f(t[i] + h/2, y[i] + k1/6 + k2/6)
        k4 = h * f(t[i] + h/2, y[i] + k1/8 + 3/8 * k3)
        k5 = h * f(t[i] + h, y[i] + k1/2 - 3/2 * k3 + 2 * k4)
        y[i+1] = y[i] + (1/6) * (k1 + 4 * k2 + k5)

    return y

def _rk5(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h/4, y[i] + (1/4) * k1)
        k3 = h * f(t[i] + h/4, y[i] + (1/8) * k1 + (1/8) * k2)
        k4 = h * f(t[i] + h/2, y[i] - (1/2) * k2 + k3)
        k5 = h * f(t[i] + (3 * h)/4, y[i] + (3/16) * k1 + (9/16) * k4)
        k6 = h * f(t[i] + h, y[i] - (3/7) * k1 + (2/7) * k2 + \
                   (12/7) * k3 - (12/7) * k4 + (8/7) * k5)
        y[i+1] = y[i] + \
            (1/90) * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)

    return y

def _rkbeuler(f, t, y, n):

    return y

def _rktrap(f, t, y, n):

    return y

def _rk2stage(f, t, y, n):

    return y

def _rk3stage(f, t, y, n):

    return y

def _ab2(f, t, y, n):

    for i in range(1, n):
        h = t[i+1] - t[i]
        y[i+1] = y[i] + (h/2) * (3 * f(t[i], y[i]) - f(t[i-1], y[i-1]))

    return y

def _ab3(f, t, y, n):

    for i in range(2, n):
        h = t[i+1] - t[i]
        y[i+1] = y[i] + (h/12) * (23 * f(t[i], y[i]) - 
                                  16 * f(t[i-1], y[i-1]) + 
                                  5 * f(t[i-2], y[i-2]))
    
    return y

def _ab4(f, t, y, n):

    for i in range(3, n):
        h = t[i+1] - t[i]
        y[i+1] = y[i] + (h/24) * (55 * f(t[i], y[i]) - 
                                  59 * f(t[i-1], y[i-1]) + 
                                  37 * f(t[i-2], y[i-2]) - 
                                  9 * f(t[i-3], y[i-3]))
    
    return y

def _ab5(f, t, y, n):

    for i in range(4, n):
        h = t[i+1] - t[i]
        y[i+1] = y[i] + (h/720) * (1901 * f(t[i], y[i]) - 
                                   2774 * f(t[i-1], y[i-1]) + 
                                   2616 * f(t[i-2], y[i-2]) - 
                                   1274 * f(t[i-3], y[i-3]) + 
                                   251 * f(t[i-4], y[i-4]))
    
    return y

def _am2(f, fty, t, y, n):

    for i in range(1, n):
        h = t[i+1] - t[i]
        fty_symbolic = str(fty).replace('t', '(' + str(t[i+1]) + ')')
        fty_symbolic = fty_symbolic.replace('y', 'y' + str(i))
        fty_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + str(h/12) +\
            ' * (5 * (' + str(fty_symbolic) + ') + ' + \
                str(8 * f(t[i], y[i]) - f(t[i-1], y[i-1])) + '))'
        y[i+1] = solve(fty_symbolic)[0]

    return y

def _am3(f, fty, t, y, n):

    for i in range(2, n):
        h = t[i+1] - t[i]
        fty_symbolic = str(fty).replace('t', '(' + str(t[i+1]) + ')')
        fty_symbolic = fty_symbolic.replace('y', 'y' + str(i))
        fty_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + \
            str(h/24) + ' * (9 * (' + str(fty_symbolic) + ') + ' + \
            str(19 * f(t[i], y[i]) - 5 * f(t[i-1], y[i-1]) + f(t[i-2], y[i-2])) \
                + '))'
        y[i+1] = solve(fty_symbolic)[0]

    return y

def _am4(f, fty, t, y, n):
    
    for i in range(3, n):
        h = t[i+1] - t[i]
        fty_symbolic = str(fty).replace('t', f'({t[i+1]})')
        fty_symbolic = fty_symbolic.replace('y', f'y{i}')
        fty_symbolic = f'y{i} - ({y[i]} + {h/720} * (251 * ({fty_symbolic}) + {646 * f(t[i], y[i]) - 264 * f(t[i-1], y[i-1]) + 106 * f(t[i-2], y[i-2]) - 19 * f(t[i-3], y[i-3])}))'
        y[i+1] = solve(fty_symbolic)[0]

    return y

# =========================================================================
    # Predictor-corrector methods
# =========================================================================

def _eheun(f, t, y, n):

    for i in range(n):
        h = t[i+1] - t[i]
        # Explicit Euler as predictor
        y[i+1] = y[i] + h * f(t[i], y[i])
        # Heun as corrector
        y[i+1] = y[i] + (h/2) * (f(t[i+1], y[i+1]) + f(t[i], y[i]))

    return y

def _abm2(f, t, y, n):

    for i in range(1, n):
        h = t[i+1] - t[i]
        # Adams-Bashforth 2-step as predictor
        y[i+1] = y[i] + (h/2) * (3 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
        # Adams-Moulton 2-step as corrector
        y[i+1] = y[i] + (h/2) * (f(t[i+1], y[i+1]) + f(t[i], y[i]))

    return y

def _abm3(f, t, y, n):

    for i in range(2, n):
        h = t[i+1] - t[i]
        # Adams-Bashforth 3-step as predictor
        y[i+1] = y[i] + (h/12) * (
            23 * f(t[i], y[i]) - 16 * f(t[i-1], y[i-1]) + 5 * f(t[i-2], y[i-2])
        )
        # Adams-Moulton 2-step as corrector
        y[i+1] = y[i] + (h/12) * (
            5 * f(t[i+1], y[i+1]) + 8 * f(t[i], y[i]) - f(t[i-1], y[i-1])
        )

    return y

def _abm4(f, t, y, n):

    for i in range(3, n):
        h = t[i+1] - t[i]
        # Adams-Bashforth 4-step as predictor
        y[i+1] = y[i] + (h/24) * (
            55 * f(t[i], y[i]) - 
            59 * f(t[i-1], y[i-1]) + 
            37 * f(t[i-2], y[i-2]) - 
            9 * f(t[i-3], y[i-3])
        )
        # Adams-Moulton 3-step as corrector
        y[i+1] = y[i] + (h/24) * (
            9 * f(t[i+1], y[i+1]) + 
            19 * f(t[i], y[i]) - 
            5 * f(t[i-1], y[i-1]) + 
            f(t[i-2], y[i-2])
        )

    return y

def _abm5(f, t, y, n):

    for i in range(4, n):
        h = t[i+1] - t[i]
        # Adams-Bashforth 5-step as predictor
        y[i+1] = y[i] + (h/720) * (
            1901 * f(t[i], y[i]) - 
            2774 * f(t[i-1], y[i-1]) + 
            2616 * f(t[i-2], y[i-2]) - 
            1274 * f(t[i-3], y[i-3]) + 
            251 * f(t[i-4], y[i-4])
        )
        # Adams-Moulton 4-step as corrector
        y[i+1] = y[i] + (h/720) * (
            251 * f(t[i+1], y[i+1]) + 
            646 * f(t[i], y[i]) - 
            264 * f(t[i-1], y[i-1]) + 
            106 * f(t[i-2], y[i-2]) - 
            19 * f(t[i-3], y[i-3])
        )
    
    return y

def _hamming(f, t, y, n):

    for i in range(3, n):
        h = t[i+1] - t[i]
        # Milne as predictor
        y[i+1] = y[i-3] + (4 * h/3) * (
            2 * f(t[i], y[i]) - f(t[i-1], y[i-1]) + 2 * f(t[i-2], y[i-2])
        )
        # Hamming as corrector
        y[i+1] = (9 * y[i] - y[i-2]) / 8 + (3 * h/8) * (
            f(t[i+1], y[i+1]) + 2 * f(t[i], y[i]) - f(t[i-1], y[i-1])
        )

    return y

def _milne_simpson(f, t, y, n):

    for i in range(3, n):
        h = t[i+1] - t[i]
        # Milne as predictor
        y[i+1] = y[i-3] + (4 * h/3) * (
            2 * f(t[i], y[i]) - f(t[i-1], y[i-1]) + 2 * f(t[i-2], y[i-2])
        )
        # Simpson as corrector
        y[i+1] = y[i-1] + (h/3) * (
            f(t[i+1], y[i+1]) + 4 * f(t[i], y[i]) + f(t[i-1], y[i-1])
        )

    return y

def _mm_simpson(f, t, y, n):

    for i in range(3, n):
        h = t[i+1] - t[i]
        # Milne as predictor
        y[i+1] = y[i-3] + (4 * h/3) * (
            2 * f(t[i], y[i]) - f(t[i-1], y[i-1]) + 2 * f(t[i-2], y[i-2])
        )
        # Modifier
        y[i+1] = y[i+1] + (28/29) * (y[i] - y[i-1])
        # Simpson as corrector
        y[i+1] = y[i-1] + (h/3) * (
            f(t[i+1], y[i+1]) + 4 * f(t[i], y[i]) + f(t[i-1], y[i-1])
        )

    return y

def _rkf(f, t, y, hmin, hmax, tolerance, n):

    t = t[0]
    tf = t[1]
    y = t[0]
    h = hmax

    T = array([t])
    Y = array([y])

    while t < tf:

        if t + h > tf:
            h = tf - t

        k1 = h * f(t, y)
        k2 = h * f(t + h/4, y + 1/4 * k1)
        k3 = h * f(t + 3/8 * h, y + 3/32 * k1 + 9/32 * k2)
        k4 = h * f(
            t + 12/13 * h, 
            y + 1932/2197 * k1 - 7200/2197 * k2 + 7296/2197 * k3
        )
        k5 = h * f(
            t + h, 
            y + 439/216 * k1 - 8 * k2 + 3680/513 * k3 - 845/4104 * k4
        )
        k6 = h * f(
            t + h/2, 
            y - 8/27 * k1 + 2 * k2 - 3544/2565 * k3 + 1859/4104 * k4 - 11/40 * k5
        )

        R = (1/h) * abs(
            1/360 * k1 - 128/4275 * k3 - 2197/75240 * k4 + 1/50 * k5 + 2/55 * k6
        )
        
        if len(R.shape) > 0:
            R = max(R)
        if R <= tolerance:
            t = t + h
            y = y + 25/216 * k1 + 1408/2565 * k3 + 2197/4104 * k4 - 1/5 * k5
            
            T = append(T, t)
            Y = append(Y, y)
            
        h = h * min(max(0.84 * (tolerance / R) ** (1/4), 0.1), 4.0)

        if h > hmax:
            h = hmax
        elif h < hmin:
            break
    y = Y

    return y

def _rkv(f, t, y, n):

    return y

def _avs(f, t, y, n):

    return y

def _extrapolation(f, t, y, n):

    return y

def _tnewton(f, t, y, n):

    return y

def _sfeuler(f, t, y, n):

    return y

def _smeuler(f, t, y, n):

    return y

def _sheun3(f, t, y, n):

    return y

def _srk4(f, t, y, n):

    return y

# -----------------------------------------------------
# Table of results 
# -----------------------------------------------------

def _table_results(exact_solution, t0, tf, ft, t, y, show_iters, col_latex, decimals):
    """
    Create a table of results.
    """
    show_iters = show_iters+1
    t_exact, y_exact = (0, 0)
    if exact_solution:
        t_exact = linspace(t0, tf, 250)
        y_exact = ft(t_exact)
        y_time_span = ft(t)
        absolute_error = abs(y_time_span - y)
        table_results = vstack([t, y, y_time_span, absolute_error]).T
        if col_latex is True:
            col_names = [
                '$\\text{Time }(t_{i})$',
                '$\\text{Approx. }(\\hat{y}_{i})$',
                '$\\text{Exact }(y_{i})$',
                '$\\text{ Error: }| y_{i} - \\hat{y}_{i} |$'
            ]
        else:
            col_names = [
                'Time (t)', 
                'Approximated (yi)', 
                'Exact solution(y)', 
                'Error: | y - yi |'
                ]
    else:
        table_results = vstack([t, y]).T
        if col_latex is True:
            col_names = [
                '$\\text{Time }(t_{i})$', '$\\text{Approx. }(\\hat{y}_{i})$'
            ]
        else:
            col_names = ['Time (t)', 'Approximated (yi)']

    table_results = table_results[:show_iters, :]
    table_results = DataFrame(
        table_results, 
        columns=col_names
    )
    
    table_results = table_results.round(decimals)

    dframe_html = dframe_to_html(dframe=table_results, row_title='$i$')

    return t_exact, y_exact, table_results, dframe_html

# -----------------------------------------------------
# Plotting 
# -----------------------------------------------------

def plot_odes(
        method, exact_solution, f_latex, t_exact, y_exact, table_results
):
    """
    Plot the ODE equation(s).
    """
    valid_figure_styles = available
    figure_properties = [
        'fast', 7, 5, 'D', 'b', 6, '-', 'b', 1.5, 
        r'$ f(t, y) = ' + f_latex + '$', 'Time (t)', 
        'Solution (y)', 'k', 13
    ]
    figure_style, figure_width, figure_height, figure_marker, figure_markerfacecolor, figure_markersize, figure_linestyle, figure_color, figure_linewidth, figure_title, figure_xtitle, figure_ytitle, figure_fontcolor, figure_fontsize = figure_properties
    
    if figure_style not in valid_figure_styles:
        raise ValueError(f"'{figure_style}' is an invalid plot style.")
    
    clf()
    with context(figure_style):
        figure(figsize = (figure_width, figure_height))
        if exact_solution:
            plot(t_exact, y_exact, 'r', linewidth = 2, label='Exact')
        
        tab_results = table_results.values
        n = tab_results.shape[0]
        if 'system' in method:
            tab_results = table_results[:n, :]
            if n <= 30: # add marker symbols
                for i in range(tab_results.shape[1]):
                    plot(
                        tab_results[:, 0],
                        tab_results[:, i],
                        marker = figure_marker,
                        label=f'{i+1}'
                    )
            else: # do not add marker symbols
                for i in range(tab_results.shape[1]):
                    plot(tab_results[:, 0], tab_results[:, i], label=f'{i+1}')
        else:
            if n <= 30:
                plot(
                    tab_results[:, 0],
                    tab_results[:, 1],
                    linestyle = figure_linestyle,
                    color = figure_color,
                    linewidth = figure_linewidth,
                    marker = figure_marker,
                    markersize = figure_markersize,
                    markerfacecolor = figure_markerfacecolor,
                    label='Solution'
                )
            else: 
                plot(
                    tab_results[:, 0],
                    tab_results[:, 1],
                    linestyle = figure_linestyle,
                    color = figure_color,
                    linewidth = figure_linewidth,
                    label='Solution'
                )
            legend(
                loc = 'best', 
                ncol = 2,
                prop = {'family': 'calibri', 'weight': 'normal', 'size': 12}
            )
            
        figure_fontdict = {'color': figure_fontcolor, 'size': figure_fontsize}
        title(figure_title, fontdict = figure_fontdict)
        xlabel(figure_xtitle, fontdict = figure_fontdict)
        ylabel(figure_ytitle, fontdict = figure_fontdict)
        tight_layout()
                
        figure_html = figure_encoded()

    return figure_html

from numpy import (
    sqrt, nan, round, isnan, zeros, argmax, dot
)
from sympy import sympify
from pandas import DataFrame, set_option
from ..core.symbolic import lambdify_expr
from ..core.arraylike import to_listuple
from ..core.options import display_options
from ..statistical.wrangle import dframe_labels
from ..core.errors import (
    NoRootInInterval, VectorLengthError, LowerGEUpperError
)
from ..core.validate import (
    val_decimals, val_listitems, val_numeric, val_boolean
)
from ..core.info_messages import info_messages

def _stop_crit(stop_crit='relative'):
    """
    Return a DataFrame title for the stopping criterion.
    """
    if 'ab' in stop_crit:
        stop_crit = 'Absolute error'
    elif 'f(root)' in stop_crit:
        stop_crit = 'Function'
    else:
        stop_crit = 'Relative error'
    
    return stop_crit
    
def _kth_error(stop_crit, b, p):
    """
    Calculate the error at the kth iteration of non-linear methods.
    """
    if stop_crit == 'absolute':
        kth_error = abs(p - b)
    else:
        if p == 0:
            p = 1e-14 # avoid division by 0
        kth_error = abs((p - b) / p)

    return kth_error

def _gauss_pivot(A, b):
    """
    Gaussian elimination with Pivoting.
    """
    n = len(b)
    s = zeros(n)
    for i in range(n):
        s[i] = max(abs(A[i, :]))
    for k in range(n-1):
        p = argmax(abs(A[k:n, k]) / s[k:n]) + k
        if p != k:
            _swap_rows(b, k, p)
            _swap_rows(s, k, p)
            _swap_rows(A, k, p)
        for i in range(k+1, n):
            if A[i, k] != 0.:
                lam = A[i, k] / A[k, k]
                A[i, (k+1):n] -= lam * A[k, (k+1):n]
                b[i] -= lam * b[k]
    b[n-1] /= A[n-1, n-1]
    for k in range(n-2, -1, -1):
        b[k] = (b[k] - dot(A[k, (k+1):n], b[(k+1):n])) / A[k, k]
    
    return b

def _swap_rows(M, i, j):
    """
    Swap rows of a matrix.
    """
    if len(M.shape) == 1:
        M[i], M,[j] = (M[j], M[i])
    else:
        M[[i, j], :] = M[[j, i], :]

def roots_nonlinear(
        method, 
        expr_f,
        start_with, 
        tol=1e-6, 
        maxit=10, 
        stop_crit='relative', 
        index_labels=0,
        to_dict=False,
        decimals=8
):
    """
    ```

    Evaluate the root(s) of a non-linear equation or a system of non-linear 
    equations

    Parameters
    ----------
    method : {bisection, ..., steffensen}
        The nonlinear method to be used to calculate the root of the 
        univariate function.
        ======================================================================
        Argument                    Description
        ======================================================================
        bisection ................. Bisection
        regula-falsi .............. Regula-Falsi / False position
        mregula-falsi ............. Modified Regula-Falsi 
        secant .................... Secant
        fixed-point ............... Fixed point iteration
        newton-raphson ............ Newton-Raphson
        mnewton-raphson ........... Modified Newton-Raphson
        aitken .................... Aitken
        steffensen ................ Steffensen
        system .................... System of nonlinear equations using Newton 
                                    Rapshson method
        ======================================================================
    expr_f : {str, symbolic}
        A univariate function whose root we seek.
    start_with : {int, float, list}
        The starting value as integer/float for open methods or 
        a list of two elements [a, b] for closed methods.
    tol : float, default=1e-6
        Tolerance level, algorithm will stop if the difference between 
        consecutive values falls below this value.
    maxit : int, default=10
        Maximum number of iterations to be performed.
    stop_crit : {absolute, relative}, default='relative'
        Specifies the criterion to be used to stop the iterations.
        ========================================================
        Argument                    Description
        ========================================================
        absolute .................. Calculate the absolute error
        relative .................. Calculate the relative error
        ========================================================
    index_labels : {int, array_like, None}, default=0
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels
        None .............. Will remove the DataFrame index       
        ==============================================================
    to_dict : bool, default=False
        If true, result will be returned as a dictionary.
    decimals : int, default=8
        Number of decimal points.
        
    Returns
    -------
    result : {tuple, dict}
        result_table : DataFrame
            A table with the approximated roots and error at each iteration.
        root : Float
            The approximated root (within the specified closed interval).
        info_msg : list
            Informational messages, if any.

    Examples
    --------
    # Bisection method
    # ----------------
    >> method = 'bisection'
    >> f = '3**(3*x + 1) - 7.5**(2*x)'
    >> a, b = (1, 2)
    >> table, root, msg = stm.roots_nonlinear(method, expr_f=f, start_with=[a, b], tol=1e-6, maxit=20, decimals=10)
    >> table
               $a_n$         $b_n$         $p_n$       $f(p_n)$  Relative error
    0   1.0000000000  2.0000000000  1.5000000000  -0.9866537608    0.3333333333
    1   1.0000000000  1.5000000000  1.2500000000  30.5931023150    0.2000000000
    2   1.2500000000  1.5000000000  1.3750000000  23.8417046249    0.0909090909
    3   1.3750000000  1.5000000000  1.4375000000  14.5912606133    0.0434782609
    4   1.4375000000  1.5000000000  1.4687500000   7.7399012107    0.0212765957
    5   1.4687500000  1.5000000000  1.4843750000   3.6319491455    0.0105263158
    6   1.4843750000  1.5000000000  1.4921875000   1.3892750639    0.0052356021
    7   1.4921875000  1.5000000000  1.4960937500   0.2183288849    0.0026109661
    8   1.4960937500  1.5000000000  1.4980468750  -0.3798619425    0.0013037810
    9   1.4960937500  1.4980468750  1.4970703125  -0.0796971815    0.0006523157
    10  1.4960937500  1.4970703125  1.4965820312   0.0695824695    0.0003262643
    11  1.4965820312  1.4970703125  1.4968261719  -0.0049906118    0.0001631055
    12  1.4965820312  1.4968261719  1.4967041016   0.0323126036    0.0000815594
    13  1.4967041016  1.4968261719  1.4967651367   0.0136651660    0.0000407780
    14  1.4967651367  1.4968261719  1.4967956543   0.0043383198    0.0000203886
    15  1.4967956543  1.4968261719  1.4968109131  -0.0003258853    0.0000101942
    16  1.4967956543  1.4968109131  1.4968032837   0.0020062824    0.0000050971
    17  1.4968032837  1.4968109131  1.4968070984   0.0008402148    0.0000025486
    18  1.4968070984  1.4968109131  1.4968090057   0.0002571688    0.0000012743
    19  1.4968090057  1.4968109131  1.4968099594  -0.0000343572    0.0000006371
    >> root
    1.49680995940000
    >> msg
    ['The maximum number of iterations (20) was reached before achieving the tolerance (1e-12).']

    # Newton-Raphson method
    # ---------------------
    >> method = 'newton-raphson'
    >> f = '3**(3*x + 1) - 7.5**(2*x)'
    >> table, root, msg = stm.roots_nonlinear(method, expr_f=f, start_with=1.25, tol=1e-12, maxit=20, decimals=14)
    >> table
                   $p_n$    Relative error
    0   1.25000000000000  0.66669188030705
    1   3.75028367491173  0.06773235047431
    2   3.51238179984504  0.07186672439981
    3   3.27688295558555  0.07634631035037
    4   3.04445040046532  0.08113233632514
    5   2.81598311157139  0.08610803875448
    6   2.59272835766937  0.09100250152036
    7   2.37646417314010  0.09524395984151
    8   2.16980349609415  0.09768487161101
    9   1.97670893733795  0.09613684032277
    10  1.80334139372224  0.08685708486551
    11  1.65922587139908  0.06533623293141
    12  1.55746685422827  0.03291034460915
    13  1.50784321442497  0.00708286465792
    14  1.49723847693222  0.00028591328887
    15  1.49681051891394  0.00000044888384
    16  1.49680984702018  0.00000000000110
    17  1.49680984701853  0.00000000000000
    >> root
    1.49680984701853
    >> msg
    ['The tolerance (1e-12) was achieved before reaching the maximum number of iterations (20).']

    # Secant method
    # -------------
    >> method = 'secant'
    >> f = '3**(3*x + 1) - 7.5**(2*x)'
    >> a, b = (1.25, 1.5)
    >> table, root, msg = stm.roots_nonlinear(method, expr_f=f, start_with=[a, b], tol=1e-12, maxit=20, decimals=14)
    >> table
               $ p_{n}$    Relative error
    0  1.25000000000000               NaN
    1  1.50000000000000               NaN
    2  1.49218919108815  0.00523446286738
    3  1.49675571719038  0.00305094949683
    4  1.49681077100894  0.00003678074719
    5  1.49680984683531  0.00000061742888
    6  1.49680984701853  0.00000000012240
    7  1.49680984701853  0.00000000000000
    >> root
    1.49680984701853
    >> msg
    ['The tolerance (1e-12) was achieved before reaching the maximum number of iterations (20).']

    # Systems of non-linear equations
    # ------------------------------
    >>> def f(x):
            f = np.zeros(len(x))
            f[0] = np.sin(x[0]) + x[1]**2 + np.log(x[2]) - 7.0
            f[1] = 3.0*x[0] + 2.0**x[1] - x[2]**3 + 1.0
            f[2] = x[0] + x[1] + x[2] - 5.0
            return f
    >>> x0 = [1, 1, 1]
    >>> table, root, msg = stm.roots_nonlinear(method='system', expr_f=f, start_with=x0, tol=1e-12, maxit=20, decimals=14)
    >>> table
                  $x_1$             $x_2$             $x_3$
    0  1.00000000000000  1.00000000000000  1.00000000000000
    1 -0.60306857517299  3.42077975313046  2.18211103668307
    2  0.46950403361466  2.58944616346791  1.94104978711361
    3  0.59283739762309  2.40347214402737  2.00369045834814
    4  0.59904430960696  2.39594479545017  2.00501089494288
    5  0.59905375763869  2.39593140197099  2.00501484039032
    6  0.59905375664043  2.39593140237794  2.00501484098163
    >>> root
    [0.59905375664043, 2.39593140237794, 2.00501484098163]
    >>> msg
    ['The tolerance (1e-12) was achieved before reaching the maximum number of iterations (20).']

    >>> def f(x):
            f = np.zeros(len(x))
            f[0] = 3 * x[0] - np.cos(x[1] * x[2]) - 3/2
            f[1] = 4 * x[0]**2 - 625 * x[1]**2 + 2 * x[2] - 1
            f[2] = 20 * x[2] + np.exp(-x[0] * x[1]) + 9
            return f
    >>> x0 = [1, 1, 1]
    >>> table, root, msg = stm.roots_nonlinear(method='system', expr_f=f, start_with=x0, tol=1e-12, maxit=20, decimals=14)
    >>> table
                  $x_1$             $x_2$             $x_3$
    0  1.00000000000000  1.00000000000000  1.00000000000000
    1  1.23270676690272  0.50310978681145 -0.47314356308327
    2  0.83261665227014  0.25178422242063 -0.49062126761998
    3  0.83323490339536  0.12839385569881 -0.49471334477320
    4  0.83327351556583  0.06907678142127 -0.49714486086123
    5  0.83327933856769  0.04358361179769 -0.49820631197918
    6  0.83328174583398  0.03611644612755 -0.49851645380337
    7  0.83328158930236  0.03534309292460 -0.49854891189213
    8  0.83328161343104  0.03533461711812 -0.49854927744111
    9  0.83328161381683  0.03533461613950 -0.49854927781101
    >>> root
    [0.83328161381683, 0.0353346161395, -0.49854927781101]
    >>> msg
    ['The tolerance (1e-12) was achieved before reaching the maximum number of iterations (20).']
    ```
    """
    display_options()
    info_msg, result_table = [[]] * 2
    if not isinstance(method, str):
        raise ValueError(f"'method' must be a string, got >> {method}")
    
    # method
    if 'false-' in method:
        method = 'regula-falsi'

    # just incase there is a typo, correct it
    method = method.replace('regular', 'regula').replace('-false', '-falsi')
    
    if method == 'systems': method = 'system'

    closed_methods = ['bisection', 'regula-falsi', 'mregula-falsi', 'secant']
    open_methods = [
        'fixed-point', 
        'newton-raphson', 
        'mnewton-raphson', 
        'aitken', 
        'steffensen'
    ]
    systems = ['system']
    methods = closed_methods + open_methods + systems
    method = val_listitems(
        par_name='method', valid_items=methods, user_input=method
    )
    
    # function
    if method != 'system': # do not do this for system of equations
        f = lambdify_expr(f=expr_f, univariate=True, par_name='f_expr')
        if 'newton' in method:
            f_sym = sympify(expr_f)
            d1f = lambdify_expr(
                f=f_sym.diff(), univariate=True, par_name='f_exp.diff()'
            )
        if 'mnewton' in method:
            d2f = lambdify_expr(
                f=f_sym.diff().diff(), 
                univariate=True, 
                par_name='f_exp.diff().diff()'
            )

    # start_with
    if method in open_methods:
        start_with = val_numeric(user_input=start_with, par_name='start_with')
    elif method in closed_methods:
        start_with = to_listuple(
            array_values=start_with, n=2, par_name='start_with'
        )
        a, b = start_with
        a = val_numeric(user_input=a, par_name='a')
        b = val_numeric(user_input=b, par_name='b')
        if a >= b:
            raise LowerGEUpperError(a=a, b=b)
    else:
        if method != 'system':
            x0 = val_numeric(
                user_input=to_listuple(array_values=x0, par_name='x0')[0], 
                par_name='x0'
            )

    # tol
    tol_str = tol # to_str will be used in info_message (avoids round-offs)
    tol = val_numeric(
        user_input=tol, limits=[0, 1], boundary='exclusive', par_name='tol'
    )
    
    # maxit
    maxit = val_numeric(user_input=maxit, par_name='maxit')
    
    # stop_crit
    valid_stop_crit = ['absolute', 'relative']
    stop_crit = val_listitems(
        par_name='stop_crit', valid_items=valid_stop_crit, user_input=stop_crit
    )
    error_title = _stop_crit(stop_crit)

    # to_dict
    to_dict = val_boolean(user_input=to_dict, default=True)

    # decimals
    decimals = val_decimals(decimals)

    # begin calculations
    if method == 'fixed-point':
        k = 1
        while k <= maxit:
            p = f(x0)
            kth_error = _kth_error(stop_crit, b=x0, p=p)
            result_table.append([x0, kth_error])
            if kth_error < tol:
                break
            k += 1
            x0 = p 
        col_names = ['$p_n$', error_title]
    
    if method == 'newton-raphson':
        k = 1
        while k <= maxit:
            p = x0 - f(x0) / d1f(x0)
            kth_error = _kth_error(stop_crit, b=x0, p=p)
            result_table.append([x0, kth_error])
            if kth_error < tol:
                break
            k += 1
            x0 = p     
        col_names = ['$p_n$', error_title]

    if method == 'mnewton-raphson':
        k, p0 = (1, x0)
        result_table.append([p0, nan])
        while k <= maxit:
            denom = (d1f(p0) ** 2 - f(p0) * d2f(p0))
            numer = (f(p0) * d1f(p0))
            if isnan(denom) or denom == 0 or isnan(numer):
                break
            p = p0 - numer / denom
            kth_error = _kth_error(stop_crit, b=p0, p=p)
            result_table.append([p, kth_error])
            if kth_error < tol:
                break
            k += 1
            p0 = p
        col_names = ['$ p_{n }$', error_title]

    if method == 'secant':
        k = 2
        p0, p1, q0, q1 = (a, b, f(a), f(b))
        result_table.append([a, nan])
        result_table.append([b, nan])
        while k <= maxit:
            p = p1 - q1 * (p1 - p0) / (q1 - q0)
            kth_error = _kth_error(stop_crit, b=p1, p=p)
            result_table.append([p, kth_error])
            if kth_error < tol:
                break
            k += 1
            p0 = p1
            q0 = q1
            p1 = p
            q1 = f(p)
        col_names = ['$ p_{n}$', error_title]
        
    if method == 'bisection':
        k, fa, fb = (1, f(a), f(b))
        if fa * fb > 0: 
            raise NoRootInInterval(user_input=[a, b])
        while k <= maxit:
            p = a + (b - a) / 2 # better than (a + b)/2
            fp = f(p)
            kth_error = _kth_error(stop_crit, b, p)
            result_table.append([a, b, p, fp, kth_error])
            if fp == 0 or kth_error < tol:
                break
            k += 1
            if fa * fp > 0:
                a = p
                fa = fp
            else:
                b = p
        col_names = [
            '$a_n$', '$b_n$', '$p_n$', '$f(p_n)$', error_title
        ]
        
    if method == 'regula-falsi':
        k, fa, fb = (1, f(a), f(b))
        # check if interval contains the root
        if fa * fb > 0: 
            raise NoRootInInterval(user_input=[a, b])
        while k <= maxit:
            p = b - fb * (b - a) / (fb - fa)
            fp = f(p)
            kth_error = _kth_error(stop_crit, b=b, p=p)
            # append 
            result_table.append([a, b, p, fp, kth_error])
            if kth_error < tol:
                break
            k += 1
            if fp * fb < 0:
                a = b
                fa = fb
            b = p
            fb = fp 
        col_names = [
            '$a_n$', '$b_n$', '$p_n$', '$f(p_n)$', error_title
        ]

    if method == 'mregula-falsi':
        k, fa, fb, result_table = (1, f(a), f(b)/2, [])
        # check if interval contains the root
        if fa * fb > 0: 
            raise NoRootInInterval(user_input=[a, b])
        while k <= maxit:
            p = b - fb * (b - a) / (fb - fa)
            fp = f(p)/2
            kth_error = _kth_error(stop_crit, b=b, p=p)
            # append 
            result_table.append([a, b, p, fp, kth_error])
            if kth_error < tol:
                break
            k += 1
            if fp * fb < 0:
                a = b
                fa = fb
            b = p
            fb = fp
        col_names = [
            '$a_n$', '$b_n$', '$p_n$', '$f(p_n)$', error_title
        ]
        
    if method == 'aitken':
        k = 1
        while k <= maxit:
            x1 = f(x0)
            x2 = f(x1)
            d = (x2 - x1) - (x1 - x0)
            if isnan(d) or d == 0:
                break
            p = x2 - pow((x2 - x1), 2) / d
            kth_error = _kth_error(stop_crit, b=x2, p=p)
            # append 
            result_table.append([x0, kth_error])
            if kth_error < tol:
                break
            k += 1
            x0 = p
        col_names = ['$p_{n}$', error_title]
        
    if method == 'steffensen':
        k, p0 = (1, x0)
        while k <= maxit:
            p1 = f(p0)
            p2 = f(p1)
            # avoid division by NaN and zero
            denom = (p2 - 2 * p1 + p0)
            if isnan(denom) or denom == 0 or isnan(p0 - (p1 - p0) ** 2):
                break
            p = p0 - (p1 - p0) ** 2 / denom
            kth_error = _kth_error(stop_crit, b=p, p=p0)
            # append
            result_table.append([p0, p1, p2, kth_error])
            if kth_error < tol:
                break
            k += 1
            p0 = p
        col_names = ['$p_{0}$', '$p_{1}$', '$p_{2}$', error_title]

    # systems of nonlinear equations with Newton-Raphson
    if method == 'system':
        def _jacobian(f, x0):
            x = x0 # array of initial guess
            n = len(x)
            jac = zeros((n, n))
            f0 = f(x)
            for i in range(n):
                temp = x[i]
                x[i] = temp + tol
                f1 = f(x)
                x[i] = temp
                jac[:, i] = (f1 - f0) / tol
            return jac, f0
        k = 1
        result_table.append(x0.tolist())
        while k <= maxit:
            jac, f0 = _jacobian(f=expr_f, x0=x0)
            x = x0
            if sqrt(dot(f0, f0) / len(x)) < tol:
                break
            dx = _gauss_pivot(jac, -f0)
            x += dx
            p = x # these are the roots
            result_table.append(x.tolist()) # should be here, not above
            if sqrt(dot(dx, dx)) < tol * max(max(abs(x)), 1.0):
                break
            k += 1
        col_names = [f'$x_{index+1}$' for index in range(len(x))]
    
    if result_table:
        index_names = dframe_labels(
            dframe=result_table, df_labels=index_labels
        )
        # create DataFrame
        set_option('display.precision', decimals)
        result_table = DataFrame(
            data=result_table, index=index_names, columns=col_names
        )
        result_table = result_table.round(decimals)
    else:
        p = nan
    # info messages
    info_msg = info_messages(maxit=maxit, tol=tol_str, k=k)
    root = sympify(round(p, decimals))

    if to_dict:
        result = {
            'table': result_table, 
            'root': root, 
            'info_msg': info_msg
        }
    else:
        result = result_table, root, info_msg

    return result
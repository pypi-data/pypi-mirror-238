from typing import Literal
from sympy import linear_eq_to_matrix
from numpy import (
    array, asfarray, zeros_like, identity, dot, inf, round
)
from numpy.linalg import norm
from pandas import DataFrame
from ..core.validate import (
    val_numeric, val_boolean, val_decimals, val_dflabels, val_listitems, 
    val_square_matrix, val_Ab
)
from ..core.errors import LengthDifferError, CompatibliltyError
from ..core.symbolic import sympify_input, get_expr_vars
from ..core.options import display_options
from ..core.arraylike import (
    relax_parameter, matrix_inverse, is_len_equal, to_listuple
)
from ..core.htmlatex import latex_display
from ..statistical.wrangle import dframe_labels
from ..core.info_messages import info_messages

def solve_linear(
        method, 
        matrix_or_eqtns, 
        b, 
        x0=None, 
        C=None, 
        w = None, 
        tol = 1e-16, 
        maxit = 10,
        variables=None,
        col_latex=True, 
        index_labels=None, 
        to_dict=False, 
        decimals=12
) -> tuple[DataFrame, Literal]:
    """
    ```

    Solve a system of linear equations using a specified iterative method.
    
    Parameters
    ----------
    method : {jacobi, ..., cgradient}, default='jacobi'
        The iterative method to be used to solve the system.
        ============================================================
        Argument                Description
        ============================================================
        jacobi ................ Jacobi iteration
        gseidel ............... Gauss-Seidel iteration
        sor ................... Successive over-relaxation iteration
        cgradient ............. Conjugate gradient method
        ============================================================
    matrix_or_eqtns : array_like
        A 2D square array with the coefficients of the unknowns in the system 
        of equations. You can also specify the system of equations directly.
    b : array_like
        A 1D array of constants (values to the right of equal sign). It is 
        disregarded is a system of equations is given in `A`.
    x0 : array_like
        A 1D array with the initial solution.
    C : array_like
        The preconditioning matrix for the Congugate gradient method. 
    w : {None, int, float}, default=None
        The relaxation parameter in SOR method. If `None`, the system will
        calculate the optimal value. 
    tol : float, default=1e-6
        Tolerance level, algorithm will stop if the difference between 
        consecutive values falls below this value.
    maxit : int, default=10
        Maximum number of iterations to be performed.
    variables : {None, array_like}, default=None
        The unknown variables in the system of equations.
    index_labels : {int, array_like, None}, default=0
        Specify index for the DataFrame.
        ==============================================================
        Argument            Description
        ==============================================================
        int ............... Specify the starting point of the index
        array_like ........ Array-like structure with the index labels
        None .............. Will remove the DataFrame index       
        ==============================================================
    col_latex : bool, default=True
        If True, column headings will be printed in Latex.
    to_dict : bool, default=False
        If true, result will be returned as a dictionary.
    decimals : int, default=8
        Number of decimal points.

    Returns
    -------
    result_table : DataFrame
        A table with approximation of the solution at each step.
    solution : str
        The solution of the linear system.

    Examples
    --------
    >> eqtns = ['x1 + 1/2*x2 + 1/3*x3 = 5/6', '1/2*x1 + 1/3*x2 + 1/4*x3 = 5/12', '1/3*x1 + 1/4*x2 + 1/5*x3 = 17/60']
    >>
    >> table

    >> sol

    >> A = np.array([[10, -1, 2, 0], [-1, 11, -1, 3], [2, -1, 10, -1], [0, 3, -1, 8]])
    >> b = np.array([6, 25, -11, 15])
    >> table, sol = stm.solve_linear(method='jacobi', matrix_or_eqtns=A, b=b, maxit=10, decimals=12)

    >> table, sol = stm.solve_linear(method='gseidel', matrix_or_eqtns=A, b=b, maxit=10, decimals=12)

    >> table, sol = stm.solve_linear(method='sor', matrix_or_eqtns=A, b=b, maxit=10, decimals=12)


    >> table, sol = stm.solve_linear(method='cgradient', matrix_or_eqtns=A, b=b, maxit=10, decimals=12)
    >> table

    >> sol

    ```
    """
    display_options()
    tol_str = tol
    # method
    valid_methods = ['jacobi', 'gseidel', 'sor', 'cgradient']
    method = val_listitems(
        par_name='method', valid_items=valid_methods, user_input=method
    )

    # A
    A = sympify_input(expr_array=matrix_or_eqtns, to_matrix=True)
    nrows, ncols = A.shape
    if nrows != ncols:
        # a system of equations was entered
        fvars = get_expr_vars(expr_array=A.tolist())
        A, b = linear_eq_to_matrix(A, fvars)
        A = asfarray(A)
        b = asfarray(b)
        nrows, ncols = A.shape # get dimensions again

    # A continue 
    A = val_square_matrix(par_name='matrix_or_eqtns', M=A)
    A = asfarray(A)

    # b
    b = asfarray(to_listuple(array_values=b, par_name='b'))

    # check compatibility
    A, b = val_Ab(A, b)

    # x0
    if x0 is None:
        x = zeros_like(b)
    else:
        x = asfarray(to_listuple(array_values=x0, par_name='x0'))
        if not is_len_equal(b, x):
            raise LengthDifferError(par_name="'b', 'x0'", user_input=[b, x])

    # C -> done within method == 'cgradient'
    
    # w -> done within method == 'sor'

    # variables
    if variables is None:
        variables = [f'x_{k+1}' for k in range(len(b))]
    else:
        variables = to_listuple(array_values=variables, par_name='variables')
        if len(variables) > ncols:
            variables = variables[:ncols]
        if len(variables) < ncols:
            raise LengthDifferError(
                par_name="'b', 'variables'", user_input=[b, variables]
            )

    # tol, ..., decimals
    tol = val_numeric(
        user_input=tol, limits=[0, 1], boundary='exclusive', par_name='tol'
    )
    maxit = val_numeric(user_input=maxit, float_=False, par_name='maxit')
    index_labels = val_dflabels(
        par_name='index_labels', user_input=index_labels
    )
    col_latex = val_boolean(user_input=col_latex, default=True)
    to_dict = val_boolean(user_input=to_dict, default=False)
    decimals = val_decimals(decimals)

    # begin computations
    X = []
    if method == 'jacobi':
        for k in range(maxit):
            X.append(x.tolist())
            x_new = zeros_like(x)
            for i in range(nrows):
                s1 = dot(A[i, :i], x[:i])
                s2 = dot(A[i, i+1:], x[i+1:])
                x_new[i] = (b[i] - s1 - s2) / A[i, i]
            if norm(x_new - x, ord=inf) / norm(x_new, ord=inf) < tol:
                break
            x = x_new.copy()
    if method == 'gseidel':
        x_new = zeros_like(x)
        for k in range(1, maxit+1):
            X.append(x.tolist())
            for i in range(nrows):
                s1 = dot(A[i, :i], x_new[:i])
                s2 = dot(A[i, i+1:], x[i+1:])
                x_new[i] = (b[i] - s1 - s2) / A[i, i]
            if norm(x_new - x, ord=inf) / norm(x_new, ord=inf) < tol:
                break
            x = x_new.copy()
    elif method == 'sor':
        if not w:
            w = relax_parameter(A) # calculate optimal relaxation parameter
        else:
            w = val_numeric(user_input=w, float_=True, par_name='w')
        for k in range(maxit):
            X.append(x.tolist())
            x_new  = x.copy()
            for i in range(nrows):
                s1 = dot(A[i, :i], x[:i])
                s2 = dot(A[i, i+1:], x_new[i+1:])
                x[i] = x[i] * (1 - w) + (w/A[i, i]) * (b[i] - s1 - s2) 
    elif method == 'cgradient':
        if C is None:
            C = identity(nrows)
        else:
            C = sympify_input(expr_array=C, to_matrix=True)
        C = val_square_matrix(par_name='C', M=C)
        if nrows != C.shape[0] or ncols != C.shape[1]:
            raise CompatibliltyError(
                A = 'matrix_or_eqtns',
                B = 'C',
                multiplication = True,
                dims_A = A.shape,
                dims_B = C.shape
            )
        
        # begin computations
        C_inverse = matrix_inverse(par_name='C', M=C)
        r = b - dot(A, x)
        w = dot(C_inverse, r)
        v = dot(C_inverse.T, w)
        alpha = dot(w, w)
        # step 3
        k = 1
        X = []
        while k <= maxit:
            X.append(x.tolist())
            # step 4
            if norm(v, inf) < tol:
                break
            # step 5
            u = dot(A, v)
            t = alpha / dot(v, u)
            x = x + t * v
            r = r - t * u
            w = dot(C_inverse, r)
            beta = dot(w, w)
            # step 6
            if abs(beta) < tol:
                if norm(r, inf) < tol:
                    break
            # step 7
            s = beta/alpha
            v = dot(C_inverse.T, w) + s * v
            alpha = beta
            k = k+1
    # info message
    info_msg = info_messages(maxit=maxit, tol=tol_str, k=k)
    X = round(array(X), decimals)
    result_table = DataFrame(X)
    solution = X[-1, :]
    index_labels = dframe_labels(
        dframe=result_table, df_labels=index_labels, index=True
    )
    col_labels = dframe_labels(
        dframe=result_table, 
        df_labels=variables, 
        index=False, 
        col_latex=col_latex
    )
    result_table.index = index_labels
    result_table.columns = col_labels
    solution_latex = latex_display(
        lhs=variables, rhs=solution, auto_display=False
    )
    if to_dict is True:
        result = {
            'result_table': result_table, 
            'solution': solution, 
            'solution_latex':solution_latex,
            'info_msg': info_msg
        }
    else:
        result = result_table, solution, solution_latex, info_msg

    return result
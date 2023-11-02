from sympy import sympify, diff
from ..core.symbolic import is_symexpr, simplify_expr
from ..core.errors import (
    SympifyError, SymbolicExprError, NumericBtwnError, IntegerError
)

def diff_parametric(
        f, g, dependent, n = 1, simp_method = 'factor', collect_term=None
):
    """
    ```

    Computes the nth order derivative of two parametric equations.
    
    Parameters
    ----------
    f : {symbolic, str}
        An expression containing the first parametric equation.
    g : {symbolic, str}
        An expression containing the second parametric equation.
    dependent: {symbolic, str}
        The dependent variable.
    n : int, default=1
        Order of differentiation.   
    simp_method: str, default='factor'
        Simplification method to be applied to the final answer.
        ================================================================
        Valid       Description
        ================================================================
        cancel      Cancel common factors in a rational function ``f``.
        collect     Collect additive terms of an expression.
        expand      Expand an expression.
        factor      Compute the factorization of expression, ``f``, 
                    into irreducibles.
        simplify    Simplifies the given expression.
        together    Combine rational expressions using symbolic methods.
    collect_term : {None, str}, default=None

    Returns
    -------
    result : symbolic
        A symbolic object representing the differentiated expression.
        
    Examples
    --------
    >> import stemlab as stm

    >> x = 't^3 + 3 * t^2'
    >> y = 't^4 - 8 * t^2'
    >> stm.diff_parametric(f=x, g=y, dependent=t, n=3)
    -(3*t**2 - 4)/(9*t**3*(t - 2)**3*(t + 2)**2)

    >> x = 'sin(t)'
    >> y = 'cos(t)'
    >> stm.diff_parametric(f=x, g=y, dependent=t, n=2, simp_method='simplify')
    1/(sin(t)**2*cos(t))

    >> x = 't * sin(t)'
    >> y = 't + t^2'
    >> stm.diff_parametric(f=x, g=y, dependent='t', n=2, simp_method='simplify')
    (-2*t*cos(t) + (2*t + 1)*(-t*sin(t) + 2*cos(t)) - 2*sin(t))/((2*t + 1)**2*(t*cos(t) + sin(t)))
    ```  
    """
    # f
    # -
    f_str = f
    try:
        f = sympify(f)
    except:
        raise SympifyError(user_input=f_str)

    if not is_symexpr(f):
        raise SymbolicExprError(par_name='f', user_input=f_str)
    # g
    # -
    g_str = g
    try:
        g = sympify(g)
    except:
        raise SympifyError(user_input=g_str)

    if not is_symexpr(g):
        raise SymbolicExprError(par_name='g', user_input=g_str)

    # dependent
    # ---------
    try:
        t = sympify(dependent)
    except:
        raise SympifyError(user_input=dependent)
    
    if not is_symexpr(t):
        raise SymbolicExprError(par_name='dependent', user_input=dependent)

    # n
    # -
    if not isinstance(n, int):
        raise IntegerError(par_name='n', user_input=n)
    
    if not (1 <= n <= 10):
        raise NumericBtwnError(
            par_name='n', limits=[1, 10], boundary='inclusive', user_input=n
        )
    
    # simp_method
    # -----------
    
    # will be validated in stm.simplify_expr() function

    # begin
    # -----
    if n == 1:
        derivative = diff(g, t) / diff(f, t)
    else:
        # perform the normal differentiation recurssively
        derivative = diff(diff_parametric(g, f, t, n-1), t) / diff(f, t)
    
    # simplify result
    result = simplify_expr(
        expression=derivative, 
        simp_method=simp_method, 
        collect_term=collect_term, 
        numer_denom=True
    )
    
    return result
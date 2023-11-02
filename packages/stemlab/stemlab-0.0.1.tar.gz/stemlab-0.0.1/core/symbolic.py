from sympy import sympify, collect, Poly, lambdify, Matrix, flatten
from numpy import array, fliplr, ravel, trim_zeros
from .errors import (
    NotInValuesError, SympifyError, BooleanError,  NotSpecifiedError, 
    SymbolicExprError, SymbolicVarsError, UnivariatePolyError, FloatError, 
    IterableError
)
from ..core.arraylike import is_iterable, to_listuple

def is_symexpr(expr):
    """
    ```

    Check if expression is symbolic (i.e. contains unknown variables).

    Parameters
    ----------
    expr : {symbolic, str}
        An object representing the value to be tested.

    Returns
    -------
    result: bool
        True/False

    Examples
    --------
    >> import stemlab as stm

    >> stm.is_symexpr('pi/4')
    False

    >> stm.is_symexpr('pi/x')
    True

    >> g = 'x^2 + x*y - 5'
    >> stm.is_symexpr(g)
    True

    ```
    """
    try:
        result = len(sympify(expr).free_symbols) > 0
    except:
        result = False

    return result
    
def expr_constant(expression, const_float=False, decimals=4):
    """
    ```

    Extracts the constant term in a specified expression.

    Parameters
    ---------
    expression : {symbolic, str}
        An expression containing the expression.
    const_float : bool, default=False
        If True, the constant will be converted to float (decimal).
    decimals : int, default=4
        Number of decimals. Only used if `const_float=True`. 

    Returns
    -------
    constant : {int, float, bool}
        Returns a constant in a specified expression if it exists and False 
        otherwise.

    Examples
    --------
    >> import stemlab as stm

    >> stm.expr_constant('2*x^2 + 2/5')
    2/5

    >> stm.expr_constant('2*x^2 + 2/5', const_float = True)
    0.4

    >> stm.expr_constant('2*x^2')
    False

    ```
    """ 
    try:
        # will crush if constant, used for terms like: sin(x)**2 + cos(x)**2
        expression = sympify(expression).simplify()
    except:
        pass

    constant = expression.func(
        *[term for term in expression.args if not term.free_symbols]
    )
    if const_float:
        constant = sympify(round(float(constant), decimals))

    if constant == 0:
        constant = None
    
    return constant

def simplify_expr(
        expression, 
        simp_method='factor', 
        collect_term=None, 
        numer_denom=False
):
    """
    ```

    Simplify a symbolic expression using a specified simplification method.
    
    Parameters
    ----------
    expression : {symbolic, str}
        The expression that is to be simplified.
    simp_method : {None, 'cancel', 'collect', ...'}, default='factor'
        The simplification type to be applied.
        ===========================================
        Argument                        Description
        ===========================================
        none
        cancel
        collect
        expand
        factor
        simplify
        together
    collect_term : {symbolic, str, list}, default=None
        An expression or list of expressions that should be used to group 
        the input expression. Required when ``simp_method='collect'``.
    numer_denom : bool, default=False
        If True, the numerator and denominator will be simplified separately. 
    
    Examples
    --------
    >> import stemlab as stm
    
    >> f = '(x + x^2)/(x*sin(y)^2 + x*cos(y)^2)'
    >> stm.simplify_expr(f, simp_method='simplify')
    x + 1
    
    >> g = 'x^2 + y*x^2 + x*y + y + a*y'
    >> stm.simplify_expr(g, simp_method='collect', collect_term=[x, y])
    x**2*(y + 1) + x*y + y*(a + 1)
    
    Returns
    -------
    result : symbolic
        A simplified form of the entered symbolic expression.
    
    ```
    """
    # expression
    # ----------
    if not is_symexpr(expression):
        result = expression # if not symbolic, just return the result as given
    
    # simp_method
    # -----------
    if simp_method is not None:
        simp_method = simp_method.lower()
    valid_methods = [
        None, 'cancel', 'collect', 'expand', 'factor', 'simplify', 'together'
    ]

    if simp_method not in valid_methods:
        raise NotInValuesError(
            par_name='simp_method', 
            valid_args=valid_methods, 
            user_input=simp_method
        )
    
    try:
        if simp_method != 'collect':
            if simp_method is not None:
                simp_method = sympify(simp_method)
    except:
        raise NotImplemented(
            "Unable to create a valid function from 'simp_method'"
        )
    
    # collect_term
    # ------------
    if simp_method == 'collect':
        if collect_term is None:
            raise NotSpecifiedError(
                par_name='simp_method', 
                par_name_arg="collect='collect'",
                user_input=simp_method
            )
        if isinstance(collect_term, str) or is_symexpr(collect_term):
            try:
                collect_term = sympify(collect_term)
            except:
                raise SympifyError(
                    par_name='collect_term', user_input=collect_term
                )
        # a loop is used just in case there are multiple variable specified 
        # e.g. [x, y]
        if isinstance(collect_term, (list, tuple)):
            k = 0 # to capture term number
            for term in collect_term:
                k += 1
                if not is_symexpr(term):
                    raise SymbolicExprError(
                        par_name=f'collect_term: term {k}', user_input=term
                    )
        else:
            if not is_symexpr(collect_term):
                raise SymbolicExprError(
                    par_name='collect_term', user_input=collect_term
                )

    # numer_denom
    # -----------
    if not isinstance(numer_denom, bool):
        raise BooleanError(par_name='numer_denom', user_input=numer_denom)

    # begin
    # -----
    result = expression # if the method is none
    if numer_denom is True:
        numerator, denominator = expression.as_numer_denom()
        if simp_method == 'collect':
            result = collect(numerator, collect_term) / \
                collect(denominator, collect_term)
        else:
            if simp_method is not None:
                result = simp_method(numerator) / simp_method(denominator)
    else:
        if simp_method == 'collect':
            result = collect(expression, collect_term)
        else:
            if simp_method is not None:
                result = simp_method(expression)

    return result

def poly_terms(expression):
    """
    ```

    Returns the term(s) of a symbolic expression, including the constant, if any.

    Parameters
    ----------
    expression : {symbolic, str}
        A univariate polynomial.

    Returns
    -------
    terms_list : list
        The term(s) of the symbolic expression.
    terms_count : int
        The number of terms.
    constant_bool : bool
    result: tuple
        Boolean value indicating whether or not the expression has a constant.

    Examples
    --------
    >> import stemlab as stm

    >> stm.poly_terms('4*x^2 - 5*x + 1')
    [['4*x**2', '5*x', '1'], 3, True]

    >> stm.poly_terms('4*x^2 - 5*x')
    [['4*x**2', '5*x'], 2, False]

    ```
    """
    # expression
    # ----------
    if isinstance(expression, str):
        try:
            expression = sympify(expression)
        except:
            raise SympifyError(user_input=expression)
    
    if not expression.is_polynomial():
        raise UnivariatePolyError(par_name='expression', user_input=expression)
        
    try:
        sym_variables = expression.free_symbols
        sym_count = len(sym_variables)
    except:
        raise SymbolicVarsError()
    
    # note that x*y passes is_polynomial() test above
    if sym_count == 0 or sym_count > 1: 
        raise UnivariatePolyError(par_name='expression', user_input=expression)
    else:
        # extract the variable (symbol)
        variable = str(list(sym_variables)[0])
    
    # args does not work for e.g. 8*x^2
    expr_list = str(expression).replace(' ', '').replace('-', '+').split('+') 
    terms_count = len(expr_list)
    terms_list = list(map(lambda x: str(x), expr_list))
    constant_term = list(filter(lambda x: variable not in x, terms_list))
    constant_bool = len(constant_term) > 0
    
    return terms_list, terms_count, constant_bool

def remove_zeros(expression, truncate_terms=1e-16):
    """
    ```

    Remove terms with coefficients are close to zero from an nth order 
    polynomial.

    Parameters
    ----------
    expression : {symbolic, str}
        A symbolic expression with the term(s) to be truncated.

    truncate_terms : float
        Smallest value for which terms should be removed. Terms below this 
        value will be removed from the polynomial.

    Examples
    --------
    >> import stemlab as stm

    >> g = 'x^3/2000 + x^2/50000 + 5*x + 8'
    >> stm.remove_zeros(g, truncate_terms = 1e-6) 
    x**3/2000 + x**2/50000 + 5*x + 8

    >> stm.remove_zeros(g, truncate_terms = 1e-4)
    x**3/2000 + 5*x + 8
    
    >> h = 5*x + 8
    >> stm.remove_zeros(h, truncate_terms = 1e-3)
    5*x + 8

    Returns
    -------
    result : {symbolic, 0}
        A symbolic expression with terms whose coefficients are greater than 
        `truncate_terms` or the value 0.
    
    ```
    """
    try:
        expression = sympify(expression)
        constant_term = expr_constant(expression, const_float = False)
        # remove constatnt
        if constant_term: # perform only if expression has a constant term
            if constant_term < truncate_terms:
                expression = str(expression)\
                    .replace(' ', '')\
                    .replace(f'-{constant_term}', '')\
                    .replace(f'+{constant_term}', '')
        expression = sympify(expression) 
    except:
        raise SympifyError(user_input=expression)

    if not expression.is_polynomial():
        raise UnivariatePolyError(par_name='expression', user_input=expression)

    if truncate_terms == 0: 
        truncate_terms = float(0)
    if (not isinstance(truncate_terms, float) or truncate_terms < 0 
        or truncate_terms > 1
    ): 
        raise FloatError(
            par_name='truncate_terms', limits=[0, 1], user_input=truncate_terms
        )

    sym_variables = expression.free_symbols
    sym_count = len(sym_variables)

    # note that x*y passes is_polynomial() test above
    if sym_count == 0 or sym_count > 1:
        raise UnivariatePolyError(par_name='expression', user_input=expression)
    else:
        # extract the variable (symbol)
        variable = str(list(sym_variables)[0])

    expr_coeffs = array(Poly(expression).all_coeffs())
    expr_coeffs = fliplr(array([expr_coeffs]))
    expr_coeffs[abs(expr_coeffs) < truncate_terms] = 0

    # other are: 'f' and 'bf' in the place of 'b'
    expr_coeffs = trim_zeros(ravel(expr_coeffs), 'b') 

    terms_list, terms_count, _ = poly_terms(expression)
    expr_list = [f'{term}*{variable} ** {k}' 
                 for k, term in enumerate(expr_coeffs)]
    
    # if the polynomial has only one term, it prevents for example 5*x**3 
    # being returned as 5*x
    if terms_count == 1:
        expr_list = terms_list
    
    expr_string = ' + '.join(expr_list)
    
    # check if we need to deduct constant that was added as placeholder
    try:
        result = sympify(expr_string) 
    except:
        result = 0

    return result

def sympify_input(expr_array, to_matrix=False):
    """
    ```
    Converts a string to a symbolic expression.

    Parameters
    ----------
    expr_array : {symbolic, array_like}
        xxxx
    to_matrix : bool, default=True
        If true, the ``expr_array`` will be converted to a matrix.

    Returns
    -------

    Examples
    --------
    >> 

    ```
    """
    try:
        expr_array = sympify(expr_array)
        if to_matrix is True:
            expr_array = Matrix(expr_array)
    except:
        raise SympifyError(par_name='expr_array', user_input=expr_array)
    
    return expr_array
        
def lambdify_expr(f, univariate=False, variables=None, par_name='f'):
    """
    ```

    Converts an equation to a Numpy function.

    Parameters
    ----------

    Returns
    -------

    Examples
    --------
    >> 

    ```
    """
    # f
    f_str = f
    try:
        f = sympify_input(expr_array=f)
    except:
        raise SympifyError(par_name=par_name, user_input=f_str)
    
    # univariate
    if not isinstance(univariate, bool):
        raise BooleanError(par_name=par_name, user_input=univariate)

    # f - continued
    if is_symexpr(f):
        fvars = f.free_symbols
        nvars = len(fvars)
        if univariate:
            if nvars == 0 or nvars > 1:
                raise UnivariatePolyError(par_name=par_name, user_input=f_str)
    else:
        raise SymbolicExprError(par_name=par_name, user_input=f_str)
    
    if variables is None:
        fvars = tuple(fvars)
    else: 
        # variables
        fvars = to_listuple(
            array_values=variables, 
            includes_str=True,  
            list_=False,
            par_name='variables'
        )
    f = lambdify(fvars, f, 'numpy')

    return f

def get_expr_vars(expr_array):
    """
    ```

    Get unknown variables in a single or a system of equations.

    Parameters
    ----------

    Returns
    -------

    Examples
    --------
    >> 

    """
    if not is_iterable(expr_array, includes_str=True):
        raise IterableError(par_name='expr_array', user_input=expr_array)
    eqtns = sympify(expr_array)
    if isinstance(eqtns, str):
        fvars = eqtns.free_symbols
    else:
        eqtns = flatten(eqtns)
        fvars = set(flatten([eqtn.free_symbols for eqtn in eqtns]))
    fvars = tuple(fvars)
    
    return fvars
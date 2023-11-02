from numpy import array, float64
from sympy import sympify, Float
from .errors import (
    NumericBtwnError, IntegerError, FloatError, IterableError, 
    NotInValuesError, SquareMatrixError, CoeffConstantsError, 
    VectorLengthError
)
from .arraylike import is_iterable, to_listuple

def val_decimals(decimals, a=-1, b=14):
    """
    Validate the number of decimal points.
    """
    try:
        a, b = (int(a), int(b))
    except:
        raise IntegerError(par_name='integer limits', user_input=decimals)
    
    if not isinstance(decimals, int) or not (a <= decimals <= b):
        raise NumericBtwnError(
            par_name='decimals', 
            limits=[a, b], 
            boundary='inclusive', 
            user_input=decimals
        )
    
    return decimals

def val_listitems(par_name, valid_items, user_input):
    
    if user_input not in valid_items:
        raise NotInValuesError(
            par_name=par_name, valid_items=valid_items, user_input=user_input
        )
    return user_input

def val_string(par_name, user_input, to_lower=True):
    if not isinstance(user_input, str):
        raise ValueError(f"'{par_name}' must be a string, got >> {user_input}")
    if to_lower:
        user_input = user_input.lower()
    return user_input

def val_numeric(
        par_name, user_input, to_float=True, limits=None, boundary='',
):
    """
    Check is a value is a float.
    """
    if not isinstance(to_float, bool):
        to_float = True
    if isinstance(user_input, (float, float64, Float)):
        NumFloatError = FloatError
    else:
        NumFloatError = IntegerError
    
    try:
        # will crush if not numeric, sympify is used to convert expressions
        _ = float(sympify(user_input))
    except:
        raise NumFloatError(par_name=par_name, user_input=user_input)
    
    if limits is not None:
        try:
            a, b = limits
        except:
            raise VectorLengthError(par_name=par_name, n=2, user_input=user_input)
        if not (a <= user_input <= b):
            raise NumFloatError(
                    par_name=par_name, 
                    limits=[a, b], 
                    boundary=boundary, 
                    user_input=user_input
            )
    if to_float is True:
        user_input = float(user_input) 
        
    return user_input

def val_boolean(user_input, default):
    """
    Validate boolean values. If invalid, then use the default.
    """
    if not isinstance(user_input, bool):
        return default
    return user_input

def val_len_equal(x, y, par_name=['x', 'y']):
    """
    Check if arrays have equal number of elements.
    """
    if len(x) != len(y):
        xname, yname = par_name
        raise ValueError(
            f"'{xname}' and '{yname}' must have the same number of elements, "
            f"got >> {len(x)} and {len(y)} elements respectively"
        )

def val_dflabels(par_name, user_input):
    
    if (not is_iterable(array_like=user_input, includes_str=True) and 
        not isinstance(user_input, int) and 
        not user_input is None
    ):
        raise IterableError(
            par_name=par_name, includes_str=True, user_input=user_input
        )
    
    if is_iterable(array_like=user_input):
        user_input = to_listuple(user_input, par_name=par_name)

    return user_input
    
def val_square_matrix(par_name, M):
    """
    Check if a matrix is square.
    """
    if not is_iterable(array_like=M):
        raise IterableError(
            par_name=par_name, includes_str=True, user_input=M
        )
    try:
        nrow, ncol = array(M).shape
    except:
        raise ValueError(f"'{par_name}' must be a 2D array, got >> {M}")
    if nrow != ncol:
        raise SquareMatrixError(par_name=par_name, dims=[nrow, ncol])
    
    return M

def val_Ab(A, b):
    """
    Validate matrix of coefficients and the vector of constants.
    """
    if A.shape[0] != len(b): # use len(b) instead of b.shape[0]
        raise CoeffConstantsError(user_input=[A, b])

    return A, b

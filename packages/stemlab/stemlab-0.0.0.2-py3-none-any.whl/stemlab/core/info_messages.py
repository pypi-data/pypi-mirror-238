from sympy import flatten

def info_messages(maxit, tol, k):
    """
    Return message for approximation calculations.
    """
    if k > maxit:
        info_msg = (
            f"The maximum number of iterations ({maxit}) was reached "
            f"before achieving the tolerance ({tol})."
        )
    elif k < maxit:
        info_msg = (
            f"The tolerance ({tol}) was achieved before "
            f"reaching the maximum number of iterations ({maxit})."
        )
    
    return flatten(info_msg)
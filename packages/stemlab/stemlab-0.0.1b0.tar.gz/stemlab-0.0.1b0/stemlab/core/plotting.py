from io import BytesIO
import base64
from sympy import degree
from matplotlib.pyplot import (
    plot, figure, clf, title, xlabel, ylabel, legend, text, tight_layout, 
    savefig, scatter
)
from IPython.display import Image
from ..core.arraylike import to_listuple
from ..core.symbolic import lambdify_expr

def interpolation_plot(x, 
                       y, 
                       x0, 
                       poly_approx_x0, 
                       poly_linspace, 
                       poly_approx_linspace, 
                       poly_deriv, 
                       poly_var, 
                       method, 
                       plot_x0, 
                       diff_order, 
                       plot_deriv, 
                       decimals = 8
):
    """
    ```

    Plot figures for interpolation results.

    Parameters
    ----------
    x : array_like
        An array with the values of x.
    y : array_like
        An array with the values of y i.e. f(x).
    x0 : int, float
        The point at which the polynomial should be approximated.
    poly_approx_x0 : int, float
        The value of the approximated polynomial at x=0. 
    poly_linspace : array_like
        An array with n linearly spaced values between min(x) and max(x)
    poly_approx_linspace : array_like
        An array with values found by substituting `poly_linspace` into 
        poly_approx.
    poly_deriv : {symbolic, str}
        An expression for the nth derivative of the function fx.
    poly_var : str
        The string to be used as the unknown variable in the polynomial.
    method : {straight-line, ..., reciprocal}
        The interpolation method to be applied.
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
    plot_x0 : bool, option
        If True, `x0` will be plotted on the graph.
    diff_order : int
        Order of differentiation
    plot_deriv : bool, default=False
        If True, the derivative will be plotted on the graph.
    decimals : int, defaul=8
        Number of decimals in the display.

    Examples
    --------
    No examples. This function is called internally by the interplation function.

    Returns
    -------
    html_code : str
        A html string with the image code.

    ```
    """
    interp_method = f'{method.capitalize()} interpolation'
    x = to_listuple(array_values=x, par_name='x')
    y = to_listuple(array_values=y, par_name='y')
    n = len(x)
    clf()
    figure(figsize = (7, 5))
    scatter(x, y, color = 'blue', marker = 'D')
    plot(
        poly_linspace, 
        poly_approx_linspace, color = 'blue', 
        label = f'$f~({poly_var})$'
    )
    if poly_deriv is not None:
        if plot_deriv and degree(poly_deriv) > 0:
            g = lambdify_expr(
                f=poly_deriv, univariate=True, par_name='poly_deriv'
            )
            poly_deriv_linspace = g(poly_linspace)
            deriv_order = "'" * diff_order
            plot(
                poly_linspace, 
                poly_deriv_linspace,
                color = 'orange', linestyle = 'dashed',
                label = f'$f~{deriv_order}~({poly_var})$'
            )
            legend(
                loc = 'best', 
                ncol = 2,
                prop = {'family': 'calibri', 'weight': 'normal', 'size': 12}
            )
    
    if (plot_x0 and x0 < x[n-1] and x0 > x[0] and 
        method not in ['not-a-knot-splines']
    ):
        try:
            plot(
                x0, 
                poly_approx_x0, 
                color = 'red', 
                marker = '*', 
                markersize = 12
            )
            x = round(float(x0), decimals)
            y = round(float(poly_approx_x0), decimals)
            text(
                x0, poly_approx_x0,
                f'  ({x}, {y})',
                fontsize = 12,
                bbox = dict(facecolor = 'gray', alpha = 0.075),
                horizontalalignment = 'left'
            )
        except:
            pass
    xlabel(poly_var)
    ylabel(f'$f~({poly_var})$')
    title(interp_method.capitalize().replace('-', ' '))
    tight_layout()
    figure_html = figure_encoded()
    
    return figure_html

def figure_encoded():
    """
    Generate base64 code for plotted graphs.
    """
    figure_file = BytesIO()
    savefig(figure_file, format = 'png')
    figure_file.seek(0)
    figure_code = base64.b64encode(figure_file.getvalue()).decode('ascii')
    figure_code = f'data:image/png;base64,{figure_code}'
    figure_html = Image(url = figure_code)

    return figure_html
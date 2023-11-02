import os
from datetime import datetime
from numpy import array, argwhere, isin, round
from sympy import latex, sympify, Matrix, flatten
from pandas import DataFrame
from IPython.display import display, Latex
from IPython.core.display import HTML
from ..core.options import display_options
from ..core.arraylike import to_listuple
from ..core.validate import val_boolean
from ..core.errors import SympifyError
from ..core.css import color_bluish

def latex_display(lhs, rhs, auto_display=True):
    """
    ```

    Display results in Latex format.

    Parameters
    ----------
    lhs : {str, list, tuple, ndarray, Series}
        The left hand side of the mathematical input.
    rhs : {str, list, tuple, ndarray, Series}
        The right hand side of the mathematical input.

    Returns
    -------
    None

    Examples
    --------
    >> lhs = ['f(x)']
    >> rhs = ['(x^2 - 1) / (x^2 + 8 * x + 15)']
    >> stm.latex_display(lhs, rhs)
    
    ## More values specified

    >> lhs = ['f(x)', 'g(x, y)']
    >> rhs = ['(x^2 - 1) / (x^2 + 8 * x + 15)',
              '(x^2 * y * sin(y)^2 + x^2 * y * cos(y)^2) / (x^2 + x)'
            ]
    >> stm.latex_display(lhs, rhs)

    >> lhs = ['f(x)', 'dy/dx']
    >> rhs = ['(x^2 - 1) / (x * sqrt(x^2 + 1))',
              '(3*x**2 + 1)/(x**2*(x**2 + 1)**(3/2))',
              '(3*x**2 + 1)/(x**4*sqrt(x**2 + 1) + x**2*sqrt(x**2 + 1))',
              '(-x**2*(x**2 - 1) + 2*x**2*(x**2 + 1) - (x**2 - 1)*(x**2 + 1))/(x**2*(x**2 + 1)**(3/2))'
            ]
    >> stm.latex_display(lhs, rhs)

    >> x, theta = sym.symbols('x alpha')
    >> h = sym.sympify('exp(-2 * alpha)/x + cos(pi * x)')
    >> lhs = ['f(x)', 'dy/dx'] + [f'd^{k} * x/(dy^{k})' for k in range(2, 6)]
    >> rhs = [sym.diff(h, x, n) for n in range(6)]
    >> stm.latex_display(lhs, rhs)

    ```
    """
    # lhs
    lhs = to_listuple(array_values=lhs, includes_str=True, par_name='lhs')
    # rhs
    rhs = to_listuple(array_values=rhs, includes_str=True, par_name='rhs')
    # check number of elements
    if len(lhs) > len(rhs):
        raise ValueError(f"'lhs' cannot have more elements than 'rhs'")
    if len(lhs) < len(rhs):
        lhs_count, rhs_count = (len(lhs), len(rhs))
        lhs += [''] * (lhs_count - rhs_count)
    # auto_display
    auto_display = val_boolean(auto_display, default=True)
    # begin latex
    latex_array = ['\\begin{aligned} \\\\']
    for index in range(len(lhs)):
        try:
            lhs_sym = sympify(lhs[index])
        except:
            lhs_sym = ''
        try:
            rhs_sym = sympify(rhs[index])
        except:
            raise SympifyError(
                par_name=f'rhs -> {rhs[index]}', user_input=rhs[index]
            )
        latex_row = (
            f'\\displaystyle {latex(lhs_sym)} &= {latex(rhs_sym)} \\\\[7pt]'
        )
        latex_array.append(latex_row)
    latex_array.append('\\end{aligned} \\\\[5pt]')
    latex_str = f"${' '.join(latex_array)}$".replace('.0 ', '')
    TEX = Latex(latex_str)
    if auto_display is True:
        display(TEX)
        return None
    else:
        return TEX
    
def matrix_to_eqtns(
    A, b, displaystyle=True, hspace=0, vspace=7, inline=True
):
    """
    ```

    Convert matrix to equations.

    A : array_like
        Coefficients matrix.
    b : array_like
        Constants matrix.
    hspace : int, default=0
        Horizontal space before the equations.
    vspace : int, default=7
        Vertical space between rows.
    inline : bool, default=True
        If `inline`, then use '$' (i.e. equations within text), 
        otherwise use '$$' (i.e. equations on independent lines).

    Returns
    -------

    Examples
    --------
    
    ```
    """
    A = Matrix(A)  # .replace(0, 123456789.987654)
    b = Matrix(b)
    Ax = []
    # create LHS Ax
    for row in range(A.shape[0]):
        terms_joined = " + ".join(
            [f"{value}*x{k+1}" for k, value in enumerate(A[row, :])]
        )
        Ax.append(sympify(terms_joined))
    Ax = Matrix(Ax)
    # join LHS (Ax) to RHS (b) to form Ax = b
    Axb = []
    for row in range(A.shape[0]):
        Axb.append([f"{latex(Ax[row, 0])} &= {latex(b[row, 0])}"])

    if displaystyle:
        displaystyle = "\\displaystyle"
    else:
        displaystyle = ""
    if inline:
        dollar = "$"
    else:
        dollar = "$$"

    if hspace == 0:
        hspace = ""
    else:
        hspace = "\\hspace{" + str(hspace) + "cm}"

    delimiter = f" \\\\[{str(vspace)}pt] \n\t"
    Axb = delimiter.join(flatten(Axb))
    Axb = (
        dollar + "\n" + hspace
        + displaystyle + "\n\\begin{aligned} \n\t"
        + Axb + " \n\\end{aligned} \n" + dollar
    )

    return Axb

def css_by_indices(x, indices, css_styles=None):

    if css_styles is None:
        css_styles = "background-color: orange; border:2px solid #000;"
    dframe = DataFrame("", index=x.index, columns=x.columns)
    dframe.iloc[tuple([tuple(item) for item in indices])] = css_styles

    return dframe

def dframe_color(
    dframe,
    style_indices,
    values=[],
    operator='',
    rows=[],
    cols=[],
    css_styles=None,
    decimals=8,
):
    """
    Color of DataFrame cells.

    Parameters
    ----------
    dframe : xxx
        xxx
    style_indices : xxx
        xxx
    values : xxx
        xxx
    operators : {'==', '<', '<=', '>', '>=', '<1&2', '<=1&2', '<1|2', '<=1|2'}, default='<'
    rows : xxx
        xxx
    cols : xxx
        xxx
    css_styles : xxx, default=None
        xxx
    decimals : int, default=8
        Number of decimal points

    Returns
    -------

    Examples
    --------
    import stemlab as stm
    >> df = datasets(id='sales')
    >> table_results = stm.dframe_color(
        dframe = df, 
        style_indices = [[1, 1], [3, 4]], 
        values = [2000], 
        operator='<', 
        rows=[2, 4, -1], 
        cols=[-1], 
        css_styles='color:blue;font-weight:bold;', 
        decimals=8)

    >> stm.dframe_color(
        dframe=df,
        style_indices=[[1, 2], [1, 1]],
        values=[],
        operator='',
        rows=[],
        cols=[],
        css_styles='color:blue;font-weight:bold;',
        decimals=8,
    )

    """
    # a user can specify either array indices, values, row or column indices
    M = array(dframe)
    if operator:
        if len(values) > 1:
            raise Exception(
                'When operator is specified, there must only be '
                'one value for the values parameter.'
            )
    try:
        row_count, column_count = dframe.shape
        if values:
            # will be True/False matrix, where True if value is in the array
            if len(values) == 1: 
                if operator == '==':
                    values = M[(M == values[0])]
                elif operator == '<':
                    values = M[(M < values[0])]
                elif operator == '<=':
                    values = M[(M <= values[0])]
                elif operator == '>':
                    values = M[(M > values[0])]
                elif operator == '>=':
                    values = M[(M >= values[0])]
                elif '&' in operator:
                    try:
                        operator_copy = (
                            operator.replace(' ', '')\
                            .replace('<', '')\
                            .replace('=', '')
                        )
                        a, b = operator_copy.split('&')
                        a, b = float(sympify(a)), float(sympify(b))
                        if '<=' in operator:
                            values = M[(M >= a) & (M <= b)]
                        else:
                            values = M[(M > a) & (M < b)]
                    except Exception as except_error:
                        raise Exception(except_error)
                elif '|' in operator:
                    try:
                        operator_copy = (
                            operator.replace(' ', '')\
                                .replace('<', '')
                                .replace('=', '')
                        )
                        a, b = operator_copy.split('|')
                        a, b = float(sympify(a)), float(sympify(b))
                        if "<=" in operator:
                            values = M[(M <= a) | (M >= b)]
                        else:
                            values = M[(M < a) | (M > b)]
                    except Exception as except_error:
                        raise Exception(except_error)
                else:
                    pass
        try:
            values = values.tolist()
        except:  # it is already a list
            pass
        values_indices = argwhere(isin(M, values) == 1).tolist()

        row_indices, col_indices, colrow_indices = [], [], []
        if rows + cols:
            if rows:
                row_indices = []
                for index in range(len(rows)):
                    for col in range(column_count):
                        row_indices.append([rows[index], col])
            if cols:
                for index in range(len(cols)):
                    for row in range(row_count):
                        col_indices.append([row, cols[index]])
            colrow_indices = row_indices + col_indices

        if style_indices:
            colrow_values = values_indices + colrow_indices
            if colrow_values:
                colrow_values = array(colrow_values)
                if len(colrow_values.shape) == 1:
                    colrow_values = colrow_values
                else:
                    colrow_values = colrow_values.T.tolist()
                indices_all = [
                    style_indices[0] + colrow_values[0],
                    style_indices[1] + colrow_values[1],
                ]
            else:
                indices_all = style_indices
            indices_all = array(indices_all).tolist()
        else:
            indices_all = values_indices + colrow_indices
            indices_all = array(indices_all).T.tolist()
        dframe = dframe.style.apply(
            css_by_indices, 
            indices=indices_all, 
            css_styles=css_styles, axis=None
        ).format(precision=decimals)
    except Exception as except_error:
        raise Exception(except_error)

    return dframe

def dframe_to_html(
    dframe,
    style_indices=[],
    values=[],
    operator='',
    rows=[],
    cols=[],
    row_title='',
    remove_tzeros=False,
    to_HTML=True,
    decimals=8,
):
    """
    Convert DataFrame to HTML code

    Parameters
    ----------
    dframe : xxx
        xxx
    style_indices : xxx
        xxx
    values : xxx
        xxx
    operator : xxx, default=''
        xxx
    rows : xxx
        xxx
    cols : xxx
        xxx
    row_title : xxx, default=''
        xxx
    remove_tzeros : xxx, default=False
        xxx
    to_HTML : xxx, default=True
        xxx
    decimals : xxx, default=8
        xxx

    Returns
    -------
    df_frame : str
        HTML code of the specified DataFrame.

    Examples
    --------

    """
    display_options()
    if style_indices + values + rows + cols:  # apply css
        try:
            df_original = dframe
            dframe = dframe_color(
                dfframe=dframe,
                style_indices=style_indices,
                values=values,
                operator=operator,
                rows=rows,
                cols=cols,
                css_styles='default',
                decimals=decimals,
            )
            # if no styling, then do not use Styler format
            if 'background-color:' not in dframe.to_html():
                dframe = df_original
        except Exception as except_error:
            raise Exception(except_error)

    dframe = dframe.to_html()
    dframe = dframe.replace(
        '<table border="1" class="dataframe">',
        '<table border="1" class="dataframe" rules = "all">',
    )
    dframe = dframe.replace(
        "<td>",
        '<td style = "text-align:right;min-width:450px;height:4px;color:red;font-family:courier;">',
    )
    dframe = dframe.replace(
        "<th>",
        '<th style = "text-align:right;min-width:30px;height:4px; line-height:23px;font-weight:normal;"">',
    )
    dframe = dframe.replace("<table", "\n\t\t<table")
    dframe = dframe.replace("</table>", "\n\t\t</table>\t")
    dframe = dframe.replace("<thead>", "\n<thead>")
    dframe = dframe.replace("</thead>", "\t\t\t</thead>")
    dframe = dframe.replace("<tbody>", "\n\t\t\t<tbody>")
    dframe = dframe.replace("</tbody>", "\t\t\t</tbody>")
    dframe = dframe.replace("<tr", '\t\t\t<tr style="line-height:23px;"')
    dframe = dframe.replace("</tr", "\t\t\t</tr")
    dframe = dframe.replace("<th", "\t\t\t\t<th")
    dframe = dframe.replace("<td", "\t\t\t\t<td")
    # for css styled dfframe
    dframe = dframe.replace(
        "<th ", '<th style="text-align:center;font-weight:normal;line-height:23px;" '
    )
    dframe = dframe.replace(
        "></th>", f'><div style="padding:0px;">{row_title}</div></th>'
    )
    dframe = dframe.replace(
        ">&nbsp;</th>", f'><div style="padding:0px;">{row_title}</div></th>'
    )
    dframe = dframe.replace(
        "<td ",
        f'<td style="font-family:courier;font-size:18px;text-align:right;min-width:50px;"',
    )
    dframe = dframe.replace(">NaN</td>", "></td>").replace(
        ">nan</td>", "></td>"
    )

    if remove_tzeros == "Removed for now":  # this has been removed for now
        dframe = dframe.replace(".00000000000000</td>", "</td>")
        dframe = dframe.replace(".0000000000000</td>", "</td>")
        dframe = dframe.replace(".000000000000</td>", "</td>")
        dframe = dframe.replace(".00000000000</td>", "</td>")
        dframe = dframe.replace(".0000000000</td>", "</td>")
        dframe = dframe.replace(".000000000</td>", "</td>")
        dframe = dframe.replace(".00000000</td>", "</td>")
        dframe = dframe.replace(".0000000</td>", "</td>")
        dframe = dframe.replace(".000000</td>", "</td>")
        dframe = dframe.replace(".00000</td>", "</td>")
        dframe = dframe.replace(".0000</td>", "</td>")
        dframe = dframe.replace(".000</td>", "</td>")
        dframe = dframe.replace(".00</td>", "</td>")
        dframe = dframe.replace(".0</td>", "</td>")
    if to_HTML is True:
        df_frame = HTML(f"<p>{dframe}</p>")
    else:
        df_frame = f"<p>{dframe}</p>"

    return df_frame

def pzt_table(*args):
    """
    Table for presenting statistics for proportion and mean comparison tests.
    """
    (table_title, sample1_name,  sample2_name, n1, n2, n12, n12_diff,
     mean1, mean2, mean12, mean12_diff, std1, std2, std12, std12_diff,
     sem1, sem2, sem12, sem12_diff, LCI1, UCI1, LCI2, UCI2, LCI12,
     UCI12, LCI12_diff, UCI12_diff, test_value, hyp_mean, dfn, dfn_name, 
     hyp_sign, crit_value, p_value, conf_level, sig_level, one_sample, 
     decision, conclusion, decimals) = args
    
    if 'z' in table_title:
        test_name = 'z'
        dfn_str = ''
        dfn_equals = ''
        dfn_name = ''
    else:
        test_name = 't'
        dfn_str = round(dfn, decimals)
        dfn_equals = '='

    if hyp_mean % 1 == 0:
        hyp_mean = int(hyp_mean)
    sample1_name = sample1_name[:12]
    if 'one' not in table_title.lower():
        sample2_name = sample2_name[:12]
    if sig_level * 100 % 1 == 0:
        sig_level_str = int(sig_level * 100)
    else:
        sig_level_str = round(sig_level * 100, decimals)

    if conf_level * 100 % 1 == 0:
        conf_level_str = int(conf_level * 100)
    else:
        sig_level_str = round(sig_level * 100, decimals)

    if one_sample is True:
        sample1_name = sample1_name.replace('_', ' ').replace('Sample 1', 'x')
        result_table = (
            f'\n\t\t\t<div style="margin-bottom:3px;"> \n'
            f"\t\t\t\t\({{\\color{{{color_bluish()}}}{{\\text{{{table_title}}}}}}}\) \n"
            f"\t\t\t</div>\n\n"
            f"\t\t\t<div> \n"
            f"\t\t\t\t\( \n"
            f"\t\t\t\t\\begin{{array}}{{l|rrrrrr}} \\hline \n"
            f"\t\t\t\t\t\\text{{Sample}} & \\text{{N}} & \\text{{Mean}} & \\text{{Diff}} & \\text{{SD}} & \\text{{SE}} & {conf_level_str}\% ~ \\text{{LCI}} & {conf_level_str}\% ~ \\text{{UCI}} \\\\[5pt] \\hline \n"
            f"\t\t\t\t\t\\text{{{sample1_name}}} & {n1} & {round(mean1, decimals)} & {round(mean1 - hyp_mean, decimals)} & {round(std1, decimals)} & {round(sem1, decimals)} & {round(LCI1, decimals)} & {round(UCI1, decimals)} \\\\ \\hline \n"
            f"\t\t\t\t\\end{{array}} \n"
            f"\t\t\t\t\) \n"
            f"\t\t\t</div> \n"
            
            f"\n\t\t\t<div> \n"
            f"\t\t\t\t\( \n"
            f"\t\t\t\t\\begin{{array}}{{lrcr}} \n"
            f"\t\t\t\t\t\\text{{Hypothesis}} & \\hspace{{2.5cm}} \\text{{Description}} & ~ & \\text{{Statistic}} \\\\[2pt] \\hline \n"
            f"\t\t\t\t\t\\text{{H}}_{{0}} : \\mu_\\text{{{sample1_name}}} = {hyp_mean} & \\text{{{test_name}-calculated}} & = & {round(test_value, decimals)} \\\\[2pt] \n"
            f"\t\t\t\t\t\\text{{H}}_{{1}} : \\mu_\\text{{{sample1_name}}} {hyp_sign} {hyp_mean} & \\text{{{dfn_name}}} & {dfn_equals} & {dfn_str} \\\\[2pt] \n"
            f"\t\t\t\t\t\\text{{Conf. level}} = { round(conf_level, decimals) } ~ ({conf_level_str}\%) & \\text{{{test_name}-critical}} & = & {round(crit_value, decimals)} \\\\[2pt] \n"
            f"\t\t\t\t\t\\text{{Sig. level}} ~ (\\alpha) = {round(sig_level, decimals)} ~ ({sig_level_str}\%) & \\text{{p-value}} & = & {round(p_value, decimals)} \\\\ \\hline \n"
            f"\t\t\t\t\\end{{array}} \n"
            f"\t\t\t\t\) \n"
            f"\t\t\t</div> \n"

            f'\n\t\t\t<div style="margin-top:15px">\n\t\t\t\t\({{\\color{{{color_bluish()}}}{{\\text{{Decision}}}}}}\)\n\t\t\t</div>'
            f'\n\n\t\t\t<div style="margin-top:10px; margin-bottom:10px;">\n\t\t\t\t{decision}\n\t\t\t</div>'
            f'\n\n\t\t\t<div>\n\t\t\t\t\({{\\color{{{color_bluish()}}}{{\\text{{Conclusion}}}}}}\)\n\t\t\t</div>'
            f'\n\n\t\t\t<div style="margin-top:10px;">\n\t\t\t\t{conclusion}\n\t\t\t</div> \n'
        )
    else:
        if 'paired' in table_title.lower():
            comb_row = ""
            diff_row = f"\\text{{Difference}} & {n12_diff} & {round(mean12_diff, decimals)} & {round(std12_diff, decimals)} & {round(sem12_diff, decimals)} & {round(LCI12_diff, decimals)} & {round(UCI12_diff, decimals)} \\\\ \\hline"
        else:
            comb_row = f"\\text{{Overall}} & {n12} & {round(mean12, decimals)} & {round(std12, decimals)} & {round(sem12, decimals)} & {round(LCI12, decimals)} & {round(UCI12, decimals)} \\\\ \\hline"
            diff_row = f"\\text{{Difference}} & ~ & {round(mean12_diff, decimals)} & ~ & {round(sem12_diff, decimals)} & {round(LCI12_diff, decimals)} & {round(UCI12_diff, decimals)} \\\\ \\hline"
        result_table = (
            f'\n\t\t\t<div style="margin-bottom:3px;"> \n'
            f"\t\t\t\t\({{\\color{{{color_bluish()}}}{{\\text{{{table_title}}}}}}}\) \n"
            f"\t\t\t</div>\n\n"
            f"\t\t\t<div> \n"
            f"\t\t\t\t\( \n"
            f"\t\t\t\t\\begin{{array}}{{l|rrrrrr}} \\hline \n"
            f"\t\t\t\t\t\\text{{Samples}} & \\text{{N}} & \\text{{Mean}} & \\text{{SD}} & \\text{{SE}} & {conf_level_str}\% ~ \\text{{LCI}} & {conf_level_str}\% ~ \\text{{UCI}} \\\\[2pt] \\hline \n"
            f"\t\t\t\t\t\\text{{{sample1_name.replace('_', ' ')}}} & {n1} & {round(mean1, decimals)} & {round(std1, decimals)} & {round(sem1, decimals)} & {round(LCI1, decimals)} & {round(UCI1, decimals)} \\\\[2pt] \n"
            f"\t\t\t\t\t\\text{{{sample2_name.replace('_', ' ')}}} & {n2} & {round(mean2, decimals)} & {round(std2, decimals)} & {round(sem2, decimals)} & {round(LCI2, decimals)} & {round(UCI2, decimals)} \\\\[2pt] \\hline \n"
            f"\t\t\t\t\t{comb_row}"
            f"\t\t\t\t\t{diff_row}"
            f"\n\t\t\t\t\\end{{array}} \n"
            f"\t\t\t\t\) \n"
            f"\t\t\t</div> \n"

            f"\n\t\t\t<div> \n"
            f"\t\t\t\t\( \n"
            f"\t\t\t\t\\begin{{array}}{{lrcr}} \n"
            f"\t\t\t\t\t\\text{{Hypothesis}} & \\hspace{{2.5cm}} \\text{{Description}} & ~ & \\text{{Statistic}} \\\\[2pt] \\hline \n"
            f"\t\t\t\t\t\\text{{H}}_{{0}} : \\mu_\\text{{{sample1_name}}} = \\mu_\\text{{{sample2_name}}} & \\text{{{test_name}-calculated}} & = & {round(test_value, decimals)} \\\\[2pt] \n"
            f"\t\t\t\t\t\\text{{H}}_{{1}} : \\mu_\\text{{{sample1_name}}} {hyp_sign} \\mu_\\text{{{sample2_name}}} & \\text{{{dfn_name}}} & {dfn_equals} & {dfn_str} \\\\[2pt] \n"
            f"\t\t\t\t\t\\text{{Conf. level}} = {round(conf_level, decimals)} ~ ({conf_level_str}\%) & \\text{{{test_name}-critical}} & = & {round(crit_value, decimals)} \\\\[2pt] \n"
            f"\t\t\t\t\t\\text{{Sig. level}} ~ (\\alpha) = {round(sig_level, decimals)} ~ ({sig_level_str}\%) & \\text{{p-value}} & = & {round(p_value, decimals)} \\\\ \\hline \n"
            f"\t\t\t\t\\end{{array}} \n"
            f"\t\t\t\t\) \n"
            f"\t\t\t</div> \n"

            f'\n\t\t\t<div style="margin-top:15px">\n\t\t\t\t\({{\\color{{{color_bluish()}}}{{\\text{{Decision}}}}}}\)\n\t\t\t</div>'
            f'\n\n\t\t\t<div style="margin-top:10px; margin-bottom:10px;">\n\t\t\t\t{decision}\n\t\t\t</div>'
            f'\n\n\t\t\t<div>\n\t\t\t\t\({{\\color{{{color_bluish()}}}{{\\text{{Conclusion}}}}}}\)\n\t\t\t</div>'
            f'\n\n\t\t\t<div style="margin-top:10px;">\n\t\t\t\t{conclusion}\n\t\t\t</div> \n'
        )

    return result_table

def file_path_name(file_path):
    """
    Validate file path and name.
    """
    if file_path is None:
        date_time = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
        file_path = f'{os.getcwd()}/results-{date_time}.tex'
    else:
        file_path = str(file_path)
        if '/' in file_path:
            file_path, file_name = file_path.rsplit(sep='/', maxsplit=1)
        else:
            file_name = file_path # what is given is a file name without path
            file_path = os.getcwd()
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
                file_path = f'{file_path}/{file_name}'
            except OSError:
                raise OSError(f"Couldn't create the folder '{file_path}'")
        # check that the file path exists
        if not os.path.exists(file_path):
            raise OSError(
                f"The file path '{file_path}' does not exist on "
                "this computer")
            
    return file_path
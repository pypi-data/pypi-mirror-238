import os
from IPython.display import display, HTML
from webbrowser import open_new_tab, open_new
from ...core.arraylike import is_iterable
from ...core.errors import IterableError
from ...core.css import color_bluish

dir_files = os.path.dirname(os.path.realpath(__file__))

def view_html(file_name, new_window=False):
    """
    Open HTML file in the default browser.
    """
    if new_window:
        open_new(file_name)
    else:
        open_new_tab(file_name)

def html_header():
    """
    Read the header file into a list.
    """
    with open(f'{dir_files}/header_html.html', 'r') as read_file:
        lines = read_file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        
    return lines

def html_footer():
    """
    Read the footer file into a list.
    """
    with open(f'{dir_files}/footer_html.html', 'r') as read_file:
        lines = read_file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        
    return lines

def write_html(file_name, html_list):
    """
    Write results to a file.
    """
    # validate
    if '.' not in file_name:
        file_name = f'{file_name}.html'

    _, file_extn = file_name.rsplit(sep='.', maxsplit=1)
    if not file_name.endswith('.html'):
        raise ValueError(
            f"'file_name' expected '.html' extension, got >> .{file_extn}"
        )
    if isinstance(html_list, str):
        html_list = [html_list]
    if not is_iterable(array_like='html_list', includes_str=True):
        raise IterableError(
            par_name='html_list', includes_str=True, user_input=html_list
        )
    # begin
    file_path = os.getcwd()
    file_name = f'{file_path}/{file_name}'
    with open(file_name, 'w') as write_file:
        # header
        for line in  html_header():
            write_file.write(f'{line}\n')
        # body
        for html_line in html_list:
            write_file.write(f'\t\t<p>\n\t\t\t{html_line}\n\t\t</p>\n\n')
        # comment below results
        browser_code = (
            f'<span style="color:{color_bluish()};">'
            f"stm.view_html('{file_name}')</span>"
        ).replace('\\', '/')
        view_in_browser = (
            '\t\t<p style="color: #777">\n\t\t\tTo view results in browser, '
            f"run the code below : <br /></span>{browser_code}\n\t\t</p>"
        )
        # do not show this for now
        # write_file.write(view_in_browser)

        # footer
        for line in html_footer():
            write_file.write(f'{line}\n')
    
    # display result
    display(HTML(filename=file_name))
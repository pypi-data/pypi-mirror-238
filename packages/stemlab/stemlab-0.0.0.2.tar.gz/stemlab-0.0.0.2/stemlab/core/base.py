import re
from numpy import sign
from pandas import DataFrame, Series
from ..core.arraylike import to_listuple

import string
import random

def rand_string(
    n=12, digits=True, include_lower=False, symbols=False
):
    """
    ```

    Generate random strings

    Parameters
    ----------


    Returns
    -------


    Examples
    --------
    >> id = pd.DataFrame([rand_string() for _ in range(n)], columns=['id'])
    ```
    """
    string_ = string.ascii_uppercase
    if digits is True:
        string_ += string.digits
    if include_lower:
        string_ = string.ascii_lowercase
    if symbols is True:
        string_ += string.symbols
    string_ = ''.join(random.choices(string_, k=n))
    #string_ = [rand_string(n=n) for _ in range(n)]
    
    return string_

def plural_sing(singular, plural, n):
    """
    Return plural or singular e.g. was/were, is/are, this/these, etc.
    """
    if n > 1:
        return  plural
    return singular

def strip_all(string_):
    """
    ```

    Remove all white spaces (leading, trailing and internal).

    Parameter
    ---------
    string_ : str
        A string containing the white spaces to be removed.

    Returns
    -------
    stripped_string : str
        A string with all white spaces removed.

    Examples
    --------

    ```
    """
    stripped_string = ' '.join(string_.split())

    return stripped_string

def chars_replace(
        df, chars_to_replace, replace_with='', columns='all', regex=True
) -> DataFrame:
    """
    ```

    Replace specified characters in a DataFrame.

    Parameters
    ----------
    df : DataFrame
        The DataFrame that contains the values to be replaced.
    
    chars_to_replace : str
        The characters in the DataFrame that need to be replaced.
    
    replace_with : str
        The string that should replace the characters specified in 
        ``replace_with``.
    
    columns : {str, list, tuple, ndarray, Series}, default='all'
        Column(s) that contain the characters to be replaced.

    Returns
    -------
    df : DataFrame
        A DataFrame with the characters replaced.
    
    Examples
    --------
    >>>

    ```
    """
    chars_to_replace = '[{' + re.escape(''.join(chars_to_replace)) + '}]'
    if isinstance(columns, str):
        if columns == 'all':
            columns = list(df.columns)
        else:
            columns = [columns]
    else:
        columns = list(columns)
    df = df[columns].replace(chars_to_replace, replace_with, regex=regex)
    
    return df

def pm_sign(value):
    """
    Returns the sign of a numerical value.
    """
    try:
        sign_ = '+'
        if sign(value) == -1:
            sign_ = '-'
    except:
        raise TypeError("Unable to get the sign of '{value}'")

    return sign_

def partial_chars(list_string):
    """
    ```

    Return partial substring for each of the words in the specified iterable.

    Parameters
    ----------
    list_string: {str, list}
        A string or list of strings containing the word/text whose characters
        are to be returned as partial substrings.

    Examples
    --------
    >> stm.partial_chars(list_string = 'subtract')
    >> array(['s', 'su', 'sub', 'subt', 'subtr', 'subtra', 'subtrac', 'subtract'],
             dtype=object)

    >> stm.partial_chars(list_string = ['add', 'subtract'])
    >> array(['a', 'ad', 'add', 's', 'su', 'sub', 'subt', 'subtr', 'subtra',
              'subtrac', 'subtract'], dtype=object)

    Returns
    -------
    result: 1d array
        A 1D Numpy array.

    ```
    """
    list_string = to_listuple(
        array_values=list_string, includes_str=True, par_name='list_string'
    )
    result = []
    for item in list_string:
        chars_count = len(item)
        for k in range(chars_count):
            result.append(item[:k+1])
    # remove duplicates do avoid ambiquity
    result = Series(result).drop_duplicates(keep = False).values
            
    return result
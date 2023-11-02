from numpy import ndarray, round
from pandas import Series, DataFrame

def get_varname(values):
    """
    ```

    Return the variable name for a specified value.

    Parameters
    ----------
    values : Any
        The value whose variable name should be returned.

    Returns
    varname : str
        The name to which ``value`` is assigned.

    Examples
    --------
    >> a = 5
    >> b = get_var_name(a)
    ```
    """
    for varname, value in globals().items():
        if value is values:
            return varname

class IterableError(TypeError):
    def __init__(
            self, par_name='object', includes_str=False, user_input='...'
    ):
        self.user_input = user_input
        self.par_name = par_name
        self.data_types = 'str, tuple, list, set, ndarray, Series'
        if includes_str is False:
            self.data_types = 'tuple, list, set, ndarray, Series'
    def __str__(self):
        return (
            f"'{self.par_name}' must be one of: {self.data_types}; "
            f"got {self.user_input}"
        )
    
class ColumnsLengthError(Exception):
    def __init__(self, dframe=None, col_names='col_names'):
        self.col_names = col_names
        self.dframe = DataFrame(dframe)
    def __str__(self):
        if self.dframe is None:
            expected = ''
        else:
            expected = f", expected {self.dframe.shape[1]} column names"
        if self.col_names is None:
            col_names = ''
        else:
            col_names = f" in '{self.col_names}'"
        return (
            f"Number of elements{col_names} must be equal to the number of "
            f"columns in the DataFrame{expected}"
        )

class RowLengthError(Exception):
    def __init__(self, par_name='index_names', dframe=None):
        self.par_name = par_name
        self.dframe = DataFrame(dframe)
    def __str__(self):
        if self.dframe is None:
            expected = ''
        else:
            expected = f", expected {self.dframe.shape[1]} row/index names"
        if self.par_name is None:
            par_name = ''
        else:
            par_name = f" in '{self.par_name}'"
        return (
            f"Number of elements{par_name} must be equal to the number "
            f"of rows in the DataFrame{expected}"
        )
    
class RequiredError(ValueError):
    def __init__(self, par_name, required_when=None):
        self.par_name = par_name
        self.required_when = required_when
    def __str__(self):
        if self.required_when is None:
            required = ''
        else:
            required = f". It is required when `{self.required_when}`"
        return (
            f"You have not provided an argument for '{self.par_name}'{required}"
        )
        
class MaxNError(ValueError):
    def __init__(self, par_name, user_input, maxn):
        self.par_name = par_name
        self.user_input = user_input
        self.maxn = maxn
    def __str__(self):
        return (
            f"'{self.par_name}' must be less than or equal to "
            f"n <= {self.maxn}, got >> {self.user_input}"
        )
     
class NotInColumnsError(ValueError):
    def __init__(self, par_name, user_input):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (
            f"'{self.user_input}' as specified in '{self.par_name}' "
            "is not one of the DataFrame columns"
        )
    
class DataFrameError(TypeError):
    def __init__(self, par_name='dframe', user_input='...'):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (
            f"Expected '{self.par_name}' to be a DataFrame, "
            f"got >> {type(self.user_input)}"
        )
       
class StringError(TypeError):
    def __init__(self, par_name, user_input):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (
            f"Expected '{self.par_name}' to be a string, "
            f"got >> {type(self.user_input)}"
        )
    
class NumpifyError(ValueError):
    def __init__(self, par_name='input'):
        self.par_name = par_name
    def __str__(self):
        return (f"Unable to convert '{self.par_name}' to 1D Numpy array")
        
class PandifyError(ValueError):
    def __init__(self, par_name='data'):
        self.par_name = par_name
    def __str__(self):
        return (f"Unable to convert '{self.par_name}' to a DataFrame")
  
class SerifyError(ValueError):
    def __init__(self, par_name='data'):
        self.par_name = par_name
    def __str__(self):
        return (f"Unable to convert '{self.par_name}' to a Series")

class NumericError(ValueError):
    def __init__(self, par_name, prefix='', user_input='...'):
        self.par_name = par_name
        self.prefix = prefix
        self.user_input = user_input
    def __str__(self):
        return (
            f"'{self.prefix}{self.par_name}' must be an integer or float, "
            f"got >> '{self.user_input}'"
        )
   
class NumpifyError(ValueError):
    def __init__(self, par_name='input'):
        self.par_name = par_name
    def __str__(self):
        return (f"Unable to convert '{self.par_name}' to 1D Numpy array")
    
class NotSpecifiedError(ValueError):
    def __init__(self, par_name, par_name_arg, user_input):
        self.par_name = par_name
        self.par_name_arg = par_name_arg
        self.user_input = user_input
    def __str__(self):
        return (
            f"'{self.par_name}' must be specified when "
            f"{self.par_name_arg}, got >> {self.user_input}"
        )

class IntegerError(ValueError):
    def __init__(self, par_name, limits=None, boundary='', user_input=None):
        self.par_name = par_name
        self.limits = limits
        self.boundary = boundary
        self.user_input = user_input
    def __str__(self):
        if self.boundary:
            self.boundary = f' {self.boundary}'
        if self.limits is not None:
            a, b = self.limits
            return (
                f"'{self.par_name}' must be an integer between "
                f"{a} and {b}{self.boundary}, got >> {self.user_input}"
            )
        return (
            f"'{self.par_name}' must be an integer (whole number), "
            f"got >> {self.user_input}"
        )

class FloatError(ValueError):
    def __init__(self, par_name, limits=None, boundary='', user_input=None):
        self.par_name = par_name
        self.limits = limits
        self.boundary = boundary
        self.user_input = user_input
    def __str__(self):
        if self.boundary:
            self.boundary = f' {self.boundary}'
        if self.limits is not None:
            a, b = self.limits
            return (
                f"'{self.par_name}' must be float (number with decimals) "
                f"between {a} and {b}{self.boundary}, got >> {self.user_input}"
            )
        return (
            f"'{self.par_name}' must be a float (number with decimals), "
            f"got >> {self.user_input}"
        )

class NumericBtwnError(ValueError):
    def __init__(self, par_name, limits=None, boundary='', user_input=None):
        self.par_name = par_name
        self.limits = limits
        self.boundary = boundary
        self.user_input = user_input
    def __str__(self):
        if self.boundary:
            self.boundary = f' {self.boundary}'
        if self.limits is not None:
            a, b = self.limits
            return (
                f"'{self.par_name}' must be a number between "
                f"{a} and {b}{self.boundary}, got >> {self.user_input}"
            )
        return (
            f"'{self.par_name}' must be a numeric value, "
            f"got >> {self.user_input}"
        )

class BooleanError(ValueError):
    def __init__(self, par_name, user_input):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (
            f"'{self.par_name}' must be boolean (True/False), "
            f"got >> {self.user_input}"
        )

class UnivariatePolyError(ValueError):
    def __init__(self, par_name, user_input):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (
            f"'{self.par_name}' must be a univariate polynomial, "
            f"got >> {self.user_input}"
        )

class SympifyError(ValueError):
    def __init__(self, par_name=None, user_input='value'):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        if self.par_name is None:
            return (
                f"Failed to convert '{self.user_input}' into a "
                f"mathematical expression or array"
            )
        else:
            return (
                f"'{self.par_name}' must be a valid mathematical "
                f"expression or array, got >> {self.user_input}"
            )

class SymbolicExprError(ValueError):
    def __init__(self, par_name, user_input):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (
            f"'{self.par_name}' must be a symbolic expression, "
            f"got >> {self.user_input}"
        )

class SymbolicVarsError(ValueError):
    def __init__(self, par_name='the expression'):
        self.par_name = par_name
    def __str__(self):
        return (f"Unable to obtain symbolic variables from '{self.par_name}'")

class ListTupleError(TypeError):
    def __init__(self, par_name, user_input):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (
            f"'{self.par_name}' must be a list, tuple, or 1D Numpy array, "
            f"got >> {self.user_input}"
        )

class SingularMatrixError(ValueError):
    def __init__(self, par_name, user_input):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (f"'{self.par_name}' is a singular matrix (det = 0)")

class DictionaryError(TypeError):
    def __init__(self, par_name, user_input):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (
            f"'{self.par_name}' must be dictionary, "
            f"got >> {self.user_input}"
        )

class NotInValuesError(ValueError):
    def __init__(self, par_name, valid_items, user_input):
        self.par_name = par_name
        self.valid_items = valid_items
        self.user_input = user_input
    def __str__(self):
        try:
            valid_items = ', '.join(map(str, self.valid_items))
        except:
            pass
        return (
            f"'{self.par_name}' must be one of: {valid_items}; "
            f"got >> {self.user_input}"
        )

class VectorLengthError(ValueError):
    def __init__(self, par_name, n, label='exactly', user_input=''):
        self.par_name = par_name
        self.n = n
        self.label = label
        self.user_input = user_input
    def __str__(self):
        s = ''
        if self.n > 1:
            s = 's'
        return (
            f"'{self.par_name}' must have {self.label} {self.n} element{s}, "
            f"got >> {self.user_input}"
        )

class LengthDifferError(ValueError):
    def __init__(self, par_name, user_input):
        self.par_name = par_name
        self.x, self.y = user_input
    def __str__(self):
        pars = self.par_name.replace(' ', '').replace(',', ' and ')
        return (
            f"{pars} must have the same number of elements, "
            f"got >> {len(self.x)} and {len(self.y)} elements respectively"
        )

class SquareMatrixError(ValueError):
    def __init__(self, par_name, dims=['r', 'c']):
        self.par_name = par_name
        self.dims = dims
    def __str__(self):
        dims = f'{self.dims[0]} rows, {self.dims[1]} columns'
        return (
            f"'{self.par_name}' must be a square matrix, got >> {dims}"
        )
    
class CompatibliltyError(ValueError):
    def __init__(
            self, 
            A = 'first array',
            B = 'second array',
            multiplication = True, 
            dims_A = ('m', 'p'), 
            dims_B = ('p', 'q')
    ):
        self.multiplication = multiplication
        self.A = A
        self.B = B
        self.dims_A = dims_A
        self.dims_B = dims_B
    def __str__(self):
        if self.multiplication is True:
            text = (
                f"Number of columns of '{self.A}' must be equal to the number "
                f"of rows of '{self.B}', got '{self.A}' size = {self.dims_A} "
                f"and '{self.B}' size = {self.dims_B}"
            )
        else:
            text = (
                f"Both '{self.A}' and '{self.B}' must have the same size, "
                f"got >> '{self.A}' size = {self.dims_A} and '{self.B}' "
                f"size = {self.dims_B}"
            )
        return (f"The arrays you have entered are not compatible. {text}")

class LowerGEUpperError(ValueError):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __str__(self):
        return (
            f"Lower limit {self.a} cannot be greater than upper limit "
            f"{self.b}"
        )

class IntervalError(ValueError):
    def __init__(self, par_name='h', gte=False):
        self.par_name = par_name
        self.gte = gte
    def __str__(self):
        gt = 'greater than'
        if self.gte is True:
            gt += ' or equal to'
        return (f"'{self.par_name}' cannot be {gt} |b-a|")
    
class InvalidError(ValueError):
    def __init__(self, par_name='parameter', user_input='Input'):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (
            f"'{self.user_input}' is an invalid value for {self.par_name}"
        )

class NonNumericError(ValueError):
    def __init__(self, par_name='', user_input=''):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        return (
            f"Expected all values in '{self.par_name}' to be numeric, "
            f"got {self.user_input}"
        )
        
class DifferenceError(ValueError):
    def __init__(self, par_name, user_input):
        self.par_name = par_name
        self.user_input = user_input
    def __str__(self):
        if len(self.user_input) > 10:
            self.user_input = f"[{', '.join(map(str, self.user_input[:10]))}, ...]"
        return (
            f"Difference between elements of '{self.par_name}' must be "
            f"constant, got {self.user_input}"
        )
    
class NoRootInInterval(ValueError):
    def __init__(self, user_input):
        self.user_input = user_input
    def __str__(self):
        a, b = self.user_input
        return (
            "The given function does not have a root in the interval "
            f"[{round(a, 8)}, {round(b, 8)}]"
        )
    
class CoeffConstantsError(ValueError):
    def __init__(self, user_input):
        self.user_input = user_input
    def __str__(self):
        A, b = self.user_input
        Asize, bsize = A.shape, b.shape
        return (
            "The coefficients matrix and vector of constants are not "
            f"compatible, got >> 'matrix_or_eqtns' size = {Asize}, "
            f"'b' size = {bsize}"
        )
    
class ValidationError(ValueError):
    def __init__(self, validation_name):
        self.validation_name = validation_name
    def __str__(self):
        return (f"Unable to validate {self.validation_name}")
    
def NotSubsetError(list_to_check, check_in_list):
    """
    Check if a given list is a subset of another list.
    """
    list_to_check_set = set(list_to_check)
    check_in_list_set = set(check_in_list)
    if not list_to_check_set.issubset(check_in_list_set):
        not_in_list = list(list_to_check_set.difference(check_in_list_set))
        not_in_list = ', '.join(map(str, not_in_list))
        if len(not_in_list) == 1:
            not_in_list = f"'{not_in_list[0]}' was"
        else:
            not_in_list = f"'{not_in_list}' were"
        raise ValueError(
            f"{not_in_list} not found in {check_in_list}"
        )
    

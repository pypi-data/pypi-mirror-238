from .diffintegration import diff_parametric
from .nonlinear import roots_nonlinear
from .numericaldifff import (
    diff_richardson
)
from .numericalint import (
    int_cotes, int_cotes_data, int_composite, 
    int_composite_data, int_romberg, int_glegendre
)
from .odes import int_odes
from .vector import (
    parametric_form, int_line, int_vector, int_surface
)
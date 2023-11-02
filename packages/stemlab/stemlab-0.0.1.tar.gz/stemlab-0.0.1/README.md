## stemlab

Stemlab is a Python library for performing mathematical computations.
It aims to become a first choice library for trainers and students
in Science, Technology, Engineering and Mathematics (STEM).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the Stemlab library.

```bash
pip install stemlab
```

## Usage

The library is imported into a Python session by running the following import statement.

```python
import stemlab as stm
```

## Examples

We will give a few examples that will demonstrate the use of the Stemlab library. Before that, the following libraries need to be installed.

```python
import numpy as np
import sympy as sym
import pandas as pd
import matplotlib.pyplot as plt
```

### Differentiation of parametric equations

```
x = 't^3 + 3 * t^2'
y = 't^4 - 8 * t^2'
result = stm.diff_parametric(f=x, g=y, dependent=t, n=3)
result
```

### Richardson extrapolation

```
f = '2**x * sin(x)'
x = 1.05
h = 0.4
n = 4
table, result = stm.diff_richardson(f, x, n, h, col_latex=False, index_labels='default', decimals=10)
table
```

### Gauss-Legendre quadrature integration

```
f = '(x^2 + 2 * x + 1) / (1 + (x + 1)^4)'
a, b, n = (0, 2, 4)
table, result = stm.int_glegendre(f, a, b, n, decimals=12)
table
```

### Initial value problems

```
f = 'y - t^2 + 1'
dydx = ['y - t^2 - 2*t + 1', 'y - t^2 - 2*t - 1', 'y - t^2 - 2*t - 1', 'y - t^2 - 2*t - 1']
ft = '(t + 1)^2 - 0.5*exp(t)'
a, b = (0, 2)
y0 = 0.5
h = 0.2

## Taylor order 4

table, figure = stm.int_odes(
	method = 'taylor4',
	ode_equation=f,
	exact_solution=ft,
	time_span=[a, b],
	initial_y=y0,
	ode_derivs=dydx,
	decimals=12
)
table

## Fourth order Runge-Kutta

table, figure = stm.int_odes(
	method = 'rk4',
	ode_equation=f,
	exact_solution=ft,
	time_span=[a, b],
	initial_y=y0,
	hmin=.01,
	hmax=.25,
	tolerance=1e-5,
	decimals=12
)
table
```

## Support

For any support on any of the functions in this library, send us an email at: ```stemxresearch@gmail.com```. We are willing to offer the necessary support where we possibly can.

## Roadmap

Future releases aim to make Stemlab a first choice library for students, trainers and professionals in Science, Technology, Engineering and Mathematics (STEM).

## Contributing

To make Stemlab a successful library while keeping the code easy. We welcome any valuable contributions towards the development and improvement of this library. 

For major changes to the library, please open an issue with us first to discuss what you would like to change and we will be more than willing to make the changes.

## Authors and acknowledgement

We are grateful to the incredible support from our developers at ```Stem Research```.

## License

[MIT](https://choosealicense.com/licenses/mit/)

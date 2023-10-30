# multipoly

A multivariate polynomial module.

This package provides a single class, `MultiPoly`, to handle multivariate polynomials of form

$$
    p(\vec{x}) = \sum_{0\leq n\leq\deg(p)}a_n(\vec{x}-\vec{c})^n = \sum_{n_0=0}^{\deg_0(p)}\cdots\sum_{n_{\dim(p)-1}=0}^{\deg_{\dim(p)-1}(p)}a_{n_0\cdots n_{\dim(p)-1}}(x_0-c_0)^{n_0}\cdots(x_{\dim(p)-1}-c_{\dim(p)-1})^{n_{\dim(p)-1}}
$$

where $n$ and $\deg(p)$ are multi-indices.
This differs from the usual upper sum limit $|n|\leq\deg(p)$ where $n$ is a multi-index and $\deg(p)$ a natural number,
because this way the degree in every variable can be controlled individually.

## Installation

```
pip install multipoly
```

## Usage

A polynomial can be initialized in two ways:
 - With the constructor `Multipoly(a, c=None)`, that takes the coefficients and optional offsets.
  The coefficients are of shape `deg`, that is a tuple with the degree for every variable.
 - By fitting data with `Multipoly.fit(X, y, deg, c=None)`.

`MultiPoly` objects have
- a dimension `dim`, the number of variables &
- a degree `deg`, the degrees in its variables.

They can
- be called on a single datapoint `p(x, y, ...)` or on multiple datapoints in a 2D `numpy.array`,
- rounded `p.round(decimals=0)`, to round coefficients `a` and offsets `c` &
- be converted to strings with `toString(symbols=None)`, where the symbols for its variables can be specified
  (`__str__` defaults to `x0, x1, ...`).

## License (MIT)

Copyright (c) 2023 Sebastian Gössl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

import numpy as np



class MultiPoly:
    """A multivariate polynomial class of the form
    p(\vec{x}) = \sum_{0\leq n\leq\deg(p)}a_n(\vec{x}-\vec{c})^n
    where n and \deg(p) are multi-indices."""
    
    def __init__(self, a, c=None):
        """Creates a multivariate polynomial with the given coefficients
        and given offsets ore zeros otherwise."""
        self.a = np.asarray(a) #coefficients
        self.c = np.asarray(c) if c is not None else np.zeros(self.dim) #offsets
    
    @staticmethod
    def fit(X, y, deg, c=None):
        """Creates a least squares fit with the given degrees and offsets
        for the given X and y values."""
        if c is None:
            c = np.zeros(len(deg))
        X, shape = np.subtract(X, c), np.asarray(deg)+1
        X_ = np.empty((len(X), np.prod(shape))) #monomials
        for i in np.ndindex(*shape):
            X_[:, np.ravel_multi_index(i, shape)] = np.prod(np.power(X, i), axis=1)
        return MultiPoly(np.linalg.lstsq(X_, y, rcond=None)[0].reshape(shape), c)
    
    
    
    #polynomial stuff
    @property
    def dim(self):
        """Number of variables."""
        return self.a.ndim
    
    @property
    def deg(self):
        """Degree in every variable."""
        return self.a.shape
    
    def __call__(self, *x):
        return sum(ai * np.prod(np.power(x-self.c, i), axis=-1) for i, ai in np.ndenumerate(self.a))
    
    
    
    #utility stuff
    def round(self, decimals=0):
        """Returns a copy of this polynomial with all coefficients and offsets
        rounded with numpy.round."""
        return MultiPoly(np.round(self.a, decimals), np.round(self.c, decimals))
    
    
    
    #python stuff
    def toString(self, symbols=None):
        """Returns a string representation with the given symbols als variables,
        or x0, x1, ... if none are provided."""
        symbols = symbols if symbols is not None else tuple(f'x{i}' for i in range(self.dim))
        terms = []
        for i, ai in np.ndenumerate(self.a):
            if ai != 0:
                monomials = []
                for si, ci, ii in zip(symbols, self.c, i):
                    if ii >= 1:
                        monomials += [(f'({si}-{ci})' if ci!=0 else str(si)) + (f'^{ii}' if ii>=2 else '')]
                terms += [str(ai) + ''.join(monomials)]
        return ' + '.join(terms)
    
    def __str__(self):
        return self.toString()

import zfit
import math
import tensorflow as tf

from zfit import z 
#-------------------------------------------------------------------
class hypexp(zfit.pdf.ZPDF):
    _N_OBS  = 1
    _PARAMS = ['mu', 'alpha', 'beta']

    def _unnormalized_pdf(self, x):
        x    = z.unstack_x(x)
        mu   = self.params['mu']
        ap   = self.params['alpha']
        bt   = self.params['beta']

        u   = (x - mu) 
        val = z.exp(-bt * x) / (1 + z.exp(-ap * u))

        return val 
#-------------------------------------------------------------------
class modexp(zfit.pdf.ZPDF):
    _N_OBS  = 1
    _PARAMS = ['mu', 'alpha', 'beta']

    def _unnormalized_pdf(self, x):
        x    = z.unstack_x(x)
        mu   = self.params['mu']
        ap   = self.params['alpha']
        bt   = self.params['beta']

        u   = (x - mu) 
        val = (1 - z.exp(-ap * u)) * z.exp(-bt * u)

        return val 
#-------------------------------------------------------------------
class genexp(zfit.pdf.ZPDF):
    _N_OBS  = 1
    _PARAMS = ['mu', 'sg', 'alpha', 'beta']

    def _unnormalized_pdf(self, x):
        x    = z.unstack_x(x)
        mu   = self.params['mu']
        sg   = self.params['sg']
        ap   = self.params['alpha']
        bt   = self.params['beta']

        u   = (x - mu) / sg
        val = (1 - z.exp(-ap * u)) * z.exp(-bt * u)

        return val 
#-------------------------------------------------------------------
class SUJohnson(zfit.pdf.ZPDF):
    _N_OBS  = 1
    _PARAMS = ['mu', 'lm', 'gamma', 'delta']

    def _unnormalized_pdf(self, x):
        x    = z.unstack_x(x)
        mu   = self.params['mu']
        lb   = self.params['lm']
        gm   = self.params['gamma']
        dl   = self.params['delta']

        u = (x - mu) / lb

        a = dl / (lb * z.sqrt(2 * math.pi))
        b = 1  / z.sqrt(1 + u ** 2)
        c = - 1/2 * (gm + dl * tf.math.asinh(u)) ** 2

        val = a * b * z.exp(c)

        return val 
#-------------------------------------------------------------------
class FermiDirac(zfit.pdf.ZPDF):
    _N_OBS  = 1
    _PARAMS = ['mu', 'ap']

    def _unnormalized_pdf(self, x):
        x    = z.unstack_x(x)
        mu   = self.params['mu']
        ap   = self.params['ap']

        exp  = (x - mu) / ap
        den  = 1 + z.exp(exp)

        return 1. / den
#-------------------------------------------------------------------
def fd_integral(limits, params, model):
    lower, upper = limits.limit1d
    mu           = params['mu']
    ap           = params['ap']

    exp1         = (upper - mu) / ap
    exp2         = (lower - mu) / ap

    num          = 1 + math.exp(exp1) 
    den          = 1 + math.exp(exp2) 

    val = upper - lower - ap * math.log(num/den);

    if math.isnan(val) or math.isinf(val) or val <= 0:
        print(f'Invalid value: {val}')
        raise

    return val
#-------------------------------------------------------------------
#limits = zfit.Space.from_axes(axes=0, limits=(zfit.Space.ANY_LOWER, zfit.Space.ANY_UPPER))
#FermiDirac.register_analytic_integral(func=fd_integral, limits=limits)
#-------------------------------------------------------------------


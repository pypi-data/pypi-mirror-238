import zfit
import numpy

import pandas            as pnd
import matplotlib.pyplot as plt

import utils_noroot      as utnr

#-------------------------------------------------------
class data:
    log = utnr.getLogger(__name__)
#-------------------------------------------------------
def res_to_dict(res):
    '''
    Will take a zfit result object
    Will return a dictionary with the fit parameters and erros as:
    {par_name : (val, err)}
    if the error is not found, will assign 0 and show a warning
    '''
    noerr = False 
    d_par = {}
    for par, d_val in res.params.items():
        nam = par.name
        val = d_val['value']
        try:
            err = d_val['hesse']['error'] 
        except:
            noerr = True
            err   = 0 

        d_par[nam] = (val, err)

    if noerr:
        data.log.warning(f'Errors not found')

    return d_par
#-------------------------------------------------------
def copy_model(pdf):
    '''
    Ment to copy PDF's to bypass dropped normlization
    when copying extended PDFs
    '''
    if not pdf.is_extended:
        return pdf.copy()

    yld = pdf.get_yield()

    pdf = pdf.copy()

    pdf = pdf.create_extended(yld)

    return pdf
#-------------------------------------------------------
def result_to_latex(res, tex_path, method='hesse'):
    '''
    Takes result object and dumps table with values of
    parameters to latex table
    '''

    if method not in ['hesse', 'minos']:
        data.log.error(f'Invalid method: {method}')
        raise ValueError

    #Can't freeze twice, freeze just in case
    try:
        res.freeze()
    except AttributeError:
        pass

    d_tab              = {}
    d_tab['Parameter'] = [ nam                     for nam,  _ in res.params.items()]
    d_tab['Value'    ] = [ dc['value']             for   _, dc in res.params.items()]

    try:
        if   method == 'hesse':
            d_tab['Error'    ] = [ dc['hesse']['error']  for   _, dc in res.params.items()]
        elif method == 'minos':
            l_err_low = [ dc['errors']['lower'] for   _, dc in res.params.items()]
            l_err_upr = [ dc['errors']['upper'] for   _, dc in res.params.items()]

            d_tab['Error'    ] = [ 0.5 * (err_low + err_upr) for err_low, err_upr in zip(l_err_low, l_err_upr) ]
    except:
        data.log.warning(f'Not including errors, run: res.hesse(name=\'hesse_np\')')

    df = pnd.DataFrame(d_tab)
    df.to_latex(tex_path, index=False)
#-------------------------------------------------------
def pdf_to_latex(pdf, tex_path):
    '''
    Takes pdf and dumps table with values of
    parameters to latex table
    '''

    l_par = list(pdf.get_params(floating=True)) + list(pdf.get_params(floating=False)) 

    d_tab              = {}
    d_tab['Parameter'] = [ par.name     for par in l_par]
    d_tab['Value'    ] = [ par.numpy()  for par in l_par]
    d_tab['Floating' ] = [ par.floating for par in l_par]

    df = pnd.DataFrame(d_tab)
    df.to_latex(tex_path, index=False)
#-------------------------------------------------------
def get_pdf_params(pdf, floating=True, numeric=True):
    '''
    Takes PDF 
    Returns {parname -> value} dictionary

    Parameters
    ---------------------
    numeric (bool) : If true the values will be numbers otherwise, zfit.parameter instances
    '''

    l_par = pdf.get_params(floating=floating)

    if numeric:
        d_par = { par.name : par.value().numpy() for par in l_par }
    else:
        d_par = { par.name : par                 for par in l_par }

    return d_par
#-------------------------------------------------------
def fix_pars(pdf, d_par):
    '''
    Will take a pdf and a {var_name -> [val, err]} map. It will fix the values of the parameters
    of the PDF according to the dictionary.

    Returns PDF with fixed parameters
    '''

    l_par     = list(pdf.get_params(floating=True)) + list(pdf.get_params(floating=False))
    d_par_pdf = { par.name : par for par in l_par }

    data.log.info('Fixing PDF parameters')
    for par_name, [val, _] in d_par.items():
        try:
            par = d_par_pdf[par_name]
        except:
            data.log.error(f'Cannot find {par_name} among:')
            data.log.error(d_par_pdf.keys())

        par.set_value(val)
        par.floating = False

        data.log.info(f'{par_name:<30}{"->":20}{val:<20}')

    return pdf
#-------------------------------------------------------
def float_pars(pdf, l_par):
    '''
    Will take a pdf and a list of variables. It will float the values of the parameters
    of the PDF 

    Returns PDF with fixed parameters
    '''

    l_par_pdf = list(pdf.get_params(floating=True)) + list(pdf.get_params(floating=False))
    d_par_pdf = { par.name : par for par in l_par_pdf }

    data.log.info('Floating PDF parameters')
    for par_name in l_par: 
        try:
            par = d_par_pdf[par_name]
        except:
            data.log.error(f'Cannot find {par_name} among:')
            data.log.error(d_par_pdf.values())
            raise

        par.floating = True 

        data.log.info(par_name)

    return pdf
#-------------------------------------------------------
def fit_result_to_pandas(res):
    '''
    Will take a results object from zfit after calling hesse and without freezing it 
    Will return a pandas dataframe with a single row and columns corresponding to the variables
    and their fit errors
    '''
    d_data = {}
    for par, d_val in res.params.items():
        name= par.name
        val = d_val['value']
        err = d_val['hesse']['error']

        d_data[f'{name} value'] = [val]
        d_data[f'{name} error'] = [err]

    df = pnd.DataFrame(d_data)

    return df
#-------------------------------------------------------
def pad_data(data, model, low=None, high=None, scale=1.0):
    '''
    Will 
    1. Remove data between low and high
    2. Make fake data from model between said interval
    3. Patch deleted data
    4. Can optionally use a scale factor in case normalization has problems
    '''
    arr_flg = (data > low) & (data < high)
    data_fl = data[~arr_flg]

    frac  = model.numeric_integrate([low, high]).numpy()
    nsb   = data_fl.size
    ntot  = nsb / (1 - frac)
    nsig  = scale * frac * ntot 
    nsig  = int(nsig)

    sdata = model.create_sampler(limits=[low, high], n=nsig)
    dat_sg= sdata.numpy().flatten()

    data  = numpy.concatenate([data_fl, dat_sg])

    return data
#-------------------------------------------------------
def print_pdf(pdf):
    s_par_flt = pdf.get_params(floating= True)
    s_par_fix = pdf.get_params(floating=False)

    data.log.info('-' * 20)
    data.log.info(f'{"Name":<30}{"Value":<20}{"Floating":<20}')
    data.log.info('-' * 20)
    for par in s_par_flt:
        value       = par.value().numpy()
        data.log.info(f'{par.name:<30}{value:<20.3f}{par.floating:<20}')

    for par in s_par_fix:
        value       = par.value().numpy()
        data.log.info(f'{par.name:<30}{value:<20.3f}{par.floating:<20}')
#-------------------------------------------------------


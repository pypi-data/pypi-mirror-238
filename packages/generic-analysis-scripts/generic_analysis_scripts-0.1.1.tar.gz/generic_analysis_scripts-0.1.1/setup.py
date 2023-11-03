from setuptools import setup, find_packages

import glob

setup(
    name            ="generic_analysis_scripts",
    version         ='0.1.1',
    description     ='Generic utilities for data analysis',
    long_description='Private package, if you do not know what this is, it is useless for you, keep moving',
    scripts         = glob.glob('scripts/*') + glob.glob('jobs/*'),
    package_dir     = {'' : 'src'},
    install_requires= open('requirements.txt').read()
)


from setuptools import setup, find_packages

setup(
    name='SpottedPy',
    version='0.1',
    packages=find_packages(),
    install_requires=[
    'numpy>=1.21.6',
    'pandas>=1.5.2',
    'scipy>=1.10.1',
    'matplotlib>=3.7.1',
    'seaborn>=0.12.2',
    'libpysal>=4.8.0',
    'esda>=2.5.1',
    'scikit-learn>=1.2.2',
    'scanpy>=1.9.5',
    'squidpy>=1.2.3',
    'anndata>=0.8.0',
    'statsmodels>=0.13.5',
],

)

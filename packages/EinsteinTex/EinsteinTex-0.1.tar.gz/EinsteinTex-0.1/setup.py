from setuptools import setup, find_packages

setup(
    name='EinsteinTex',
    version='0.1',
    description = 'A package for creating LaTeX files for General Relativity.',
    author = 'Daniel Linford',
    author_email = 'dlinford@purdue.edu',
    packages=find_packages(),
    install_requires=['sympy', 'einsteinpy'],
)

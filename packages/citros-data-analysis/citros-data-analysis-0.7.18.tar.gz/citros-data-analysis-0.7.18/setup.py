import os
from setuptools import setup, find_packages

def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()

def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

setup(
    name = "citros-data-analysis",
    version=get_version("citros_data_analysis/__init__.py"),
    author ="Yalyalieva", 
    author_email="lidia@lulav.space",
    license = "LICENSE.txt",
    description = "Package for data analysis",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),    
    packages=find_packages(exclude=["tests","ipnb",".devcontainer",".git","env"]),
    python_requires='>=3.8',
    install_requires = [ 
        "numpy",
        "pymongo",
        "pandas",
        "psycopg2-binary",
        "matplotlib",
        "scipy",
        "scikit-learn",
        "gmr",
        "prettytable",
        "termcolor",
        "gql",
        "pyjwt",
        "requests",
        "requests_toolbelt"
    ],
    url = "https://github.com/lulav/citros_data_analysis", 
)
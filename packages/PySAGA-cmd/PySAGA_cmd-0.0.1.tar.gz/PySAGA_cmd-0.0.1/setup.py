from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'A package that allows you to run SAGA GIS tools in a Python environment.'

setup(
    name="PySAGA_cmd",
    version=VERSION,
    author="Cuvuliuc Alex-Andrei",
    author_email="<cuvuliucalexandrei@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'gis', 'SAGA GIS', 'saga_cmd', 'PySAGA'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)

from setuptools import setup

setup(
    name='BebrPandasEtl',
    version='0.1',
    packages=['Core'],
    url='',
    license='MIT',
    author='Benoit Braeckeveldt',
    install_requires=[
        'pandas',
        'lxml',
        'diagrams',
        'cx',
        'tqdm',
        'SQLAlchemy',
        'openpyxl',
        'click',
        'mypy-extensions',
        'colorama',
        'termtables',
        'art',
        'SQLAlchemy-Utils',
        'PySide6',
        'fsspec',
        'qt-material']
)
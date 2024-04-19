from setuptools import setup, find_packages

setup(
    name='pydiff',
    version='0.1',
    packages=find_packages(),
    py_modules=['pydiff'],
    install_requires=[
        'black',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
        ]
    }
)

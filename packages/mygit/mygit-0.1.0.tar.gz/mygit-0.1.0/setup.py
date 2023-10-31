from setuptools import Extension, setup

setup(
    name='mygit',
    version='0.1.0',
    py_modules=['mygit'],
    entry_points = {
        'console_scripts': ['mygit=mygit:main'],
    }
)

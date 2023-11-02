from setuptools import setup, find_packages

setup(
    name="g16_input_generator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "tkinter",
        "rdkit"
    ],
    entry_points={
        'console_scripts': [
            'g16_input_generator=g16_input_generator.main:main_function',  # if you have a main function to execute your code
        ],
    },
)

from setuptools import setup, find_packages

setup(
    name="g16_input_generator",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "rdkit"
    ],
    entry_points={
        'console_scripts': [
            'g16_input_generator=g16_input_generator.main:main_function',  # if you have a main function to execute your code
        ],
    },
)

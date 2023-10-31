from setuptools import setup, find_packages

setup(
    name='fgslpyrest',
    version='1.0.0',
    author='Flávio Gomes da Silva Lisboa',
    author_email='flavio.lisboa@fgsl.eti.br',
    description='A class to make HTTP REST requests',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)

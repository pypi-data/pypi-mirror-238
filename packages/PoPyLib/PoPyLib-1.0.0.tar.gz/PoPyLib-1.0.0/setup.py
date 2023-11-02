from setuptools import setup, find_packages

setup(
    name='PoPyLib',
    version='1.0.0',
    description='A Python Library covering basic math, geometry, and string functions',
    author='Paul Estephan',
    packages=find_packages(),  # This will automatically discover and include all packages
    install_requires=['sympy'],  # List any dependencies here
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

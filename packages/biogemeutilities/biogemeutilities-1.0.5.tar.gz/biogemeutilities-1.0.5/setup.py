from setuptools import setup, find_packages


classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering"
]


install_requires=[
    "biogeme>=3.2.12",
    "pandas>=2.0.3",
    "numpy>=1.24.3",
    "xlsxwriter>=3.1.2"
]


setup(
    name='biogemeutilities',
    version='1.0.5',
    author='Mikkel Thorhauge',
    author_email='',
    url='',
    license='MIT',
    classifiers=classifiers,
    description='Add features to the biogeme package',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    keywords=['biogeme','discrete choice models', 'confidence interval', 'calibrate'],
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3.8.18'
)
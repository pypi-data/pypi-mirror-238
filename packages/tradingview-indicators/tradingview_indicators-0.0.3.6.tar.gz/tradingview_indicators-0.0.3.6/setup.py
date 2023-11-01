from setuptools import setup, find_packages

VERSION = '0.0.3.6'
DESCRIPTION = 'An accurate calculation of technical analysis indicators with values aligning with those in TradingView.'

with open('README.md') as f:
    long_description = f.read()

setup(
    name="tradingview_indicators",
    version=VERSION,
    author="m-marqx (Mateus Marques)",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
    keywords=['python', 'tradingview', 'technical analysis', 'indicators'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
from setuptools import setup, find_packages

setup(
    name="govdata",
    author="Giancarlo Rizzo",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        'Jinja2==3.0.3',
        'pandas==2.0.3',
        'pretty-errors==1.2.25',
        'pytest==7.4.3',
        'pytest-cov==4.1.0',
        'requests==2.31.0',
        'requests-mock==1.11.0',
        "pytest-cov",
    ]
)
from setuptools import setup, find_packages

setup(
    name='map_numbers_lb',
    version='0.1',
    description='A library to convert numbers/digits into luxembourgish numerals.',
    long_description=open('README.md').read(),
    author='github.com/michelBBC',
    author_email='',
    url='https://github.com/michelBBC/map-numbers-lu',
    packages=['map_numbers_lb'],
    python_requires='>=3.7',
    include_package_data=True,
    install_requires=[
        'pytest~=6.2.5',
        'pytest-cov'
    ]
)

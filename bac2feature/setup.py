from setuptools import setup, find_packages

version = '1.1'

setup(
    name='Bac2Feature',
    version=version,
    description='An easy-to-use interface to predict bacterial and archaeal traits from 16S rRNA gene sequences',
    keywords='Bac2Feature',
    author='Masaki Fujiyoshi',
    author_email='fujiyoshi-masaki353@g.ecc.u-tokyo.ac.jp',
    url='',
    license='GPL-3.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bac2feature = bac2feature.cmd.bac2feature:main'
        ]},
    include_package_data=True,
    install_requires=[],
    setup_requires=[],
    tests_require=[]
)

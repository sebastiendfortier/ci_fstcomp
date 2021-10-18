# -*- coding: utf-8 -*-
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

v_file = open("VERSION")
__version__ = v_file.readline()
v_file.close()


setuptools.setup(
    name='ci_fstcomp',
    version=__version__,
    description='fstcomp library for python an ci client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastien Fortier",
    author_email="sebastien.fortier@canada.ca",
    url='https://gitlab.science.gc.ca/sbf000/ci_fstcomp',
    # packages = find_packages('ci_fstcomp'),
    # package_dir={'':'ci_fstcomp'},
    # py_modules=['ci_fstcomp.ci_fstcomp', 'ci_fstcomp.fstcomp', 'ci_fstcomp.std_io', 'ci_fstcomp.dataframe'],
    # package_data={'ci_fstcomp': ['fstcompstats.pyf','fstcompstats.f90','fstcompstats.cpython-36m-x86_64-linux-gnu.so']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Linux",
    ],
    install_requires=[
        'pandas>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'ci_fstcomp=ci_fstcomp.ci_fstcomp:cli',
        ]
    },
    packages=setuptools.find_packages(exclude='test'),
    include_package_data=True,
    python_requires='>=3.6',
)

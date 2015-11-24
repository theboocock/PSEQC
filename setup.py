from setuptools import setup, find_packages

import os 

def locate_packages():
    packages = ['snpqc']
    for (dirpath, dirnames, _) in os.walk(packages[0]):
        for dirname in dirnames:
            package = os.path.join(dirpath, dirname).replace(os.sep, ".")
            packages.append(package)
    return packages

setup(
    name="snpqc",
    version=".1",
    packages=locate_packages(),
    author="James Boocock",
    author_email="james.boocock@otago.ac.nz",
    description="Basic SNP QC using Shiny and Plink/seq (also works for indels)", 
    license="Mit",
    zip_safe=False,
     entry_points={
        'console_scripts': [
            'snpqc = snpqc.pipeline:main',
        ]
        },
    url="github.com/smilefreak/snpqc",
    use_2to3=True,
)

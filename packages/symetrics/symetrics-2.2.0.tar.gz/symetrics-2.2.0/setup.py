from setuptools import setup, find_packages

VERSION = '2.2.0' 
DESCRIPTION = 'Symetrics API'
LONG_DESCRIPTION = 'Package for SYMETRICS API'
REQUIRED_PACKAGES = [
    'numpy==1.24.4',
    'pandas==2.0.2',
    'scikit-learn==1.2.2'
]

setup(
        name="symetrics", 
        version=VERSION,
        author="Linnaeus Bundalian",
        author_email="linnaeusbundalian@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        url='https://lbundalian.github.io/symetrics/',
        install_requires=REQUIRED_PACKAGES,
        keywords=['python', 'synonymous variants'],
        include_package_data=True,
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
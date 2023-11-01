from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='calcat',
    version='1.0.1',
    py_modules=["calcat"],
    package_dir={'': 'src'},
    classifiers=["Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.9",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent"],
    author='Agnieszka Thiel',
    author_email='ag.thiel.arc@gmail.com',
    description='A Python package for basic arithmetic operations.',
    url='https://github.com/TuringCollegeSubmissions/athiel-DWWP.1.5',
    license='MIT',
    extras_require = {
        "dev": [
            "pytest>=7.4.3",
        ],
    },
)
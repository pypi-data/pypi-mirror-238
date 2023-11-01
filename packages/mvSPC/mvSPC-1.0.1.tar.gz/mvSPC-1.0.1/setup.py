from setuptools import find_packages, setup


setup(
    name="mvSPC",
    version="1.0.1",
    author="Henrik Hviid Hansen, Sebastian Olivier Nymann Topalian, Davide Cacciarelli",
    author_email="hehha@orsted.com, sebtop@kt.dtu.dk, dcac@dtu.dk",
    description="Plug and play statistical process control functions for Python",
    long_description="Python package based on work from 3 PhD projects at the Technical University of Denmark covering multivariate statistical process control (MSPC), autoencoders for MSPC and determination of delays for dynamic principal component analysis",
    long_description_content_type="markdown",
    url="https://github.com/hviidhenrik/pySPC",
    packages=find_packages(exclude=["tests*"]),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        "scikit_learn",
        "scipy",
        "statsmodels",
        "torch",
        "openpyxl",
        "seaborn"
    ],
)

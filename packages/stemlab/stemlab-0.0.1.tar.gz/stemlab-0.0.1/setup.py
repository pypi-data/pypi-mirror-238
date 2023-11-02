import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stemlab",
    version="0.0.1",
    author="STEM Research",
    author_email="stemxresearch@gmail.com",
    description="Mathematical Computing and Analysis in STEM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stemilab/stemlab",
    license='MIT',
    python_requires='>=3.6',
    install_requires=['numpy', 'scipy', 'statsmodels', 'sympy', 'pandas', 'matplotlib'],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
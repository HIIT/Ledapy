import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ledapy",
    version="1.0",
    author="Marco Filetti",
    description="Ledapy is a port of Ledalab (www.ledalab.de) for Python",
    url="https://github.com/HIIT/ledapy",
    packages=setuptools.find_packages(),
    install_requires = ["numpy", "scipy", "sympy", "matplotlib"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

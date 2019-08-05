import setuptools

setuptools.setup(
    name="ledapy",
    version="1.2",
    author="Marco Filetti",
    description="Ledapy is a minimal port of Ledalab (www.ledalab.de) for Python",
    url="https://github.com/HIIT/ledapy",
    packages=setuptools.find_packages(),
    install_requires = ["numpy", "scipy", "sympy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

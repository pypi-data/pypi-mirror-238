from setuptools import setup

if __name__ == "__main__":
    setup(
        name="htflow-utils",
        version="0.0.1",
        description="utility functions and classes for SurfFlow and TriboFlow",
        long_description=open("README.md").read(),
        url="https://github.com/fyalcin/htflow-utils",
        author="Michael Wolloch, Firat Yalcin",
        author_email="michael.wolloch@univie.ac.at, firat.yalcin@univie.ac.at",
        license="MIT",
        install_requires=["pymatgen"],
        extras_require={
            "workflows": ["ase", "matgl"],
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Operating System :: OS Independent",
            "Topic :: Other/Nonlisted Topic",
            "Topic :: Scientific/Engineering",
        ],
    )

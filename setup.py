import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    required = fh.read().splitlines()

extra_required = {"plot": list()}
with open("extra-requirements.txt", "r") as fh:
    extra_required["plot"] = fh.read().splitlines()


extra_required["plot"].remove("-r requirements.txt")

setuptools.setup(
    name="tsp-solvers",
    version="0.0.13",
    author="Guillermo González-Santander",
    author_email="g.gsantanderdelacruz@gmail.com",
    description="Set of different methods to solve the Travelling Salesman Problem. Each method has its own class",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/ggsdc/tsp-solvers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=required,
    extras_require=extra_required,
)

import setuptools

setuptools.setup(
    include_package_data=True,
    name="myadipkg_selva",
    version="0.0.1",
    description="ADI Python Package module",
    url="https://github.com/selvariyan-adi/mydemopkg",
    author="selvariyan.natarajan",
    author_email="selvariyan.natarajan@analog.com",
    packages=setuptools.find_packages(),
    long_description="ADI Python Package module",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

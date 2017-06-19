import setuptools

setuptools.setup(
    name="python-isign",
    version="0.1.1",
    description="Python client for isign.io API.",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/isign",
    license="MIT",
    author="Paulius Maruška",
    author_email="paulius.maruska@gmail.com",
    install_requires=[
        "python-dateutil",
        "requests",
    ],
)

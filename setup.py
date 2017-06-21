import setuptools

setuptools.setup(
    name="python-isign",
    version="0.2.0",
    description="Python client for isign.io API.",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/Paulius-Maruska/python-isign",
    license="MIT",
    author="Paulius Maruška",
    author_email="paulius.maruska@gmail.com",
    install_requires=[
        "python-dateutil",
        "requests",
    ],
    keywords=["isign", "client"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries",
    ],
)

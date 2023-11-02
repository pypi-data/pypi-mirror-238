import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read().strip()

setuptools.setup(
    name="utils_cv-baiyigali",
    version=version,
    author="baiyigali",
    author_email="1304646911@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    test_suite="nose.collector",
    tests_require=["nose"],
    python_requires=">=3.6",
    install_requires=['numpy', 'pandas', 'nltk'],
)

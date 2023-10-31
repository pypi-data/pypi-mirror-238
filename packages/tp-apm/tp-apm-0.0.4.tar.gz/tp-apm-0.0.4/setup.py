import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="tp-apm",
    version="0.0.4",
    author="pengjun",
    author_email="mr_lonely@foxmail.com",
    description="tp apm tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=[],
    install_requires=[
        'requests'
    ],
    dependency_links=[],
    python_requires='>=3.7',
)
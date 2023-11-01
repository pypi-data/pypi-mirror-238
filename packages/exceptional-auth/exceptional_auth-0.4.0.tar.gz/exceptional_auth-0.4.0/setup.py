import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('VERSION', 'r') as fh:
    version = fh.read()

setuptools.setup(
    name="exceptional_auth",
    version=version,
    author="Alex Fischer",
    author_email="alex@quadrant.net",
    description="Exception-based authentication helpers for django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quadrant-newmedia/exceptional_auth",
    packages=['exceptional_auth'],
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["Django>=2.2,<5"],
)
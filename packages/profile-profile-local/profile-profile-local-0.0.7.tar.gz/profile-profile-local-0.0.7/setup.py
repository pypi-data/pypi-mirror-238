import setuptools
# used by python -m build
# python -m build needs pyproject.toml or setup.py
setuptools.setup(
    # TODO: Please update the name and delete this line i.e. XXX-local or XXX-remote (without the -python-package suffix)
    name='profile-profile-local',
    version='0.0.7',
    author="Circles",
    author_email="info@circles.life",
    # TODO: Please update the description and delete this line
    description="PyPI Package for Circles profile-profile-local Python",
    # TODO: Please update the long description and delete this line
    long_description="This is a package for sharing common profile-profile-local function used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/circles",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
    ],
)

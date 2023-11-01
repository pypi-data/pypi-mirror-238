"""Setup."""

import setuptools

DIST_NAME = 'utils'
VERSION = "2.0.4"
DESCRIPTION = "Utilities, complementing the Python Standard Library"

setuptools.setup(
    name="%s-nuuuwan" % DIST_NAME,
    version=VERSION,
    author="Nuwan I. Senaratna",
    author_email="nuuuwan@gmail.com",
    description=DESCRIPTION,
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/nuuuwan/%s" % DIST_NAME,
    project_urls={
        "Bug Tracker": "https://github.com/nuuuwan/%s/issues" % DIST_NAME,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        'utils_base-nuuuwan',
        'utils_twitter-nuuuwan',
        'utils_www-nuuuwan',
        'utils_git-nuuuwan',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)

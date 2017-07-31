from setuptools import find_packages, setup

from absorber_ds.version import __version__, licence
from absorber_ds import __doc__, __author__, __author_email__

setup(
    name='tangods-absorber',
    author=__author__,
    author_email=__author_email__,
    version=__version__,
    license=licence,
    description="Tango device server for vacuum absorbers.",
    long_description=__doc__,
    url="https://github.com/synchrotron-solaris/dev-solaris-absorber.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["setuptools"],
    entry_points={
        "console_scripts": ["Absorber = "
                            "absorber_ds.absorber:run"]}
    )

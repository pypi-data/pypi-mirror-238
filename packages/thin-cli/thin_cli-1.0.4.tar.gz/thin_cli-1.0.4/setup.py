from setuptools import setup, find_packages

setup(
    name="thin_cli",
    version="1.0.4",
    description="A thin command line interface framework.",
    author="Avery Cowan",
    url="https://github.com/averycowan/lite_cli",
    packages=find_packages(),
    package_data={"thin_cli": ["py.typed"]},
    install_requires=[],
)

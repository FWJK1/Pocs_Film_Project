from setuptools import setup, find_packages

setup(
    name="code_package",        # Name of your package
    version="0.1",
    packages=find_packages(where="Code"),  # This will include all subpackages (like 'Utility') under 'Code'
    package_dir={"": "Code"},  # Points to the 'Code' directory
)
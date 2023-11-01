from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_desctiption = f.read()

setup(
    name='hash_controller',
    packages=find_packages(),
    long_description=long_desctiption,
    long_description_content_type="text/markdown",
    description='File controller via hash',
    version='0.1.5',
    url='https://github.com/edmachina/hash_controller',
    author='Ezequiel Marcel',
    author_email='ezequiel.marcel@edmachina.com',
    keywords=['pip','hash','controller'],
    install_requires=["pymongo>=4.5.0"],
    python_requires='>=3.9',
)

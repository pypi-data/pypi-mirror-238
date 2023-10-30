from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name='NormalPyRunner',
    version='0.1.2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['normalpyrunner'],
    packages=find_packages(),
    install_requires=[
        # List your project dependencies here
    ],
)
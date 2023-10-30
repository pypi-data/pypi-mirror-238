from setuptools import setup

def get_desc():
    with open("README.md", "r") as f:
        return f.read()

setup(
    name='fastpython',
    version='1.2.0',
    author='MaxymPlayz',
    packages=['fastpython'],
    install_requires=[],
    long_description = get_desc(),
    long_description_content_type = 'text/markdown',
)
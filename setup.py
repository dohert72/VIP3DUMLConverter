
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()


setup(
    name='VIP3DUMLConverter',
    version='0.1.0',
    description='Converts XML output descriptions of UML diagrams\
     and converts them into a 3D printable format.',
    long_description=readme,
    author='Brad Doherty',
    author_email='dohert72@msu.edu',
    url='https://github.com/dohert72/VIP3DUMLConverter.git',
    packages=find_packages(exclude=('tests', 'docs'))
)

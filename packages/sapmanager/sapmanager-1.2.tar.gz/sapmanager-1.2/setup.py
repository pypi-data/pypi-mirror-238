from setuptools import setup
import os


current_directory = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
    README = f.read()

setup(
    name='sapmanager',
    version='1.2',
    license='MIT',
    description='An unofficial library to run SAP logged into the selected ambient with the credentials provided, facilitating Scripting.',
    long_description_content_type="text/markdown",
    long_description=README,
    author='Ricardo Castro',
    author_email='srrenks@gmail.com',
    url='https://github.com/SrRenks/sapmanager',
    packages=['sapmanager'],
    install_requires=['pywin32', 'wheel'],
)

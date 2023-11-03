from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyevaltool',
    version='0.1.2',
    description='A package to evaluate the models.',
    author= 'Ateendra Jha',
    author_email="ateendrajha@outlook.com",
    url = 'https://www.drateendrajha.com/projects/pyevaltool',
    long_description_content_type="text/markdown",
    long_description = long_description,
    packages=setuptools.find_packages(),
    keywords=['testing', 'evaluate', 'model'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['pyevaltool'],
    package_dir={'':'src'},
    install_requires = [
        'pandas'
    ]
)
import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    include_package_data=True,
    name='SimpleApplication',
    version='1.2.1',
    description="Simple Application in Python",
    url='https://gitlab.com/carrivalegervasi/provacg.git',
    author="CarrivaleGervasi",
    packages=setuptools.find_packages(),
    install_requires=required,
    long_description='A Readme is coming soon',
    long_description_content_type="text/markdown",
)
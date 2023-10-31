from setuptools import setup, find_packages

with open('README.md') as file:
    long_description = file.read()

setup(
    name='VPGen',
    version='0.9.5',
    author='Savvin Anton',
    author_email='anv.savvin@gmail.com',
    long_description_content_type='text/markdown',
    long_description=long_description,
    homepage='https://github.com/SavvinAnton/VPGen',
    license='GPL-3.0 license',
    description='Generate porosity medium',
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    platforms=['Windows', 'Unix'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True,
)

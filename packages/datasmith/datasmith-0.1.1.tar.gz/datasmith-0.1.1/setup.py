from setuptools import setup, find_packages

setup(
    name='datasmith',
    version='0.1.1',
    author='Adarsh Liju Abraham , Aditya Poddar',
    author_email='adarsh.liju.abraham@gmail.com , poddar.aditya2014@gmail.com',
    description='Random data generation based on specific attrbutes.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

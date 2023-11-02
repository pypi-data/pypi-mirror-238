from setuptools import setup, find_packages

setup(
    name='2023_assignement_DevOps',
    version='2.0.0',
    setup_requires=["wheel"],
    description='Assignment1',
    author='GruppoELA',
    author_email='l.perfetti2001@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'pytest', 
        'prospector',
        'bandit',
        'mkdocs',
        'twine',
    ],
)

"""
Installation configuration for the `todolist` package.

This module configures package details and required dependencies.
"""

from setuptools import setup, find_packages

setup(
    name='todolist_Telecom',
    version='1.0.30',  # Vous pouvez ajuster cette version selon vos besoins
    description='Bibliothèque pour gérer des tâches et des listes de tâches',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Top-1-KBD/to_do_list.git',
    author='TOP1_organisation',  # Remplacez par votre nom
    author_email='elyes.rezzoug@telecom-paris.fr',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        # list of packages required to run this module
        'pytest>=7.4.2',
        'coverage>=7.3.2',
        'exceptiongroup==1.1.3',
        'pyt==1.0.5',
        'safety==2.3.5',
        'Sphinx==7.2.6'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='todolist, tasks, task management',
    python_requires='>=3.7, <4',
)

from setuptools import setup, find_packages

setup(
    name="linkora",
    version="1.0.0",
    description="Outil simple de transfert de fichiers via sockets",
    author="Votre Nom",
    packages=find_packages(),
    scripts=['bin/linkora'],
    install_requires=[],
    python_requires='>=3.6',
)
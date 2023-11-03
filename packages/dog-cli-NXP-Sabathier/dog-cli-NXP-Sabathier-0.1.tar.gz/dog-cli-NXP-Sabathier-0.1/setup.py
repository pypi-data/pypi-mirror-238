from setuptools import setup, find_packages

setup(
    name="dog-cli-NXP-Sabathier",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'dog-breeds=dog_cli.main:cli',
        ],
    },
    author="Sabathier NXP",
    description="Un CLI pour l'API dog.ceo",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://gitlab.com/andysabathier/sabathier-cli-dogapi.git", # depot git
)

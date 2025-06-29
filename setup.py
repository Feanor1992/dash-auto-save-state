"""
Setup configuration for dash-auto-save-state package
"""
from setuptools import setup, find_packages

# Read README file
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# Read requirements
with open('requirements.txt', 'r', encoding='utf-8') as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]


setup(
    name='dash-auto-save-state',
    version='0.1.0',
    author='Artem Liubarski',
    author_email='feanor1992@gmail.com',
    description='Automatically save and restore Dash component states to prevent data loss',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Feanor1992/dash-auto-save-state',
    packages=find_packages(),
    install_requires=requirements,
    keywords=[
        'dash', 'plotly', 'web-app', 'auto-save', 'state-management',
        'localStorage', 'data-persistence', 'dash-hook', 'plugin'
    ],
    include_package_data=True
)

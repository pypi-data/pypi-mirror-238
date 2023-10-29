from setuptools import setup

# Read the content of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='walkerlayout',
    version='1.0.2',
    description='A time-linear Python implementation of Walker\'s algorithm for level-based tree layouting/drawing',
    author='Elias Foramitti',
    author_email='elias@foramitti.com',
    packages=['walkerlayout'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    project_urls={
        'GitHub': 'https://github.com/EliasLF/walkerlayout',
    },
)
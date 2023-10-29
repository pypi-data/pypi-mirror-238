from setuptools import setup, find_packages

#to build: python3 setup.py sdist build


setup(
    name='SearchDb',
    version='1.0.1',
    license='GPLv2',
    author='cpuboi',
    description="Python dictionary backed by SQLite, includes fast text search and more advanced data structures",
    url='https://github.com/cpuboi/SearchDb',
    keywords=['SQLite', 'dictionary', 'text search'],
    packages=find_packages(),
    classifiers=['Development Status :: 4 - Beta'],
    python_requires='>=3.9', # Older might work, have not tested,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)

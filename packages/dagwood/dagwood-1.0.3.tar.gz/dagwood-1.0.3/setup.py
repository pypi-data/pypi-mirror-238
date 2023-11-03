from setuptools import setup, find_packages

# Read in the README.md for the long description.
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dagwood',
    version='1.0.3',
    packages=find_packages(),
    install_requires=[
        # any future dependencies
    ],
    author='Odai Athamneh',
    author_email='heyodai@gmail.com',
    description='Simple logging tool. Write to console and to file in one step.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/heyodai/dagwood',
)

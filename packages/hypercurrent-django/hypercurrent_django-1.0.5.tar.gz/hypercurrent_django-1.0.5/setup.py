from setuptools import setup, find_packages

setup(
    name='hypercurrent_django',
    version='1.0.5',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
        'hypercurrent_metering',  
    ],
    author='HyperCurrent, Inc',
    author_email='info@hypercurrent.io',
    description='HyperCurrent Middleware for Python Django',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='Apache Software License',
    url='https://github.com/hypercurrentio/hypercurrentdjango',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
)


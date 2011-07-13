from setuptools import setup, find_packages

setup(
    name='searchengine',
    version='0.1',
    description='Simple search engine - an internal prototype',
    long_description = "%s\n\n%s" % (open('README.rst', 'r').read(), open('AUTHORS.rst', 'r').read()),
    author='Jonathan Bydendyk',
    author_email='jpbydendyk@gmail.com',
    license='BSD',
    url='http://github.com/qoda/python-searchengine',
    packages = find_packages(),
    dependency_links = [],
    install_requires = [
        'whoosh',
        'pymongo',
    ],
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Search",
    ],
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


#readme = open('README.rst').read()
#history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='hls_autocomplete',
    version='0.1.0',
    description='Autocomplete for "hdfs dfs -ls".',
    #long_description=readme + '\n\n' + history,
    author='Simon Dollé',
    author_email='simon.dolle@gmail.com',
    url='https://github.com/simondolle/hls-complete',
    packages=[
        'hls_autocomplete',
    ],
    package_dir={'hls_autocomplete':
                 'hls_autocomplete'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='dgim',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            '_hls_get_completions = hls_autocomplete.get_completions:main',
            'hls = hls_autocomplete.hls_cmd:main'
        ]
    },
    #test_suite='tests'
    test_suite = 'nose.collector'
)

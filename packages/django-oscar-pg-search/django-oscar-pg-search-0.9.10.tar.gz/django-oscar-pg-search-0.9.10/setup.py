#!/usr/bin/env python
from setuptools import find_packages, setup
from src.oscar_pg_search import __version__


install_requires = [
    'django>=3.0,<5',
    'django-oscar>=2.0,<3.3',
]

tests_require = [
    'coverage>=5.5,<5.6',
]

setup(
    name='django-oscar-pg-search',
    version=__version__,
    author="Snake-Soft",
    author_email="info@snake-soft.com",
    description="Pure Postgresql search backend for Django Oscar",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
)

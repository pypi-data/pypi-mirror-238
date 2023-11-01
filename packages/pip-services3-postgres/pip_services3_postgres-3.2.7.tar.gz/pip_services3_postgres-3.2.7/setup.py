"""
Pip.Services Postgres
------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_postgres provides Postgres persistence components.

Links
`````

* `website <http://github.com/pip-services/pip-services>`_
* `development version <http://github.com/pip-services3-python/pip-services3-postgres-python>`

"""

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

from setuptools import find_packages
from setuptools import setup

setup(
    name='pip_services3_postgres',
    version='3.2.7',
    url='http://github.com/pip-services3-python/pip-services3-postgres-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='Postgres persistence components for Pip.Services in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'psycopg2-binary >= 2.9.3, < 3.0',

        'pip-services3-commons >= 3.3.9, < 4.0',
        'pip-services3-components >= 3.5.0, < 4.0',
        'pip_services3_data >= 3.2.3, < 4.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

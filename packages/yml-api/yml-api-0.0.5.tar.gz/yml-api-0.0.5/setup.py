# python setup.py sdist && twine upload/yml-api-0.0.1.tar.gz

import os
from setuptools import find_packages, setup

setup(
    name='yml-api',
    version='0.0.5',
    packages=find_packages(exclude=('pnp', 'pnp.*')),
    install_requires=[],
    extras_require={
        'dev': [
            'djangorestframework==3.14.0', 'markdown-it-py==3.0.0',
            'drf-yasg==1.21.7', 'coreapi==2.3.3', 'psycopg2-binary==2.9.5',
            'selenium==4.11.2', 'xlrd==2.0.1', 'django-redis==5.4.0',
            'django-filter==23.2', 'gunicorn==21.2.0', 'xlwt==1.3.0'
        ]
    },
    include_package_data=True,
    license='BSD License',
    description='API generator based on yml file',
    long_description='',
    url='https://github.com/brenokcc',
    author='Breno Silva',
    author_email='brenokcc@yahoo.com.br',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

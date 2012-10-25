import os
from setuptools import setup, find_packages

from app_metrics import VERSION


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='django-pagebits',
    version=".".join(map(str, VERSION)),
    description='django-pagebits is better more end user friendly version of django-chunks',
    long_description=readme,
    author='Frank Wiles',
    author_email='frank@revsys.com',
    url='https://github.com/frankwiles/django-pagebits',
    packages=find_packages(),
    install_requires=[
        'django >= 1.4.0',
        'django-ckeditor >= 3.6.2.1',
        'PIL >= 1.1.7',
        'Pillow >= 1.7.7',
    ],
    tests_require=[
        'django-debug-toolbar',
        'django-coverage',
        'coverage',
        'psycopg2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)


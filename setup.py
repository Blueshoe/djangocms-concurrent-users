# -*- coding: utf-8 -*-from setuptools import setup, find_packages
from setuptools import find_packages, setup

from djangocms_concurrent_users import __version__

setup(
    name="djangocms-concurrent-users",
    version=__version__,
    url='https://github.com/Blueshoe/djangocms-concurrent-users',
    license='MIT',
    description="Django-CMS Plugin for blocking pages which are edited by another user",
    long_description=open('README.rst').read(),
    author='Michael Schilonka',
    author_email='michael@blueshoe.de',
    packages=find_packages(),
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        "Django >= 1.8",
        "django-filer >= 1.2.0",
        "django-cms >= 3.4",
    ],
    include_package_data=True,
    zip_safe=False,
)

import sys

from setuptools import setup, find_packages

install_requires=[]

# require argparse for Pyton < 2.7
if sys.version_info < (2, 7):
    install_requires.append('argparse>=1.1')


setup(
    name='JSOGen',
    version='0.1.0',
    url='http://github.com/bukka/jsogen/',
    license='BSD',
    author='Jakub Zelenka',
    author_email='bukka@php.net',
    description='JavaScript Object Generator',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ],
    entry_points = {
        'console_scripts': [
            'glue = jsogen.jsogen:main',
        ]
    }
)
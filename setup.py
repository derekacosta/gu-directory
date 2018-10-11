from setuptools import setup

setup(name='gu-directory',
    version='1.0',
    description='Search Georgetown University Directory',
    install_requires=['requests', 'bs4'],
    url='https://github.com/justicesuh/gu-directory',
    author='Justice Suh',
    author_email='justice.suh@gmail.com',
    license='MIT License',
    packages=['directory'],
    zip_safe=False
)

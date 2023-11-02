"""PySnoo2 setup script."""
from setuptools import setup

_VERSION = '0.3'


def readme():
    """Pipe README.rst"""
    with open('README.md') as desc:
        return desc.read()


setup(
    name='pysnoo2',
    packages=['pysnoo2'],
    version=_VERSION,
    description='A Python library and CLI to communicate with'
                ' the Snoo Smart Baby Sleeper and Bassinet from Happiest Baby',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Dan Patten',
    author_email='dan@danpatten.com',
    url='https://github.com/DanPatten/pysnoo2',
    license='MIT',
    python_requires='>=3.7, <4',
    include_package_data=True,
    install_requires=['oauthlib', 'aiohttp', 'pubnub>=5.0.0'],
    test_suite='tests',
    scripts=['scripts/snoo'],
    keywords=[
        'baby',
        'snoo',
        'happiest baby',
        'home automation',
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)

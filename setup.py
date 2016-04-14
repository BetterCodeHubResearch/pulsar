#!/usr/bin/env python
from setuptools import setup, find_packages
from extensions import ext

import pulsar_config as config
import pulsar_test


meta = dict(
    name='pulsar',
    author="Luca Sbardella",
    author_email="luca@quantmind.com",
    maintainer_email="luca@quantmind.com",
    url="https://github.com/quantmind/pulsar",
    license="BSD",
    long_description=config.read('README.rst'),
    include_package_data=True,
    setup_requires=['wheel'],
    packages=find_packages(include=['pulsar', 'pulsar.*', 'pulsar_test']),
    entry_points={
        "distutils.commands": [
            "pulsar_test = pulsar_test:Test"
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content']
)


class PulsarTest(pulsar_test.Test):
    start_coverate = True


def run_setup(with_cext):
    params = ext.params() if with_cext else {}
    params.update(meta)
    cmdclass = params.get('cmdclass', {})
    cmdclass['test'] = PulsarTest
    params['cmdclass'] = cmdclass
    setup(**config.setup(params, 'pulsar'))


if __name__ == '__main__':
    try:
        run_setup(True)
    except ext.BuildFailed as exc:
        print('WARNING: C extensions could not be compiled: %s' % exc.msg)
        run_setup(False)

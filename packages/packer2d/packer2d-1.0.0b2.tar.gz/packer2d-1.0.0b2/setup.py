#!/usr/bin/env python
from setuptools import setup

info = {}

with open('packer2d/__init__.py') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, info)
            info['version'] = info['__version__']
            break

with open('README.md') as f:
    info['long_description'] = f.read()

version_low = info['version'].lower()

if 'beta' in version_low:
    status_classifier = 'Development Status :: 4 - Beta'
elif 'alpha' in version_low:
    status_classifier = 'Development Status :: 3 - Alpha'
else:
    status_classifier = 'Development Status :: 5 - Production/Stable'

setup_info = dict(
    name='packer2d',
    version=info['version'],
    packages=['packer2d'],
    license='BSD-2-Clause',
    description='2D bin packer',
    long_description=info['long_description'],
    long_description_content_type='text/markdown',
    author='Guillermo Romero (Gato)',
    author_email='gato@felingineering.com',
    url='https://gitlab.com/felingineer/packer2d',
    download_url='https://gitlab.com/felingineer/packer2d',
    keywords=['BIN', 'PACKING', '2D'],
    install_requires=[],
    classifiers=[
        status_classifier,
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent",
    ]
)

setup(**setup_info)

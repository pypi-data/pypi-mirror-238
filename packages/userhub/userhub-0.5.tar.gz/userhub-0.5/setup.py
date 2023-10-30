"""
Setup the Python package
"""

import pathlib
import re
from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

WORK_DIR = pathlib.Path(__file__).parent


def get_version():
    """ Get version """

    txt = (WORK_DIR / 'userhub' / '__init__.py').read_text('utf-8')

    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError as e:
        raise RuntimeError('Unable to determine version') from e


setup(
    name='userhub',
    version=get_version(),
    description='User Authorization System',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chilleco/userhub',
    author='Alexey Poloz',
    author_email='alexypoloz@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords=(
        'auth, auth system, auth hub, user authenticator, authentication system'
    ),
    packages=find_packages(exclude=('tests',)),
    python_requires='>=3.7, <4',
    install_requires=[
        'aiohttp',  # Because of conflicts with main repo
    ],
    project_urls={
        'Source': 'https://github.com/chilleco/userhub',
    },
    license='MIT',
    include_package_data=False,
)

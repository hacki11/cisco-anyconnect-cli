from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='cisco-anyconnect-cli',
    packages=['cisco_anyconnect_cli'],
    version='0.6',
    license='apache-2.0',
    description='Cisco AnyConnect command line interface',
    author='Juergen Schmid',
    url='https://github.com/hacki11/cisco-anyconnect-cli',
    keywords=['vpn', 'cisco', 'anyconnect', 'cli'],
    install_requires=[
        'click',
        'keepasshttp'
    ],
    entry_points={
        'console_scripts': ['anyconnect=cisco_anyconnect_cli.cli:main'],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows'
    ],
)

from setuptools import setup, find_packages


setup(
    name='spacemodel',
    version='0.0.1',
    author='Jay',
    author_email='Jay184@users.noreply.github.com',
    description='Provides Active-Record style wrappers to Deta Base using Pydantic.',
    url='https://github.com/Jay184/spacemodel',
    project_urls={
        'Bug Tracker': 'https://github.com/Jay184/spacemodel/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    py_modules=['spacemodel'],
    include_package_data=True,
    install_requires=[
        'deta==1.2.0',
        'pydantic==2.4.2',
    ],
    extras_require={
        'dev': [
            'pkginfo==1.8.3',
            'build',
            'twine',
            'pytest',
        ]
    },
    python_requires='>=3.9'
)

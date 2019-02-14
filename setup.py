from setuptools import find_packages, setup

LONG_DESCRIPTION = (
    'Python tools for setting up and versioning '
    'Grafana instances'
)

setup(
        name='grafanatools',
        version='0.0.1',
        packages=find_packages(where='src'),
        package_dir={'grafanatools': 'src/grafanatools'},
        url='https://github.com/callumstew/grafanatools',
        author='Callum Stewart',
        author_email='callum.stewart@gmail.com',
        description='Grafana python tools',
        long_description=LONG_DESCRIPTION,
        install_requires=[
            'requests'
        ],
        classifiers=[
            'Programming Language :: Python',
        ]
)

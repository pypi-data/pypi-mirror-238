from setuptools import setup, find_packages

setup(
    name='sodas',
    version='0.2.4',
    description='Sodas Workflow Development Tools',
    author='ETRI SODAS+',
    author_email='siwoonson@etri.re.kr',
    url='',
    packages=find_packages(),
    install_requires=[
        'boto3==1.26.45',
        'pandas',
        'requests',
        'python-dotenv',
    ],
    extras_require={},
    setup_requires=[],
    tests_require=[],
    entry_points={},
    package_data={}
)
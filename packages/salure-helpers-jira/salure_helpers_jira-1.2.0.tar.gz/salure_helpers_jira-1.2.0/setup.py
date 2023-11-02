from setuptools import setup


setup(
    name='salure_helpers_jira',
    version='1.2.0',
    description='JIRA wrapper from Salure',
    long_description='JIRA wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.jira"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'pandas>=1,<3',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)
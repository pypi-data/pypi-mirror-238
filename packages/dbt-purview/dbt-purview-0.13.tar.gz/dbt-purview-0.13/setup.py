from setuptools import setup, find_packages

setup(
    name='dbt-purview',
    version='0.13',
    packages=find_packages(),
    install_requires=[
        'click',
        'databricks-sql-connector',
        'requests',
        'pytz',
        'typing',
        'datetime',
        'apache-airflow',
        'snowflake-sqlalchemy'
    ],
    entry_points={
        'console_scripts': [
            'dbtpurview = dbtpurview.main:dbtpurview',
        ],
    },
)
import setuptools

description = 'Utility for parse csv-file from https://data.gov.ru/opendata/7708660670-proizvcalendar'

setuptools.setup(
    name='russian_working_calendar_parser',
    version='0.0.1',
    author='Igor Iakovlev',
    author_email='igorxut@example.com',
    description=description,
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/igorxut/russian-working-calendar-parser',
    packages=['russian_working_calendar_parser'],
    install_requires=[
        'typing',
    ],
    classifiers=(
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)

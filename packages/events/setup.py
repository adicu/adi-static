from setuptools import setup

setup(
    name='lektor-events',
    version='0.1',
    author=u'ADI',
    author_email='infrastructure@adicu.com',
    license='MIT',
    py_modules=['lektor_events'],
    entry_points={
        'lektor.plugins': [
            'events = lektor_events:EventsPlugin',
        ]
    }
)

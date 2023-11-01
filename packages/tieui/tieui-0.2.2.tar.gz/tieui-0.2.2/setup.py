from setuptools import setup, find_packages

setup(
    name='tieui',
    version='0.2.2',
    packages=find_packages(),
    install_requires=[
        'flask_cors',
        'flask_socketio',
        'flask',
        'openai',
        'gunicorn',
        'eventlet',
        'stripe',
        'sendgrid',
        'websocket-client',
    ],
    author='TieUi',
    author_email='info@tieUi.com',
    description='Tie Ui package for local development',
    url='https://tieui.app',
)

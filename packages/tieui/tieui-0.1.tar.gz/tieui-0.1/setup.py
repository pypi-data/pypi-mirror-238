from setuptools import setup, find_packages

setup(
    name='tieui',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "requests",
        "socketio",
        "inspect",
        "flask",
        "flask_socketio",
        "flask_cors",
        "time",
        "json",
        "os"
    ],
    author='TieUi',
    author_email='info@tieUi.com',
    description='Tie Ui package for local development',
    url='https://tieui.app',
)

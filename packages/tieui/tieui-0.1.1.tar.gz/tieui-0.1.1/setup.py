from setuptools import setup, find_packages

setup(
    name='tieui',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        "requests",
        "socketio",
        "flask",
        "flask_socketio",
        "flask_cors"
    ],
    author='TieUi',
    author_email='info@tieUi.com',
    description='Tie Ui package for local development',
    url='https://tieui.app',
)

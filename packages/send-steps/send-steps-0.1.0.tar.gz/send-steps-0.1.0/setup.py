from setuptools import setup

setup(
    name='send-steps',
    version='0.1.0',
    install_requires = [
    'click',
    'requests',
    'python-dotenv',
    'python-gitlab',
    'radish-bdd',
    ],
    py_modules=['send_steps'],
    entry_points={
        'console_scripts': [
            'send-steps=send_steps:main',
        ],
    },
)

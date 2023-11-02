from setuptools import setup, find_packages

setup(
    name='synapse-wiki',
    version='0.0.1',
    packages=find_packages(),
    author='Synapse',
    author_email='alex@synapse.wiki',
    description='A python client for the Synapse API',
    url='https://github.com/synapsewiki/synapse-python',
    install_requires = [
        'requests',
    ],
)

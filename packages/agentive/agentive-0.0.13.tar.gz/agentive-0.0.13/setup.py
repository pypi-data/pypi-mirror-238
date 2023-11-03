from setuptools import setup, find_packages

setup(
    name='agentive',
    version='0.0.13',
    description='Python-based framework for building modular and extensible language agents',
    author='Morningside AI',
    install_requires=[
        'requests',
        'pandas',
        'tenacity',
        'openai',
        'pydantic',
        'tqdm',
        'tiktoken',
        'numpy',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)
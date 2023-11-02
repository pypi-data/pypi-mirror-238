from setuptools import setup, find_packages

setup(
    name='ChatTDD',
    version='0.2.5',
    packages=find_packages(),
    install_requires=[
        'click',
        'openai>=0.27.0',
        'pytest',
        'python-dotenv',
        'langchain',
        'keyring'
    ],
    entry_points={
        'console_scripts': [
            'chattdd = chattdd.cli:cli',
        ],
    },
    author='Simen Huuse',
    author_email='s.huuse+chattdd@gmail.com',
    description='A utility to assist in building Test-Driven Python code using Langchain and OpenAI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shuuse/ChatTDD',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
)

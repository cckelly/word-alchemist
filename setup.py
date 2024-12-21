from setuptools import setup, find_packages

setup(
    name='word-alchemist',
    version='0.1.0',
    description='Simple Python CLI to help you brainstorm the name of your next product, studio, brand etc',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['syllapy'],
    author='Charles Kelly',
    entry_points={
        'console_scripts': [
            'word-alchemist=word_alchemist.main:main',
        ],
    },
    license='MIT',
    url='https://github.com/cckelly/word-alchemist',
    packages=find_packages(),
    python_requires=">=3.6",
)
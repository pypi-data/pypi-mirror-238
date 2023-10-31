from setuptools import setup, find_packages

setup(
    name='discordion',
    version='0.1.0',
    description='A Discord bot powered by GPT for various tasks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Odder',
    author_email='oscarrothandersen@gmail.com',
    url='https://github.com/odder/discordion',
    packages=find_packages(exclude=['venv', '*.examples*']),
    install_requires=[
        'discord.py',
        'sqlitedict',
        'openai',
        '',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='discord bot GPT',
)
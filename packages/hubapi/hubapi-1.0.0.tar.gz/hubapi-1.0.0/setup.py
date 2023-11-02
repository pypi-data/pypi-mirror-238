from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='hubapi',
    version='1.0.0',
    author='emalashenkov',
    author_email='egor_malashenkov@mail.ru',
    description='package for hubspot api',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='',
    project_urls={
        'Documentation': 'https://github.com/'
    },
    python_requires='>=3.7'
)

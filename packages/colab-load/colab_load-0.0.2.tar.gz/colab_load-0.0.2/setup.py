from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='colab_load',
    version='0.0.2',
    author='@GusGus153',
    author_email='dimons2006@yandex.ru',
    description='Library to download .ipynb from google colab.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Filin153/colab_load.git',
    packages=find_packages(),
    install_requires=['requests==2.31.0', 'selenium==4.14.0', 'numpy==1.26.1', 'fake-useragent==1.3.0'],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='colab load file ipynb ',
    project_urls={
        'GitHub': 'https://github.com/Filin153/colab_load.git'
    },
    python_requires='>=3.6'
)
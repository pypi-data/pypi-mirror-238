from setuptools import setup

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='FakesUsers',
  version='3.0',
  author='filcher2011',
  author_email='filcher2011@mail.ru',
  description='FakesUsers - Python library that regenerates random names, phone numbers and addresses. For now, only the Russian generation is available, but over time we will add other generations.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=['FakesUsers'],
  install_requires=['requests>=2.25.1'],
  keywords='FakesUsers',
  python_requires='>=3.7'
)
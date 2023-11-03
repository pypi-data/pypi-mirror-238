from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='vlad_new',
  version='1.0.0',
  author='KhimichVladyslav',
  author_email='khimich.vladyslav@gmail.com',
  description='This is my first module',
  long_description=readme(),
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  python_requires='>=3.7'
)
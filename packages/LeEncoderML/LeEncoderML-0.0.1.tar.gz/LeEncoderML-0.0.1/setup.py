from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Science/Research',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 

setup(
    name="LeEncoderML",
    version="0.0.1",
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    packages=find_packages(),
    install_requires=['pandas','sklearn'],
    classifiers=classifiers,
    license='MIT', 
    keywords='encoder', 
    author="Varun Vinodh",
    author_email="varunvinodh25@gmail.com",
    description="Python script for managing categorical data in machine learning, ensuring proper encoding and handling of unseen labels.",
    url="",
)


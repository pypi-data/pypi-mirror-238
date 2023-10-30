from setuptools import find_packages, setup

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
    name='introsort_multithreaded',
    packages=['introsort_multithreaded'],
    package_data = {'introsort_multithreaded': ['sorting.pyd']},
    version='0.0.4',
    description='multithreaded introsort',
    long_description=open('README.txt').read(),
    author='Chong Yih Yang',
    author_email='chongyihyang713@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='sorting', 
)
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.12',
]

setup(
    name='Mustraxlib',
    version='2.0.0',
    description='Simple tools for convenient programming',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Programmer101',
    author_email='wsl.com.uk@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Efficiency',
    packages=find_packages(),
    install_requires=['bs4', 'requests','argon2-cffi']
)

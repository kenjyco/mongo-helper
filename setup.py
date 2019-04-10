from setuptools import setup, find_packages


with open('README.rst', 'r') as fp:
    long_description = fp.read()

setup(
    name='mongo-helper',
    version='0.0.3',
    description='Helper funcs and tools for working with MongoDB',
    long_description=long_description,
    author='Ken',
    author_email='kenjyco@gmail.com',
    license='MIT',
    url='https://github.com/kenjyco/mongo-helper',
    download_url='https://github.com/kenjyco/mongo-helper/tarball/v0.0.3',
    packages=find_packages(),
    install_requires=[
        'pymongo==3.7.2',
        'settings-helper',
        'dt-helper',
    ],
    include_package_data=True,
    package_dir={'': '.'},
    package_data={
        '': ['*.ini'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: Developers',
    ],
    keywords = ['mongo', 'mongodb', 'helper']
)

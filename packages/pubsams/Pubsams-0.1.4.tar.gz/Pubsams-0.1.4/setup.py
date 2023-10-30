from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Pubsams',
    version='0.1.4',
    description='Alterantive Package for PubSam',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Ahmed Alhilal',
    author_email='Aalhilal@kfu.ed.sa',
    license='MIT',
    classifiers=classifiers,
    keywords='Cheminoframtics',
    packages=find_packages(),
    install_requires=[
        'rdkit',
        'Pillow',
        'ipython',
        'mordred',
        'pandas',
        'statsmodels',
        'matplotlib'
    ]

)
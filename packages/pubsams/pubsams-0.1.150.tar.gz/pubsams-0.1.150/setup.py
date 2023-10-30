from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pubsams',
  version='0.1.150',
  description='Find smilarity between compound and active and inactive compound in bioassay and common substracture',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ahmed Alhilal',
  author_email='aalhilal@kfu.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='chemiformatics, pubchem, conversion', 
  packages=find_packages(),
  install_requires=['rdkit','pybase64',"panel-chemistry","py3Dmol",'requests','Pillow','ipython',"mordred","pandas","statsmodels","ipyplot"],
)

from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    documentation = readme.read()

setup(name='MorseCodePy',
      packages=find_packages(),
      requires=['pygame'],
      package_data={'MorseCodePy': ['sounds/*.wav', 'images/*']},
      include_package_data=True,
      version='2.1.10',
      author='CrazyFlyKite',
      author_email='karpenkoartem2846@gmail.com',
      url='https://github.com/CrazyFlyKite/MorseCodePy/',
      description='Easily and correctly encode, decode and play the Morse code',
      long_description=documentation,
      long_description_content_type='text/markdown'
      )

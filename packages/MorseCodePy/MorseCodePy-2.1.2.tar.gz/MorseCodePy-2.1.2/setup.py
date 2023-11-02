from setuptools import setup

with open('README.md', 'r') as readme:
    documentation = readme.read()

setup(name='MorseCodePy',
      packages=['MorseCodePy'],
      requires=['pygame'],
      version='2.1.2',
      author='CrazyFlyKite',
      author_email='karpenkoartem2846@gmail.com',
      url='https://github.com/CrazyFlyKite/MorseCodePy/',
      description='Easily and correctly encode and decode text into Morse code',
      long_description=documentation,
      long_description_content_type='text/markdown'
      )

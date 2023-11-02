from setuptools import setup

try:
    with open('README.md', 'r') as readme:
        documentation = readme.read()
except FileNotFoundError:
    documentation = 'README.md not found!'

setup(name='MorseCodePy',
      packages=['MorseCodePy'],
      requires=['pygame'],
      version='2.1.1',
      author='CrazyFlyKite',
      author_email='karpenkoartem2846@gmail.com',
      url='https://github.com/CrazyFlyKite/MorseCodePy/',
      description='Easily and correctly encode and decode text into Morse code',
      long_description=documentation,
      long_description_content_type='text/markdown'
      )

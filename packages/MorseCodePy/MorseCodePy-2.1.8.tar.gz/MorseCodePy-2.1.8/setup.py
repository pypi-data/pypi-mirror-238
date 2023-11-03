from setuptools import setup

with open('README.md', 'r') as readme:
    documentation = readme.read()

setup(name='MorseCodePy',
      packages=['MorseCodePy'],
      requires=['pygame'],
      package_data={'morsecodepy': ['sounds/*.wav'], 'MorseCodePy': ['images/*.png']},
      include_package_data=True,
      version='2.1.8',
      author='CrazyFlyKite',
      author_email='karpenkoartem2846@gmail.com',
      url='https://github.com/CrazyFlyKite/MorseCodePy/',
      description='Easily and correctly encode, decode and play the Morse code',
      long_description=documentation,
      long_description_content_type='text/markdown'
      )

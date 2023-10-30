from setuptools import setup, find_packages

with open('README.md', 'r') as f:
      long_description = f.read()

setup(name='tubtools',
      description='Scraping tools for the TU Berlin web portals',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://git.tu-berlin.de/tkn/tubtools',
      author='Sebastian Bräuer',
      author_email='braeuer@tu-berlin.de',
      license='MIT',
      zip_safe=False,
      install_requires=[
            'fleep',
            'requests',
            'beautifulsoup4',
            'keyring'
      ],
      python_requires='>=3.7',
      packages=find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3",
            'Development Status :: 3 - Alpha',
            "License :: OSI Approved :: MIT License",
      ],
      entry_points={
            'console_scripts': [
                  'isis = tubtools.isis:main',
                  'isisdl = tubtools.isis:legacy_isisdl',
                  'moses = tubtools.moses.cli:main'
            ]
      })

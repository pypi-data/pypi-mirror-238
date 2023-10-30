from setuptools import setup, find_packages
from sdownloader import __version__ as package_version


with open("README.md", "r") as f:
    read_me = f.read()

setup(name="sdownloader",
      version=package_version,
      description="A little program to download given list of matrices from SuiteSparse.",
      long_description = read_me,
      long_description_content_type='text/markdown',
      url="https://github.com/talhaokur/sdownloader",
      author="Talha Okur",
      author_email="talhao@acm.org",
      license="MIT",
      packages=find_packages(),
      install_requires=[
          "requests",
      ],
      python_requires=">=3",
      classifiers=[
          "Programming Language :: Python :: 3",
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
          "Intended Audience :: Science/Research"
      ],
      entry_points={
          'console_scripts': [
              'sdownloader=sdownloader.main:main',],
              },
      project_urls={
          'Source': 'https://github.com/talhaokur/sdownloader',
          'Tracker': 'https://github.com/talhaokur/sdownloader/issues',
      })

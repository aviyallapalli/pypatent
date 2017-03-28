from setuptools import setup, find_packages
import pypatent

requirements = []
with open("requirements.txt", "r") as f:
    requirements = f.readlines()

setup(name="pypatent",
      version=pypatent.__version__,
      author="greedyrook",
      author_email="greedyrook@gmail.com",
      url="https://github.com/greedyrook/pypatent",
      license="MIT License",
      packages=find_packages(),
      install_requires=requirements,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3 :: Only",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ]
      )

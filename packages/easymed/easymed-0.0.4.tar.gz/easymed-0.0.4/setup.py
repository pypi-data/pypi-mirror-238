from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='easymed', 
      version='0.0.4',
      description='One stop medical toolkit',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='EasyMed in BUPT',
      author_email='bool1020@bupt.edu.cn',
      url='https://github.com/EasyMed2023',
      install_requires=[
        'tqdm',
        'torch',
        'opencv-python'
        ],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.10',
      ],
      python_requires='>=3.7',
      )
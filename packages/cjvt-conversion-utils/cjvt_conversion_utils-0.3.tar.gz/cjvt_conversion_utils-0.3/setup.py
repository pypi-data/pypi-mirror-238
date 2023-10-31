from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cjvt_conversion_utils',
      version='0.3',
      description='CJVT conversion utilities',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://gitea.cjvt.si/generic/conversion_utils',
      author='CJVT',
      author_email='pypi@cjvt.si',
      license='MIT',
      packages=['conversion_utils', 'conversion_utils.resources', 'conversion_utils.tests'],
      install_requires=['lxml', 'importlib_resources'],
      include_package_data=True,
      zip_safe=True)

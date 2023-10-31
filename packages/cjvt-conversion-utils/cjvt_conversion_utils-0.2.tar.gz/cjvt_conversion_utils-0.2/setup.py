from setuptools import setup

setup(name='cjvt_conversion_utils',
      version='0.2',
      description='CJVT conversion utilities',
      url='https://gitea.cjvt.si/generic/conversion_utils',
      author='CJVT',
      author_email='pypi@cjvt.si',
      license='MIT',
      packages=['conversion_utils', 'conversion_utils.resources', 'conversion_utils.tests'],
      install_requires=['lxml', 'importlib_resources'],
      include_package_data=True,
      zip_safe=True)

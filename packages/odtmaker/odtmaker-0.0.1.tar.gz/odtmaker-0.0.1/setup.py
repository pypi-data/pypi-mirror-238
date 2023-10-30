from setuptools import setup


setup(name='odtmaker',
      version='0.0.1',
      description='Small ODT generator',
      url='https://bitbucket.org/rmonico/odtmaker',
      author='Rafael Monico',
      author_email='rmonico1@gmail.com',
      license='GPL3',
      include_package_data=True,
      packages=['odtmaker', ],
      entry_points={
          'console_scripts': ['odtmaker=odtmaker.cli.__main__:main'],
      },
      zip_safe=False,
      install_requires=['ipdb'])

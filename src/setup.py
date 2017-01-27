from setuptools import setup,find_packages,Command
import os
import sys


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


# Declare your packages' dependencies here, for eg:
requires=[
            'cmd2==0.6.7',
            'argparse',
            'progressbar==2.3',
            'termcolor==1.1.0',
            'hurry.filesize==0.9',
            'pyyaml==3.12',
         ]

if os.name != "nt":
    if not "linux" in sys.platform:
        #mac os
        requires.append('readline')
else:   #On Windows
    requires.append('pyreadline==2.0')

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf '+ROOT_DIR+'/build '+ROOT_DIR+'/dist '+ROOT_DIR+'/*.pyc '+ROOT_DIR+'/*.egg-info')
        os.system('find '+ROOT_DIR+' -iname "*.pyc" -exec rm {} +')
                    
setup (
  install_requires=requires,
  
  name = 'ussclicore',
  version = '1.0.8',
  description='UShareSoft cli core module',
  #long_description='',
  packages = find_packages(),
  author = 'Joris Bremond',
  author_email = 'joris.bremond@usharesoft.com',
  license="Apache License 2.0",
  #url = '',
  classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),

  # ... custom build command
  cmdclass={
    'clean': CleanCommand,
  },
  
  #long_description= 'Long description of the package',
  
)

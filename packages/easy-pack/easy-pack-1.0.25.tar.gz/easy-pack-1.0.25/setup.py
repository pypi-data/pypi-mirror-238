from setuptools import setup

import os
readme_file = 'resources/readme.md' if os.path.isfile('resources/readme.md') else './easy_pack/readme.md'
with open(readme_file) as f:
	long_description = f.read()

setup(name='easy-pack',description='easy packing!',author='german espinosa',author_email='germanespinosa@gmail.com',long_description=long_description,long_description_content_type='text/markdown',packages=['easy_pack'],install_requires=['twine'],license='MIT',version='1.0.25',zip_safe=False)

from setuptools import setup

import os
if os.path.isfile('./easy_pack/readme.md'):
	with open('./easy_pack/readme.md') as f:
		long_description = f.read()
else:
	long_description = ''
setup(name='easy-pack',description='easy packing!',author='german espinosa',author_email='germanespinosa@gmail.com',long_description=long_description,long_description_content_type='text/markdown',packages=['easy_pack'],install_requires=['twine'],license='MIT',version='1.0.32',zip_safe=False)

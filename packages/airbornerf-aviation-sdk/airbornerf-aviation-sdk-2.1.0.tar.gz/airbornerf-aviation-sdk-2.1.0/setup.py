from setuptools import setup

setup(
	name='airbornerf-aviation-sdk',
	version='2.1.0',
	description='AirborneRF Aviation SDK',
	packages=['arf'],
	license='Proprietary',
	author='Thomas Wana',
	author_email='support@airbornerf.com',
	url='https://www.airbornerf.com/',
	install_requires=[
		'requests', 'numpy'
	],
)

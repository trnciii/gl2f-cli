from setuptools import setup, find_packages

setup(
	name='gl2f',
	version='0.0.1',
	url='https://github.com/trnciii/gl2f-cli',
	license='MIT',

	packages=['gl2f'],
	install_requires=[
		'requests',
	],

	entry_points={
		'console_scripts': [
			'gl2blogs = gl2f.blogs:ls'
		]
	}
)
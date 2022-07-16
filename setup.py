from setuptools import setup, find_packages

setup(
	name='gl2f-cli',
	version='0.0.1',
	url='https://github.com/trnciii/gl2f-cli',
	license='MIT',
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'gl2blogs = gl2f.blogs:ls'
		]
	}
)
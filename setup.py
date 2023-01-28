from setuptools import setup, find_packages

setup(
	name='gl2f',
	description='CLI tool for GL2 family',
	version='0.3.3',
	url='https://github.com/trnciii/gl2f-cli',
	license='MIT',
	packages=find_packages(),
	package_data={'gl2f':['data/*', 'data/site/*']},
	install_requires=[
		'requests',
		'libsixel-python',
		'Pillow',
		'webdriver_manager',
		'selenium'
	],
	entry_points={
		'console_scripts': [
			'gl2f = gl2f.__main__:main',
		]
	}
)

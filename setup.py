from setuptools import setup, find_packages

setup(
	name='gl2f',
	version='0.2.1',
	url='https://github.com/trnciii/gl2f-cli',
	license='MIT',
	packages=find_packages(),
	package_data={'gl2f':['data/site/*']},
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
			'gl2b = gl2f.__main__:partial.blogs',
			'gl2r = gl2f.__main__:partial.radio',
			'gl2n = gl2f.__main__:partial.news',
			'gl2d = gl2f.__main__:partial.today',
		]
	}
)

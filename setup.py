from setuptools import setup, find_packages

setup(
	name='gl2f',
	version='0.0.1',
	url='https://github.com/trnciii/gl2f-cli',
	license='MIT',
	packages=find_packages(),
	install_requires=[
		'requests',
		'webdriver_manager',
		'selenium'
	],
	entry_points={
		'console_scripts': [
			'gl2f = gl2f.__main__:main',
			'gl2b = gl2f.ls.main:main.blogs',
			'gl2r = gl2f.ls.main:main.radio',
			'gl2n = gl2f.ls.main:main.news',
		]
	}
)
from setuptools import setup, find_packages

setup(
	name='gl2f',
	version='0.0.1',
	url='https://github.com/trnciii/gl2f-cli',
	license='MIT',
	packages=find_packages(),
	install_requires=[
		'requests',
	],
	entry_points={
		'console_scripts': [
			'gl2f = gl2f.__main__:main',
			'gl2f-blogs = gl2f.blogs:main',
			'gl2f-radio = gl2f.radio:main',
			'gl2f-news = gl2f.news:main',
			'gl2f-auth = gl2f.auth:main'
		]
	}
)
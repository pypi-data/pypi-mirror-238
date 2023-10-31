import setuptools
with open(r'C:\Users\AleksFOLT\Desktop\Pypi-uploader-main\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='gigathon-api',
	version='0.0.1',
	author='__token__',
	author_email='aleksfolt@ya.ru',
	description='100 percent free gigathon-api',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['gigathon-api'],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
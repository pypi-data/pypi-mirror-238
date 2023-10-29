import setuptools
with open(r'C:\Users\User\Desktop\test\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='donate',
	version='1.3.0',
	author='Redpiar',
	author_email='Regeonwix@gmail.com',
	description='library for donations',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['donate'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=['requests\n', 'aiohttp'],
	python_requires='>=3.6',
)
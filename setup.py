from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

requirements = [
	"imutils",
	"opencv-python",
	"pytesseract",
	"Pillow",
]

setup(
    name='pytextractor',
    version='0.0.1',
    author='danny crasto',
    author_email='danwald79@gmail.com',
    description='text extractor from images',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/danwald/pytextractor/',
    packages=find_packages(),
    install_requires=requirements,
	license='MIT',
    classifiers=[
		'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
		'License :: OSI Approved :: MIT License',
    ],
)

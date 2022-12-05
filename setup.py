from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

requirements = (
    'imutils>=0.5.4',
    'opencv-python>=4.5.3.56',
    'Pillow>=9.3.0',
    'pytesseract>=0.3.7',
    'requests>=2.26.0',
)

dev_requirements = (
    'pip>=22.0.4',
    'wheel>=0.33.1',
    'ipdb>=0.13.9',
    'pytest>=4.3.0',
    'twine>=1.13.0',
    'pytest-cov>=2.6.1',
)

setup(
    name='pytextractor',
    version='1.1.0',
    author='danny crasto',
    author_email='danwald79@gmail.com',
    description='text extractor from images',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/danwald/pytextractor/',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={"dev": dev_requirements},
    use_scm_version=True,
    setup_requires=['pytest-runner', 'setuptools_scm', ],
    tests_require=['pytest', ],
    license='MIT',
    include_package_data=False,
    entry_points={'console_scripts': ['text_detector=pytextractor.text_detection:text_detector']},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
    ],
)

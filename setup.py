from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

requirements = (
    'imutils',
    'opencv-python',
    'Pillow',
    'pytesseract',
    'requests',
)

dev_requirements = (
    'pytest',
)

setup(
    name='pytextractor',
    version='2.0.0',
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
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
    ],
)

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

requirements = [
    'imutils==0.5.2',
    'opencv-python==4.1.1.26',
    'Pillow==6.2.2',
    'pytesseract==0.2.6',
    'requests==2.22.0',
]


setup(
    name='pytextractor',
    version='0.6',
    author='danny crasto',
    author_email='danwald79@gmail.com',
    description='text extractor from images',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/danwald/pytextractor/',
    packages=find_packages(),
    install_requires=requirements,
    use_scm_version = True,
    setup_requires=['pytest-runner', 'setuptools_scm',],
    tests_require=['pytest', ],
    license='MIT',
    include_package_data=False,
    entry_points={'console_scripts': ['text_detector=pytextractor.text_detection:text_detector']},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
)

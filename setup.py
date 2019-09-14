from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

requirements = [
    'imutils==0.5.2',
    'opencv-python==4.0.0.21',
    'Pillow==5.4.1',
    'pytesseract==0.2.6',
]

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        import os
        import requests
        import pytextractor
        import sys

        pkg_path = os.path.dirname(pytextractor.__file__)
        data_file = os.path.join(pkg_path, 'data/frozen_east_text_detection.pb')
        print('Writing east to {}'.format(data_file))
        with open(data_file, 'wb') as fp:
            with requests.get('https://tinyurl.com/yxdd7kb5', stream=True) as response:
                for chunk in response.iter_content(chunk_size=2048):
                    sys.stdout.flush()
                    fp.write(chunk)
        install.run(self)

setup(
    name='pytextractor',
    version='0.3',
    author='danny crasto',
    author_email='danwald79@gmail.com',
    description='text extractor from images',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/danwald/pytextractor/', packages=find_packages(),
    install_requires=requirements,
    use_scm_version = True,
    setup_requires=['pytest-runner', 'setuptools_scm', 'requests'],
    tests_require=['pytest', ],
    license='MIT',
    include_package_data=True,
    exclude_package_data={'': ['*.pb']},
    entry_points={'console_scripts': ['text_detector=pytextractor.text_detection:text_detector']},
    cmdclass = { 'install': PostInstallCommand },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
)

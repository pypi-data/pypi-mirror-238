import re
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

VERSION_FILE = "bfgbidding/_version.py"
with open(VERSION_FILE, 'r') as f_version:
    version_string = f_version.read()
version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(version_re, version_string, re.M)
if mo:
    version_string = mo.group(1)
else:
    raise RuntimeError(f'Unable to find version string in {VERSION_FILE}.')


setup_args = dict(
    name='bfgbidding',
    version=version_string,
    description='A collection of modules that json and toml config files.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='jeff watkins',
    author_email='support@bidforgame.com',
    keywords=['bridge, bidding'],
    url='https://psionman@bitbucket.org/psionman/bfgbidding.git',
    download_url='https://pypi.org/project/bfgbidding/',
)

install_requires = [
    'username', 'nose', 'pytest'
]

if __name__ == '__main__':
    setup(
            package_data={
                'bfgbidding': [
                    'tests/test_data/*.json',
                    'comment_data/*.json',
                    ]
            },
        include_package_data=True,
        **setup_args,
        install_requires=install_requires
        )

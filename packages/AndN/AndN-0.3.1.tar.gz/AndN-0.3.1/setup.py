import setuptools

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()
setuptools.setup(
    name='AndN',
    version='0.3.1',
    url='https://github.com/grayrail000/AndroidQQ',
    packages=setuptools.find_packages(),
    license='',
    author='1a',
    author_email='',
    description='',
    install_requires=requirements

)

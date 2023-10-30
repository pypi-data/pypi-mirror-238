from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    readme = file.read()

setup(
    name='pygame_simple_core',
    version='0.2.3',
    license='MIT license',
    author='Vinicius Putti Morais',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='viniputtim@gmail.com',
    keywords='pygame',
    description='a easy to use framework to fastly make games with pygame',
    packages=find_packages(),
    install_requires=['pygame']
)

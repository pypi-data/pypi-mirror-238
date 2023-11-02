from setuptools import setup, find_packages

# Read the content of the README file
with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='streamsights-ott-platform',
    version='1.0.0',
    author='Sneha Iyer',
    author_email='iyersneha243@gmail.com',
    description='StreamSights OTT Platform User Class',
    long_description=long_description,  # Use the content of README.md
    long_description_content_type='text/markdown',
    packages=find_packages(),
)






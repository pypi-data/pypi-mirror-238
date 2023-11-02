
from setuptools import setup, find_packages


version = '1.0.7'
url = 'https://github.com/pmaigutyak/product-images'

with open('requirements.txt') as f:
    requires = f.read().splitlines()


setup(
    name='product-images',
    version=version,
    description='Django run app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='%s/archive/%s.tar.gz' % (url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=requires
)

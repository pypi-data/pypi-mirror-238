# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guido']

package_data = \
{'': ['*'], 'guido': ['data/*', 'templates/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'h5py>=3.3.0,<4.0.0',
 'mcdm>=1.4,<2.0',
 'ncls>=0.0.60,<0.0.61',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.1,<2.0.0',
 'pyfaidx>=0.6.1,<0.7.0',
 'pyranges>=0.0.101,<0.0.102',
 'scikit-allel>=1.3.5,<2.0.0',
 'zarr>=2.8.3,<3.0.0']

setup_kwargs = {
    'name': 'guido',
    'version': '0.1.4a1',
    'description': '',
    'long_description': 'None',
    'author': 'Nace Kranjc',
    'author_email': 'nace.kranjc@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.9,<=3.10',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biu',
 'biu.lstm_unet',
 'biu.lstm_unet.models',
 'biu.progress',
 'biu.siam_unet',
 'biu.siam_unet.helpers',
 'biu.unet']

package_data = \
{'': ['*']}

install_requires = \
['albumentations>=1.3.0,<2.0.0',
 'barbar>=0.2.1,<0.3.0',
 'numpy>=1.19.5,<2.1.0',
 'packaging',
 'scikit-image>=0.18.2,<1.0.0',
 'scipy>=1.9.1,<2.2.0',
 'tifffile',
 'torch>=1.9.0,<2.2.0',
 'tqdm>=4.61.2,<5.0.0']

setup_kwargs = {
    'name': 'bio-image-unet',
    'version': '0.6.1',
    'description': 'Implementations of U-Net and Siam U-Net for biological image segmentation',
    'long_description': '# Bio Image U-Net\n\nImplementations of U-Net and Siam U-Net for biological image segmentation\n\n### Authors\n[Daniel Härtter](daniel.haertter@duke.edu) (Duke University, University of Göttingen) \\\n[Yuxi Long](longyuxi@live.com) (Duke University) \\\nAndreas Primeßnig\n\n### Installation\nInstall with ``pip install git+https://github.com/danihae/bio-image-unet``\n\n\n### Usage example\n[iPython Notebook for getting started with U-Net](https://github.com/danihae/bio-image-unet/blob/master/using_unet.ipynb) \\\n[iPython Notebook for getting started with Siam U-Net](https://github.com/danihae/bio-image-unet/blob/master/using_siam_unet.ipynb)\n\n### Documentation\n\nTBD\n',
    'author': 'Daniel Haertter',
    'author_email': 'dani.hae@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)

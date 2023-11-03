# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scpca', 'scpca.models', 'scpca.plots', 'scpca.train', 'scpca.utils']

package_data = \
{'': ['*']}

install_requires = \
['adjusttext>=0.7.3,<0.8.0',
 'gseapy>=1.0.4,<2.0.0',
 'pyro-ppl<1.8.4',
 'scanpy>=1.8.2',
 'torch<2.0.0']

extras_require = \
{'docs': ['Sphinx<7.0.0',
          'sphinxcontrib-napoleon==0.7',
          'nbsphinx==0.8.9',
          'sphinx-autodoc-typehints==1.23.0',
          'sphinx-book-theme>=1.0.1,<2.0.0',
          'sphinxcontrib-bibtex>=2.6.1,<3.0.0',
          'sphinx-autopackagesummary>=1.3,<2.0'],
 'notebook': ['jupyter']}

setup_kwargs = {
    'name': 'scpca',
    'version': '0.3.1',
    'description': 'Single-cell PCA.',
    'long_description': '\n# scPCA - A probabilistic factor model for single-cell data\n\n![pypi](https://img.shields.io/pypi/v/scpca.svg)\n![release workflow](https://github.com/sagar87/scPCA/actions/workflows/release.yaml/badge.svg)\n![push workflow](https://github.com/sagar87/scPCA/actions/workflows/branch.yaml/badge.svg)\n\nscPCA is a versatile matrix factorisation framework designed to analyze single-cell data across diverse experimental designs.\n\n![scPCA schematic](https://github.com/sagar87/scPCA/blob/main/docs/scpca_schematic.png?raw=true)\n\n*scPCA is a young project and breaking changes are to be expected.*\n\n## Quick install\n\nscPCA makes use `torch`, `pyro` and `anndata`. We highly recommend to run scPCA on a GPU device.\n\n### Via Pypi\n\nThe easiest option to install `scpca` is via Pypi. Simply type\n\n```\n$ pip install scpca\n```\n\n\ninto your shell and hit enter.\n\n* Free software: MIT license\n* Documentation: https://sagar87.github.io/scPCA/index.html\n\n## Credits\n\n* Harald Vöhringer\n',
    'author': 'Harald Vohringer',
    'author_email': 'harald.voeh@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)

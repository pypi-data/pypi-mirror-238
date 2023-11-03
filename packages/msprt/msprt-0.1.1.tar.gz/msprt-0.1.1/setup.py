# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['msprt']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.8.1,<4.0.0', 'numpy>=1.26.1,<2.0.0', 'scipy>=1.11.3,<2.0.0']

setup_kwargs = {
    'name': 'msprt',
    'version': '0.1.1',
    'description': '',
    'long_description': "# Python mSPRT Package:\n\nThis package provides a Python implementation for calculating the Mixture Sequential Probability Ratio Test (mSPRT). \n\nmSPRT is a statistical hypothesis test that can be used to decide if a observed data supports one of two hypotheses, based on a sequence of independent and identically distributed observations.\n\nMain functionalities:\n1. Calculating mixture variance\n\n$$\n\\tau^2 = \\sigma^2 \\frac{\\Phi(-b)}{\\frac{1}{b}\\phi(b)-\\Phi(-b)}\n$$\n\n2. Calculating test statistic for normal distribution\n\n$$\n\\tilde{\\Lambda}_n = \\sqrt{\\frac{2\\sigma^2}{V_n + n\\tau^2}}\\exp\\left(\\frac{n^2\\tau^2(\\bar{Y}_n - \\bar{X}_n-\\theta_0)^2}{4\\sigma^2(2\\sigma^2+n\\tau^2)}\\right).\n$$\n\n3. Calculating test statistic for Bernoulli distribution\n\n$$\n\\tilde{\\Lambda}_n = \\sqrt{\\frac{V_n}{V_n + n\\tau^2}}\\exp{\\left(\\frac{n^2\\tau^2(\\bar{Y}_n - \\bar{X}_n-\\theta_0)^2}{2V_n(V_n+n\\tau^2)}\\right)}\n$$\n\n\n\n## Installation:\n\nThe mSPRT package can be easily installed using pip:\n\n```bash\npip install msprt\n```\n\n## Pre-requisite\nPython >=3.10;<3.13\n\n## Dependencies:\n\nThe mSPRT package depends on the following Python libraries:\n- Numpy\n- Scipy\n- Matplotlib\n\nThese dependencies can also be easily installed using pip:\n\n```bash\npip install numpy scipy matplotlib\n```\n\n## How to Use:\n\nFirst, import the mSPRT package:\n\n```python\nfrom msprt import msprt\n```\n\nThen, prepare the two sample lists that you want to compare.\n\n```python\nx = [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]\ny = [0.2, 0.1, 0.4, 0.6, 0.7, 0.8]\n```\n\nNext, call the `msprt` object with observation lists, along with the parameters for the mSPRT test, such as the `alpha` and the `theta` values (by default it assumes you are using a normal distribution and alpha is set to 0.05).\n\n```python\nresult = msprt(x=x, y=y, sigma=1.0)\n```\n\nIf you want to use a Bernoulli distribution, specify it as such:\n\n```python\nresult = msprt(x=x, y=y, theta=0.5, distribution='bernoulli')\n```\n\nTo plot the results, use the `plot` method:\n\n```python\nresult.plot()\n```\n\nFor detailed information about each parameter, please refer to the comments in the source code.\n\n## Contact:\n\nIf you find any problems with the implementation, you can leave the ticket on Github.\n\n[mSPRT GitHub Page](https://github.com/ovidijusku/msprt)\n\n## License:\n\nThis project is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. See the `LICENSE` file for more information.\n\n## References (real heroes)\n1. Johari, R., Pekelis, L., & Walsh, D. J. (2019). Always Valid Inference: Bringing Sequential Analysis to A/B Testing. arXiv:1512.04922 [math.ST]. [Link to the paper](https://doi.org/10.48550/arXiv.1512.04922)\n2. The R and C++ implementations of the paper are available in the GitHub repository maintained by Erik Stenberg: [GitHub Repository](https://github.com/erik-stenberg/mixtureSPRT).\n",
    'author': 'Ovidijus Kuzminas',
    'author_email': 'ovidijus4733@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.13',
}


setup(**setup_kwargs)

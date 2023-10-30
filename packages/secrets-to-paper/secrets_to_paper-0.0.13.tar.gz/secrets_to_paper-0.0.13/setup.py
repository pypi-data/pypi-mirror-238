# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secrets_to_paper',
 'secrets_to_paper.build',
 'secrets_to_paper.export',
 'secrets_to_paper.parse',
 'secrets_to_paper.parse.hid']

package_data = \
{'': ['*'], 'secrets_to_paper': ['templates/*']}

install_requires = \
['click>=8.1.7,<9.0.0',
 'cryptography>=41.0.5,<42.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'opencv-contrib-python>=4.8.1.78,<5.0.0.0',
 'opencv-python>=4.8.1.78,<5.0.0.0',
 'pdfplumber>=0.10.3,<0.11.0',
 'pillow>=10.1.0,<11.0.0',
 'pyzbar>=0.1.9,<0.2.0',
 'qrcode>=7.4.2,<8.0.0',
 'weasyprint>=60.1,<61.0']

entry_points = \
{'console_scripts': ['stp = secrets_to_paper.stp:stp']}

setup_kwargs = {
    'name': 'secrets-to-paper',
    'version': '0.0.13',
    'description': 'A command line tool to help with key-to-paper and paper-to-key.',
    'long_description': "# secrets-to-paper\n\nA command-line tool to convert secret keys to printable PDFs and to parse those\nPDFs back to usable secret keys.\n\nNote: Python 3.10+ is required to use this package.\nPython 3.8 introduced a new computation for\n[modular inverses](https://docs.python.org/3/library/functions.html#pow).\n\n> Changed in version 3.8: For int operands, the three-argument form of pow now\n> allows the second argument to be negative, permitting computation of modular\n> inverses.\n\n## Dependencies\n\n- paperkey [source](http://www.jabberwocky.com/software/paperkey/)\n  / [Debian Package](https://packages.debian.org/sid/paperkey)\n\n  paperkey is a command line tool to export GnuPG keys on paper. It reduces the\n  size of the exported key, by removing the public key parts from the private\n  key. Paperkey also includes CRC-24 checksums in the key to allow the user\n  to check whether their private key has been restored correctly.\n\n- zbar [source](https://github.com/mchehab/zbar)\n  / [Debian Package](https://packages.debian.org/sid/libzbar0)\n\n  for reading QR codes (2D matrix)\n\n### USB Scanner\n\n<https://github.com/libusb/hidapi>\n\nNote: in Linux, USB devices follow a path like this:\n\nKernel:\n\n- usb core\n- ushbid (a Linux kernel driver)\n- hid subsystem\n- input subsystem\n- event devices\n\nUserspace:\n\n- libinput (a library for handling Linux input devices `/dev/input/`)\n- libinput Xorg driver\n- Xorg or Wayland Compositor driver (which uses the libinput library)\n- mouse drawn on the screen\n\n### Webcam Imports\n\nYou can also use a webcam with OpenCV to read QR codes.\n\n### Ubuntu/Linux\n\n#### Add PPA\n\n```bash\nsudo apt install software-properties-common\nsudo add-apt-repository ppa:jaredvacanti/security-dev\nsudo apt-get update\n\n# install the package\nsudo apt install python3-secrets-to-paper\n```\n\n### MacOS X\n\n```bash\nbrew tap jaredvacanti/taps\nbrew install secrets-to-paper\n```\n\n## Usage\n\n```bash\nUsage: stp [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --debug / --no-debug\n  --help                Show this message and exit.\n\nCommands:\n  export      Helper functions for writing secret keys to paper.\n  export-gpg  Helper functions for writing GPG keys to paper.\n  gen         Helper function to generate RSA private key from P and Q or ECC\n              private key from A, B, and D.\n  parse       Helper functions to parse paper keys into usable PEM format.\n```\n\n## Development\n\n### Initializing a virtual environment\n\n```bash\n# requires >= python3.10\npyenv shell 3.10\n\n# init & activate virtualenvironment\npython -m venv .venv\nsource .venv/bin/activate\n\n# install poetry in venv, and use to install local package\npip install --upgrade pip\npip install poetry\npoetry install\n```\n\nThis makes an executable `stp` available in your `$PATH` after poetry\ninstallations. During development, it's often more convenient to run\n\n```bash\npoetry run stp ...\n```\n\ninstead of re-installing before invocations.\n\n### Using GPGME\n\nThis is not installed from PyPI.\n\n<https://github.com/gpg/gpgme/blob/master/lang/python/doc/src/gpgme-python-howto.org>\n\n> it appears that a copy of the compiled module\n> may be installed into a virtualenv of the same major and minor version\n> matching the build. Alternatively it is possible to utilise a `sites.pth`\n> file in the `site-packages/` directory of a virtualenv installation, which\n> links back to the system installations corresponding directory in order to\n> import anything installed system wide. This may or may not be appropriate\n> on a case by case basis.\n\nYou can link the system installed version into your virtual environment during\ndevelopment:\n\n```bash\nln -s /usr/lib/python3/dist-packages/gpg/ .venv/lib/python3.10/site-packages/\n\n# delete the link\nrm -rf .venv/lib/python3.10/site-packages/gpg/\n```\n\n### Building Debian Package\n\n```bash\ngit checkout debian/master\ngbp buildpackage\n```\n\n## Testing\n\nYou can generate a private and public key for testing purposes using `openssl`.\n\n```bash\npoetry run pytest\n```\n",
    'author': 'Jared Vacanti',
    'author_email': 'jaredvacanti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://salsa.debian.org/jvacanti/secrets-to-paper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

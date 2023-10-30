# secrets-to-paper

A command-line tool to convert secret keys to printable PDFs and to parse those
PDFs back to usable secret keys.

Note: Python 3.10+ is required to use this package.
Python 3.8 introduced a new computation for
[modular inverses](https://docs.python.org/3/library/functions.html#pow).

> Changed in version 3.8: For int operands, the three-argument form of pow now
> allows the second argument to be negative, permitting computation of modular
> inverses.

## Dependencies

- paperkey [source](http://www.jabberwocky.com/software/paperkey/)
  / [Debian Package](https://packages.debian.org/sid/paperkey)

  paperkey is a command line tool to export GnuPG keys on paper. It reduces the
  size of the exported key, by removing the public key parts from the private
  key. Paperkey also includes CRC-24 checksums in the key to allow the user
  to check whether their private key has been restored correctly.

- zbar [source](https://github.com/mchehab/zbar)
  / [Debian Package](https://packages.debian.org/sid/libzbar0)

  for reading QR codes (2D matrix)

### USB Scanner

<https://github.com/libusb/hidapi>

Note: in Linux, USB devices follow a path like this:

Kernel:

- usb core
- ushbid (a Linux kernel driver)
- hid subsystem
- input subsystem
- event devices

Userspace:

- libinput (a library for handling Linux input devices `/dev/input/`)
- libinput Xorg driver
- Xorg or Wayland Compositor driver (which uses the libinput library)
- mouse drawn on the screen

### Webcam Imports

You can also use a webcam with OpenCV to read QR codes.

### Ubuntu/Linux

#### Add PPA

```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:jaredvacanti/security-dev
sudo apt-get update

# install the package
sudo apt install python3-secrets-to-paper
```

### MacOS X

```bash
brew tap jaredvacanti/taps
brew install secrets-to-paper
```

## Usage

```bash
Usage: stp [OPTIONS] COMMAND [ARGS]...

Options:
  --debug / --no-debug
  --help                Show this message and exit.

Commands:
  export      Helper functions for writing secret keys to paper.
  export-gpg  Helper functions for writing GPG keys to paper.
  gen         Helper function to generate RSA private key from P and Q or ECC
              private key from A, B, and D.
  parse       Helper functions to parse paper keys into usable PEM format.
```

## Development

### Initializing a virtual environment

```bash
# requires >= python3.10
pyenv shell 3.10

# init & activate virtualenvironment
python -m venv .venv
source .venv/bin/activate

# install poetry in venv, and use to install local package
pip install --upgrade pip
pip install poetry
poetry install
```

This makes an executable `stp` available in your `$PATH` after poetry
installations. During development, it's often more convenient to run

```bash
poetry run stp ...
```

instead of re-installing before invocations.

### Using GPGME

This is not installed from PyPI.

<https://github.com/gpg/gpgme/blob/master/lang/python/doc/src/gpgme-python-howto.org>

> it appears that a copy of the compiled module
> may be installed into a virtualenv of the same major and minor version
> matching the build. Alternatively it is possible to utilise a `sites.pth`
> file in the `site-packages/` directory of a virtualenv installation, which
> links back to the system installations corresponding directory in order to
> import anything installed system wide. This may or may not be appropriate
> on a case by case basis.

You can link the system installed version into your virtual environment during
development:

```bash
ln -s /usr/lib/python3/dist-packages/gpg/ .venv/lib/python3.10/site-packages/

# delete the link
rm -rf .venv/lib/python3.10/site-packages/gpg/
```

### Building Debian Package

```bash
git checkout debian/master
gbp buildpackage
```

## Testing

You can generate a private and public key for testing purposes using `openssl`.

```bash
poetry run pytest
```

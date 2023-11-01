# odhpy

## Installation

This package may be installed using pip from Bitbucket (requires authentication), or directly from PyPi (public). These are both shown below.

```bash
pip install git+https://bitbucket.org/odhydrology/odhpy.git
```

```bash
pip install odhpy
```

## Usage

```python
import odhpy

# returns the package version
odhpy.__version__

# prints 'Hello world!' to the console
odhpy.hello_world()
```

## Uploading to PyPi

First build a distribution from an anaconda prompt in the root of your project, and then upload the dist to PyPi using Twine. Twine will prompt you for your PyPi username and password.

```bash
python setup.py sdist
```

```bash
twine upload dist/*
```

## Unit Tests

Install the nose2 test-runner framework. Then from the root project folder run the nose2 module. This will automatically find and run tests in any modules named "test_*".

```bash
pip install nose2
```

```bash
python -m nose2
```

## License

None.

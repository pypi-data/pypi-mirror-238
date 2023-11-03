# Overview
This library contains useful wrappers around the Tonic Textual API

## Usage

Instantiate the API wrapper using the following code:

```
from tonic_textual.api import TonicTextual

# Do not include trailing backslash in TONIC_URL
api = TonicTextual(TONIC_TEXTUAL_URL, API_KEY)
```

Once instantiated, the following endpoints are available for consumption. Note that available endpoints and response types are limited. Available fields may be severely limited compared to the current Tonic API.

## Build and package

Update the version in pyproject.toml.  Ensure you are in the python_sdk/ folder in the repo root for the following instructions.

Update build and twine

```
python -m pip install --upgrade build
python -m pip install --upgrade twine
```

Clean out dist folder

```
rm dist/ -rf
```

Now build

```
python -m build
```

And ship

```
python -m twine upload .\dist\*
```

The username is __token__ and the pw is your token including the 'pypi-'

# gdrive-datastore

A package that facilitates storing data to Google Drive

## build

To build distribution, simply run:

> python -m build

## install locally for testing

To install localling for testing, simply run:

> python -m pip install .

## test locally

To test locally, simply run:

> pytest tests

## upload to test pypi

Before uploading, make sure you have a `.pypirc` file in your home directory that contains an API token for the test pypi site.  If this did not exist, the dev container would have created a directory of that name in its place.  You will hve to remove the created directory before creating the file.

To upload to test pypi, simply run:

> python -m twine upload --repository testpypi dist/*

## install from test pypi

To install from test pypi, simply run: 

> python -m pip install --index-url https://test.pypi.org/simple/ --no-deps gdrive-datastore

## upload to pypi

Before uploading, make sure you have a `.pypirc` file in your home directory that contains an API token for the test pypi site.  If this did not exist, the dev container would have created a directory of that name in its place.  You will hve to remove the created directory before creating the file.

To upload to test pypi, simply run:

> python -m twine upload dist/*

## install from pypi

To install from pypi, simply run: 

> python -m pip install gdrive-datastore

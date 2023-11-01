# Образец пакета PyPi

This is a simple exercise to publish a package onto PyPi.

## Build

python setup.py sdist bdist_wheel

## Upload

twine upload --repository pypi dist/* --skip-existing

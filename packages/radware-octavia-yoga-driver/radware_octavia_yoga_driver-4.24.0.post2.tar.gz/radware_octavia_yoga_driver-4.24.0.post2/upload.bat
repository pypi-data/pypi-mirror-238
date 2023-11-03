@echo off

rem make source distribution and upload the package
python -m twine upload --repository pypi dist/*
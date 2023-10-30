use the library in other Python scripts. 
Create a new Python script in a different directory and 
import and use the send function from the library

```
from potatoscript.potatoConfig import Config as config

you have to input the following values to  Config(smtp_server,smtp_port,sender)

[Database]
db = h5_bare_vos_debug
host = localhost
user = root
pw = 
```

To update a Python library that you've previously published on PyPI, you need to follow these general steps:

### 1. Update Your Code

Make the necessary changes and improvements to your library code.

### 2. Update Version Number

Increment the version number in your `setup.py` file. This is crucial for PyPI to recognize that a new version is available.

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name='my_library',
    version='0.2',  # Update the version number
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
)
```

### 3. Re-package Your Library

Re-run the following command to create a new distribution of your updated library:

```bash
python setup.py sdist bdist_wheel
```

### 4. Upload the Updated Version

Use `twine` to upload the new version to PyPI:

```bash
twine upload dist/*
```

### 5. Verify on PyPI

Visit the PyPI website (https://pypi.org/) and confirm that the new version of your library is listed.

### 6. Notify Users (Optional)

Consider notifying users about the new version, especially if the update includes important changes, bug fixes, or new features. You can use release notes or a dedicated announcement.

That's it! Users can now update their installations by running:

```bash
pip install --upgrade my_library
```
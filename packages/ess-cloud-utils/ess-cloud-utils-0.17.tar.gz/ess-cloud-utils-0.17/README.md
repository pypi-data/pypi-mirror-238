# ESS Cloud Utils

## Preparation for PyPi

Step 1 -> install the Twine app:
```shell
pip install twine
```

Step 2 -> After registration to PyPi (https://pypi.org/) create .pypirc in home folder with the content:
```text
[pypi]
username = dfssdfdsdsf
password = dfsdfdsfdsf
```


## Pushing to PyPi


Step 1 -> update the version in setup.py

Step 2 -> call 
```shell
python setup.py sdist
```

Step 3 -> call
```shell
twine upload dist/*
```


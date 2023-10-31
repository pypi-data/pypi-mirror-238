# fgslpyrest

Python component to make HTTP RESTful requests.

## Using the component 

### Making a HTTP GET request in the terminal

The sequence of commands below make a HTTP GET request and check if the response has the word "German". The response, in this case, is HTML. The last parameter enables verbose output.

```shell
$ python
>>> from fgslpyrest.http.Rest import Rest
>>> rest = Rest()
>>> response = rest.doGet([],"https://time.is/pt_br/UTC",200,True)
>>> print(response.find("German"))
```

The next sequence of commands make a HTTP request which returns a JSON object.

```shell
$ python
>>> import json
>>> from fgslpyrest.http.Rest import Rest
>>> rest = Rest()
>>> response = rest.doGet([],"https://reqres.in/api/users/2",200)
>>> user = json.loads(response)
>>> print(user["data"]["email"])
```

## For developers

### Building the package

```shell
python setup.py sdist
```

### Upload the package to PyPI

```shell
twine upload dist/*
```

# 



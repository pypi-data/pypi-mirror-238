<p align="center">
  <p align="center">
    <a href="https://www.turon.io" target="_blank">
      <img src="docs/source/_static/logo.png" alt="Turon" width="250" height="84">
    </a>
  </p>
  <p align="center">
    Users and logs provide clues. Sentry provides answers.
  </p>
</p>


`Turon <https://www.turon.io>`_ is a platform that allows developers and data teams to build highly performant APIs on top of their data warehouses.

This is the API documentation for Turon's official Python SDK.

Don't already have an account and Turon project? Head over to `turon.io <https://app.turon.io>`_, then return to this page.

Install
-------

Install our Python SDK using `pip <https://pip.pypa.io/en/stable/>`_:

```shell
pip install --upgrade turon
```

Usage
-----

```python
 from turon import Turon
 from turon.exceptions import APIException

 turon = Turon('TURON_APP_KEY', 'TURON_API_KEY')
 query = turon.query('GetUserById', user_id='582091167')

 try:
    user = query.to_dict()
 except APIException as excinfo:
    if excinfo.code == 404:
       print('User could not be found.')
```

Documentation
-------------

More detailed API documentation can be found [here](https://tryturon.github.io/turon-py/).


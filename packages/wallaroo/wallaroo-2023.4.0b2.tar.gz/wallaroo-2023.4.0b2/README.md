# Python SDK for Wallaroo

This repo contains the python SDK used to interface with the Wallaroo API. The structure is as follows:

- Package name: Wallaroo
- Modules contained: sdk
- [SDK documentation](https://wallaroolabs.github.io/wallaroo-docs/sdk.html)

## Building

Building the SDK requires `Python`, `Rust`, and `NodeJS` to be installed in your environment.

This SDK has moved from using setuptools to using Hatch.

To build both `wheel` and `sdist` targets, you must be in the `platform` directory, or use the `-C` flag to target it.

```sh
# From <your path>/platform
make sdk
```
or
```sh
# From <your path>/platform/sdk
make -C .. sdk
```

The `make sdk` command generates an OpenAPI schema from all of our Rust microservices and then creates a Python Client in `wallaroo/wallaroo_ml_ops_api_client` for you to easily query the microservices with.

## Tests

To execute all tests run:

```sh
make unit_tests
```

To execute a specific test run, for example:

```sh
pytest -k test_client
```

To update snapshots used for testing, you can run:

```sh
pytest -k test_checks --snapshot-update
```

## Build

Make sure you have the latest version of 'build'

```sh
make build-sdk
```

This will generate a distribution package in the dist directory.

## Generate Documentation

pdoc3 is used to generate the documentation for the SDK.
To generate the documentation run:

```sh
make doc
```

This will generate documentation files in the [html](html) directory

To remove generated files:

```sh
make clean
```

## readthedocs.com Documentation

Extensive user-facing documentation is hosted by [ReadTheDocs](https://readthedocs.com). The system is configured to point to the `platform` repo. Documentation can be generated for a specific branch or tag by going to the [Versions](https://readthedocs.com/projects/wallaroo-platform/versions/) page and activating the version.

Release documentation can be published by activing the tag that corresponds to the release and changing the "Privacy Level" to `Public`.

## Deployment

To deploy the SDK to PyPI, `hatch publish` will upload both `whl` and `sdist` targets. Ideally, only the `whl` should need to be published, and excludes the documentation and unit testing around the SDK that end users might not need (and maybe even 'should not have') access to.

To test your configuration and see what the deployment looks like, you can locally set up a simple PyPI server.

To start the server on port 8080:
```sh
python -m pip install pypiserver passlib
python -m htpasswd -sc htpasswd.txt <username>
python -m pypiserver run -p 8080 -P htpasswd.txt ~/packages -v
```

To test publish:
```sh
hatch config set publish.index.repos.private.url 'http://localhost:8080'
hatch publish -r private
```

The packages will be found in `~/packages`. `unzip` can be used to extract `.whl`s, `tar` for the `tar.gz` sdist target.

To test that the created `whl` was successfully uploaded, you can install it with:
```sh
pip install --extra-index-url http://localhost:8080 wallaroo
```


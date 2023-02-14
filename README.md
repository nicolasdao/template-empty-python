# EMPTY PYTHON3 PROJECT

This (almost) empty project helps getting started with Python3. This project contains five dev dependencies:
- `easypipinstall` to maintain dependencies in a similar fashion to NPM.
- `black` to clean and format your code to follow the Python conventions.
- `flake8` to lint.
- `build` to optionally build your package.
- `twine` to optionally publish your package to PyPI.

`black` and `flake8` are executed sequentially via the `make t` command, while `build` is executed via the `make b` command and `twine` is executed via `make p` or `make bp` (build and then publish). To learn more about what those commands do and how to configure them, please refer to these sections: 
- [Install dependencies with `easypipinstall`](#install-dependencies-with-easypipinstall)
- [Linting and formatting](#linting-and-formatting)
- [Building and distributing your package](#building-and-distributing-your-package)

To install this template:

```
npx degit https://github.com/nicolasdao/template-empty-python.git YOUR_PROJECT_NAME
```

Then run, the following commands to initialize this project:

```
cd YOUR_PROJECT_NAME; \
python3 -m venv .venv; \
source .venv/bin/activate; \
pip install --upgrade pip; \
pip install -r requirements.txt; \
mv ./src/empty-python ./src/YOUR_PROJECT_NAME
```

If you're using Linux or Mac, all those commands can be combined as follow:

```
func() { \
	npx degit https://github.com/nicolasdao/template-empty-python.git $1; \
	cd $1; \
	python3 -m venv .venv; \
	source .venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt; \
	mv ./src/empty-python ./src/$1
}; func YOUR_PROJECT_NAME
```

# Table of contents

> * [Dev](#dev)
>	- [CLI commands](#cli-commands)
>	- [Install dependencies with `easypipinstall`](#install-dependencies-with-easypipinstall)
>	- [Linting and formatting](#linting-and-formatting)
>	- [Building and distributing your package](#building-and-distributing-your-package)

# Dev
## CLI commands

`make` commands:

| Command | Description |
|:--------|:------------|
| `make b` | Builds the package. |
| `make p` | Publish the package to https://pypi.org. |
| `make bp` | Builds the package and then publish it to https://pypi.org. |
| `make install` | Install the dependencies defined in the `requirements.txt`. This file contains all the dependencies (i.e., both prod and dev). |
| `make install-prod` | Install the dependencies defined in the `prod-requirements.txt`. This file only contains the production dependencies. |
| `make n` | Starts a Jupyter notebook for this project. |
| `make t` | Formats adnd then lints the project. |
| `easyi numpy` | Instals `numpy` and update `setup.cfg`, `prod-requirements.txt` and `requirements.txt`. |
| `easyi flake8 -D` | Instals `flake8` and update `setup.cfg` and `requirements.txt`. |
| `easyu numpy` | Uninstals `numpy` and update `setup.cfg`, `prod-requirements.txt` and `requirements.txt`. |

## Install dependencies with `easypipinstall`

`easypipinstall` adds two new CLI utilities: `easyi` (install) and `easyu` (uninstall).

Examples:
```
easyi numpy
```

This installs `numpy` (via `pip install`) then automatically updates the following files:
- `setup.cfg` (WARNING: this file must already exists):
	```
	[options]
	install_requires = 
		numpy
	```
- `requirements.txt` and `prod-requirements.txt`

```
easyi flake8 black -D
```

This installs `flake8` and `black` (via `pip install`) then automatically updates the following files:
- `setup.cfg` (WARNING: this file must already exists):
	```
	[options.extras_require]
	dev = 
		black
		flake8
	```
- `requirements.txt` only, as those dependencies are installed for development purposes only.

```
easyu flake8
```

This uninstalls `flake8` as well as all its dependencies. Those dependencies are uninstalled only if they are not used by other project dependencies. The `setup.cfg` and `requirements.txt` are automatically updated accordingly.

## Linting and formatting

```
make t
```

This command runs the following two python executables:

```
black ./
flake8 ./
```

- `black` formats all the `.py` files, while `flake8` lints them. 
- `black` is configured in the `pyproject.toml` file under the `[tool.black]` section.
- `flake8` is configured in the `setup.cfg` file under the `[flake8]` section.

## Building and distributing your package

To build your package, run:

```
make b
```

This command is a wrapper around `python3 -m build`.

To build and publish your package to https://pypi.org, run:

```
make p
```

This command is a wrapper around the following commands:

```
python3 -m build; \
twine upload dist/*
```



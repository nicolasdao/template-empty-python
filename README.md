# EMPTY PYTHON3 PROJECT

This (almost) empty project helps getting started with Python3. This project contains 2 dev dependencies:
- `black` to clean and format your code to follow the Python conventions.
- `flake8` to lint.

Those 2 tools are run sequentially via the `make t` command. To learn more this command does and how to configure it, please refer to the [Linting and formatting](#linting-and-formatting) section.

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
>	- [Linting and formatting](#linting-and-formatting)

# Dev
## CLI commands

`make` commands:

| Command | Description |
|:--------|:------------|
| `make install` | Install the dependencies defined in the `requirements.txt`. This file contains all the dependencies (i.e., both prod and dev). |
| `make install-prod` | Install the dependencies defined in the `prod-requirements.txt`. This file only contains the production dependencies. |
| `make i lib="numpy requests"` | Wrapper around `pip install` followed by `pip freeze`. It also updates the `setup.cfg`'s section `[options]install_requires`. `pip freeze` freezes the dependencies in both a `requirements.txt` (dev + prod) and `prod-requirements.txt` (prod). |
| `make i-dev lib="numpy requests"` | Wrapper around `pip install` followed by `pip freeze`. It also updates the `setup.cfg`'s section `[options.extras_require]dev`. `pip freeze` only freezes the dependencies in `requirements.txt` (dev + prod). |
| `make u lib="numpy requests"` | Wrapper around `pip uninstall` followed by `pip freeze`. Both `requirements.txt` (dev + prod) and `prod-requirements.txt` (prod) are updated. |
| `make n` | Starts a Jupyter notebook for this project |

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
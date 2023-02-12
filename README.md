# EMPTY PYTHON3 PROJECT

This empty project helps getting started with Python3

To install this template:

```
npx degit https://github.com/nicolasdao/template-empty-python.git YOUR_PROJECT_NAME
```

Then run, the following commands to initialize this project:

```
cd YOUR_PROJECT_NAME; \
python3 -m venv .venv; \
source .venv/bin/activate; \
pip install --upgrade pip
```

If you're using Linux or Mac, all those commands can be combined as follow:

```
func() { \
	npx degit https://github.com/nicolasdao/template-empty-python.git $1; \
	cd $1; \
	python3 -m venv .venv; \
	source .venv/bin/activate; \
	pip install --upgrade pip;
}; func YOUR_PROJECT_NAME
```

`make` commands:

| Command | Description |
|:--------|:------------|
| `make install` | Install the dependencies defined in the `requirements.txt`. This file contains all the dependencies (i.e., both prod and dev). |
| `make install-prod` | Install the dependencies defined in the `prod-requirements.txt`. This file only contains the production dependencies. |
| `make i lib="numpy requests"` | Wrapper around `pip install` followed by `pip freeze`. It also updates the `setup.cfg`'s section `[options]install_requires`. `pip freeze` freezes the dependencies in both a `requirements.txt` (dev + prod) and `prod-requirements.txt` (prod). |
| `make i-dev lib="numpy requests"` | Wrapper around `pip install` followed by `pip freeze`. It also updates the `setup.cfg`'s section `[options.extras_require]dev`. `pip freeze` only freezes the dependencies in `requirements.txt` (dev + prod). |
| `make u lib="numpy requests"` | Wrapper around `pip uninstall` followed by `pip freeze`. Both `requirements.txt` (dev + prod) and `prod-requirements.txt` (prod) are updated. |
| `make n` | Starts a Jupyter notebook for this project |


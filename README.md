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
source .venv/bin/activate;
```

If you're using Linux or Mac, all those commands can be combined as follow:

```
func() { \
	npx degit https://github.com/nicolasdao/template-empty-python.git $1; \
	cd $1; \
	python3 -m venv .venv; \
	source .venv/bin/activate;
}; func YOUR_PROJECT_NAME
```

`make` commands:

| Command | Description |
|:--------|:------------|
| `make install` | Install the dependencies defined in the `requirements.txt` |
| `make i lib="numpy requests"` | Wrapper around `pip install` followed by `pip freeze` |
| `make u lib="numpy requests"` | Wrapper around `pip uninstall` followed by `pip freeze` |
| `make n` | Starts a Jupyter notebook for this project |


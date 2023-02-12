install:
	pip install -r requirements.txt
install-prod:
	pip install -r prod-requirements.txt
i:
	python3 install.py $(lib)
i-dev:
	python3 install.py $(lib) -D
u:
	python3 install.py $(lib) -u
n:
	jupyter notebook
initenv:
	python3 -m venv .venv
act:
	source .venv/bin/activate
deact:
	deactivate
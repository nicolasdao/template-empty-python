install:
	pip install -r requirements.txt
i:
	pip install $(lib); \
	pip freeze > requirements.txt;
u:
	pip uninstall $(lib) -y; \
	pip freeze > requirements.txt;
n:
	jupyter notebook


build:
	python -m build

clean:
	rm -rf dist
upload:
	twine upload -u __token__ -p `cat token` --repository pypi dist/*

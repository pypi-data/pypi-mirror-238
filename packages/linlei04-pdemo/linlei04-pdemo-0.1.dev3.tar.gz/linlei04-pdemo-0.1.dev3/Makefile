test:
	tox

build:
	rm -rf dist/* && python -m build

release: build
	twine upload dist/*
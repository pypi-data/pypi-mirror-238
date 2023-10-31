pyproject.toml: pyproject.toml.template
	python - << EOF
	with open("pyproject.toml.template", encoding="utf-8") as f: \
	    template = f.read()
	
	with open("requirements.txt", encoding="utf-8") as f: \
	    requirements = f.read()
	
	requirements = requirements.strip().splitlines()
	
	template = template.format(dependencies=str(requirements))
	
	with open("pyproject.toml", "w", encoding="utf-8") as f: \
	    f.write(template)
	EOF

.PHONY: publish
.ONESHELL:

publish: pyproject.toml
	python -m pip install --upgrade build
	python -m build
	python -m pip install --upgrade twine
	python3 -m twine upload dist/*
	rm dist -r
	rm pyproject.toml

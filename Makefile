.PHONY: test typecheck

LIBRARY = ancv

test:
	pytest

typecheck:
	mypy -p ${LIBRARY}

requirements.txt:
	poetry export --with=dev --output=requirements.txt

depgraph.svg:
	@command -v dot > /dev/null || (echo "Please install graphviz for its 'dot' command." && exit 1)
	@pydeps --max-bacon=4 --cluster -T svg -o "$@" ${LIBRARY}

resume.py:
	datamodel-codegen \
		--url "https://raw.githubusercontent.com/jsonresume/resume-schema/master/schema.json" \
		--input-file-type jsonschema \
		--target-python-version 3.9 \
		--output "$@"

github.py:
	datamodel-codegen \
		--url "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions-next/api.github.com/dereferenced/api.github.com.deref.json" \
		--input-file-type openapi \
		--target-python-version 3.9 \
		--openapi-scopes paths \
		--output "$@"

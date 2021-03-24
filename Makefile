PY=python -m py_compile
.PHONY:
    test
test:
    python -m pytest

local_dev:
	python main.py
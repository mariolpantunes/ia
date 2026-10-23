# Explicit virtual environment at the repository root (./venv).
# The venv is never activated: every command calls venv/bin/python directly.
PYTHON ?= python3
VENV   := venv
VPY    := $(VENV)/bin/python

.PHONY: venv test clean

# Create ./venv and install requirements.txt into it.
# A stamp file tracks the install (venv/bin/python is a symlink, not touchable).
STAMP  := $(VENV)/.installed

venv: $(STAMP)
$(STAMP): requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VPY) -m pip install -q --upgrade pip
	$(VPY) -m pip install -q -r requirements.txt
	touch $(STAMP)

# Run every exercise test suite (each exercise folder is its own rootdir).
test: venv
	cd practice/ex01 && ../../$(VPY) -m pytest -q
	cd practice/ex02 && ../../$(VPY) -m pytest -q

# Remove the virtual environment and test caches.
clean:
	rm -rf $(VENV) .pytest_cache practice/*/.pytest_cache

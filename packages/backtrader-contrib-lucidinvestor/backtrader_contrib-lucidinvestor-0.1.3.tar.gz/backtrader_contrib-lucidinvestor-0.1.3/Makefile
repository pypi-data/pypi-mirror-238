.PHONY: create_venv clean

Makefile_DIR:=$(shell dirname "$(realpath $(firstword $(MAKEFILE_LIST)))")
SHELL:=/bin/bash
.ONESHELL:

create_venv: requirements.txt ## build venv for targeted python version: $make create_venv py_version=3.10 conf_dir=<path_to_netrc/pip.conf> e.g. py_version=3.10 netrc_dir=/my/path << NO TRAILING /
ifeq ($(py_version),)
	@echo "Missing argument. Usage: make create_venv py_version=<your_python_version> e.g. py_version=3.10"
	@exit 1
endif

	@test -d venv-$(py_version) || virtualenv -p python$(py_version) venv-$(py_version)
	. venv-$(py_version)/bin/activate; pip install --upgrade pip
	. venv-$(py_version)/bin/activate; pip install -Ur requirements.txt

clean: ## Tidy up local environment: $make clean venv_folder=venv-3.10
ifeq ($(venv_folder),)
	@echo "Missing argument. Usage: make clean venv_folder=<your_venv_folder_name> e.g. venv-3.10"
	@exit 1
endif

	@rm -rf __pycache__
	@rm -rf $(venv_folder)
	@find -iname "*.pyc" -delete

.PHONY: help
help:  ## Show help message
	@awk 'BEGIN {FS = ": .*##"; printf "\nUsage:\n  make <commands> <args>\033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+(\\:[$$()% 0-9a-zA-Z_-]+)*:.*?##/ { gsub(/\\:/,":", $$1); printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

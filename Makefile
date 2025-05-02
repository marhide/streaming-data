PROJECT_NAME = streaming-data
REGION = ${AWS_DEFAULT_REGION}
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PROFILE = default
PIP:=pip
VENV = venv
PYTHON = $(VENV)/bin/python3
QUEUE_NAME = ${SQS_QUEUE_NAME}

CHDIR_SHELL := $(SHELL)
define chdir
   $(eval _D=$(firstword $(1) $(@D)))
   $(info $(MAKE): cd $(_D)) $(eval SHELL = cd $(_D); $(CHDIR_SHELL))
endef


## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

test-requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./test_requirements.txt)

# Set Up

## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install safety
safety:
	$(call execute_in_env, $(PIP) install safety)

## Install black
black:
	$(call execute_in_env, $(PIP) install black)

## Install coverage
coverage:
	$(call execute_in_env, $(PIP) install coverage)

## Set up dev requirements (bandit, safety, black)
dev-setup: requirements bandit safety black coverage


setup: create-environment dev-setup 


## Run the security test (bandit + safety)
security-test:
	$(call execute_in_env, safety check -r ./requirements.txt)
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Run the black code check
run-black:
	$(call execute_in_env, black  ./src/*.py ./test/*.py)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -vvvrP)

## Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=src test/)

## Run all checks
run-checks: security-test run-black unit-test check-coverage

## create secrete tfvars file
tfvars:
	python -c 'from src.setup import create_secrets_tfvars_file; create_secrets_tfvars_file(queue_name="$(SQS_QUEUE_NAME)"+".fifo")'

## terraform init and apply new infrastructure
terraform-apply:
	$(call chdir,terraform)
	terraform init
	terraform apply -auto-approve

## delete secret tfvars file
delete-tfvars:
	python -c 'import os; os.remove("terraform/secrets.auto.tfvars")'

## create a new sqs queue
new-sqs-queue: 
	make tfvars
	make terraform-apply
	make delete-tfvars

## runs the application
run-app:
	export PYTHONPATH=$(WD)
	python src/main.py

delete-sqs-queue:
	$(call chdir,terraform)
	terraform destroy
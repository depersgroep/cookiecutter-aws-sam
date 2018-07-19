#################################################
# Please use mmake: https://github.com/tj/mmake #
#################################################

SHELL=bash

APP_NAME={{ cookiecutter.project_name.lower().replace(' ', '-') }}
SUFFIX={{ cookiecutter.cloudformation_resource_suffix.lower() }}

# In order to use moto in AWS CodeBuild the following to environment varibales need to be unset.
# https://forums.aws.amazon.com/thread.jspa?messageID=785174
unexport AWS_DEFAULT_REGION
unexport AWS_CONTAINER_CREDENTIALS_RELATIVE_URI

check_defined = \
		$(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

# Remove all python artifacts.
clean:
	$(info [*] Destroying environment....)
	rm -fr build/
	rm -fr dist/
	rm -f requirements.txt
	find . -name '*.orig' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	find . -name '__pycache__' -exec rm -fr {} +
.PHONY: clean

install: _install_packages _install_dev_packages
.PHONY: install

uninstall:
	$(info [*] Destroy entire virtualenv....)
	@pipenv --rm
.PHONY: uninstall

# Lint python code.
lint:
	$(info [*] Running python codestyle check....)
	@pipenv run pycodestyle --max-line-length 100 --ignore E402,W503,E704 --statistics src/
.PHONY: lint

# Run the unit tests.
test: lint
	$(info [*] Running pytest on tests/....)
	@AWS_XRAY_CONTEXT_MISSING=LOG_ERROR pipenv run python -m pytest -s -v tests/

# Run the unit tests.
# unittest:
# 	@echo "Running unittests..."
# 	AWS_XRAY_CONTEXT_MISSING=LOG_ERROR pytest -s -v .
# .PHONY: unittest

# Run test coverage.
coverage:
	$(info [*] Running test coverage on tests/....)
	@AWS_XRAY_CONTEXT_MISSING=LOG_ERROR pipenv run python -m pytest --cov=src \
		--cov-report term-missing --no-cov-on-fail --cov-fail-under 35 tests/ -v
.PHONY: coverage

build: _clone_service_to_build _install_deps
.PHONY: build

sam: _clone_service_to_build
	sam local start-api
.PHONY: sam

# Create the CloudFormation stack.
create-pipeline:
	@:$(call check_defined, OAUTH_TOKEN)
	@echo "Creating Cloudformation Stack ${APP_NAME}-pipeline."
	@aws cloudformation create-stack --stack-name ${APP_NAME}-${SUFFIX}-pipeline --template-body file://pipeline.yaml --parameters \
		ParameterKey=ApplicationName,ParameterValue=${APP_NAME} \
		ParameterKey=ArtifactBucket,ParameterValue=${APP_NAME}-${SUFFIX}-cfn \
		ParameterKey=GitHubOAuthToken,ParameterValue=${OAUTH_TOKEN} \
		ParameterKey=GitHubUser,ParameterValue={{ cookiecutter.github_user }} \
		ParameterKey=GitHubRepository,ParameterValue={{ cookiecutter.github_repo }} \
		ParameterKey=GitHubBranch,ParameterValue=master \
		--region eu-west-1 --capabilities CAPABILITY_NAMED_IAM --output text
	@echo "Waiting for Cloudformation stack to complete..."
	@aws cloudformation wait stack-create-complete --region eu-west-1 --stack-name ${APP_NAME}-${SUFFIX}-pipeline
	@echo "Deployment complete!"
.PHONY: create-pipeline

# Update the CloudFormation stack.
update-pipeline:
	@:$(call check_defined, OAUTH_TOKEN)
	@echo "updating Cloudformation Stack ${APP_NAME}-pipeline."
	@aws cloudformation update-stack --stack-name ${APP_NAME}-${SUFFIX}-pipeline --template-body file://pipeline.yaml --parameters \
		ParameterKey=ApplicationName,ParameterValue=${APP_NAME} \
		ParameterKey=ArtifactBucket,ParameterValue=${APP_NAME}-${SUFFIX}-cfn \
		ParameterKey=GitHubOAuthToken,ParameterValue=${OAUTH_TOKEN} \
		ParameterKey=GitHubUser,ParameterValue={{ cookiecutter.github_user }} \
		ParameterKey=GitHubRepository,ParameterValue={{ cookiecutter.github_repo }} \
		ParameterKey=GitHubBranch,ParameterValue=master \
		--region eu-west-1 --capabilities CAPABILITY_NAMED_IAM --output text
	@echo "Waiting for Cloudformation update stack to complete..."
	@aws cloudformation wait stack-update-complete --region eu-west-1 --stack-name ${APP_NAME}-${SUFFIX}-pipeline
	@echo "Stack update complete!"
.PHONY: update-pipeline

# Delete the CloudFormation stack.
delete-pipeline:
	@echo "Delete Cloudformation Stack ${APP_NAME}-pipeline."
	@aws cloudformation delete-stack --region eu-west-1 --stack-name ${APP_NAME}-pipeline
	@echo "Waiting for Cloudformation delete stack to complete..."
	@aws cloudformation wait stack-delete-complete --region eu-west-1 --stack-name ${APP_NAME}-pipeline
	@echo "Stack removed!"
.PHONY: delete-pipeline

###################
#     Helpers     #
###################

_install_packages:
	$(info [*] Install required packages....)
	@pipenv install

_install_dev_packages:
	$(info [*] Install required dev-packages....)
	@pipenv install -d

_install_deps:
	$(info [*] Installing service dependencies....)
	@test -d build/ || mkdir build/
	@pipenv lock -r > requirements.txt
	@pipenv run pip install \
		--isolated \
		--disable-pip-version-check \
		-Ur requirements.txt -t build/

_clone_service_to_build:
	$(info [*] Cloning '$(SERVICE)' to build directory....)
	@test -d build/ || mkdir build/
	cp -av src/* build/

# {{ cookiecutter.project_name }}

This project has build on the **GitOps** principles, so this Git repo act as your **Source of Truth**.....Elaborate on DR, IAC,....

## Technology stack

### AWS SAM

This project uses [AWS Serverless Application Model (AWS SAM)](https://github.com/awslabs/serverless-application-model).

> **See [Serverless Application Model (SAM) HOWTO Guide](https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md) for more details in how to get started.**

### CodePipeline, CodeBuild & CodeDeploy

A pipeline is included in this stack in order to deploy your code on AWS. The pipeline is consists out of tree major steps:

1. **Source**: listen for Github code changes
1. **Build**: 
	- clean the workspace
	- lint your code and run unit tests
	- package the code for deployment
1. **Deploy**: 
	- Create a CloudFormation changeset
	- Deploy your code through CloudFormation on AWS
	- Use CodeBuild to parse swagger.yaml and deploy the API docs

### Swagger
[Swagger](https://swagger.io/) is used both to configure AWS API Gateway and to document your API endpoints. The API docs will be exposed under `Prod/api-docs`.

## Getting Started

### Prerequisites

* AWS CLI already configured with at least PowerUser permission
* [Python 3 installed](https://www.python.org/downloads/)
* [Pipenv installed](https://github.com/pypa/pipenv)
    - `pip install --user pipenv`
* [Docker installed](https://www.docker.com/community-edition)
* [AWS SAM CLI installed](https://github.com/awslabs/aws-sam-cli) 
	- `pip install --user aws-sam-cli`

### Installation

1. Provided that you have the requirements above installed, proceed by installing the application dependencies and development dependencies:

	```bash
	pipenv install
	pipenv install -d
	```
1. [Add your code to Github](https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/)
	- In your GitHub create a new repository named `{{ cookiecutter.github_repo }}`
	- Push your code to Github:

		```bash
		git init
		git add .
		git commit -m "Initial commit"
		git remote add origin git@github.com:{{ cookiecutter.github_user }}/{{ cookiecutter.github_repo }}.git
		git push -u origin master
		```
1. Setup AWS CodePipeline: in order to install the pipeline a GitHub token is required. To create a token go to: https://github.com/settings/tokens and create a token with `repo` and `admin:repo_hook` permissions. Next run:

	```bash
	make create-pipeline OAUTH_TOKEN=your_github_token 
	```
	
You're all set. The newly created AWS CodePipeline will be triggered automatically and in minutes your application will deployed on AWS.

## Running the tests

`Pytest` is used to discover tests created under `tests` folder.
Here's how you can run tests our initial unit tests:

```bash
make test
```

## Local development

In order to run your code locally all dependencies need to be build and packaged on your local machine:
```
make build
```

Afterwards invoking your functions locally through a local API Gateway can be achieved by running:

```bash
make sam
```

If the previous command ran successfully you should now be able to hit the following local endpoint to invoke your functions:
- `http://localhost:3000/rest/one`
- `http://localhost:3000/rest/two`


## Usage


TODO: add all make targets

To install the CodePipeine:

```bash
make create-pipeline OAUTH_TOKEN=your_github_token 
```
To update the CodePipeline:

```bash
make update-pipeline OAUTH_TOKEN=your_github_token
```

To remove the pipeline run:

```bash
make delete-pipeline
```

## Appendix

### Makefile

It is important that the Makefile created only works on OSX/Linux but the tasks above can easily be turned into a Powershell or any scripting language you may want too.

Find all available targets: `make help`



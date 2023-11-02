# 2023_assignment1_recipes

## Group components:  
**Name**: Davide Borgonovo - **Student ID**: 905044 - **e-mail**: d.borgonovo5@campus.unimib.it  
**Name**: Fabio Villa - **Student ID**: 907506 - **e-mail**: f.villa93@campus.unimib.it

## Project description
This is a demo project created for the first assignment of Software Development Process course delivered at University of Milano - Bicocca. The aim of the project is to set up a CI/CD pipeline to automate the entire development process using the Gitlab CI/CD infrastructure.

The project consists in a python application that uses the Django Rest Framework (https://docs.djangoproject.com/en/4.1/).
The application is written ad hoc for the assignment to demonstrate the several steps of a CI/CD pipeline.
Django by default uses a sqlite database which is queried to be able to serve the data to the administration interface.
The application is a simple kitchen recipe book. It is a CRUD (Create, Read, Update and Delete), so it is possible to register the recipes and ingredients of each recipe.

- Repository: https://gitlab.com/sborbi/2023_assignment1_recipes
- Pages: https://2023-assignment1-recipes-sborbi-cea6a8b74f0ff78da30e8e2f0dc5622.gitlab.io/

## Used tools and package
- gitlab CI/CD: https://docs.gitlab.com/ee/ci/index.html
- pip: https://pypi.org/project/pip/
- virtualenv: https://pypi.org/project/virtualenv/
- prospector: https://pypi.org/project/prospector/
- bandit: https://pypi.org/project/bandit/
- coverage: https://pypi.org/project/coverage/
- setuptools: https://pypi.org/project/setuptools/
- twine: https://pypi.org/project/twine/
- mkdocs: https://www.mkdocs.org/user-guide/

## Preliminary notes
- In the Prospector analysis warnings that are not relevant to the correct functioning of the program but which concern configuration elements have been silenced.
- Unit and Integration tests were not written with the aim of verifying the functioning of all parts of the code, but to demonstrate the correct functioning of the part of the pipeline that concerns their execution.
- What is written in the project documentation is correct, however it is incomplete. This because the objective was not to make it usable for an end user but to demonstrate the correct functioning of the pipeline stage.

## Pipeline
GitLab CI/CD has been used to implement the pipelines. It is fully integrated with GitLab and can be used in any repository for free.
GitLab CI/CD is configured by a file called .gitlab-ci.yml placed at the repository's root. The .gitlab-ci.yml file defines, using a YAML DSL (Domain Specific Language), the structure and order of the pipelines. It also determines what to execute and what decisions to take when specific conditions are encountered.
The pipeline was created keeping in mind the DAG (Directed Acyclic Graph) structure to maximize efficiency. The pipeline is made up of the following stages:

- **build**: this stage lays the foundations for subsequent stages. Packages, requirements and dependencies necessary for the correct execution of the pipeline are installed in this part of the run. The Python virtual environment is also created.
- **verify**: in this stage the static analysis of the code takes place with two different programs; Prospector to analyse the Python code and output information about errors, potential problems, convention violations and complexity and bandit to find common security issues in the Python code.
- **unit-test**: within this stage single functions executions testing takes place. The Coverage package is used to check the percentage of code executed by the tests.
- **integration-test**: within this stage multiple software modules are combined and then tested as a group. The Coverage package is used to check the percentage of code executed by the tests.
- **bumpversion**: in this stage the version of the Python application is updated in order to avoid version conflict when pushing the package to PyPI.
- **package**: in this stage the Python application is packed and become ready for the distribution using Python Setuptools.
- **release**: within this stage Twine is used to upload the Python package created in the previous stage to PyPI.
- **docs**: in this stage a Static Site Generator (SSG) named MkDocs is used to create a static documentation made of HTML pages that will be uploaded to GilabPages.

## License
This project is licensed under the AGPLv3. See the LICENSE file for details.
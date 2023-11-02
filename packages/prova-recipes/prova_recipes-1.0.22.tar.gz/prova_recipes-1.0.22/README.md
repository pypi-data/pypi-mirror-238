# First assignment

## Group components:  
**Name**: Davide Borgonovo - **Student ID**: 905044 - **e-mail**: d.borgonovo5@campus.unimib.it  
**Name**: Fabio Villa - **Student ID**: 907506 - **e-mail**: f.villa93@campus.unimib.it

## Project description

The project consists in a python application that uses the Django Rest Framework.

The application is written ad hoc for the assignment.

Django by default uses a sqlite database which is queried to be able to serve the data to the administration interface.

## Preliminary notes
- In the Prospector analysis warnings that are not relevant to the correct functioning of the program but which concern configuration elements have been silenced.
- Unit and Integration tests were not written with the aim of verifying the functioning of all parts of the code, but to demonstrate the correct functioning of the part of the pipeline that concerns their execution.
- What is written in the project documentation is correct, however it is incomplete. This because the objective was not to make it usable for an end user but to demonstrate the correct functioning of the pipeline stage.

## Pipeline
The pipeline was created keeping in mind the DAG (Directed Acyclic Graph) structure to maximize efficiency. The pipeline is made up of the following stages:

- **build**: this stage lays the foundations for subsequent stages. Packages, requirements and dependencies necessary for the correct execution of the pipeline are installed in this part of the run. The Python virtual environment is also created.
- **verify**: in this stage the static analysis of the code takes place with two different programs; Prospector to analyse the Python code and output information about errors, potential problems, convention violations and complexity and bandit to find common security issues in the Python code.
- **unit-test**: within this stage single functions executions testing takes place. The Coverage package is used to check the percentage of code executed by the tests.
- **integration-test**: within this stage multiple software modules are combined and then tested as a group. The Coverage package is used to check the percentage of code executed by the tests.
- **package**: in this stage the Python application is packed and become ready for the distribution using Python Setuptools.
- **release**: within this stage Twine is used to upload the Python package created in the previous stage to PyPI.
- **docs**: in this stage a Static Site Generator (SSG) named MkDocs is used to create a static documentation made of HTML pages that will be uploaded to GilabPages.
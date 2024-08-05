![https://github.com/dpai/flask_grocery_api/actions?query=workflow%3A%22build%22](https://github.com/dpai/flask_grocery_api/actions/workflows/main.yml/badge.svg)
# API Development with Flask - Origins
My goal with this project was to learn web app development. Instead of taking a coursework on the relevant tools, I implemented a personal 
project using Flask. All material that I needed was found online. 

I have no background in web apps so I just searched online videos, articles etc. to gain knowledge and applied to the project.

Below I will list all my references and also mention why I read those articles. 

Secondary goals: 
- Learn how to deploy the project online for use over the web. 
- Work with continuous integration, and learn how to use Github actions.
- REST API design
- Practice TDD


# Building the app
Building the app is straightforward. There should be Python installed on the system and the pipenv package for Python.
Note: Sometimes on Windows the pipenv executable is not found because it was not included in the PATH. This should be added manually.

Checkout the source. Open a `pipenv shell` and do a `pipenv install`. This will install all the needed dependencies.
For running the tests development packaged need to be installed. Add the `--dev` option to the install command above to install the development packages

# Running the test
Open a pipenv shell
First a temporary database needs to be generated. 
For the test environment build an sqlite database by running the following command under the tests folder - `python -m loadtestdatabase`
Then issue the command `pytest` to execute the tests.

# Deploying the app
TODO


# Translator Testing Model

This is a preliminary schema repo for defining test cases in Translator that can be reused in different test suites.  e.g. a test case in plain language might be something like _"what drugs may treat MS? I expect fingolimod to return in the top 10 results in less than 5 mins."_  

Capturing these details in metadata that is parsable and usable by test runners is the objective of this schema.  We also want to harmonize our language and nomenclature for the metadata we need (which of these data are required and which are optional for each kind of test case, etc.) so that downstream testing code can utilize a common framework for understanding.

## Website

[https://TranslatorSRI.github.io/translator_testing_model](https://TranslatorSRI.github.io/TranslatorTestingModel)

## Repository Structure

* [examples/](examples/) - example data
* [project/](project/) - project files (do not edit these)
* [src/](src/translator_testing_model/README.md) - source files (edit these)
  * [translator testing model specification](src/translator_testing_model/README.md)
    * [schema](src/translator_testing_model/schema/translator_testing_model.yaml) -- LinkML schema
      (edit this)
    * [datamodel](src/translator_testing_model/datamodel/README.md) -- generated
      Python datamodels
      * [Pydantic V1](src/translator_testing_model/datamodel/pydanticmodel.py)
      * [Pydantic V2](src/translator_testing_model/datamodel/pydanticmodel_v2.py)
      * [Python Dataclasses](src/translator_testing_model/datamodel/translator_testing_model.py)
* [tests/](tests/test_data.py) - Python tests

## Developer Documentation

<details>
The project uses [Poetry](https://python-poetry.org/) to manage its dependencies. Install Poetry then:

* `poetry shell`: start up a poetry shell virtual environment
* `poetry install`: to install required dependencies

Then use the `make` command to generate project artifacts:

* `make gen-project`: regenerates core project artifacts
* `make all`: make everything
* `make deploy`: deploys site

</details>

## Credits

This project was made with
[linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter).

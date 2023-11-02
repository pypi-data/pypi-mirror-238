# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nmdc_schema']

package_data = \
{'': ['*']}

install_requires = \
['click-log>=0.4.0,<0.5.0',
 'linkml-runtime>=1.5.0,<2.0.0',
 'linkml>=1.5.0,<2.0.0']

entry_points = \
{'console_scripts': ['anyuri-strings-to-iris = '
                     'nmdc_schema.anyuri_strings_to_iris:expand_curies',
                     'build-datafile-from-api-requests = '
                     'nmdc_schema.build_datafile_from_api_requests:main',
                     'class-sparql = nmdc_schema.class_sparql:main',
                     'fetch-nmdc-schema = '
                     'nmdc_schema.nmdc_data:get_nmdc_jsonschema',
                     'generate-import-slots-regardless = '
                     'nmdc_schema.generate_import_slots_regardless:main',
                     'get-mixs-slots-matching-slot-list = '
                     'nmdc_schema.get_mixs_slots_matching_slot_list:main',
                     'get-mixs-slots-used-in-schema = '
                     'nmdc_schema.get_mixs_slots_used_in_schema:main',
                     'get-slots-from-class = '
                     'nmdc_schema.get_slots_from_class:main',
                     'migration-recursion = '
                     'nmdc_schema.migration_recursion:main',
                     'nmdc-data = nmdc_schema.nmdc_data:cli',
                     'nmdc-version = nmdc_schema.nmdc_version:cli',
                     'pure-export = nmdc_schema.mongo_dump_api_emph:cli',
                     'test-more-tolerant-schema = '
                     'nmdc_schema.test_more_tolerant_schema:do_test']}

setup_kwargs = {
    'name': 'nmdc-schema',
    'version': '9.0.2',
    'description': 'Schema resources for the National Microbiome Data Collaborative (NMDC)',
    'long_description': '<p align="center">\n    <img src="images/nmdc_logo_long.jpeg" width="100" height="40"/>\n</p>\n\n# National Microbiome Data Collaborative Schema\n\n[![PyPI - License](https://img.shields.io/pypi/l/nmdc-schema)](https://github.com/microbiomedata/nmdc-schema/blob/main/LICENSE)\n[![PyPI version](https://badge.fury.io/py/nmdc-schema.svg)](https://badge.fury.io/py/nmdc-schema)\n\nThe NMDC is a multi-organizational effort to integrate microbiome data across diverse areas in medicine, agriculture,\nbioenergy, and the environment. This integrated platform facilitates comprehensive discovery of and access to\nmultidisciplinary microbiome data in order to unlock new possibilities with microbiome data science.\n\nThis repository mainly defines a [LinkML](https://github.com/linkml/linkml) schema for managing metadata from\nthe [National Microbiome Data Collaborative (NMDC)](https://microbiomedata.org/).\n\n## Repository Contents Overview\n\nSome products that are maintained, and tasks orchestrated within this repository are:\n\n- Maintenance of LinkML YAML that specifies the NMDC Schema\n    - [src/schema/nmdc.yaml](src/schema/nmdc.yaml)\n    - and various other YAML schemas imported by it,\n      like [prov.yaml](src/schema/prov.yaml), [annotation.yaml](src/schema/annotation.yaml), etc. all which you can find\n      in the [src/schema](src/schema/) folder\n- Makefile targets for converting the schema from it\'s native LinkML YAML format to other artifact\n  like [JSON Schema](project/jsonschema/nmdc.schema.json)\n- Build, deployment and distribution of the schema as a PyPI package\n- Automatic publishing of refreshed documentation upon change to the schema,\n  accessible [here](https://microbiomedata.github.io/nmdc-schema/)\n\n## Background\n\nThe NMDC [Introduction to metadata and ontologies](https://microbiomedata.org/introduction-to-metadata-and-ontologies/)\nprimer provides some the context for this project.\n\n## Maintaining the Schema\n\n**New system requirement: [Mike Farah\'s GO-based yq](https://github.com/mikefarah/yq)**\n\nSome optional components use the Java-based [ROBOT](http://robot.obolibrary.org/) or Jena arq.\nJena riot is also a part of the MongoDB dumping, repairing and validation workflow, if the user wishes\nto generate and validate RDF/TTL.\n\nSee [MAINTAINERS.md](MAINTAINERS.md) for instructions on maintaining and updating the schema.\n\n## Makefiles\n\nMakefiles are text files people can use to tell [`make`](https://www.gnu.org/software/make/manual/make.html#Introduction) (a computer program) how it can _make_ things (or—in general—_do_ things). In the world of Makefiles, those _things_ are called _targets_.\n\nThis repo contains 2 Makefiles:\n- `Makefile`, based on the generic Makefile from the [LinkML cookiecutter](https://github.com/linkml/linkml-project-cookiecutter)\n- `project.Makefile`, which contains _targets_ that are specific to this project\n\nHere\'s an example of using `make` in this repo:\n\n```shell\n# Deletes all files in `examples/output`.\nmake examples-clean\n```\n> The `examples-clean` _target_ is defined in the `project.Makefile`. In this repo, the `Makefile` `include`s the `project.Makefile`. As a result, `make` has access to the _targets_ defined in both files.\n\n## Data downloads\n\nThe NMDC\'s metadata about biosamples, studies, bioinformatics workflows, etc. can be obtained from our nmdc-runtime API.\nTry entering "biosample_set" or "study_set" into the `collection_name` box\nat https://api.microbiomedata.org/docs#/metadata/list_from_collection_nmdcschema__collection_name__get\n\nOr use the API programmatically! Note that some collections are large, so the responses are paged.\n\nYou can learn about the other available collections at https://microbiomedata.github.io/nmdc-schema/Database/\n',
    'author': 'Bill Duncan',
    'author_email': 'wdduncan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://microbiomedata.github.io/nmdc-schema/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

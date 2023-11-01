# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lookml_zenml']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0,<9.0',
 'lkml>=1.3.1,<2.0.0',
 'ruamel.yaml>=0.17.32,<0.18.0']

entry_points = \
{'console_scripts': ['lookml_zenml = lookml_zenml:cli_group']}

setup_kwargs = {
    'name': 'lookml-zenml',
    'version': '0.1.0',
    'description': '',
    'long_description': "# LookML to ZenML\n\nLibrary for translating LookML configuration into ZenML for easy onboarding to Zenlytic.\n\nTo install the package run \n\n```\n$ pip install lookml-zenml\n```\n\nTo convert a entire project run the following command from your command line interface after installing the package. Note: make sure you specify your LookML project as the first argument, and you create a directory for the ZenML output.\n\n```\n$ lookml_zenml convert ./my_lookml_project --out-directory ./my_new_zenml_project\n```\n\nThis is the standard way to convert a LookML project. This will convert dashboards, views, and models into the ZenML equivalent.\n\n\n---\n\n\nYou can also use this library to convert objects on a one-off basis. This is not as robust as converting the whole project due to loss of information for the dashboards and logic about joins in found in the explores that we add to the views. \n\n\nTo convert a model run the following command. Note: if you specify `--out-directory` the library will write a yml file to that directory, otherwise it will return the converted code to stdout.\n\n```\n$ lookml_zenml model ./my_lookml_project/my_model.model.lkml --out-directory ./my_new_dir\n```\n\n\nTo convert a view run the following command. Note: if you specify `--out-directory` the library will write a yml file to that directory, otherwise it will return the converted code to stdout.\n\n```\n$ lookml_zenml view ./my_lookml_project/my_view.view.lkml --out-directory ./my_new_dir\n```\n\nTo convert a dashboard run this command. Note: for dashboards the directory is required. If you do not have the directory of lookml files, you can point to an empty directory and the conversion will run, but will put all metrics on a dashboard into the `slice_by` heading because it will be unable to determine the field type of the fields. You'll then have to correct those manually.\n\n```\n$ lookml_zenml dashboard ./my_lookml_project/my_dashboard.dashboard.lookml --directory ./my_lookml_project\n```\n",
    'author': 'Paul Blankley',
    'author_email': 'paul@zenlytic.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)

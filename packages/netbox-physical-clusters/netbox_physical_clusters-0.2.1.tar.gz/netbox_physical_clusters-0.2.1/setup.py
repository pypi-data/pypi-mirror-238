# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_physical_clusters',
 'netbox_physical_clusters.api',
 'netbox_physical_clusters.core',
 'netbox_physical_clusters.core.models',
 'netbox_physical_clusters.forms',
 'netbox_physical_clusters.graphql',
 'netbox_physical_clusters.migrations',
 'netbox_physical_clusters.models',
 'netbox_physical_clusters.tests']

package_data = \
{'': ['*'],
 'netbox_physical_clusters': ['templates/netbox_physical_clusters/*',
                              'templates/netbox_physical_clusters/physical_cluster/*']}

setup_kwargs = {
    'name': 'netbox-physical-clusters',
    'version': '0.2.1',
    'description': 'A netbox plugin for managing multiple physical cluster types',
    'long_description': '\nA netbox plugin for managing multiple cluster types by site\n\n<a href="https://github.com/sapcc/netbox-physical-clusters/forks"><img src="https://img.shields.io/github/forks/sapcc/netbox-physical-clusters" alt="Forks Badge"/></a>\n<a href="https://github.com/sapcc/netbox-physical-clusters/pulls"><img src="https://img.shields.io/github/issues-pr/sapcc/netbox-physical-clusters" alt="Pull Requests Badge"/></a>\n<a href="https://github.com/sapcc/netbox-physical-clusters/issues"><img src="https://img.shields.io/github/issues/sapcc/netbox-physical-clusters" alt="Issues Badge"/></a>\n<a href="https://github.com/sapcc/netbox-physical-clusters/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/sapcc/netbox-physical-clusters?color=2b9348"></a>\n<a href="https://github.com/sapcc/netbox-physical-clusters/blob/master/LICENSE"><img src="https://img.shields.io/github/license/sapcc/netbox-physical-clusters?color=2b9348" alt="License Badge"/></a>\n\n## Installing the Plugin in Netbox\n\n### Prerequisites\n\n- The plugin is compatible with Netbox 3.5.0 and higher.\n- Databases supported: PostgreSQL\n- Python supported : Python3 >= 3.10\n\n### Install Guide\n\n> NOTE: Plugins can be installed manually or using Python\'s `pip`. See the [netbox documentation](https://docs.netbox.dev/en/stable/plugins/) for more details. The pip package name for this plugin is [`netbox-physical-clusters`](https://pypi.org/project/netbox-physical-clusters/).\n\nThe plugin is available as a Python package via PyPI and can be installed with `pip`:\n\n```shell\npip install netbox-physical-clusters\n```\n\nTo ensure the device cluster plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Netbox root directory (alongside `requirements.txt`) and list the `netbox_physical_clusters` package:\n\n```shell\necho netbox-physical-clusters >> local_requirements.txt\n```\n\nOnce installed, the plugin needs to be enabled in your Netbox configuration. The following block of code below shows the additional configuration required to be added to your `$NETBOX_ROOT/netbox/configuration.py` file:\n\n- Append `"netbox_physical_clusters"` to the `PLUGINS` list.\n- Append the `"netbox_physical_clusters"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.\n\n```python\nPLUGINS = [\n    "netbox_physical_clusters",\n]\n```\n\n## Post Install Steps\n\nOnce the Netbox configuration is updated, run the post install steps from the _Netbox Home_ to run migrations and clear any cache:\n\n```shell\n# Apply any database migrations\npython3 netbox/manage.py migrate\n# Trace any missing cable paths (not typically needed)\npython3 netbox/manage.py trace_paths --no-input\n# Collect static files\npython3 netbox/manage.py collectstatic --no-input\n# Delete any stale content types\npython3 netbox/manage.py remove_stale_contenttypes --no-input\n# Rebuild the search cache (lazily)\npython3 netbox/manage.py reindex --lazy\n# Delete any expired user sessions\npython3 netbox/manage.py clearsessions\n# Clear the cache\npython3 netbox/manage.py clearcache\n```\n\nThen restart the Netbox services:\n\n```shell\nsudo systemctl restart netbox netbox-rq\n```\n',
    'author': 'Pat McLean',
    'author_email': 'patrick.mclean@sap.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sapcc/netbox-physical-clusters',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['fastmeteo']

package_data = \
{'': ['*']}

install_requires = \
['click',
 'dask',
 'fastapi',
 'fsspec',
 'gcsfs',
 'numpy',
 'pandas',
 'requests',
 'uvicorn',
 'xarray',
 'zarr']

entry_points = \
{'console_scripts': ['fastmeteo-serve = fastmeteo.server:main']}

setup_kwargs = {
    'name': 'fastmeteo',
    'version': '0.1',
    'description': 'Fast interpolation for ERA5 data with Zarr',
    'long_description': '# Fast Meteo\n\nA super-fast Python package to obtain meteorological parameters for your flight trajectories.\n\n\n## Install\n\n\n\n## Usage\nOnce the library is installed, you ca get the weather information for a given flight or position with the following code, which the basic information of time, latitude, longitude, and altitude.\n\n\n```\nimport pandas as pd\nfrom fastmeteo import Grid\n\n# define the location for local store\nmmg = Grid(local_store="/tmp/era5-zarr")\n\n\nflight = pd.DataFrame(\n    {\n        "timestamp": ["2021-10-12T01:10:00", "2021-10-12T01:20:00"],\n        "latitude": [40.3, 42.5],\n        "longitude": [4.2, 6.6],\n        "altitude": [25_000, 30_000],\n    }\n)\n\n# obtain weather information\nflight_new = mmg.interpolate(flight)\n```\n\nWhen running the tool in a server-client mode. The following script can be used to start a FastAPI service on the server, which handles the flight date request, obtaining Google ARCO data if the partition is not on the server, perform the interpolation of weather data, and return the final data to the client.\n\n```\nfastmeteo-serve --local-store /tmp/era5-zarr\n```\n\nAt the client side, the following code can be used to submit and get the process flight with meteorology data.\n\n```\nfrom fastmeteo import Client\n\nclient = Client()\n\n# send the flight and receive the new DataFrame\nflight_new = client.submit_flight(flight)\n```\n',
    'author': 'Junzi Sun',
    'author_email': 'j.sun-1@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)

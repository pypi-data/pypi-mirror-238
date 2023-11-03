# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geohexgrid']

package_data = \
{'': ['*']}

install_requires = \
['Rtree>=1.0.0', 'geopandas>=0.11.1']

setup_kwargs = {
    'name': 'geohexgrid',
    'version': '1.1.0',
    'description': "A Python library for making geographic hexagon grids like QGIS's `create grid` function",
    'long_description': 'Geohexgrid\n**********\nA Python 3.9+ library for making geographic hexagon grids like QGIS\'s `create grid function <https://docs.qgis.org/3.22/en/docs/user_manual/processing_algs/qgis/vectorcreation.html?highlight=create%20grid#create-grid>`_.\nNot designed for making `discrete global grid systems <https://en.wikipedia.org/wiki/Discrete_global_grid>`_ like Uber\'s H3.\n\nHere\'s an example of its main use, namely, minimally covering a GeoDataFrame of features with a flat-top hexagon grid of given resolution.\n\n.. code-block:: python\n\n  import geopandas as gpd\n  import geohexgrid as ghg\n\n  # Load New Zealand territorial authorities projected in EPSG 2193 (NZTM)\n  shapes = gpd.read_file(DATA_DIR / "nz_tas.gpkg")\n\n  # Cover it minimally with hexagons of circumradius 10 kilometres\n  grid = ghg.make_grid(shapes, 10_000, intersect=True)\n\n  # Plot\n  base = shapes.plot(color=\'red\', figsize=(20, 20), aspect="equal")\n  grid.plot(ax=base, color=\'white\', edgecolor="blue", alpha=0.5)\n\n\n.. image:: geohexgrid.png\n  :width: 400\n  :alt: hexagon grid of 10,000-metre circumradius covering New Zealand\n\n\nContributors\n============\n- Alex Raichev (2014-09), maintainer\n\n\nInstallation\n============\nInstall from PyPI, e.g. via ``poetry add geohexgrid``.\n\n\nExamples\n=========\nSee the Jupyter notebook at ``notebooks/examples.ipynb``.\n\n\nNotes\n======\n- This project\'s development status is Alpha.\n  Alex uses this project for work and changes it breakingly when it suits his needs.\n- This project uses semantic versioning.\n- Thanks to `MRCagney <https://mrcagney.com>`_ for periodically funding this project.\n- Red Blog Games has a `great write up of non-geographic hexagon grids <https://www.redblobgames.com/grids/hexagons>`_.\n- Alex wanted to chose a shorter name for this package, such as \'hexgrid\', \'geohex\', or \'hexcover\', but those were already taken or too close to taken on PyPI.\n\n\nChanges\n=======\n\n1.1.0, 2023-10-27\n-----------------\n- Added the ``clip`` option to the function ``grid_from_gdf``.\n- Updated dependencies.\n- Re-ordered functions.\n- Changed the cell ID separotor to a comma.\n\n1.0.0, 2022-08-15\n-----------------\n- First release.',
    'author': 'Alex Raichev',
    'author_email': 'araichev@mrcagney.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/mrcagney/geohexgrid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)

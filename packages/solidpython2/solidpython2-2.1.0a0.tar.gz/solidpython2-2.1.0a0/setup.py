# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solid2',
 'solid2.core',
 'solid2.core.builtins',
 'solid2.core.object_base',
 'solid2.examples',
 'solid2.examples..ipynb_checkpoints',
 'solid2.extensions',
 'solid2.extensions.bosl2',
 'solid2.extensions.bosl2.BOSL2.scripts',
 'solid2.extensions.greedy_scad_interface',
 'solid2.libs',
 'solid2.libs.py_scadparser']

package_data = \
{'': ['*'],
 'solid2.examples': ['11-font/*'],
 'solid2.extensions.bosl2': ['BOSL2/*',
                             'BOSL2/.github/*',
                             'BOSL2/.github/ISSUE_TEMPLATE/*',
                             'BOSL2/.github/workflows/*',
                             'BOSL2/examples/*',
                             'BOSL2/images/*',
                             'BOSL2/tests/*',
                             'BOSL2/tutorials/*']}

install_requires = \
['ply>=3.11,<4.0', 'setuptools>=65.6.3']

setup_kwargs = {
    'name': 'solidpython2',
    'version': '2.1.0a0',
    'description': 'Python interface to the OpenSCAD declarative geometry language',
    'long_description': "SolidPython\n===========\n   \nOpenSCAD for Python\n-------------------\n\nSolidPython is a generalization of Phillip Tiefenbacher's openscad\nmodule, found on `Thingiverse <http://www.thingiverse.com/thing:1481>`__. It\ngenerates valid OpenSCAD code from Python code with minimal overhead. Here's a\nsimple example:\n\nThis Python code:\n\n.. code:: python\n\n    from solid2 import *\n    d = cube(5) + sphere(5).right(5) - cylinder(r=2, h=6)\n\nGenerates this OpenSCAD code:\n\n.. code::\n\n    difference(){\n        union(){\n            cube(5);\n            translate( [5, 0,0]){\n                sphere(5);\n            }\n        }\n        cylinder(r=2, h=6);\n    }\n\nAs can be clearly seen, the SolidPython code is a lot shorter (and I think a lot better readable and maintainable) than the OpenSCAD code it compiles to.\n\nAdvantages\n----------\n\nIn contrast to OpenSCAD -- which is a constrained domain specific language --\nPython is a full blown modern programming language and as such supports\npretty much all modern programming features. Furthermore a huge number of\nlibraries is available.\n\nSolidPython lets you use all these fancy python features to generate your\nconstructive solid geometry models.\n\nOn the one hand it makes the generation of your models a lot easier, because\nyou don't need to learn another domain specific language and you can use all\nthe programming technique you're already familiar with. On the other hand it\ngives you a lot more power, because you can use all the comprehensive python\nlibraries to generate your models.\n\n\nGetting Started\n---------------\n\nThe `wiki <https://github.com/jeff-dh/SolidPython/wiki>`__ is the place to look for docs and tutorials. Furthermore the `examples <https://github.com/jeff-dh/SolidPython/tree/master-2.0.0-beta-dev/solid2/examples>`__ might be interesting to you too.\n\nContact\n=======\n\nEnjoy!\n\nIf you have any questions or bug reports please report them to the SolidPython\n`GitHub page <https://github.com/jeff-dh/SolidPython>`__!\n\nCheers!\n\nLicense\n=======\n\nThis library is free software; you can redistribute it and/or modify it\nunder the terms of the GNU Lesser General Public License as published by\nthe Free Software Foundation; either version 2.1 of the License, or (at\nyour option) any later version.\n\nThis library is distributed in the hope that it will be useful, but\nWITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser\nGeneral Public License for more details.\n\n`Full text of the\nlicense <http://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt>`__.\n\nSome class docstrings are derived from the `OpenSCAD User Manual\n<https://en.wikibooks.org/wiki/OpenSCAD_User_Manual>`__, so \nare available under the `Creative Commons Attribution-ShareAlike License\n<https://creativecommons.org/licenses/by-sa/3.0/>`__. \n\n",
    'author': 'jeff',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jeff-dh/SolidPython',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chipscopy',
 'chipscopy._cli',
 'chipscopy.api',
 'chipscopy.api._detail',
 'chipscopy.api.ddr',
 'chipscopy.api.device',
 'chipscopy.api.hbm',
 'chipscopy.api.ibert',
 'chipscopy.api.ibert.eye_scan',
 'chipscopy.api.ibert.link',
 'chipscopy.api.ibert.yk_scan',
 'chipscopy.api.ila',
 'chipscopy.api.ila.tsm',
 'chipscopy.api.noc',
 'chipscopy.api.noc.graphing',
 'chipscopy.client',
 'chipscopy.client.node',
 'chipscopy.client.util',
 'chipscopy.dm',
 'chipscopy.dm.harden',
 'chipscopy.dm.harden.noc_perfmon',
 'chipscopy.examples.ddr',
 'chipscopy.examples.ibert.versal_gtm',
 'chipscopy.examples.ibert.versal_gty',
 'chipscopy.examples.ibert.versal_gtyp',
 'chipscopy.examples.ila_and_vio',
 'chipscopy.examples.jtag',
 'chipscopy.examples.memory',
 'chipscopy.examples.noc_perfmon',
 'chipscopy.examples.program',
 'chipscopy.examples.sysmon',
 'chipscopy.proxies',
 'chipscopy.shared',
 'chipscopy.tcf',
 'chipscopy.tcf.channel',
 'chipscopy.tcf.native',
 'chipscopy.tcf.native.services',
 'chipscopy.tcf.native.services.local',
 'chipscopy.tcf.native.services.remote',
 'chipscopy.tcf.services',
 'chipscopy.tcf.services.local',
 'chipscopy.tcf.services.remote',
 'chipscopy.tcf.tests',
 'chipscopy.tcf.util',
 'chipscopy.utils',
 'chipscopy.utils.logger',
 'chipscopy.utils.noc_utils',
 'chipscopy.xvc']

package_data = \
{'': ['*'],
 'chipscopy': ['examples/designs/vck190/production/chipscopy_ced/*',
               'examples/designs/vhk158/production/chipscopy_ced/*',
               'examples/designs/vmk180/production/chipscopy_ced/*',
               'examples/designs/vpk120/production/chipscopy_ced/*',
               'examples/designs/vpk120/production/pcie_pio_ced/*',
               'examples/img/*'],
 'chipscopy.examples.ila_and_vio': ['img/*']}

install_requires = \
['Click>=8.1,<9.0',
 'antlr4-python3-runtime==4.10',
 'importlib_metadata>=6.8,<7.0',
 'loguru>=0.7,<0.8',
 'more-itertools>=10.1,<11.0',
 'rich>=13.5,<14.0',
 'typing_extensions>=4.7,<5.0']

extras_require = \
{'core-addons': ['kaleido==0.2.1',
                 'plotly>=5.16,<6.0',
                 'pandas>=1.5,<2.0',
                 'matplotlib>=3.7,<4.0',
                 'PyQt5>=5.15,<6.0'],
 'jupyter': ['notebook>=7.0,<8.0', 'ipywidgets>=8.1,<9.0'],
 'pytcf': ['pytcf>=0.0.7,<0.0.8']}

entry_points = \
{'console_scripts': ['chipscopy-get-examples = '
                     'chipscopy._cli.example_delivery:main',
                     'csutil = chipscopy._cli._chipscopy:main']}

setup_kwargs = {
    'name': 'chipscopy',
    'version': '2023.2.1698639225',
    'description': 'Open-source project from Xilinx® that enables high-level control of Versal debug IP running in hardware',
    'long_description': '# 🐍 ChipScoPy README\n\n[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n![](https://raw.githubusercontent.com/Xilinx/chipscopy/master/docs/images/chipscopy_logo_head_right_transparent_background.png)\n\nChipScoPy is an open-source project from Xilinx® that enables high-level control of Versal debug IP running in hardware.\nUsing a simple Python API, developers can control and communicate with ChipScope® debug IP such as the Integrated Logic\nAnalyzer (ILA), Virtual IO (VIO), device memory access, and more.\n\nChipScoPy communicates with Versal devices. It does not work with older devices such as Ultrascale+ and 7-Series devices.\n\n-------------------------------------------------------------------------------\n\n![](https://raw.githubusercontent.com/Xilinx/chipscopy/master/docs/images/chipscopy_overview.png)\n\n-------------------------------------------------------------------------------\n\n[ChipScoPy Overview](https://xilinx.github.io/chipscopy/2023.2/overview.html)\n\n-------------------------------------------------------------------------------\n\n[System Requirements](https://xilinx.github.io/chipscopy/2023.2/system_requirements.html)\n\n-------------------------------------------------------------------------------\n\n[ChipScoPy Installation](https://xilinx.github.io/chipscopy/2023.2/chipscopy_installation.html)\n\n-------------------------------------------------------------------------------\n\n[ChipScoPy Examples](https://github.com/Xilinx/chipscopy/tree/master/chipscopy/examples)\n\n-------------------------------------------------------------------------------\n\n[FAQ](https://github.com/Xilinx/chipscopy/blob/master/FAQ.md)\n\n-------------------------------------------------------------------------------\n\n[API Documentation](https://xilinx.github.io/chipscopy/)\n\n-------------------------------------------------------------------------------\n',
    'author': 'Xilinx ChipScope Team',
    'author_email': 'None',
    'maintainer': 'Xilinx ChipScope Team',
    'maintainer_email': 'None',
    'url': 'https://github.com/Xilinx/chipscopy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)

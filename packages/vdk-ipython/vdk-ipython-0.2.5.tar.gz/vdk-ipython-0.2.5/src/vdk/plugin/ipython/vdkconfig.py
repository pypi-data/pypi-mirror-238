# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import logging
from copy import deepcopy

import toml
from IPython import get_ipython
from IPython.core.magic_arguments import magic_arguments, argument

from vdk.plugin.ipython.common import show_ipython_error, VDK_CONFIG_IPYTHON_KEY
from vdk.plugin.ipython.job import JobControl

log = logging.getLogger(__name__)

value_storage = {}
reverse_value_storage = {}


@magic_arguments()
@argument("-p", "--parser", type=str, default="toml")
def vdkconfig(line, cell):
    """
    Load VDK Configuration from a config cell

    :param line: str
            Not used in this function but required for cell magic.
    :param cell: str
            The configuration in toml format.

    """

    parsed_config = toml.loads(cell)
    get_ipython().push(variables={VDK_CONFIG_IPYTHON_KEY: deepcopy(parsed_config)}, interactive=False)

    vdk: JobControl = get_ipython().user_global_ns.get("VDK", None)
    if vdk and vdk.is_initialized():
        vdk.finalize()

    # for key, value in parsed_config.items():
    #     parsed_config[key] = f"[OBFUSCATED]"
    # obfuscated_config = toml.dumps(parsed_config)
    # get_ipython().set_next_input(f"%%vdkconfig\n{obfuscated_config}", replace=True)

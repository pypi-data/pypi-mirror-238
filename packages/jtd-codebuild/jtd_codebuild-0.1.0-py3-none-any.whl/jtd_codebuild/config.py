# flake8: noqa: E402

import os
import json
from typing import Dict, AnyStr, Any


_CONFIG_NAME = "jtd-codebuild.json"


def get_config(cwd: str) -> Dict[AnyStr, Any]:
    """Get configutation from :const:`_CONFIG_NAME` file
    in the current working directory.

    You can checkout the schema of the configuration file in `README.md <../README.md>`_.

    Args:
        cwd: The current working directory.

    Returns:
        The configuration dictionary.
    """

    with open(os.path.join(cwd, _CONFIG_NAME), "r") as f:
        config = json.load(f)

    return config

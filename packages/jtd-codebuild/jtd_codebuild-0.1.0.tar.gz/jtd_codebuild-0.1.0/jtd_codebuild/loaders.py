# flake8: noqa: E402

import os
import yaml
from typing import Dict, AnyStr, Any
from .config import get_config
from .utils import file_is_yaml


def load_definitions(cwd: str) -> Dict[AnyStr, Any]:
    """Load definition files from its directory given by the configuration file.

    Args:
        cwd: The current working directory.

    Returns:
        A dictionary of all definitions.
        Key is the definition name, value is the definition.
    """
    config = get_config(cwd)
    definition_path = os.path.join(cwd, config["definitions-path"])

    definitions = {}

    # Recursively load all definitions
    for root, dirs, files in os.walk(definition_path):
        for file in files:
            if file_is_yaml(file):
                filepath = os.path.join(root, file)
                with open(filepath, "r") as f:
                    definition_parts = yaml.load(f, Loader=yaml.FullLoader)
                    for definition_name, definition in definition_parts.items():
                        definitions[definition_name] = definition

    return definitions


def load_root_schema(cwd: str) -> Dict[AnyStr, Any]:
    """Load the root schema from the schema file given by the configuration file.

    Args:
        cwd: The current working directory.

    Returns:
        The root schema.
    """
    config = get_config(cwd)
    schema_path = os.path.join(cwd, config["root-schema-path"])

    with open(schema_path, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

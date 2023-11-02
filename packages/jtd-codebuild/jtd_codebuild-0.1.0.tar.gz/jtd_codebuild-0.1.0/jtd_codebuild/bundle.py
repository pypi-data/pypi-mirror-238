import os
from functools import reduce
from typing import Dict, AnyStr, Any
from .loaders import load_definitions, load_root_schema
from .config import get_config


def _merge(
    a: Dict[AnyStr, Any],
    b: Dict[AnyStr, Any],
) -> Dict[AnyStr, Any]:
    """Merges two dictionaries in shallow manner.

    If the same key exists in both dictionaries,
    the value in `b` will take precedence.

    Args:
        a: The first dictionary.
        b: The second dictionary.

    Returns:
        The merged dictionary.
    """
    return {**a, **b}


def bundle_schema(cwd: str) -> Dict[AnyStr, Any]:
    """Bundles modularized schema files into a single schema file.

    This function will load all the schema files specified in the
    configuration file and packages specified as includes.

    Args:
        cwd: The current working directory.

    Returns:
        The bundled schema.
    """
    # Get configuration of the package
    config = get_config(cwd)

    # Extract schemas from includes
    schemas = [
        bundle_schema(os.path.join(cwd, include))
        for include in config.get("includes", [])
    ]

    # Extract definitions from includes schemas
    definitions = [schema["definitions"] for schema in schemas]

    # Load definitions and append it to the list
    definitions.append(load_definitions(cwd))

    # Load root schema
    root_schema = load_root_schema(cwd)

    # Add definitions to root schema
    root_schema["definitions"] = reduce(_merge, definitions)

    return root_schema

import os
import json
import subprocess
from typing import List
from .bundle import bundle_schema
from .config import get_config
from .utils import safe_open, wait_for_processes
from .generators import (
    JTDCodeGenerator,
    JTDCodeGeneratorTypescriptTarget,
    JTDCodeGeneratorPythonTarget,
)


def jtd_codebuild(cwd: str) -> None:
    """Generate code from the JSON Type Definition files.

    Args:
        cwd: The current working directory.
    """
    # We use basename of cwd as the name of the package
    # we're trying to generate a schema for
    package_name = os.path.basename(cwd)

    print(f"[jtd-codebuild] Start building: {package_name}")
    config = get_config(cwd)

    print("[jtd-codebuild] Bundling schema files...")
    schema = bundle_schema(cwd)

    # Write a full schema file to output specified
    # by the configuration file in json format
    print("[jtd-codebuild] Writing full schema...")
    output_path = os.path.join(cwd, config["output-schema-path"])
    with safe_open(output_path, "w") as f:
        json.dump(schema, f, indent=2)

    print("[jtd-codebuild] Generating code...")
    # Generate code from the full schema file
    targets = config["targets"]
    processes: List[subprocess.Popen] = []
    for target in targets:
        generator: JTDCodeGenerator = None

        target_language = target["language"]
        if target_language == "typescript":
            # Case: TypeScript
            generator = JTDCodeGeneratorTypescriptTarget(cwd, output_path)
        elif target_language == "python":
            # Case: Python
            generator = JTDCodeGeneratorPythonTarget(cwd, output_path)
        else:
            # Default case
            generator = JTDCodeGenerator(cwd, output_path)

        processes.extend(generator.generate(target))

    # Wait for all processes to finish
    wait_for_processes(processes)

    print("[jtd-codebuild] Done!")

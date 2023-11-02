import os
import subprocess
from typing import Dict, Any, AnyStr, List
from ..utils import safe_mkdir


class JTDCodeGenerator:
    """Generate code from the JSON Type Definition files.

    Attributes:
        cwd: The current working directory.
        schema_path: The path to the JSON Type Definition schema file.
    """

    def __init__(self, cwd: str, schema_path: str):
        """Initialize the JTDCodeGenerator.

        Args:
            cwd: The current working directory.
            schema_path: The path to the JSON Type Definition schema file.
        """
        self.cwd = cwd
        self.schema_path = schema_path

    def _codegen_command(
        self,
        schema_path: str,
        output_dir: str,
        target_language: str,
    ) -> str:
        """Generate code from a JSON Type Definition schema file.

        Args:
            schema_path: The path to the JSON Type Definition schema file.
            output_dir: The output directory.
            target_language: The target language.

        Returns:
            The command to generate code.
        """
        return f"jtd-codegen {schema_path} --{target_language}-out {output_dir}"

    def get_target_path(self, target: Dict[AnyStr, Any]) -> AnyStr:
        """Get the target path.

        Args:
            target: Target configuration.

        Returns:
            The target path.
        """
        return os.path.join(self.cwd, target["path"])

    def generate(
        self,
        target: Dict[AnyStr, Any],
    ) -> List[subprocess.Popen]:
        """Generate code from the JSON Type Definition files.

        Args:
            target: Target configuration.

        Returns:
            A list of subprocesses created by the code generation.
        """
        target_language = target["language"]
        target_path = self.get_target_path(target)
        safe_mkdir(target_path)
        process = subprocess.Popen(
            self._codegen_command(self.schema_path, target_path, target_language),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return [process]

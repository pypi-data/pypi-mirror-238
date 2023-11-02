import os
import subprocess
from typing import Dict, Any, AnyStr, List
from ..utils import wait_for_processes
from .generator import JTDCodeGenerator


class JTDCodeGeneratorTypescriptTarget(JTDCodeGenerator):
    """Generate code from the JSON Type Definition files for TypeScript.

    It does a normal code generation which is done by :class:`JTDCodeGenerator`_,
    and in addition it performs typescript -> javascript compilation
    if tsconfig is provided.
    """

    def generate(self, target: Dict[AnyStr, Any]) -> List[subprocess.Popen]:
        if target["language"] != "typescript":
            raise ValueError("Target language must be typescript")

        processes = super().generate(target)
        if "tsconfig-path" not in target:
            return processes

        # Wait for existing processes to finish before starting the compilation
        # process.
        wait_for_processes(processes, print_stdout=False)

        # Compile the generated TypeScript code to JavaScript
        tsconfig_path = os.path.join(self.cwd, target["tsconfig-path"])
        compile_process = subprocess.Popen(
            f"tsc --project {tsconfig_path}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return processes + [compile_process]

# flake8: noqa: W503
import os
import re
import subprocess
from typing import Dict, Any, AnyStr, List
from io import TextIOWrapper
from ..utils import wait_for_processes
from .generator import JTDCodeGenerator


class JTDCodeGeneratorPythonTarget(JTDCodeGenerator):
    """Generate code from the JSON Type Definition files for Python.

    It does a normal code generation which is done by :class:`JTDCodeGenerator`_,
    and in addition it substitutes python built-in dataclass decorator
    to pydantic's dataclass decorator if `use-pydantic` is set to true.
    """

    class_regex = r"^class ([a-zA-Z0-9_]+)[(]{0,1}(.*)[)]{0,1}:$"
    """This regex captures the class name from the class definition line.

    It captures 2 groups:
        1. The class name
        2. The arguments passed to the class

    For example, if the class definition line is `class DummyClass:`,
    it captures `DummyClass` as the class name.

    If the class definition line is `class DummyClass(SomeClass):`,
    it captures `DummyClass` as the class name and `SomeClass` as the argument.
    """

    type_hint_regex = r"^[ ]{4}[a-zA-Z0-9_]+:[ ]{1}'[a-zA-Z0-9\[\],_\'\" ]+'$"
    """This regex captures the type hint line.
    
    For example, if the type hint line is `    a: 'Dict[str, Any]'`,
    regex captures this line.
    """

    def _open_schema_file(
        self,
        target_path: str,
        mode: str,
    ) -> TextIOWrapper:
        """Open the schema file.

        Args:
            target_path: The target path.

        Returns:
            The opened schema file.
        """
        schema_file_path = os.path.join(target_path, "__init__.py")
        return open(schema_file_path, mode)

    def _substitute_types_to_impls(
        self,
        lines: List[AnyStr],
    ) -> List[AnyStr]:
        """Substitute types to implementations.
        For example, `Dict`, to `dict`, `Any` to `object`, etc.

        Args:
            lines: The lines to substitute.

        Returns:
            The substituted lines.
        """
        for i, line in enumerate(lines):
            # If the line is a type hint, substitute it to an implementation.
            if re.match(self.type_hint_regex, line) is not None:
                lines[i] = (
                    line.replace("Dict", "dict")
                    .replace("Any", "object")
                    .replace("List", "list")
                )

        return lines

    def _append_none_to_optional_fields(
        self,
        lines: List[AnyStr],
    ) -> List[AnyStr]:
        """Append `None` to the optional fields.

        Args:
            lines: The lines to append.

        Returns:
            The appended lines.
        """
        for i, line in enumerate(lines):
            # If the line is a type hint and the type starts with `Optional`,
            # append `None` to the type.
            if (
                re.match(self.type_hint_regex, line) is not None
                and "'Optional[" in line
            ):
                code, _ = line.split("\n")
                lines[i] = f"{code} = None\n"

        return lines

    def _inject_rebuild_dataclass_calls(
        self,
        lines: List[AnyStr],
    ) -> List[AnyStr]:
        """Injects `rebuild_dataclass`_ calls to the code.

        Args:
            lines: The lines to inject.

        Returns:
            The injected lines.
        """
        rebuild_model_calls: List[str] = [
            "\n",
            "# Rebuild models\n",
            "\n",
        ]

        # Find the line where the `dataclass` decorator is called
        for i, line in enumerate(lines):
            # Extract the class name if the line is a class definition
            regex_match: re.Match = re.match(self.class_regex, line)
            if regex_match is None:
                continue
            class_name = regex_match.group(1)

            # Inject `rebuild_dataclass` call
            rebuild_model_calls.append(f"rebuild_dataclass({class_name})\n")

        # Append the `rebuild_dataclass` calls to the end of the file
        lines.extend(rebuild_model_calls)

        return lines

    def generate(self, target: Dict[AnyStr, Any]) -> List[subprocess.Popen]:
        if target["language"] != "python":
            raise ValueError("Target language must be python")

        processes = super().generate(target)
        if "use-pydantic" not in target or not target["use-pydantic"]:
            return processes

        # Wait for existing processes to finish before starting the modification
        # process.
        wait_for_processes(processes, print_stdout=False)

        # Inject pydantic's dataclass decorator to the generated code
        # if `use-pydantic` is set to true.
        target_path = self.get_target_path(target)
        with self._open_schema_file(target_path, "r") as f:
            lines = f.readlines()

        # Disable linter for the entire file
        lines.insert(0, "# flake8: noqa\n")

        # Remove built-in dataclass decorator imoprt
        lines.remove("from dataclasses import dataclass\n")

        # Import pydantic's dataclass decorator
        # and related functions
        lines.insert(2, "import dataclasses\n")
        lines.insert(
            3, "from pydantic.dataclasses import dataclass, rebuild_dataclass\n"
        )

        # Substitute `typing` package types to actual implementations
        lines = self._substitute_types_to_impls(lines)

        # Append `None` to the optional fields
        lines = self._append_none_to_optional_fields(lines)

        # Inject :meth:`.model_rebuild`_ calls for every models
        lines = self._inject_rebuild_dataclass_calls(lines)

        # Write the modified code to the file
        with self._open_schema_file(target_path, "w") as f:
            f.writelines(lines)

        return processes

# flake8: noqa: E402

import os
import subprocess
from typing import Any, List


def file_is_yaml(file: str) -> bool:
    """Check if a file is a YAML file.

    Args:
        file: The file name.

    Returns:
        True if the file is a YAML file, False otherwise.
    """
    return file.endswith(".yaml") or file.endswith(".yml")


def safe_mkdir(path: str) -> None:
    """Create a directory with creating its parent directories if they do not exist.

    Args:
        path: The directory path.
    """
    os.makedirs(path, exist_ok=True)


def safe_open(file_path: str, mode: str) -> Any:
    """Open a file with creating its parent directories if they do not exist.

    Args:
        file_path: The file path.
        mode: The file open mode.

    Returns:
        The opened file.
    """
    safe_mkdir(os.path.dirname(file_path))
    return open(file_path, mode)


def wait_for_processes(
    processes: List[subprocess.Popen],
    print_stdout: bool = True,
    print_stderr: bool = True,
) -> None:
    """Wait for all processes to finish.

    Args:
        processes: The list of processes.
        print_stdout: Whether to print stdout.
        print_stderr: Whether to print stderr.
    """
    # Wait for existing processes to finish before starting the modification
    for process in processes:
        process.wait()

        # Print stdout and stderr
        stdout, stderr = process.communicate()

        if stdout and print_stdout:
            # Print stdout if it exists and `print_stdout` is set to true
            print(stdout.decode("utf-8"))
        if stderr:
            if print_stderr:
                # Print stderr if it exists and `print_stderr` is set to true
                print(stderr.decode("utf-8"))
            # Raise an exception if stderr exists
            exit(1)

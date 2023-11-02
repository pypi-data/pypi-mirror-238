import os
import subprocess


def test_example_project_1():
    # Get current working directory
    cwd = os.path.dirname(__file__)

    # Run the command
    subprocess.check_call(
        "jtd-codebuild fixtures/example-project-1",
        shell=True,
        cwd=cwd,
    )

    # Check the output
    assert os.path.exists(
        os.path.join(
            cwd,
            "fixtures/example-project-1/gen/schema.jtd.json",
        )
    )
    assert os.path.exists(
        os.path.join(
            cwd,
            "fixtures/example-project-1/gen/python/__init__.py",
        )
    )

    # More tests here...

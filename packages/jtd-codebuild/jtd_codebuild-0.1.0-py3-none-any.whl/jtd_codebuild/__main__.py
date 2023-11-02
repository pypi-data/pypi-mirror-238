import os
import click
from .codebuild import jtd_codebuild


@click.command()
@click.argument("path", type=click.Path(exists=True))
def cli(path):
    """JTD CodeBuild"""
    # Get the path of the target directory
    target_path = os.path.join(os.getcwd(), path)

    # Run the JTD CodeBuild
    jtd_codebuild(target_path)


if __name__ == "__main__":
    cli()

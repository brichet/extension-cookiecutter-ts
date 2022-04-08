#!/usr/bin/env python
from pathlib import Path
from os import chdir
from cookiecutter.main import cookiecutter

PROJECT_DIRECTORY = Path.cwd()


def remove_path(path: str) -> None:
    """Remove the provided path.
    
    If the target path is a directory, remove it recursively.
    """
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        for f in path.iterdir():
            remove_path(f)
        path.rmdir()


if __name__ == "__main__":

    context = """
{{ cookiecutter | jsonify }}
"""
    # print(context)

    if not "{{ cookiecutter.has_settings }}".lower().startswith("y"):
        remove_path(PROJECT_DIRECTORY / "schema")

    if "{{ cookiecutter.kind }}".lower() == "theme":
        for f in (
            "style/index.js",
            "style/base.css"
        ):
            remove_path(PROJECT_DIRECTORY / f)
    else:
        remove_path(PROJECT_DIRECTORY / "style/variables.css")

    if not "{{ cookiecutter.kind }}".lower() == "server":
        for f in (
            "{{ cookiecutter.python_name }}/handlers.py",
            "src/handler.ts",
            "jupyter-config"
        ):
            remove_path(PROJECT_DIRECTORY / f)

    if not "{{ cookiecutter.has_binder }}".lower().startswith("y"):
        remove_path(PROJECT_DIRECTORY / "binder")
        remove_path(PROJECT_DIRECTORY / ".github/workflows/binder-on-pr.yml")

    if "{{ cookiecutter.kind }}".lower() == "server":
        print("About server settings :")
        extra_context = {
            "_kind": "server",
            "_python_name": "{{ cookiecutter.python_name }}"
        }

        cookiecutter("{{ cookiecutter._template }}",
                     directory="server", 
                     extra_context=extra_context,
                     checkout="nested_cookiecutter"
        )

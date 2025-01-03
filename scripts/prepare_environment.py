
"""
Prepare a new Replit Environment
"""

from contextlib import suppress
from difflib import get_close_matches
from importlib import import_module
from os import environ, getenv
from os.path import abspath, exists
from pathlib import Path
from subprocess import CalledProcessError, run
from textwrap import dedent, indent
from typing import List, Optional, Tuple


def check_packages(required_packages: Optional[List[str]] = None) -> Tuple[str, ...]:
    """Check which required packages are missing from the environment.

    Args:
        required_packages: List of package names to check

    Returns:
        Tuple of missing package names
    """
    missing_packages = ()
    for package in required_packages or []:
        try:
            import_module(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is not installed")
            missing_packages += (package,)
    return missing_packages


def install_missing_packages(packages: Optional[Tuple[str, ...]] = None) -> None:
    """Install packages that are missing from the environment.

    Args:
        packages: Tuple of package names to install

    Raises:
        CalledProcessError: If package installation fails
    """
    for package in packages or []:
        try:
            run(["pip", "install", package])
            print(f"Successfully installed {package}")
        except CalledProcessError as e:
            print(f"Failed to install {package}: {e}")


def setup_github_repo(github_token: str,
                    project_name: str,
                    user_name: str,
                    user_email: str) -> None:
    """Create and configure a GitHub repository for the project.

    Args:
        github_token: GitHub authentication token
        project_name: Name of the project/repository
        user_name: GitHub username
        user_email: User's email address

    Raises:
        Exception: If repository initialization or configuration fails
    """
    try:
        if not exists(".git"):
            run(["git", "init"], check=True)
        run(["git", "config", "--global", "user.name", user_name], check=True)
        run(["git", "config", "--global", "user.email", user_email], check=True)
        
        try:
            run(["git", "remote", "remove", "origin"])
        except Exception as e:
            print(f"Error initializing repository: {str(e)}")

        print(f"\nGit repository initialized as '{project_name}'")
    except Exception as e:
        print(f"Error initializing repository: {str(e)}")

    try:
        from replit import db
        from requests import post

        response = post(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json",
            },
            json={
                "name": project_name,
                "private": False,
                "auto_init": False,
            },
        )
        
        if response.status_code != 201:
            print(f"Error creating repository: {response.json()}")
            repo_url_cleaned = db["GIT_URL_CLEANED"]
        else:
            response_json = response.json()
            db["GITHUB_TOKEN"] = github_token
            db["GIT_NAME"] = user_name
            db["GIT_EMAIL"] = user_email
            repo_url_cleaned = db["GIT_URL_CLEANED"] = response_json["html_url"]
            
        with suppress(Exception):
            run(["git", "stash"])
        with suppress(Exception):
            run(["git", "remote", "add", "origin", repo_url_cleaned])
        with suppress(Exception):
            run(["git", "pull", "origin", "main", "--rebase"])
        with suppress(Exception):
            run(["git", "stash", "pop"])
        with suppress(Exception):
            run(["git", "add", "."])
        with suppress(Exception):
            run(["git", "commit", "-m", "Initial commit"])
        with suppress(Exception):
            run(["git", "push", "-u", "origin", "main"])
            
        print(f"\nRepository created and configured: {repo_url_cleaned}")
    except Exception as e:
        print(f"Error setting up repository: {str(e)}")


def run_all() -> None:
    """Execute all environment setup tasks."""
    home = "."
    project_info = {
        "templates": {
            "pyproject": {
                "build-system": {
                    "requires": ["setuptools>=45", "wheel"],
                    "build-backend": "setuptools.build_meta"
                },
                "project": {
                    "name": "",
                    "version": "",
                    "description": "",
                    "readme": "README.md",
                    "requires-python": ">=3.11",
                    "authors": [{"name": "", "email": ""}],
                    "license": {"file": "LICENSE"},
                    "classifiers": [
                        "Intended Audience :: Developers",
                        "Intended Audience :: Science/Research",
                        "License :: OSI Approved :: MIT License",
                        "Programming Language :: Python :: 3",
                        "Programming Language :: Python :: 3.11",
                        "Operating System :: OS Independent",
                        "Natural Language :: English",
                        "Typing :: Typed"
                    ],
                    "urls": {"Homepage": "", "Repository": ""}
                }
            }
        }
    }

    setup = project_info["setup"]
    missing_packages = check_packages(setup["required_packages"])
    if missing_packages:
        install_missing_packages(missing_packages)

    print("\nAll required packages are installed!")

    from replit import info
    from requests import get
    from toml import dump

    try:
        response = get(str(info.replit_id_url), allow_redirects=False, timeout=5)
        project_name = (response.url.split("/")[-1] if response.url != str(info.replit_id_url)
                      else str(response.content).split("/")[-1].removesuffix("'"))
        
        setup_github_repo(
            getenv("GITHUB_TOKEN", ""),
            project_name,
            setup["user_config"]["user_name"],
            setup["user_config"]["user_email"]
        )
    except Exception as e:
        print(f"Error during setup: {str(e)}")


if __name__ == "__main__":
    run_all()

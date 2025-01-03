from contextlib import suppress
from subprocess import run

with suppress(Exception):
    for cmd in [[
            "git", "clone",
            "https://github.com/paulovcmedeiros/toml-formatter.git",
            "toml-formatter"
    ],
                [
                    "python", "-m", "pip", "install", "--user", "poetry",
                    "--break-system-packages"
                ],
                [
                    "python", "-m", "pip", "install", "--user", "-e",
                    "toml-formatter"
                ], ["rm", "-rf", "toml-formatter"]]:
        run(cmd)

import os, sys, platform, subprocess
from subprocess import run, CalledProcessError


def main():
    try:
        clone_dir = 'toml-formatter'
        run([
            'git', 'clone',
            'https://github.com/paulovcmedeiros/toml-formatter.git', clone_dir
        ])
        run([
            sys.executable, '-m', 'pip', 'install', '--user', 'poetry',
            '--break-system-packages'
        ])
        run([
            sys.executable, '-m', 'pip', 'install', '--user', '-e', clone_dir
        ],
            check=True)

        bin_dir = os.path.join(
            clone_dir, 'Scripts' if platform.system() == 'Windows' else 'bin')
        os.environ['PATH'] = f"{bin_dir}:{os.environ.get('PATH', '')}"
        print("Installation completed successfully.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

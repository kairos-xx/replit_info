import os
from subprocess import CalledProcessError, run
import subprocess
import sys
import platform

def clone_repository(repo_url, clone_dir):
    """Clone the Git repository."""
    try:
        run(['git', 'clone', repo_url, clone_dir])
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        sys.exit(1)

def install_poetry():
    """Install Poetry using pip."""
    try:
        run([sys.executable, '-m', 'pip', 'install', '--user', 'poetry', '--break-system-packages'])
    except subprocess.CalledProcessError as e:
        print(f"Error installing Poetry: {e}")
        sys.exit(1)

def install_package(clone_dir):
    """Install the package using Poetry."""
    try:
        run(['poetry', 'install', '--only main'], cwd=clone_dir)
    except subprocess.CalledProcessError as e:
        print(f"Error installing the package: {e}")
        sys.exit(1)

def add_to_path(directory):
    """Add the specified directory to the system PATH."""
    os.environ['PATH'] = f"{directory}:{os.environ.get('PATH', '')}"
    print(f"Added {directory} to PATH temporarily")
    if platform.system() == 'Windows':
        # Windows-specific method to add to PATH
        import winreg as reg
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, 'Environment', 0, reg.KEY_ALL_ACCESS) as key:
                current_path = reg.QueryValueEx(key, 'Path')[0]
                if directory not in current_path:
                    new_path = f"{current_path};{directory}"
                    reg.SetValueEx(key, 'Path', 0, reg.REG_EXPAND_SZ, new_path)
                    print(f"Added {directory} to system PATH. Please restart your session for changes to take effect.")
        except Exception as e:
            print(f"Error adding to PATH: {e}")
            sys.exit(1)
    else:
        # Unix-based method to add to PATH
        shell_profile = os.path.expanduser('~/.bashrc')
        if not os.path.exists(shell_profile):
            shell_profile = os.path.expanduser('~/.bash_profile')
        if not os.path.exists(shell_profile):
            shell_profile = os.path.expanduser('~/.profile')
        try:
            with open(shell_profile, 'a') as file:
                file.write(f'\nexport PATH="{directory}:$PATH"\n')
            print(f"Added {directory} to PATH in {shell_profile}. Please run 'source {shell_profile}' or restart your session for changes to take effect.")
        except Exception as e:
            print(f"Error adding to PATH: {e}")
            sys.exit(1)

def main():
    repo_url = 'https://github.com/paulovcmedeiros/toml-formatter.git'
    clone_dir = 'toml-formatter'

    clone_repository(repo_url, clone_dir)
    install_poetry()
    install_package(clone_dir)

    # Determine the directory containing the 'toml-formatter' executable
    if platform.system() == 'Windows':
        bin_dir = os.path.join(clone_dir, 'Scripts')
    else:
        bin_dir = os.path.join(clone_dir, 'bin')

    add_to_path(bin_dir)
    print("Installation completed successfully.")

if __name__ == "__main__":
    main()

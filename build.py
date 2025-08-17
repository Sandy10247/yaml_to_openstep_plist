import os
import subprocess
import sys
import venv
import argparse

def run_command(command, check=True):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, check=check, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.cmd}\nError: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def setup_venv():
    """Create and activate a virtual environment."""
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
    
    # Activate virtual environment
    if sys.platform == "win32":
        activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")
    
    print(f"Virtual environment created at {venv_dir}. Activate it manually if needed:")
    print(f"  On Unix/macOS: source {activate_script}")
    print(f"  On Windows: {activate_script}")
    
    # For pip commands, use the venv's Python
    python_bin = os.path.join(venv_dir, "Scripts" if sys.platform == "win32" else "bin", "python")
    return python_bin

def install_dependencies(python_bin):
    """Install required dependencies."""
    print("Installing dependencies...")
    run_command([python_bin, "-m", "pip", "install", "--upgrade", "pip"])
    run_command([python_bin, "-m", "pip", "install", "build", "hatchling", "twine", "pyyaml>=5.1"])

def build_package(python_bin):
    """Build the package."""
    print("Building package...")
    run_command([python_bin, "-m", "build"])

def upload_package(repository):
    """Upload the package to PyPI or TestPyPI."""
    print(f"Uploading to {repository}...")
    repo_flag = "--repository" if repository == "testpypi" else "--repository-url"
    repo_url = "https://test.pypi.org/legacy/" if repository == "testpypi" else "https://upload.pypi.org/legacy/"
    run_command(["twine", "upload", repo_flag, repo_url, "dist/*"])

def main():
    parser = argparse.ArgumentParser(description="Build and optionally upload yaml_to_openstep_plist to PyPI.")
    parser.add_argument("--upload", choices=["pypi", "testpypi"], help="Upload to PyPI or TestPyPI")
    args = parser.parse_args()

    # Set up virtual environment and get Python binary
    python_bin = setup_venv()

    # Install dependencies
    install_dependencies(python_bin)

    # Build package
    build_package(python_bin)

    # Upload if requested
    if args.upload:
        upload_package(args.upload)

    print("Build completed successfully. Package files are in the 'dist/' directory.")
    if args.upload:
        print(f"Package uploaded to {args.upload}.")

if __name__ == "__main__":
    main()
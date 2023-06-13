# Adopted from https://github.com/C0untFloyd/bark-gui/blob/main/installer/installer.py

import argparse
import glob
import os
import shutil
import site
import subprocess
import sys

script_dir = os.getcwd()


def run_cmd(cmd, capture_output=False, env=None):
    # Run shell commands
    return subprocess.run(cmd, shell=True, capture_output=capture_output, env=env)


def check_env():
    # If we have access to conda, we are probably in an environment
    conda_not_exist = run_cmd("conda", capture_output=True).returncode
    if conda_not_exist:
        print("Conda is not installed. Exiting...")
        sys.exit()
    
    # Ensure this is a new environment and not the base environment
    if os.environ["CONDA_DEFAULT_ENV"] == "base":
        print("Create an environment for this project and activate it. Exiting...")
        sys.exit()


def install_dependencies():
    # Install Git and clone repo
    run_cmd("conda install -y -k git")
    run_cmd("git clone https://github.com/facebookresearch/audiocraft")

    # Select your GPU or, choose to run in CPU mode
    print("Do you have a GPU (Nvidia)?")
    print("Enter Y for Yes")
    print()
    gpuchoice = input("Input> ").lower()

    if gpuchoice == "y":
        run_cmd("python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --force-reinstall")

    # Install the webui dependencies
    update_dependencies()


def update_dependencies():
    os.chdir("audiocraft")
	# do a hard reset for to update even if there are local changes
    run_cmd("git fetch --all")
    run_cmd("git reset --hard origin/main")
    run_cmd("git pull")
    # Installs/Updates dependencies from all requirements.txt
    run_cmd("python -m pip install .")
    run_cmd("python -m pip install -r requirements.txt")


def start_app():
    os.chdir("audiocraft")
    # forward commandline arguments
    sys.argv.pop(0)
    args = ' '.join(sys.argv)
    run_cmd(f'python app.py {args}')


if __name__ == "__main__":
    # Verifies we are in a conda environment
    check_env()

    # If webui has already been installed, skip and run
    if not os.path.exists("audiocraft/"):
        install_dependencies()
    else:
        # moved update from batch to here, because of batch limitations
        updatechoice = input("Check for Updates? [y/n]").lower()
        if updatechoice == "y":
           update_dependencies()

    # Run the model with webui
    os.chdir(script_dir)
    start_app()
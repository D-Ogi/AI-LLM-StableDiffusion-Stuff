# Audiocraft Linux One-Click Installer

This repository contains an One-Click Installer script for [Audiocraft](https://github.com/facebookresearch/audiocraft), a PyTorch library developed by Facebook Research for deep learning research on audio generation.

## Overview of the Script

The script performs the following actions:

1. Navigates to the directory where the script is located.
2. Checks if the directory contains spaces, which can cause issues during the installation.
3. Sets the configuration for installing Miniconda and the environment.
4. Checks if Miniconda is already installed.
5. If Miniconda is not installed, it downloads and installs Miniconda.
6. Creates a Conda environment with Python 3.9.
7. Activates the newly created environment.
8. Installs `ffmpeg` from the conda-forge channel.
9. Downloads a Python script named `installer.py`.
10. Runs the downloaded Python script, which is expected to launch Audiocraft GUI.
11. Prints "Done!" when the script finishes running.

## Instructions

To use the script, follow these steps:

1. Save the script as `run_install.sh` or any other name with the `.sh` extension.
2. Make the script executable with the command: `chmod +x run_install.sh`.
3. Execute the script by running: `./run_install.sh`.

Please ensure that you have `curl` installed on your system before running the script. If it is not already installed, you can install it using the command `sudo apt-get install curl`.

## License

This project is under the MIT License.


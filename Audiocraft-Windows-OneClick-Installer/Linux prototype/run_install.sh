#!/bin/bash
# Bash script based on Batch file by https://github.com/C0untFloyd/bark-gui

# Please set the following command line arguments to your preferred settings
COMMANDLINE_ARGS=""

# Go to script directory
cd "$(dirname "$0")"

# Check for spaces in path
if [[ $(pwd) =~ " " ]]; then
    echo "This script relies on Miniconda which cannot be silently installed under a path with spaces."
    exit 1
fi

# Config
INSTALL_DIR="$(pwd)/libs"
CONDA_ROOT_PREFIX="$(pwd)/conda"
INSTALL_ENV_DIR="$(pwd)/env"
MINICONDA_DOWNLOAD_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
conda_exists="false"

# Check if conda is installed
if command -v "$CONDA_ROOT_PREFIX/bin/conda" &> /dev/null; then
    conda_exists="true"
fi

# (if necessary) Install conda into a contained environment
if [ "$conda_exists" == "false" ]; then
    echo "Downloading Miniconda from $MINICONDA_DOWNLOAD_URL to $INSTALL_DIR/miniconda_installer.sh"

    mkdir -p "$INSTALL_DIR"
    curl -L "$MINICONDA_DOWNLOAD_URL" -o "$INSTALL_DIR/miniconda_installer.sh" || { echo "Miniconda failed to download."; exit 1; }

    echo "Installing Miniconda to $CONDA_ROOT_PREFIX"
    bash "$INSTALL_DIR/miniconda_installer.sh" -b -p "$CONDA_ROOT_PREFIX" || { echo "Miniconda installation failed."; exit 1; }

    # Test the conda binary
    echo "Miniconda version:"
    "$CONDA_ROOT_PREFIX/bin/conda" --version || { echo "Miniconda not found."; exit 1; }
fi

# Create the installer env
if [ ! -d "$INSTALL_ENV_DIR" ]; then
    echo "Creating Conda environment"
    "$CONDA_ROOT_PREFIX/bin/conda" create --yes --prefix "$INSTALL_ENV_DIR" python=3.9 || { echo "Conda environment creation failed."; exit 1; }
fi

# Check if conda environment was actually created
if [ ! -f "$INSTALL_ENV_DIR/bin/python" ]; then
    echo "Conda environment is empty."
    exit 1
fi

# Activate installer env
source "$CONDA_ROOT_PREFIX/bin/activate" "$INSTALL_ENV_DIR" || { echo "Miniconda activation failed."; exit 1; }

# Install ffmpeg if it does not exist
"$CONDA_ROOT_PREFIX/bin/conda" install -y -q -c conda-forge ffmpeg || { echo "ffmpeg installation failed."; exit 1; }

# Download the install.py or replace it with a newly downloaded version
FILE_URL="https://raw.githubusercontent.com/D-Ogi/AI-LLM-StableDiffusion-Stuff/main/Audiocraft-Windows-OneClick-Installer/installer.py"
FILE_PATH="$INSTALL_DIR/installer.py"

curl -L "$FILE_URL" -o "$FILE_PATH" || { echo "File failed to download."; exit 1; }

# Setup installer env
echo "Launching Audiocraft GUI"
python "$FILE_PATH" $COMMANDLINE_ARGS

echo "Done!"

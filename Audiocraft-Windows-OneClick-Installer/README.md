# Audiocraft Windows One-Click Installer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains a Windows One-Click Installer for [Audiocraft](https://github.com/facebookresearch/audiocraft), a PyTorch library developed by Facebook Research for deep learning research on audio generation. The installer is intended to facilitate the installation process of Audiocraft on Windows platforms.

## About Audiocraft

![docs badge](https://github.com/facebookresearch/audiocraft/workflows/audiocraft_docs/badge.svg)
![linter badge](https://github.com/facebookresearch/audiocraft/workflows/audiocraft_linter/badge.svg)
![tests badge](https://github.com/facebookresearch/audiocraft/workflows/audiocraft_tests/badge.svg)

Audiocraft is a Python library built on PyTorch, primarily used for deep learning research in audio generation. It is particularly known for MusicGen, a state-of-the-art controllable text-to-music model. MusicGen is an auto-regressive Transformer model trained with an EnCodec tokenizer. For more details and demos, visit the [official Audiocraft repository](https://github.com/facebookresearch/audiocraft).

## One-Click Installer

This installer is intended for users who want to quickly set up Audiocraft on a Windows system. It has been adopted from [bark-gui](https://github.com/C0untFloyd/bark-gui) and modified to work with Audiocraft.

### Components

- `windows_run_install.bat`: This is a Batch file script for Windows systems that sets up the environment and handles the installation of Audiocraft. It downloads and installs Miniconda, Git, and other dependencies required for Audiocraft.

- `installer.py`: This Python script is automatically downloaded by `windows_run_install.bat`. It checks for Conda installation, creates an environment, installs Git, clones the Audiocraft repository, and sets up dependencies.

### How It Works

The `windows_run_install.bat` script uses Miniconda to create an isolated Python environment on your system. It downloads `installer.py`, which then installs Audiocraft and its dependencies within this environment. This ensures that your system remains clean and avoids conflicts with other Python packages.

### Installation Instructions

1. Download the `windows_run_install.bat` file from this repository.
2. Double-click the downloaded `windows_run_install.bat` file.

This is all it takes! The script will automatically handle the rest of the installation process for you.

## Compatibility

This installer is intended for Windows platforms. However, it might work with Windows Subsystem for Linux (WSL) and native Linux distributions as well, although this has not been extensively tested.

## License

This project is licensed under the MIT License, the same as the [bark-gui](https://github.com/C0untFloyd/bark-gui) repository from which it was adopted.

## Acknowledgements

This installer is adapted from [bark-gui](https://github.com/C0untFloyd/bark-gui) by [C0untFloyd](https://github.com/C0untFloyd) and modified for Audiocraft. We thank the contributors of bark-gui for their work.

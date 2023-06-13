:: Batch File by https://github.com/C0untFloyd/bark-gui

@echo off
REM Please set the following commandline arguments to your prefered settings
set COMMANDLINE_ARGS=

cd /D "%~dp0"

echo "%CD%"| findstr /C:" " >nul && echo This script relies on Miniconda which can not be silently installed under a path with spaces. && goto end

set PATH=%PATH%;%SystemRoot%\system32

@rem config
set INSTALL_DIR=%cd%\libs
set CONDA_ROOT_PREFIX=%cd%\conda
set INSTALL_ENV_DIR=%cd%\env
set MINICONDA_DOWNLOAD_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
set conda_exists=F

@rem figure out whether git and conda needs to be installed
call "%CONDA_ROOT_PREFIX%\_conda.exe" --version >nul 2>&1
if "%ERRORLEVEL%" EQU "0" set conda_exists=T

@rem (if necessary) install git and conda into a contained environment
@rem download conda
if "%conda_exists%" == "F" (
	echo Downloading Miniconda from %MINICONDA_DOWNLOAD_URL% to %INSTALL_DIR%\miniconda_installer.exe

	mkdir "%INSTALL_DIR%"
	call curl -Lk "%MINICONDA_DOWNLOAD_URL%" > "%INSTALL_DIR%\miniconda_installer.exe" || ( echo. && echo Miniconda failed to download. && goto end )

	echo Installing Miniconda to %CONDA_ROOT_PREFIX%
	start /wait "" "%INSTALL_DIR%\miniconda_installer.exe" /InstallationType=JustMe /NoShortcuts=1 /AddToPath=0 /RegisterPython=0 /NoRegistry=1 /S /D=%CONDA_ROOT_PREFIX%

	@rem test the conda binary
	echo Miniconda version:
	call "%CONDA_ROOT_PREFIX%\_conda.exe" --version || ( echo. && echo Miniconda not found. && goto end )
)

@rem create the installer env
if not exist "%INSTALL_ENV_DIR%" (
  echo Packages to install: %PACKAGES_TO_INSTALL%
  call "%CONDA_ROOT_PREFIX%\_conda.exe" create --no-shortcuts -y -k --prefix "%INSTALL_ENV_DIR%" python=3.9  || ( echo. && echo Conda environment creation failed. && goto end )
)

@rem check if conda environment was actually created
if not exist "%INSTALL_ENV_DIR%\python.exe" ( echo. && echo Conda environment is empty. && goto end )

@rem activate installer env
call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" || ( echo. && echo Miniconda hook not found. && goto end )

@rem install ffmpeg if it not exists
call "%CONDA_ROOT_PREFIX%\_conda.exe" install -y -q -c conda-forge ffmpeg

@rem download the install.py or replace it with a newly downloaded version
set FILE_URL=https://raw.githubusercontent.com/D-Ogi/AI-LLM-StableDiffusion-Stuff/main/Audiocraft-Windows-OneClick-Installer/installer.py
set FILE_PATH=%INSTALL_DIR%\installer.py

call curl -Lk "%FILE_URL%" > "%FILE_PATH%" || ( echo. && echo File failed to download. && goto end )

@rem setup installer env
::echo Launching Audiocraft GUI - please edit windows_run.bat to customize commandline arguments
echo Launching Audiocraft GUI
call python installer.py %COMMANDLINE_ARGS%

echo.
echo Done!

:end
pause




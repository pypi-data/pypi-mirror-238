#!/usr/bin/bash

# set -eo # exit on error or undefined variable

# ensure the user is root
# if [ "$EUID" -ne 0 ]
  # then echo "Please run as root"
  # exit
# fi

# install dependencies if OS is ubuntu
# apt install -y python-is-python3 python3-pip # 2&>1 > /dev/null
# apt update # 2&>1 > /dev/null

# Store the current python version in a variable
python_version="python"$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1,2)

# If the .local directory is not on PATH, add it
if [[ ! ":$PATH:" == *":/home/$USER/.local/bin:"* ]]; then
    export PATH=/home/$USER/.local/bin:$PATH
    echo "export PATH=/home/$USER/.local/bin:$PATH" >> ~/.bashrc
fi

# If pip is not installed, install it
if ! command -v pip &> /dev/null
then
	echo "pip could not be found, installing..."
	sudo apt install -y python3-pip # 2&>1 > /dev/null
fi


# Install the mgtron package globally
pip install --user -U mgtron # 2&>1 > /dev/null

# if the icons directory does not exist, create it
if [ ! -d ~/.local/share/icons ]; then
  mkdir -p ~/.local/share/icons
fi

# if the applications directory does not exist, create it
if [ ! -d ~/.local/share/applications ]; then
  mkdir -p ~/.local/share/applications
fi

# Place the mgtron icon in icons folder
cp ~/.local/lib/${python_version}/site-packages/src/assets/mgtron.svg ~/.local/share/icons/ # 2&>1 > /dev/null

# Place the mgtron.desktop file in applications folder
cp ~/.local/lib/${python_version}/site-packages/src/assets/mgtron.desktop ~/.local/share/applications/ # 2&>1 > /dev/null

# Install the boot picture script
sudo bash ~/.local/lib/${python_version}/site-packages/src/assets/init_cellantenna.sh ~/.local/lib/${python_version}/site-packages/src/assets/CA_subheading.png  # 2&>1 > /dev/null

sudo usermod -a -G dialout $USER
sudo reboot

# Set the `mgtron` GUI to launch on boot
# mgtron

#!/usr/bin/env bash

# GTK app written in Python to control Waydroid settings
# 
# 1) Add options to clone the repo to ~/.local/share/waydroid-settings
# 2) Copy the Waydroid-Settings.sh file to ~/.local/bin/ and set it to be executable
# 3) Copy the waydroid-settings.desktop file to /home/<username>/.local/share/applications
SCRIPT_FILE=~/.local/share/waydroid-settings/waydroid-settings.sh
if test -f "$SCRIPT_FILE"; then
    echo "$SCRIPT_FILE exists."
else
	git clone --recurse-submodules https://github.com/axel358/Waydroid-Settings ~/.local/share/waydroid-settings
	git submodule init
	git submodule update
fi

cp ~/.local/share/waydroid-settings/waydroid-settings.sh ~/.local/bin/
sudo chmod +x ~/.local/bin/waydroid-settings.sh
cp ~/.local/share/waydroid-settings/waydroid-settings.desktop ~/.local/share/applications/

echo "All set. Thanks for installing."

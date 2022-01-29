#!/usr/bin/env bash

# GTK app written in Python to control Waydroid settings
# Run this installer to also update to the latest release
# 
# 1) Add options to clone the repo to ~/.cache/waydroid-settings/waydroid-settings
# 2) Move to /usr/share/waydroid-settings
# 2) Copy the Waydroid-Settings.sh file to /usr/bin/ and set it to be executable
# 3) Copy the waydroid-settings.desktop file to /usr/local/share/applications/

SCRIPT_FILE=/usr/share/waydroid-settings/waydroid-settings.sh
HPATH=$HOME

if test -f "$SCRIPT_FILE"; then
    echo "$SCRIPT_FILE exists."
else
	mkdir -p $HPATH/.cache/waydroid-settings
	cd $HPATH/.cache/waydroid-settings
	git clone --recurse-submodules https://github.com/axel358/Waydroid-Settings waydroid-settings
	cd waydroid-settings
	git submodule init
	git submodule update
	cd ..
	sudo mv waydroid-settings/ /usr/share/
fi

cp -f /usr/share/waydroid-settings/waydroid-settings.sh /usr/bin/
sudo chmod +x /usr/bin/waydroid-settings.sh
cp -f /usr/share/waydroid-settings/waydroid-settings.desktop /usr/local/share/applications/

echo "All set. Thanks for installing."

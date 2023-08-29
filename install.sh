#!/usr/bin/env bash

sudo cp -r usr/* /usr/
sudo chmod +x /usr/bin/waydroid-settings
sudo chmod +x /usr/bin/waydroid-helper
sudo update-desktop-database /usr/share/applications
sudo update-icon-caches /usr/share/icons/hicolor

#!/usr/bin/env bash

sudo rm -rf $HOME/.local/share/waydroid-settings /usr/share/waydroid-settings /usr/lib/waydroid-settings
sudo rm -f /usr/bin/waydroid-settings
sudo rm -f /usr/bin/waydroid-helper
sudo rm -f /usr/share/applications/waydroid-settings.desktop
sudo rm -f /usr/share/applications/install-to-waydroid.desktop
sudo rm -f /usr/share/icons/hicolor/512x512/apps/cu.axel.WaydroidSettings.png
sudo rm -f /usr/share/polkit-1/actions/org.freedesktop.policykit.waydroid-helper.policy

echo "Waydroid Settings has been uninstalled"

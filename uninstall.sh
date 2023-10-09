#!/usr/bin/env bash

# Check if the system is immutable and set directory variables.
if sudo touch /bin/testfile 2>/dev/null; then
    # System is not immutable
    sudo rm -f /bin/testfile
    bindir="/usr/bin"
    sharedir="/usr/share"
    applicationsdir="/usr/share/applications"
    polkitdir="/usr/share/polkit-1"
else
    # System is immutable
    bindir="$HOME/.local/bin"
    sharedir="$HOME/.local/share"
    applicationsdir="$HOME/.local/share/applications"
    polkitdir="/etc/polkit-1/"
fi

sudo rm -rf $HOME/.local/share/waydroid-settings /usr/share/waydroid-settings /usr/lib/waydroid-settings
sudo rm -f $bindir/waydroid-settings
sudo rm -f $bindir/waydroid-helper
sudo rm -f $applicationsdir/waydroid-settings.desktop
sudo rm -f $applicationsdir/install-to-waydroid.desktop
sudo rm -f $sharedir/icons/hicolor/512x512/apps/cu.axel.WaydroidSettings.png
sudo rm -f $polkitdir/actions/org.freedesktop.policykit.waydroid-helper.policy

echo "Waydroid Settings has been uninstalled"

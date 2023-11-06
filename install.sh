#!/usr/bin/env bash

# Check if the system is immutable and set directory variables.
if touch sudo /bin/testfile 2>/dev/null; then
    # System is not immutable
    sudo rm -f /bin/testfile
    maindir="/usr"
    bindir="/usr/bin"
    libdir="/usr/lib"
    sharedir="/usr/share"
    applicationsdir="/usr/share/applications"
else
    # System is immutable
    maindir="$HOME/.local/"
    bindir="$HOME/.local/bin"
    libdir="$HOME/.local/lib"
    sharedir="$HOME/.local/share"
    applicationsdir="$HOME/.local/share/applications"
fi

# Check if script is from cloned repo or just coppied from github
if [ -n "$(git config --get remote.origin.url)" ]; then
    echo
    echo "Cloned repo"
    CLONED=true
else
    echo
    echo "Copied from github"
    TEMPDIR=`mktemp -d`
    CLONED=false
fi

# If CLONED == false, then use git to clone the repo
if [ "$CLONED" = false ]; then
    echo "Cloning waydroid-settings..."
    git clone https://github.com/axel358/waydroid-settings.git $TEMPDIR
    cd $TEMPDIR
fi

echo
echo "Installing..."
sudo cp -r usr/* $maindir #what does this do
sudo chmod +x $bindir/waydroid-settings
sudo chmod +x $bindir/waydroid-helper
sudo update-desktop-database $applicationsdir
sudo update-icon-caches $maindir/icons/hicolor

# if scripts/* exist, then copy those to ~/.local/share/waydroid-settings
echo
echo "Copying scripts to ~/.local/share/waydroid-settings"

if [ -n "$(find scripts -maxdepth 1 -type f)" ]; then
    mkdir -p ~/.local/share/waydroid-settings
    mkdir -p ~/.local/share/waydroid-settings/scripts
    cp -r scripts/* ~/.local/share/waydroid-settings/scripts
else
    # curl each url in the .gitmodules file and copy to ~/.local/share/waydroid-settings
    git submodule update --init --recursive
    mkdir -p ~/.local/share/waydroid-settings
    mkdir -p ~/.local/share/waydroid-settings/scripts
    cp -r scripts/* ~/.local/share/waydroid-settings/scripts
fi

# if CLONEED == false, then cleanup ~/.local/share/waydroid-settings
if [ "$CLONED" = false ]; then
    echo
    echo "Cleaning up"
    rm -rf $TEMPDIR
fi

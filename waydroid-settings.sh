#!/usr/bin/env bash

if [ -d ~/.local/share/waydroid-settings ]; then
	cd ~/.local/share/waydroid-settings
	./waydroid-settings.py
elif [ -d /usr/share/waydroid-settings ]; then
	cd /usr/share/waydroid-settings
	./waydroid-settings.py
fi


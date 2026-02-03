#!/bin/bash

###Disable writing of .DS_Store files###
defaults write com.apple.desktopservices DSDontWriteNetworkStores true

###Find and remove all .DS_Store files###
find . -name .DS_Store -exec rm -r {} \;

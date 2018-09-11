#!/bin/bash
VERSION=$1
echo plugin_version=\"$1\" >lib/version.py
git add lib/version.py
git commit -m "creating build version $1"
git archive -o planningcenter_$VERSION.zip --prefix=planningcenter/ -9 HEAD

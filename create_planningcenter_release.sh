#!/bin/bash
VERSION=$1
if [ "$1" == "" ]
then
  echo "Syntax: ./create_planningcetnter_release.sh <VERSION>"
  exit 1
fi
echo plugin_version=\"$1\" >lib/version.py
git add lib/version.py
git commit -m "creating build version $1"
git tag "$1"
git archive -o planningcenter_$VERSION.zip --prefix=planningcenter/ -9 HEAD

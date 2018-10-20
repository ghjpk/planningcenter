#!/bin/bash
VERSION=$1
if [ "$1" == "" ]
then
    echo "Syntax: ./create_planningcetnter_release.sh <VERSION>"
    exit 1
fi

# Remember current branch and checkout master branch
branch=$(git symbolic-ref --short HEAD)
if ! [ $branch = "master" ]; then
    if ! git checkout master; then
        echo unable to checkout master branch
        exit 1
    fi
fi

# Get updated code
if ! git pull; then
    echo unable to pull latest code
    exit 1
fi

# set the version into the code and add it to git
echo plugin_version=\"$1\" >lib/version.py
git add lib/version.py
git commit -m "creating build version $1"
git archive -o planningcenter_$VERSION.zip --prefix=planningcenter/ -9 master
git add planningcenter_$VERSION.zip
git commit -m "adding the finished zip file to the repository"
git tag "$1"

git push

if ! [ $branch = "master" ]; then
    git checkout $branch
fi

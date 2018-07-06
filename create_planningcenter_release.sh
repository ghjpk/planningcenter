#!/bin/bash
VERSION=$1
git archive -o planningcenter_$VERSION.zip --prefix=planningcenter/ -9 HEAD

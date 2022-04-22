#!/bin/bash

# add this to crontab

FNAME="updates.txt"
DATE=`date`

pushd ~/workspace
touch $FNAME
echo $DATE > $FNAME
git add .
git commit -m "$DATE"
git push origin master
popd

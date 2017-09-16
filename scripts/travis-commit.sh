#!/bin/bash

set -ev

git checkout master
python scripts/get_facebook_events.py

if [[ -n "$(git status -s)" ]]; then
    git add .
    git commit -m "Updating events from Facebook"
    git push git@github.com:adicu/adi-static master
fi

#!/bin/bash

# 1) Run les scrapers
echo "[Run Nitrogen Scraper]"
if ! timeout 1s xset q &>/dev/null; then
    echo "No X server detected. Running with XVFB"
    node nitrogen/main.js --xvfb
else
    node nitrogen/main.js
fi

# 2) Corrélations
echo "[Find correlation with GoL Data]"
pipenv run python gol/gol.py

# 3) Maths
echo "[Do the maths and export]"
exit

# 4) Git
echo "[Commit and Push]"
git add data/* 
git commit -m "$(date +'Daily data update %m-%d-%Y')"
# git push
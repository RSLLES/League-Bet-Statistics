#!/bin/bash

# 0) Update
# Stash here ton ensure there is no merge conflicts with run_whole_pipeline
git stash
git pull
git stash pop

# 1) Run les scrapers
echo "[Run Nitrogen Scraper]"
if ! timeout 1s xset q &>/dev/null; then
    echo "No X server detected. Running with XVFB"
    node nitrogen/main.js --xvfb --path=/usr/bin/chromium-browser
else
    node nitrogen/main.js
fi

# 2) Corrélations
echo "[Find correlation with GoL Data]"
python3 -m pipenv run python gol/gol.py

# 3) Maths
echo "[Do the maths]"
python3 -m pipenv run python trends/compare.py

# 4) Git
echo "[Commit and Push]"
git add data/data_unmatched.json
git add data/id_history.json
for f in data/processed/*
do
    git add $f
done

for f in trends/best_selectors/*
do
    git add $f
done
git commit -m "$(date +'Daily data update %m-%d-%Y')"
git push
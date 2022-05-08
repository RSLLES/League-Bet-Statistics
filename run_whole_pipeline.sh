#/bin/bash

# 1) Run les scrapers
echo "[Run Nitrogen Scraper]"
node nitrogen/main.js

# 2) Corrélations
echo "[Find correlation with GoL Data]"
pipenv run python gol/gol.py

# 3) Maths
echo "[Do the maths and export as README.md]"
exit

# 4) Git
echo "[Commit and Push]"
git commit -a README.md
git push
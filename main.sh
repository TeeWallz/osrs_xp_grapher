#!/bin/bash

cd /home/tom/git/home/osrs_xp_grapher/
source venv/bin/activate
python main.py

git rm --cached levels.png
git reset levels.png

git add -A
git commit -m "New Level"
git push

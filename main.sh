#!/bin/bash

source venv/bin/activate
python main.py

git add -A
git commit -m "New Level"
git push
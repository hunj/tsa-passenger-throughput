#!/bin/bash

git add output.csv
git commit -m ":octocat: Update data $(date +%m/%d/%Y)"
git push origin main

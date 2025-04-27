# Developer/Maintainer Cheatsheet

Hello! This is a beginner-friendly guide specifically for developers/maintainers (currently just Eldiiar Bekbolotov) to run the program on their device.

## Local Setup

Guide for: Visual Studio Code on Mac

### Mac: Seting up Virtual Environment and Installation

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`python app.py`

### Mac: Deactivate Virtual Environment and Push Files

`deactivate`

`rm -rf venv/`

`rm -rf __pycache__`

Push files:
`git add .`

`git rm --cached .env`

`git commit -m "Add version/commit msg"`

`git push origin main`

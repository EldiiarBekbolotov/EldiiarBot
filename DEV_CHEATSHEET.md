# Developer/Maintainer Cheatsheet

Interested in contributing to this project? Let me know in the Discussions tab on the GitHub repository.

This is a _beginner-friendly guide_ specifically for developers/maintainers (currently just Eldiiar Bekbolotov) to run EldiiarBot on their device.

Note that all code dependant on environmental variables or secret files will not work locally because they are stored in cloud (e.g. Render, Supabase). Therefore, you will be primarily editing the website, Flask routes, and other non-environmental variable scripts.

## Local Setup

## What you need

_Python 3.8+_: Ensure Python is installed. Run `python3 --version` (macOS) or `python --version` (Windows) to check.

_Git_: Install Git for version control. Verify with `git --version`.

# Guide for: Visual Studio Code on Mac

### Mac: Seting up Virtual Environment and Installation

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`python app.py`

### Mac: Deactivate Virtual Environment

`deactivate`

`rm -rf venv/`

`rm -rf __pycache__`

### Push to GitHub

Push files:
`git add .`

`git rm --cached .env`

`git commit -m "Add version/commit msg"`

`git push origin main`

# Guide for: Visual Studio Code on Windows

### Windows: Seting up Virtual Environment and Installation

`python -m venv venv`

`venv\Scripts\activate`

`pip install -r requirements.txt`

`python app.py`

### Windows: Deactivate Virtual Environment

`deactivate`

`rmdir /s /q venv`

`rmdir /s /q __pycache__`

### Push to GitHub

Push files:
`git add .`

`git rm --cached .env`

`git commit -m "Add version/commit msg"`

`git push origin main`

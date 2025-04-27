# Developer/Maintainer Cheatsheet

## Local Setup

Mac:
`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`python app.py`

and once you're done
`deactivate`
`rm -rf venv/`
`rm -rf __pycache__`
`git add .`
`git commit -m "Add version/commit msg"`
`git push origin main`

# streamlit-custom-component

Streamlit component that allows you to play MIDI.

## Installation instructions

```sh
pip install streamlit-pianoroll
```

## Usage instructions

```python
import streamlit as st

from pianoroll_streamlit import pianoroll

st.write("This is a pianoroll!")

pianoroll()
```


## Development instructions

* Initialize and run the component template frontend:
```
$ cd pianoroll_streamlit/frontend
$ npm install    # Install npm dependencies
$ npm run start  # Start the Webpack dev server
```
* From a separate terminal, run the template's Streamlit app:
```
$ cd template
$ . venv/bin/activate  # activate the venv you created earlier
$ pip install -e . # install template as editable package
$ streamlit run pianoroll_streamlit/example.py  # run the example
```
* If all goes well, you should see something like this:


### Code Style

This repository uses pre-commit hooks with forced python formatting ([black](https://github.com/psf/black),
[flake8](https://flake8.pycqa.org/en/latest/), and [isort](https://pycqa.github.io/isort/)):

```sh
pip install pre-commit
pre-commit install
```

Whenever you execute `git commit` the files altered / added within the commit will be checked and corrected.
`black` and `isort` can modify files locally - if that happens you have to `git add` them again.
You might also be prompted to introduce some fixes manually.

To run the hooks against all files without running `git commit`:

```sh
pre-commit run --all-files
```

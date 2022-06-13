# Rock, Paper, Scissors... And How

Hello. If you've arrived here, you may be either wanting to play a Rock, Paper, Scissors game, or see how to create one using Python. If either (or both) of those things are correct, then you're in the right place.

This game is built on FastAPI. It allows two players (or one vs a computer) to engage in a friendly game of Rock, Paper, Scissors and can be played through a web browser.

## Install

To start, fork the repository from source. Then, clone (or download) the fork locally.

Navigate to your local repository at the project root. Something like:

```
cd rps-game
```

## Setup Project

Create and activate a new virtual environment. It will be some variation of this, depending on operating system:

```
python -m venv .venv
.venv/Scripts/activate
```

Make sure that your virtual environment is activated, then install the dependencies:

```
python -m pip install -r requirements.txt
```

## Give It A Spin

You can run a FastAPI application locally by using uvicorn. It will run in your local host, aka http://localhost:8000/

The uvicorn command is the following:

```
uvicorn app.main:app --reload
```

The `--reload` flag will refresh the page any time you make changes to the code base.


## License
MIT
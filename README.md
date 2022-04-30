# pong_game
Multiplayer (4 player over network) ping pong game

![example workflow](https://github.com/vkmrishad/loan_app/actions/workflows/black.yaml/badge.svg)
![example workflow](https://github.com/vkmrishad/loan_app/actions/workflows/django-ci.yaml/badge.svg)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Clone

    git clone https://github.com/vkmrishad/pong_game.git
    or
    git clone git@github.com:vkmrishad/pong_game.git

## Environment and Package Management
Install Poetry

    $ pip install poetry
    or
    $ pip3 install poetry

Activate or Create Env

    $ poetry shell

Install Packages from Poetry

    $ poetry install

NB: When using virtualenv, install from `$ pip install -r requirements.txt`.

## Runserver
First need to run `server.py`

    $ python3 server.py

After that run app in 4 terminals (Should run 4 games to start)

    $ python3 run.py

## Vesrio

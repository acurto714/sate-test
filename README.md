# sate-test

This is a django application developed as a technical interview for the satellogic company.

## How to start
Let's assume that you have `pyenv` installed on our machine (if not, you can do it by following these steps)

```bash
pyenv virtualenv 3.7.8 satellogic
pyenv activate satellogic
make install
make migrate
make run
```

and that's it, you already have your django app running. Time to try it!

## How to test
In the examples directory you can find several test files.

## About highest profit tasks selector algorithm
TBD


## Some devs tools
The environment installed in the first step corresponds to a developer env. It's possible to handle everything from a Makefile.
These settings include: flake8, black, pytest, coverage, and pre-commit.


## Some possible improvements
1. Load file and enqueue job to search the optimus schedule. Return an ID to be able search the result.



## TODO list
* logs
* docker image and docker compose
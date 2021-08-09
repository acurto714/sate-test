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
Below are some tests/improvements that could be done but that for time reasons weren't made in this first version.

1. Use a jobs queue: when uploading the file, new job is queued to process it in background and only an ID is returned.
So, that later it's possible to search for the result by the ID.
1. Add download result possibility.
1. Try another faster algorithm, especially for large cases (maybe in C?).
1. Use docker to make the code more portable.
1. Use swagger to facilitate the interface with the APIs.

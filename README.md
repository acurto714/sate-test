# sate-test

This is a django application developed as a technical interview for the satellogic company.

## How to start
Let's assume that you have `pyenv` installed on our machine (if not, you can do it by following [these](https://github.com/pyenv/pyenv) steps)

```bash
pyenv virtualenv 3.7.8 satellogic
pyenv activate satellogic
make install
make migrate
make run
```

and that's it, you already have your django app running. Time to try it!

## How to test
In the [examples](examples/) directory you can find several test files.

## About highest profit tasks selector algorithm
Algorithms for combinatorial optimizations, operations research, optimization problem, scheduling and other branches of problem solving were analyzed.
In this research an algorithm called: **Maximal weighted independent set** was found. This is a variant of `Maximal independent set` that considers the weights of the nodes.
In summary, the algorithm looks for the largest sub-set of independent nodes (that is, there is no edge between any pair of nodes in the set) that maximize the weight of the nodes.
Looking for implementations of this algorithm in python, it was found that the function [max_weight_clique](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.max_weight_clique.html) from the [networkx](https://networkx.org/documentation/stable/index.html) library was approaching the resolution of the problem, the difference is that this algorithm looked for adjacent nodes. A test was performed reversing this condition and the algorithm worked correctly. For this reason that the networkx implementation was extended with the minimal changes required for this problem.

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

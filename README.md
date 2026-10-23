# ia

Solutions for the practical guides of Inteligência Artificial / Sistemas Inteligentes I
(Universidade de Aveiro). The original materials are in Portuguese; everything produced
here (code comments, docstrings, docs) is in English.

## Layout

- `theory/`: lecture slides (PDF).
- `practice/exNN/`: one folder per guide, with the guide PDF, solutions and tests.
- `requirements.txt`: Python dependencies for all exercises.
- `Makefile`: creates the virtual environment and runs the tests.

## Virtual environment

The venv lives at the repository root in `./venv` and is never activated:
every command calls `venv/bin/python` explicitly.

```bash
make venv    # python3 -m venv venv && venv/bin/python -m pip install -r requirements.txt
make test    # runs pytest inside each exercise folder with venv/bin/python
make clean   # removes venv and pytest caches
```

To run one exercise by hand: `cd practice/ex01 && ../../venv/bin/python -m pytest -q`.

## Exercises

- `practice/ex01`: Guide 1, programming in Python in functional style
  (recursion, lambda expressions, higher-order functions, sorting, classes).
  Practical guide: [`practice/ex01/guiao-prog.pdf`](practice/ex01/guiao-prog.pdf).
- `practice/ex02`: Guide 2, automated problem solving (tree search with
  breadth-first/depth-first/depth-limited/uniform-cost/greedy/A* strategies,
  STRIPS planning in the blocks world, and constraint-based search for
  assignment problems with forward checking; this is not the full AC-3
  propagation of the slides, the pinned test numbers require it).
  Practical guides: [`practice/ex02/guiao-pesquisa-en.pdf`](practice/ex02/guiao-pesquisa-en.pdf)
  (English), [`practice/ex02/guiao-pesquisa.pdf`](practice/ex02/guiao-pesquisa.pdf) (Portuguese).

# Advent of Code

Coding challenges solved for [Advent of Code](https://adventofcode.com).

- [AoC 2022](2022): 49/50 solved.
- [AoC 2023](2023): 27/50 solved
- [AoC 2024](2024): WIP

### Setup

To use the `makefile` for setting up the daily challenge, first: create a file called `sessionid` and add a single line with your session id - you can get this by inspecting the Advent of Code cookies in your browser (right-click -> Inspect -> Storage -> Cookies).

Run `make files year=X day=Y` to get the input for year X, day Y and create code files based on the template.

Using pre-commit hooks:

```
pip install black
pip install pre-commit
pre-commit install
```

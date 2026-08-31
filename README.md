*This activity has been created as part of the 42 curriculum by naldibis, labdalla.*

# A_maze_ing

A configurable maze generator, solver and visualizer written in Python. The program reads its parameters from a plain-text configuration file, generates a maze of the requested dimensions, computes the shortest path between the entry and the exit, writes the result to a text file, and renders the whole thing in a graphical window using the MLX library.

---

## Description

The goal of the project is to build a complete maze pipeline, from configuration to visual output, while keeping each stage independent from the others.

The program is split into four stages that communicate through well-defined data rather than shared state:

1. **Configuration** — reads and validates `config.txt`, exposing every setting through a single `Configuration` class.
2. **Generation** — builds a maze with an iterative depth-first search with backtracking, then optionally braids it into an imperfect maze.
3. **Solving** — finds the shortest path from entry to exit with a breadth-first search and encodes it as a string of cardinal moves.
4. **Display** — renders the maze, the entry and exit markers, the solution path and the on-screen controls in an MLX window.

Two details are worth pointing out:

- Every maze large enough (at least 9x9) has the **"42" symbol carved into its center**. Those cells are locked before generation starts and are never touched again, so the symbol survives both the DFS carving pass and the braiding pass.
- The maze is stored in a **compact hexadecimal format**, one character per cell, which makes the output file readable by any other program without needing to know anything about our internal classes.

### Maze output format

The generator writes the maze as a grid of hexadecimal digits. Each cell is a 4-bit mask of its walls, where a bit set to `1` means the wall is present:

| Wall  | Bit | Value |
|-------|-----|-------|
| North | 0   | 1     |
| East  | 1   | 2     |
| South | 2   | 4     |
| West  | 3   | 8     |

A cell with value `9` (`1001`) therefore has its north and west walls standing, and is open to the east and south. `F` is a fully closed cell, `0` a fully open one.

The output file produced by a run looks like this:

```
9139139153
A86A846A96
AC568156C3
83F906FFFA
AAFC4157FA
AAFFFAFFFA
C413FAFD52
956AFAFFFA
A952903952
C45446C456

0, 0
9, 9
SSSESSSEESSSEENESEEE
```

The grid is followed by a blank line, the entry point, the exit point, and the solution path encoded as a string of `N`, `E`, `S`, `W` moves.

---

## Instructions

### Requirements

- Python 3.10 or later.
- Two wheels, both shipped with the repository:
  - `mlx-2.2-py3-none-any.whl`, the graphics library provided by 42.
  - `mazegen-1.0.0-py3-none-any.whl`, our own maze generator, built from `maze_generation.py` through `setup.py`.

### Installation and execution

```bash
make run        # installs if needed, then runs the program
```

Or manually:

```bash
pip install mlx-2.2-py3-none-any.whl
pip install mazegen-1.0.0-py3-none-any.whl
python3 a_maze_ing.py config.txt
```

The program takes exactly one argument and it must be `config.txt`. Any other invocation prints the usage line and exits.

### Available make targets

| Target        | Effect                                                                 |
|---------------|------------------------------------------------------------------------|
| `install`     | Installs the MLX wheel and the `mazegen` wheel                          |
| `run`         | Installs the wheel then runs the program on `config.txt`                |
| `debug`       | Runs the program under `pdb`                                            |
| `clean`       | Removes `__pycache__` directories and the mypy cache                    |
| `lint`        | Runs `flake8`, then `mypy` with untyped-definition and return checks    |
| `lint-strict` | Runs `flake8`, then `mypy --strict`                                     |

### Controls

Once the window is open:

| Key | Action                                  |
|-----|-----------------------------------------|
| `Q` | Quit and close the window               |
| `R` | Regenerate a new maze and solve it      |
| `S` | Show or hide the solution path          |
| `C` | Cycle through the three color themes    |

Both lower and upper case are accepted.

---

## Configuration file

The configuration file is a list of `KEY = VALUE` pairs, one per line. Empty lines are ignored, and any line starting with `#` is treated as a comment. Spaces around the `=` sign are stripped, so `WIDTH=10` and `WIDTH = 10` are equivalent.

```
# Default Config.txt
WIDTH = 10
HEIGHT = 10
ENTRY = 0,0
EXIT = 9,9
OUTPUT_FILE = maze.txt
PERFECT = False
# You can either enter a seed as an int value or leave it blank or
# zero to have a different maze every time you regenerate
SEED = 0
```

### Keys

| Key           | Type            | Constraints                                                              |
|---------------|-----------------|--------------------------------------------------------------------------|
| `WIDTH`       | integer         | Between 1 and 55 inclusive                                                |
| `HEIGHT`      | integer         | Between 1 and 35 inclusive                                                |
| `ENTRY`       | `x,y` integers  | Must be inside the grid, and must differ from `EXIT`                      |
| `EXIT`        | `x,y` integers  | Must be inside the grid, and must differ from `ENTRY`                     |
| `OUTPUT_FILE` | string          | Path of the file the maze is written to                                   |
| `PERFECT`     | `True`/`False`  | `True` yields a perfect maze, `False` braids it into an imperfect one     |
| `SEED`        | integer         | A non-zero value makes generation reproducible; `0` randomizes every run  |

The upper bounds on `WIDTH` and `HEIGHT` are not arbitrary. Each cell is drawn as a 26x26 pixel tile inside a 1920x1080 window, so 55x35 is the largest grid that still fits on a 42 workstation screen alongside the controls panel.

Coordinates follow the `x,y` convention where `x` is the column and `y` is the row, both zero-based and counted from the top-left corner.

### Validation

The configuration is rejected, with an explicit message, when:

- a line is not a well-formed `KEY = VALUE` pair;
- the same key appears twice;
- fewer than six recognized keys are present;
- `PERFECT` holds anything other than `True` or `False`;
- `WIDTH` or `HEIGHT` is not a positive integer, or exceeds its maximum;
- `ENTRY` or `EXIT` falls outside the grid;
- `ENTRY` and `EXIT` are the same cell;
- `ENTRY` or `EXIT` lands on a cell reserved for the "42" symbol.

---

## Technical choices

### Generation: iterative depth-first search with backtracking

The maze starts as a full grid of cells with all four walls standing. A random starting cell is picked, and the algorithm repeatedly walks to a random unvisited neighbour, breaking the wall between the two cells and pushing the new cell onto a stack. When the current cell has no unvisited neighbours left, the algorithm pops the stack and resumes from the previous cell. The process ends when every cell has been visited.

**Why this algorithm.** Three reasons drove the choice:

1. **It fits the "42" constraint naturally.** The symbol is drawn first by marking its cells as `visited` and `is_42`. Because DFS only ever carves into cells it has not visited, and because `break_wall` refuses to modify a cell flagged `is_42`, the symbol is protected without a single special case in the carving loop itself. An algorithm such as Kruskal's or Prim's, which reason about edges and sets rather than a walk, would have needed explicit exclusion logic threaded through the whole implementation.
2. **The mazes it produces look good.** DFS is biased towards long, winding corridors with few short dead ends, which is visually far more interesting than the short, bushy corridors produced by Prim's algorithm.
3. **It is written iteratively rather than recursively.** At the maximum size of 55x35 the recursion depth could reach 1925 frames, which is uncomfortably close to Python's default limit. Managing the stack explicitly removes the problem entirely and keeps memory usage predictable.

### Imperfect mazes: braiding

When `PERFECT = False`, a second pass sweeps the grid and looks for cells with exactly three standing walls, which are precisely the dead ends. For each one, a random direction is chosen and the corresponding wall is broken, provided the neighbour exists and is not part of the "42" symbol. The sweep is repeated several times, since breaking one wall can turn a neighbouring cell into a new dead end.

The result is a maze with loops and multiple routes between any two points, which makes the pathfinding stage meaningful: a solver on a perfect maze has no choice to make, while on a braided maze it has to prove the path it returns is actually the shortest one.

### Solving: breadth-first search

The solver explores the maze level by level from the entry point, using a queue and a `parent_map` that records which cell each newly discovered cell was reached from. Movement between two adjacent cells is only allowed when the wall separating them has been broken, which is read directly from the `Cell` wall flags.

**Why this algorithm.** On an unweighted grid, BFS is guaranteed to find a shortest path, and it finds it the first time it reaches the exit. That guarantee matters here because braided mazes contain several valid routes, and the project asks for the shortest. DFS would return a valid path but rarely the shortest one, and A\* would only pay off on grids far larger than 55x35, at the cost of a heuristic that has to be justified. BFS gives the correct answer with no tuning.

Once the exit is reached, the solver walks the `parent_map` backwards to reconstruct the cell sequence, then converts each consecutive pair of coordinates into a single character (`N`, `E`, `S`, `W`) by looking at their difference. The resulting string is what gets written to the output file and what the display module replays tile by tile.

### Display

The renderer maps every hexadecimal character to a pre-rendered 26x26 PNG tile, so drawing a maze is a matter of reading the output file and blitting one image per character. The grid is horizontally centered inside the window based on its width, and the solution path is drawn with a short delay between tiles so the route is animated rather than appearing all at once.

---

## Reusability

The reusable component is **`maze_generator.py`**, which contains the `Cell` and `MazeGenerator` classes.

It is a genuinely standalone module: it imports nothing from `configuration`, `algorithm` or `graphical_display`, and depends only on Python's standard `random`. Every parameter it needs is passed to its constructor, and it never reads a file, prints to the screen, or reaches into global state.

To make that independence concrete rather than merely claimed, the module is **packaged and distributed as a wheel**. A `setup.py` at the root declares it as the sole distributable module, and `make install` installs the built `mazegen-1.0.0-py3-none-any.whl` alongside MLX. The rest of the project then consumes it exactly the way any third-party user would, through a plain `import`, which means a broken dependency on our internals would fail loudly instead of going unnoticed.

Building the wheel from source:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=55,
    height=35,
    entry={"x": 0, "y": 0},
    exit={"x": 54, "y": 34},
    perfect=False,
    seed=1,
)

maze = generator.generate_paths(seed=1)   # returns the grid as list[list[Cell]]
generator.maze_output("output.txt")       # writes the hexadecimal representation
```

Running `python3 maze_generator.py` directly executes a small demo `main()` that generates a 55x35 maze and writes it to `output.txt`, which makes the module testable in isolation without launching the graphical window.

Two design decisions make it portable to another project:

- **The output format is a contract, not an implementation detail.** Any consumer that understands the four-bit wall encoding can use the generated file without importing our classes at all. That is exactly how the display module consumes it.
- **Every public method returns data instead of causing side effects.** `generate_paths` returns the grid, `get_hexa` returns a character, `has_neighbours` returns a boolean. The only method that touches the filesystem is `maze_output`, and it is optional.

The `configuration` package is reusable in a narrower sense: the parsing helpers in `configuration_utils.py` handle any `KEY = VALUE` file with comment support, and adapting them to a different project is a matter of changing the class attributes and the validation rules.

---

## Project structure

```
.
├── a_maze_ing.py                    Entry point, argument handling, orchestration
├── maze_generation/                 Standalone reusable module: Cell, MazeGenerator
│   ├── maze_generator.py             
├── setup.py                         Packaging metadata for the mazegen wheel
├── Makefile
├── LICENSE.md                       MIT license
├── config.txt                       Default configuration
├── mlx-2.2-py3-none-any.whl
├── mazegen-1.0.0-py3-none-any.whl   Built distribution of maze_generation.py
├── configuration/
│   ├── __init__.py            Exports Configuration and ConfigError
│   ├── configuration.py       Configuration class, loading and validation
│   └── configuration_utils.py Parsing, type conversion, bounds checking
├── algorithm/
│   ├── __init__.py            Exports run
│   └── find_paths.py          BFS solver and the run() orchestrator
├── graphical_display/
│   ├── __init__.py            Exports display_output
│   ├── display.py             MLX window, rendering, key hooks
│   └── display_utils.py       Theme and control image tables
└── images/
    ├── first_set/             Theme 1 tiles
    ├── second_set/            Theme 2 tiles
    ├── third_set/             Theme 3 tiles
    └── controls/              On-screen control legend
```

---

## Additional features


- **Three color themes.** Each theme is a complete set of wall tiles plus its own background, entry, exit and path sprites, cycled at runtime with `C`.
- **Animated path drawing.** The solution is drawn one tile at a time rather than instantly.
- **Packaged generator.** The generator ships as an installable wheel rather than a loose file, so its independence from the rest of the project is enforced by the import system.

---

## Team and project management

### Roles

| Member     | Responsibility                                                                 |
|------------|---------------------------------------------------------------------------------|
| `labdalla` | Configuration system: file parsing, type conversion, validation rules, error handling |
| `naldibis` | Pathfinding: the BFS solver, path reconstruction and the move-string encoding    |

Everything else, including the maze generation algorithm, the "42" symbol, the braiding pass, the graphical display, the themes, the keyboard controls and the tooling, was written jointly.

### Planning and how it evolved

We planned the project as four sequential stages, each on its own branch, merged into `main` through a pull request once it worked in isolation:

```
config  ->  maze_generation  ->  search_algo  ->  visual_representation
```

The order was deliberate. Configuration had to come first because everything downstream depends on the parameters it produces; generation before solving because there is nothing to solve otherwise; display last because it consumes the output of all three.

The plan mostly held, but three things changed along the way:

1. **The generator was extracted into a standalone module partway through.** It initially lived alongside the rest of the code and imported from `config` directly. The reusability requirement pushed us to cut that dependency and pass every parameter explicitly through the constructor, which turned out to be a better design regardless of the requirement.
2. **Braiding was not in the original plan.** We started by building only perfect mazes. Adding imperfect mazes came later, once we realized that a shortest-path solver on a perfect maze is not really demonstrating anything, since there is only one route to find.
3. **The window resolution was revised.** The display was first written for a 2560x1440 layout and had to be brought down to 1920x1080 to match the actual screens in the cluster, which is also what fixed the maximum maze dimensions at 55x35.
4. **Packaging came at the end.** Turning the generator into a distributable wheel was not part of the initial plan. Doing it forced us to rename the `config` package to `configuration`, since the shorter name was too generic to sit safely at the top level of a distribution, and it confirmed that the module really had no hidden dependencies on the rest of the code.

### What worked well

- **Branch per stage with pull requests.** Reviewing each other's code before merging caught problems early and meant neither of us was ever blocked by the other's unfinished work.
- **The hexadecimal output format as an interface.** Because the display reads a file rather than our objects, the rendering work could proceed against a hand-written maze file before the generator was finished.
- **Seeding.** Being able to reproduce an exact maze turned intermittent visual glitches into deterministic, debuggable failures.
- **Linting from the start.** Running `flake8` and `mypy` continuously, rather than cleaning up at the end, kept the codebase consistent between two authors with different habits.

### What could be improved

- **Image loading is not cached.** Every redraw re-reads each PNG from disk through `mlx_png_file_to_image`, which is noticeably slow on large mazes. Loading each tile once into a dictionary at startup would fix it.
- **There are no automated tests.** Verification was done by inspection and by eye. A small test suite over the generator and the solver, using fixed seeds, would have been cheap to write and would have caught regressions faster.

### Tools

- **Git and GitHub** — feature branches, pull requests and code review between the two of us.
- **MLX** — the graphics library used for the window and image rendering.
- **flake8** — style and lint checking, enforced through `make lint`.
- **mypy** — static type checking, including a `--strict` target.
- **pdb** — interactive debugging through `make debug`.
- **Make** — a single entry point for installing, running, cleaning and checking the project.
- **setuptools and build** — used to package the generator into the `mazegen` wheel from `setup.py`.

---

## Resources

### Maze generation and pathfinding

- Wikipedia, *Maze generation algorithm*: <https://en.wikipedia.org/wiki/Maze_generation_algorithm>
- Wikipedia, *Breadth-first search*: <https://en.wikipedia.org/wiki/Breadth-first_search>
- Youtube, *Create Wheel Files in Python*: <https://www.youtube.com/watch?v=AM2dgUAdwaQ>

### Use of AI

AI was only used to generate this README.md file, help with docstrings and give resources.

---

## License

This project is released under the MIT License. See [LICENSE.md](LICENSE.md).

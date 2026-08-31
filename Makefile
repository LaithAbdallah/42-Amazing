install:
	pip install -q mlx-2.2-py3-none-any.whl
	pip install -q mazegen-1.0.0-py3-none-any.whl

run: install
	python3 a_maze_ing.py config.txt


debug:
	python -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .mypy_cache

lint:
	flake8 . 
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict
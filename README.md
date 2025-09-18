Radiant Crystal
===============

Minimal instructions to run the project locally.

Prerequisites
-------------
- Python 3.9+ (project was developed with CPython 3.9)
- Install dependencies:

PowerShell
```
python -m pip install -r requirements.txt
```

How to run
----------
Run the main script from the project root:

PowerShell
```
python "RadiantCrystal.py"
```

Run tests
--------
Create and activate a virtual environment, then run tests with unittest:

PowerShell
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -v
```

Notes
-----
- Many modules are still stubs or partially implemented. See `Player.py` and `CombatController.py` for working minimal implementations.
- Consider running inside a virtualenv.

Next steps
----------
- Add an `EventHandler` module and wire input through a central controller.
- Convert project into a package and use relative imports for reliability.
- Add unit tests and CI.

Continuous integration
----------------------
A GitHub Actions workflow is included at `.github/workflows/python-tests.yml` which runs the unit tests on push and pull requests.

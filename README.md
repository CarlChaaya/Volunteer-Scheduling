# Volunteer Workforce Scheduler

Constraint-programming tool that builds balanced volunteer rosters for the Lebanese Red Cross. The optimisation model is powered by Google OR-Tools CP-SAT and paired with a lightweight Tkinter GUI for non-technical coordinators.

## Features
- Enforces operational constraints (roles per shift, trainer coverage, single shift per rescuer)
- Handles preference scoring to maximise satisfied requests while avoiding unwanted shifts
- Randomised tie-breaking to produce multiple valid rosters for manual review
- Exports schedules to Excel using the template in `Rescuers_Sample.xlsx`

## Quick Start
```bash
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
python main.py
```

The GUI accepts an input workbook that follows the schema illustrated in the sample file. Update the volunteer list, roles, and preference columns before generating a new roster.

## Roadmap
- Package the optimiser as a CLI for batch processing
- Add automated test coverage for constraint regression
- Integrate email notifications once a schedule is published
- Containerise the app for deployment on internal infrastructure

Please open an issue if you encounter feasibility problems or would like additional constraints to be supported.

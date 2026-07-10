# OpenCode Agent Instructions

This repository contains rotor dynamics simulations using the `ross` library.

## Project Structure
- **Core Logic:** Python scripts (`*.py`) run the simulations.
- **Data:** `rotor_model_lpco2.toml` is an auto-generated model file. Do not manually edit this file as it is managed by the `ROSS` library.

## Workflow
- There are no standard web/application build tools.
- Simulations are executed by running the individual Python scripts (e.g., `python modelo_lpco2.py`).
- Any modifications to the rotor model should be done in the Python code itself, which then generates or updates the TOML files.

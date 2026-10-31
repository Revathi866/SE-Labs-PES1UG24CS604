# Lab 6 — Museum Admission

**Lab 6: Code and Branch Coverage Analysis**

## About

This project focuses on analysing and improving test coverage for a Python-based Museum Admission system.

The application provides three main functionalities:

- **Ticket Pricing:** Calculates ticket prices based on visitor category, age, day of the week, and guided tour selection.
- **Group Discounts:** Calculates discounts based on group size and whether the group is a school group.
- **Gallery Entry:** Determines whether visitors can enter, wait, or join a queue based on gallery capacity and timed slot availability.

## Project Structure

| File | Description |
|---|---|
| `museum_admission.py` | Main application module containing ticket pricing, group discount, and gallery entry functions. |
| `test_museum_admission.py` | Original starter test cases provided in the assigned repository. |
| `CodeCoverageTest_54_museum_admission.py` | Additional test cases written to achieve high code coverage. |
| `BranchCoverageTest_54_museum_admission.py` | Test cases designed to cover both outcomes of conditional branches. |
| `screenshots/` | Contains terminal screenshots of the code coverage and branch coverage reports. |

## Tools and Technologies

- Python 3.13.1
- pytest
- coverage.py

## Coverage Analysis

The application was tested using Python's `coverage` tool and `pytest`.

### 1. Code Coverage

Command used:

```bash
coverage run --source=museum_admission -m pytest -v CodeCoverageTest_54_museum_admission.py
coverage report -m
```

**Result: 100% Code Coverage**

- Total statements: 36
- Missing statements: 0
- Tests passed: 18

### 2. Branch Coverage

Command used:

```bash
coverage run --branch --source=museum_admission -m pytest -v BranchCoverageTest_54_museum_admission.py
coverage report -m
```

**Result: 100% Branch Coverage**

- Total statements: 36
- Missing statements: 0
- Total branches: 28
- Partially covered branches: 0
- Tests passed: 19

Both coverage targets exceed the minimum requirement of 90%.

## Screenshots

The `screenshots/` folder contains:

- `code_coverage.png` — Terminal output showing 100% code coverage.
- `branch_coverage.png` — Terminal output showing 100% branch coverage.

## Installation and Execution

Install the required dependencies:

```bash
pip install coverage pytest
```

Run the code coverage tests:

```bash
coverage erase
coverage run --source=museum_admission -m pytest -v CodeCoverageTest_54_museum_admission.py
coverage report -m
```

Run the branch coverage tests:

```bash
coverage erase
coverage run --branch --source=museum_admission -m pytest -v BranchCoverageTest_54_museum_admission.py
coverage report -m
```

## Original Assigned Repository

The original application and starter test files were provided in the following repository:
https://github.com/SETAPESU26/L6_L7_54_museum_admission/tree/main/LAB6

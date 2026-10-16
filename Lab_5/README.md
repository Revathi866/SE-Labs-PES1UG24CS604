# Lab 5 — Static Code Analysis

## Overview

This lab focuses on improving the code quality, formatting, and security of a Python-based warehouse stock management program. Three static analysis tools — Pylint, Bandit, and Flake8 — were used to identify issues and verify the improvements.

## Original Repository

The original assignment and source code can be found here:

https://github.com/SETAPESU26/L5_54_warehouse-stock

This repository contains my Lab 5 submission as part of the SE Labs repository.

## Objectives

- Identify code quality issues using Pylint.
- Detect potential security problems using Bandit.
- Check Python formatting and style using Flake8.
- Fix the reported issues and rerun the tools.
- Compare the results before and after making changes.

## Tools Used

| Tool | Purpose |
|---|---|
| Pylint | Checks code quality, naming, documentation, and common programming issues. |
| Bandit | Detects potential security problems in Python code. |
| Flake8 | Checks Python style and formatting issues. |

## Files in This Folder

| File | Description |
|---|---|
| `warehouse_stock_manager.py` | Updated warehouse stock management program. |
| `pylint_report.txt` | Pylint report before fixes. |
| `bandit_report.txt` | Bandit report before fixes. |
| `flake8_report.txt` | Flake8 report before fixes. |
| `pylint_report_after.txt` | Pylint report after fixes. |
| `bandit_report_after.txt` | Bandit report after fixes. |
| `flake8_report_after.txt` | Flake8 report after fixes. |
| `issues.md` | Summary of issues found and their fixes. |
| `reflection.md` | Lab reflection and learning outcomes. |

## Setup

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required tools:

```bash
pip install pylint bandit flake8
```

## Running the Program

Run the warehouse stock manager:

```bash
python warehouse_stock_manager.py
```

The program demonstrates stock operations, saves and loads stock data, and prints a warehouse stock report.

To enable supervisor adjustments, set the `WAREHOUSE_SUPERVISOR_PASSWORD` environment variable before running the program.

## Running Static Analysis

Run each tool and save its report:

```bash
pylint warehouse_stock_manager.py > pylint_report_after.txt
bandit -r warehouse_stock_manager.py > bandit_report_after.txt
flake8 warehouse_stock_manager.py > flake8_report_after.txt
```

## Results

The final checks produced the following results:

- **Pylint:** 10.00/10.
- **Bandit:** No issues identified.
- **Flake8:** No style issues reported.

The original reports are retained to compare the findings before and after the fixes.

## Learning Outcomes

This lab provided practical experience in using static analysis tools, identifying security and code quality issues, improving Python code, and documenting the results of the analysis.

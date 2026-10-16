
"""Manage warehouse stock and generate stock audit reports."""

import ast
import hashlib
import json
import os
import operator
from datetime import datetime

warehouse_stock = {}
AUDIT_FILE = "warehouse_audit.log"

SUPERVISOR_PASSWORD = os.getenv("WAREHOUSE_SUPERVISOR_PASSWORD")

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}
UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_formula(formula, current):
    """Evaluate a restricted arithmetic formula using the current stock."""
    try:
        tree = ast.parse(formula, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid arithmetic formula") from exc

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.Name) and node.id == "current":
            return current

        if isinstance(node, ast.BinOp):
            operation = BINARY_OPERATORS.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported arithmetic operator")
            return operation(evaluate(node.left), evaluate(node.right))

        if isinstance(node, ast.UnaryOp):
            operation = UNARY_OPERATORS.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported unary operator")
            return operation(evaluate(node.operand))

        raise ValueError("Unsupported expression in formula")

    result = evaluate(tree)
    if type(result) not in (int, float):
        raise ValueError("Formula must produce a number")
    if not -1e12 <= result <= 1e12:
        raise ValueError("Formula result is outside the allowed range")
    return result


def add_stock(sku="default", qty=0, history=None):
    """Add units to a stock item and optionally record the change."""
    if not sku:
        return
    if type(qty) not in (int, float):
        raise ValueError("Quantity must be numeric")

    warehouse_stock[sku] = warehouse_stock.get(sku, 0) + qty
    if history is not None:
        history.append(
            f"{datetime.now()}: Received {qty} units of {sku}"
        )


def remove_stock(sku, qty):
    """Remove units from stock, ignoring items that do not exist."""
    if sku not in warehouse_stock:
        return
    if type(qty) not in (int, float):
        raise ValueError("Quantity must be numeric")

    warehouse_stock[sku] -= qty
    if warehouse_stock[sku] <= 0:
        del warehouse_stock[sku]


def get_stock(sku):
    """Return the quantity of an item, or zero if it is absent."""
    return warehouse_stock.get(sku, 0)


def sku_checksum(sku):
    """Return a short, non-security fingerprint for a bin label."""
    return hashlib.md5(
        str(sku).encode(), usedforsecurity=False
    ).hexdigest()[:6]


def load_stock(file="warehouse.json"):
    """Load warehouse stock from a JSON file."""
    with open(file, "r", encoding="utf-8") as stock_file:
        loaded_stock = json.load(stock_file)
    if not isinstance(loaded_stock, dict):
        raise ValueError("Stock file must contain a JSON object")
    warehouse_stock.clear()
    warehouse_stock.update(loaded_stock)


def save_stock(file="warehouse.json"):
    """Save warehouse stock to a JSON file."""
    with open(file, "w", encoding="utf-8") as stock_file:
        json.dump(warehouse_stock, stock_file)


def print_report():
    """Print the current warehouse stock report."""
    print("Warehouse Stock Report")
    for sku, quantity in warehouse_stock.items():
        checksum = sku_checksum(sku)
        print(sku, "->", quantity, "units [chk:", checksum + "]")


def check_reorder(threshold=10):
    """Return stock item identifiers below the reorder threshold."""
    return [
        sku for sku, quantity in warehouse_stock.items()
        if quantity < threshold
    ]


def apply_adjustment(sku, formula, password):
    """Apply a safe arithmetic adjustment and record it in the audit log."""
    if not SUPERVISOR_PASSWORD or password != SUPERVISOR_PASSWORD:
        raise PermissionError("Invalid or missing supervisor password")

    current = warehouse_stock.get(sku, 0)
    updated_quantity = safe_formula(formula, current)
    if updated_quantity < 0:
        raise ValueError("Stock quantity cannot be negative")

    with open(AUDIT_FILE, "a", encoding="utf-8") as audit_file:
        audit_file.write(
            f"Adjusted {sku} using formula {formula} "
            f"at {datetime.now()}\n"
        )
    warehouse_stock[sku] = updated_quantity


def main():
    """Demonstrate warehouse stock operations."""
    add_stock("WID-001", 40)
    add_stock("WID-002", -4)
    remove_stock("WID-001", 12)
    remove_stock("GHOST-9", 1)
    remove_stock("WID-001", 500)

    print("WID-002 stock:", get_stock("WID-002"))
    print("Needs reorder:", check_reorder())

    password = SUPERVISOR_PASSWORD
    if password:
        apply_adjustment("WID-002", "current + 25", password)
    else:
        print("Set WAREHOUSE_SUPERVISOR_PASSWORD to enable adjustments.")

    save_stock()
    load_stock()
    print_report()
    print("Stock audit complete")


if __name__ == "__main__":
    main()

"""
Day 2 - Sales Analytics Without Pandas

Tasks 1-7 use only the standard library.
Pandas is used only in verify_with_pandas to check the results.
"""

import csv
import math
from pathlib import Path


DATA_PATH = Path("data") / "electronics_sales.csv"
HIGH_VALUE_THRESHOLD = 50_000


def read_sales(path: Path = DATA_PATH) -> list[dict[str, str]]:
    """Read the CSV with the csv module and return the raw rows."""
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        columns = reader.fieldnames or []

    print(f"Rows: {len(rows)}")
    print(f"Columns: {columns}")
    return rows


def parse_number(value: str | None) -> float | None:
    """Convert a supported messy numeric string to a float."""
    if value is None:
        return None

    cleaned = value.strip()

    # This dataset contains the word "two" in one quantity cell.
    if cleaned.lower() == "two":
        return 2.0

    # Remove thousands separators, such as the comma in "38,999".
    cleaned = cleaned.replace(",", "")

    # Remove a leading currency label, such as "KES 18999".
    if cleaned.upper().startswith("KES "):
        cleaned = cleaned[4:].strip()

    if not cleaned:
        return None

    try:
        number = float(cleaned)
    except ValueError:
        return None

    # Reject special values such as NaN and infinity.
    if not math.isfinite(number):
        return None

    return number


def convert_rows(
    rows: list[dict[str, str]],
) -> tuple[list[dict], list[dict]]:
    """Return clean rows and skipped rows, with a reason for each skip."""
    clean_rows = []
    skipped_rows = []

    # CSV row 1 is the header, so data starts at row 2.
    for row_number, row in enumerate(rows, start=2):
        quantity = parse_number(row.get("quantity"))
        unit_price = parse_number(row.get("unit_price_kes"))

        if quantity is None:
            skipped_rows.append({
                "sale_id": row.get("sale_id", "unknown"),
                "row_number": row_number,
                "reason": "quantity is missing or invalid",
            })
            continue

        if unit_price is None:
            skipped_rows.append({
                "sale_id": row.get("sale_id", "unknown"),
                "row_number": row_number,
                "reason": "unit price is missing or invalid",
            })
            continue

        if quantity < 0 or unit_price < 0:
            skipped_rows.append({
                "sale_id": row.get("sale_id", "unknown"),
                "row_number": row_number,
                "reason": "quantity or unit price is negative",
            })
            continue

        # Copy the original row, then replace numeric text with numbers.
        clean_row = dict(row)
        clean_row["quantity"] = quantity
        clean_row["unit_price_kes"] = unit_price
        clean_row["revenue"] = quantity * unit_price
        clean_rows.append(clean_row)

    return clean_rows, skipped_rows


def total_revenue(rows: list[dict]) -> float:
    """Add up the revenue for all clean rows."""
    total = 0.0

    for row in rows:
        total += row["revenue"]

    return total


def revenue_by(rows: list[dict], field: str) -> dict[str, float]:
    """Add revenue by a field, such as product, store, or payment_method."""
    totals = {}

    for row in rows:
        group_name = row[field]
        totals[group_name] = totals.get(group_name, 0.0) + row["revenue"]

    return totals


def top_n(
    totals: dict[str, float],
    n: int = 3,
) -> list[tuple[str, float]]:
    """Return the n highest (name, revenue) pairs."""
    # Ties are broken alphabetically by name.
    ranked = sorted(
        totals.items(),
        key=lambda item: (-item[1], item[0]),
    )
    return ranked[:n]


def high_value(rows: list[dict], threshold: float) -> list[dict]:
    """Return transactions at or above the threshold."""
    return [row for row in rows if row["revenue"] >= threshold]


def mean(values: list[float]) -> float:
    """Calculate the arithmetic mean."""
    if not values:
        raise ValueError("mean requires at least one value")

    return sum(values) / len(values)


def median(values: list[float]) -> float:
    """Calculate the median."""
    if not values:
        raise ValueError("median requires at least one value")

    ordered = sorted(values)
    middle = len(ordered) // 2

    if len(ordered) % 2 == 1:
        return ordered[middle]

    return (ordered[middle - 1] + ordered[middle]) / 2


def minimum_maximum(values: list[float]) -> tuple[float, float]:
    """Find the smallest and largest values without min() or max()."""
    if not values:
        raise ValueError("minimum_maximum requires at least one value")

    smallest = values[0]
    largest = values[0]

    for value in values[1:]:
        if value < smallest:
            smallest = value
        if value > largest:
            largest = value

    return smallest, largest


def verify_with_pandas(path: Path, my_results: dict) -> None:
    """Recompute headline results with pandas and print MATCH or MISMATCH."""
    import pandas as pd

    frame = pd.read_csv(path, dtype=str, keep_default_na=False)

    # Apply the same number parsing rules used by convert_rows.
    frame["quantity"] = frame["quantity"].apply(parse_number)
    frame["unit_price_kes"] = frame["unit_price_kes"].apply(parse_number)

    # Skip rows with invalid values or negative quantities/prices.
    frame = frame.dropna(subset=["quantity", "unit_price_kes"])
    frame = frame[
        (frame["quantity"] >= 0)
        & (frame["unit_price_kes"] >= 0)
    ].copy()

    frame["revenue"] = frame["quantity"] * frame["unit_price_kes"]

    pandas_total = float(frame["revenue"].sum())
    total_matches = math.isclose(
        pandas_total,
        my_results["total_revenue"],
        abs_tol=0.005,
    )

    if total_matches:
        print("Pandas total revenue: MATCH")
    else:
        print(
            "Pandas total revenue: MISMATCH "
            f"(pandas={pandas_total:.2f}, "
            f"my code={my_results['total_revenue']:.2f})"
        )

    # Compare the grouped revenue totals for each requested field.
    for field in ("product", "store", "payment_method"):
        pandas_totals = frame.groupby(field)["revenue"].sum().to_dict()
        my_totals = my_results[f"{field}_revenue"]

        same_keys = set(pandas_totals) == set(my_totals)
        same_values = same_keys and all(
            math.isclose(
                float(pandas_totals[key]),
                my_totals[key],
                abs_tol=0.005,
            )
            for key in pandas_totals
        )

        if same_values:
            print(f"Pandas {field} breakdown: MATCH")
        else:
            print(f"Pandas {field} breakdown: MISMATCH")


if __name__ == "__main__":
    raw_rows = read_sales()
    clean_rows, skipped_rows = convert_rows(raw_rows)

    print(f"Clean rows: {len(clean_rows)}")
    print(f"Skipped rows: {len(skipped_rows)}")

    for skipped_row in skipped_rows:
        print("Skipped:", skipped_row)

    total = total_revenue(clean_rows)
    print(f"\nTotal revenue: KES {total:,.2f}")

    product_totals = revenue_by(clean_rows, "product")
    store_totals = revenue_by(clean_rows, "store")
    payment_totals = revenue_by(clean_rows, "payment_method")

    print("\nRevenue by product:")
    for product, revenue in sorted(
        product_totals.items(),
        key=lambda item: (-item[1], item[0]),
    ):
        print(f"{product}: KES {revenue:,.2f}")

    print("\nTop three products:")
    for product, revenue in top_n(product_totals, 3):
        print(f"{product}: KES {revenue:,.2f}")

    qualifying_sales = high_value(clean_rows, HIGH_VALUE_THRESHOLD)
    print(f"\nSales at or above KES {HIGH_VALUE_THRESHOLD:,.2f}:")
    for row in qualifying_sales:
        print(
            f"{row['sale_id']} | {row['product']} | "
            f"{row['store']} | KES {row['revenue']:,.2f}"
        )

    # Dict comprehension: count qualifying sales for each store.
    stores = {row["store"] for row in clean_rows}
    high_value_by_store = {
        store: sum(
            1 for row in qualifying_sales
            if row["store"] == store
        )
        for store in stores
    }

    print("\nHigh-value sale count by store:")
    for store, count in sorted(high_value_by_store.items()):
        print(f"{store}: {count}")

    revenues = [row["revenue"] for row in clean_rows]

    print(f"\nMean transaction revenue: KES {mean(revenues):,.2f}")
    print(f"Median transaction revenue: KES {median(revenues):,.2f}")

    smallest, largest = minimum_maximum(revenues)
    print(f"Minimum transaction revenue: KES {smallest:,.2f}")
    print(f"Maximum transaction revenue: KES {largest:,.2f}")

    my_results = {
        "total_revenue": total,
        "product_revenue": product_totals,
        "store_revenue": store_totals,
        "payment_method_revenue": payment_totals,
    }

    print("\nPandas verification:")
    verify_with_pandas(DATA_PATH, my_results)
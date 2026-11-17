"""What the land around the trench pays in property tax, and what the deck could pay.

Every lot within 250 m of the trench outline, from the 2025 tax roll joined to the assessor's
parcel layer (../data/tax-near-trench.csv). The homes estimate uses the buildings of 20 or more
homes inside that circle (../data/apartment-buildings.csv): their homes per acre, times the homes
block, rounded to 50.
"""
import _setup  # noqa: F401
from commons import metrics, read_csv
import area


def numbers():
    t = metrics("cap-i-95", "tax-near-trench.csv")
    a = area.numbers()
    per_acre = t["taxes_billed"] / t["taxable_acres"]
    b = read_csv("cap-i-95", "data", "apartment-buildings.csv")
    homes = sum(int(r["homes"]) for r in b)
    homes_per_acre = homes / sum(float(r["lot_acres"]) for r in b)
    deck_homes = round(round(a["homes_block_acres"], 1) * round(homes_per_acre) / 50) * 50
    tax_per_home = sum(float(r["tax_2025_usd"]) for r in b) / homes
    return {
        "tax_per_acre": per_acre,
        "trench_tax_a_year": a["trench_acres"] * per_acre,
        "phase_one_tax_a_year": a["phase_one_acres"] * per_acre,
        "zero_acres": t["zero_acres"],
        "apartment_buildings": len(b),
        "apartment_homes": homes,
        "zero_share": t["zero_acres"] / (t["zero_acres"] + t["taxable_acres"]),
        "homes_per_acre": homes_per_acre,
        "deck_homes": deck_homes,
        "tax_per_home": tax_per_home,
        "deck_homes_tax_a_year": deck_homes * tax_per_home,
    }


if __name__ == "__main__":
    for k, v in numbers().items():
        print(f"{k:24} {v:,.3f}")

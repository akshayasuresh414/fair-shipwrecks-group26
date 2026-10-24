"""
FAIR Data Engineering - Group 26
Step: "Understand and prepare the data" (FAIRification process, step 3)

This script takes the raw Kaggle CSV (Ship, Flag, Sunk date, Notes, Coordinates)
and produces a cleaned, enriched CSV with the following columns:

    ship_id          - row-stable integer id (0-based), used to build URIs later
    ship_name        - cleaned Ship name
    flag             - cleaned Flag / operator value
    flag_type        - "country" or "military_organisation" (derived from Flag)
    sunk_year        - a normalised 4-digit year parsed out of "Sunk date" (may be null)
    sunk_date_raw     - original Sunk date text, kept for provenance
    latitude          - decimal degrees (derived from Coordinates)
    longitude         - decimal degrees (derived from Coordinates)
    cause_of_loss     - controlled value derived from Notes (torpedoed, mined, ran
                        aground, collision, storm, fire, scuttled, capsized, shelled
                        /bombed, unknown)
    vessel_type       - controlled value derived from Notes (cargo ship, tanker,
                        ferry, cruiser, destroyer, submarine, frigate, corvette,
                        gunboat, minesweeper, schooner, steamer, trawler, tug,
                        barge, liner, yacht, fishing vessel, unknown)
    notes             - original free-text Notes (kept for provenance/traceability)

Run:
    python3 prepare_data.py
Produces:
    data/shipwrecks_clean.csv       (full cleaned file)
    data/shipwrecks_clean_coords.csv (subset: rows that have coordinates - this is
                                      the subset we will actually triplify, per the
                                      proposal's scoping decision)
"""
import re
import pandas as pd

IN_PATH = "data/raw_shipwrecks.csv"
OUT_PATH_FULL = "data/shipwrecks_clean.csv"
OUT_PATH_COORDS = "data/shipwrecks_clean_coords.csv"

# --- Known military/naval operators (vs. plain countries) -----------------
# Anything matching these substrings is tagged as a military organisation;
# everything else with a non-null Flag is tagged as a country.
MILITARY_KEYWORDS = [
    "navy", "kriegsmarine", "royal navy", "imperial", "confederate states navy",
    "army", "air force", "marine", "coast guard", "fleet", "squadron",
]

# --- Cause of loss keyword -> controlled value, checked in this priority order
CAUSE_PATTERNS = [
    ("torpedoed", [r"torpedo"]),
    ("mined", [r"\bmine(d|s)?\b", r"struck a mine"]),
    ("shelled_or_bombed", [r"shell", r"bomb"]),
    ("hijacked", [r"hijack"]),
    ("scuttled", [r"scuttl"]),
    ("collision", [r"collision", r"collided"]),
    ("ran_aground", [r"ran aground", r"\baground\b", r"\breef\b", r"\brocks?\b"]),
    ("storm_or_weather", [r"\bstorm\b", r"\bgale\b", r"\bhurricane\b", r"\btyphoon\b"]),
    ("fire_or_explosion", [r"\bfire\b", r"\bexplosion\b"]),
    ("capsized", [r"capsiz"]),
]

# --- Vessel type keyword -> controlled value, checked in this priority order
TYPE_PATTERNS = [
    ("submarine", [r"\bu-boat\b", r"\bsubmarine\b"]),
    ("destroyer", [r"\bdestroyer\b"]),
    ("cruiser", [r"\bcruiser\b"]),
    ("frigate", [r"\bfrigate\b"]),
    ("corvette", [r"\bcorvette\b"]),
    ("gunboat", [r"\bgunboat\b"]),
    ("minesweeper", [r"\bminesweeper\b"]),
    ("patrol_boat", [r"\bpatrol boat\b"]),
    ("tanker", [r"\btanker\b"]),
    ("ferry", [r"\bferry\b"]),
    ("cargo_ship", [r"\bcargo\b", r"\bfreighter\b"]),
    ("liner", [r"\bliner\b"]),
    ("steamer", [r"\bsteamer\b", r"\bsteamship\b"]),
    ("schooner", [r"\bschooner\b"]),
    ("trawler", [r"\btrawler\b"]),
    ("fishing_vessel", [r"\bfishing\b"]),
    ("tug", [r"\btug\b"]),
    ("barge", [r"\bbarge\b"]),
    ("yacht", [r"\byacht\b"]),
]

DMS_RE = re.compile(
    r"(?P<dlat>\d{1,3})[°\s]+(?P<mlat>\d{1,2})?['′]?\s*(?P<slat>[\d.]+)?[\"″]?\s*(?P<hlat>[NS])"
    r"\s+"
    r"(?P<dlon>\d{1,3})[°\s]+(?P<mlon>\d{1,2})?['′]?\s*(?P<slon>[\d.]+)?[\"″]?\s*(?P<hlon>[EW])",
    re.IGNORECASE,
)


def dms_to_dd(deg, minute, sec, hemi):
    deg = float(deg or 0)
    minute = float(minute or 0)
    sec = float(sec or 0)
    dd = deg + minute / 60 + sec / 3600
    if hemi.upper() in ("S", "W"):
        dd = -dd
    return round(dd, 6)


def parse_coordinates(coord_str):
    """Parse a 'Coordinates' cell like '4°04′54″S 39°43′12″E' into (lat, lon)."""
    if not isinstance(coord_str, str) or not coord_str.strip():
        return (None, None)
    m = DMS_RE.search(coord_str)
    if not m:
        return (None, None)
    lat = dms_to_dd(m.group("dlat"), m.group("mlat"), m.group("slat"), m.group("hlat"))
    lon = dms_to_dd(m.group("dlon"), m.group("mlon"), m.group("slon"), m.group("hlon"))
    return (lat, lon)


def parse_year(date_str):
    """Pull a plausible 4-digit year out of a messy date string."""
    if not isinstance(date_str, str) or not date_str.strip():
        return None
    years = re.findall(r"\b(1[0-9]{3}|20[0-2][0-9])\b", date_str)
    if years:
        return int(years[0])
    return None


def classify_flag(flag):
    if not isinstance(flag, str) or not flag.strip():
        return None
    low = flag.lower()
    for kw in MILITARY_KEYWORDS:
        if kw in low:
            return "military_organisation"
    return "country"


def classify_from_notes(notes, patterns, default="unknown"):
    if not isinstance(notes, str):
        return default
    low = notes.lower()
    for label, regs in patterns:
        for r in regs:
            if re.search(r, low):
                return label
    return default


def main():
    df = pd.read_csv(IN_PATH)
    df = df.rename(columns={
        "Ship": "ship_name",
        "Flag": "flag",
        "Sunk date": "sunk_date_raw",
        "Notes": "notes",
        "Coordinates": "coordinates_raw",
    })

    df["ship_id"] = df.index

    df["flag_type"] = df["flag"].apply(classify_flag)
    df["sunk_year"] = df["sunk_date_raw"].apply(parse_year)

    lat_lon = df["coordinates_raw"].apply(parse_coordinates)
    df["latitude"] = lat_lon.apply(lambda t: t[0])
    df["longitude"] = lat_lon.apply(lambda t: t[1])

    df["cause_of_loss"] = df["notes"].apply(lambda n: classify_from_notes(n, CAUSE_PATTERNS))
    df["vessel_type"] = df["notes"].apply(lambda n: classify_from_notes(n, TYPE_PATTERNS))

    # drop rows with no ship name at all (18 rows) - these cannot be meaningfully
    # identified/triplified since Ship is our primary label
    df_full = df[df["ship_name"].notna()].copy()

    cols = [
        "ship_id", "ship_name", "flag", "flag_type", "sunk_year", "sunk_date_raw",
        "latitude", "longitude", "cause_of_loss", "vessel_type", "notes",
    ]
    df_full = df_full[cols]

    df_full.to_csv(OUT_PATH_FULL, index=False)

    df_coords = df_full[df_full["latitude"].notna() & df_full["longitude"].notna()].copy()
    df_coords.to_csv(OUT_PATH_COORDS, index=False)

    print(f"Full cleaned dataset:   {len(df_full)} rows -> {OUT_PATH_FULL}")
    print(f"Coordinates subset:     {len(df_coords)} rows -> {OUT_PATH_COORDS}")
    print()
    print("cause_of_loss distribution (full):")
    print(df_full["cause_of_loss"].value_counts())
    print()
    print("vessel_type distribution (full):")
    print(df_full["vessel_type"].value_counts())
    print()
    print("flag_type distribution (full):")
    print(df_full["flag_type"].value_counts(dropna=False))


if __name__ == "__main__":
    main()

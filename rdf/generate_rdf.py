"""
FAIR Data Engineering - Group 26


This script transforms the cleaned shipwrecks subset (rows that have
coordinates - see data/prepare_data.py) into RDF (Turtle).

"""
import re
import pandas as pd
from rdflib import Graph, Namespace, Literal, RDF, RDFS, XSD, URIRef
from rdflib.namespace import DCTERMS, FOAF

DATA_CSV = "../data/shipwrecks_clean_coords.csv"
OUT_TTL = "data.ttl"

GRP = Namespace("https://w3id.org/FAIR-course-UT/2026/group26/data#")
ONT = Namespace("https://w3id.org/FAIR-course-UT/2026/group26/ont#")
SCHEMA = Namespace("http://schema.org/")
GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
WD = Namespace("http://www.wikidata.org/entity/")

# -----------------------------------------------------------------------
# Minimal, manually curated reconciliation table: Flag value -> Wikidata
# entity. This stands in for OpenRefine's reconciliation service for the
# most frequent Flag values in the dataset (the ones that occur 20+
# times), to demonstrate the Interoperability step (linking to an
# external knowledge base) without requiring network access at run time.
# Any Flag value not in this table is still represented as a labelled
# :Operator resource in our own namespace, so no information is lost -
# it is simply not yet reconciled to Wikidata.
# -----------------------------------------------------------------------
WIKIDATA_RECONCILIATION = {
    "Royal Navy": WD["Q172771"],
    "United States Navy": WD["Q11247"],
    "United States": WD["Q30"],
    "United Kingdom": WD["Q145"],
    "Kriegsmarine": WD["Q387596"],
    "Imperial Japanese Navy": WD["Q858785"],
    "Canada": WD["Q16"],
    "Imperial German Navy": WD["Q287613"],
    "Royal Australian Navy": WD["Q911469"],
    "French Navy": WD["Q1138116"],
    "Norway": WD["Q20"],
    "Spain": WD["Q29"],
    "Australia": WD["Q408"],
    "Greece": WD["Q41"],
    "France": WD["Q142"],
    "Panama": WD["Q804"],
    "Netherlands": WD["Q29999"],
}

VESSEL_TYPE_PREFIX = "VesselType_"
CAUSE_PREFIX = "CauseOfLoss_"


def slug(value: str) -> str:
    """Make a URI-safe slug out of a ship name."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unnamed"


def build_graph(df: pd.DataFrame) -> Graph:
    g = Graph()
    g.bind("grp", GRP)
    g.bind("ont", ONT)
    g.bind("schema", SCHEMA)
    g.bind("geo", GEO)
    g.bind("wd", WD)
    g.bind("dct", DCTERMS)
    g.bind("foaf", FOAF)

    seen_slugs = {}

    for _, row in df.iterrows():
        rid = int(row["ship_id"])
        base_slug = slug(str(row["ship_name"]))
        # disambiguate duplicate slugs (e.g. two ships with the same name)
        n = seen_slugs.get(base_slug, 0)
        seen_slugs[base_slug] = n + 1
        uri_slug = base_slug if n == 0 else f"{base_slug}-{n}"
        subj = GRP[f"shipwreck-{rid}-{uri_slug}"]

        g.add((subj, RDF.type, ONT.Shipwreck))
        g.add((subj, RDF.type, SCHEMA.Event))
        g.add((subj, ONT.vesselName, Literal(str(row["ship_name"]), datatype=XSD.string)))
        g.add((subj, RDFS.label, Literal(f"Sinking of {row['ship_name']}", lang="en")))

        if pd.notna(row.get("notes")):
            g.add((subj, ONT.description, Literal(str(row["notes"]), datatype=XSD.string)))

        if pd.notna(row.get("sunk_year")):
            g.add((subj, ONT.sunkYear, Literal(int(row["sunk_year"]), datatype=XSD.gYear)))
        if pd.notna(row.get("sunk_date_raw")):
            g.add((subj, ONT.sunkDateRaw, Literal(str(row["sunk_date_raw"]), datatype=XSD.string)))

        if pd.notna(row.get("latitude")) and pd.notna(row.get("longitude")):
            g.add((subj, GEO.lat, Literal(float(row["latitude"]), datatype=XSD.float)))
            g.add((subj, GEO.long, Literal(float(row["longitude"]), datatype=XSD.float)))

        # Operator (Flag) - link to Wikidata when we have a reconciliation
        # entry, otherwise mint a local Operator resource carrying the
        # same label so the information is never dropped.
        flag = row.get("flag")
        if pd.notna(flag):
            flag = str(flag)
            if flag in WIKIDATA_RECONCILIATION:
                op_uri = WIKIDATA_RECONCILIATION[flag]
            else:
                op_uri = GRP[f"operator-{slug(flag)}"]
                op_class = ONT.NavalForce if row.get("flag_type") == "military_organisation" else ONT.Country
                g.add((op_uri, RDF.type, op_class))
                g.add((op_uri, RDFS.label, Literal(flag, lang="en")))
            g.add((subj, ONT.operatedBy, op_uri))

        # Vessel type / cause of loss -> controlled vocabulary concepts
        # defined in our own ontology.
        vt = row.get("vessel_type")
        if pd.notna(vt):
            g.add((subj, ONT.hasVesselType, ONT[f"{VESSEL_TYPE_PREFIX}{vt}"]))
        cl = row.get("cause_of_loss")
        if pd.notna(cl):
            g.add((subj, ONT.hasCauseOfLoss, ONT[f"{CAUSE_PREFIX}{cl}"]))

    return g


def main():
    df = pd.read_csv(DATA_CSV)
    g = build_graph(df)
    g.serialize(destination=OUT_TTL, format="turtle")
    print(f"Wrote {len(g)} triples for {len(df)} shipwreck events -> {OUT_TTL}")


if __name__ == "__main__":
    main()

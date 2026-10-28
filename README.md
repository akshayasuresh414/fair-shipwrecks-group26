FAIRified Shipwrecks (Sunk Ships) dataset (Group 26)

FAIR Data Engineering, University of Twente, 2026. Group 26: Akshaya Suresh, Kishor Sriraman.

The Kaggle dataset "Shipwrecks (Sunk ships)" (ship, flag, sunk date, notes, coordinates), FAIRified as RDF. 943 shipwreck events that have coordinates are described with schema.org, WGS84 and a small Group 26 ontology (Shipwreck, Operator, VesselType, CauseOfLoss). Frequent operators are linked to Wikidata.

Source and licence

- Source: Kaggle, "Shipwrecks (Sunk ships)" (PASTE KAGGLE URL HERE), probably compiled from Wikipedia's lists of shipwrecks
- Licence of the FAIRified dataset, as declared in the metadata: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/
- The licence of the upstream Kaggle upload is not independently confirmed.
- Version 1.0.0. Coverage: global, 7th century to 2020s.

Persistent identifiers (W3ID)

Namespace: https://w3id.org/FAIR-course-UT/2026/group26/

| Identifier | Resolves to |
|---|---|
| https://w3id.org/FAIR-course-UT/2026/group26/ont | ontology/group26-ont.ttl |
| https://w3id.org/FAIR-course-UT/2026/group26/data | rdf/data.ttl |
| https://w3id.org/FAIR-course-UT/2026/group26/data/original | data/raw_shipwrecks.csv |
| https://w3id.org/FAIR-course-UT/2026/group26/dataset | metadata/dataset.ttl |

Ontology terms (…/ont#Shipwreck) and shipwreck resources (…/data#shipwreck-…) resolve to the ontology and data files respectively. The redirect rules are maintained in the course pid-relay repository (https://github.com/luizbonino/pid-relay, folder rules/FAIR-course-UT/2026/group26/, pull request #43).

Repository structure

| Folder | Content |
|---|---|
| data/ | Original Kaggle CSV, cleaned CSVs (3,941 rows; 943-row coordinate subset) and prepare_data.py |
| ontology/ | Group 26 ontology (built in Protégé) |
| rdf/ | generate_rdf.py and the FAIRified RDF data (Turtle, 10,621 triples) |
| metadata/ | DCAT records for the dataset and its two distributions (dataset.ttl, distribution-original.ttl, distribution-fairified.ttl) and the SHACL shapes (dataset-shape.ttl, distribution-shape.ttl) |
| docs/ | Semantic model diagram (PNG and Graphviz source) |

Data preparation

- 18 rows without a ship name removed: 3,959 raw rows became 3,941 clean rows.
- Coordinates converted from degrees, minutes, seconds to decimal latitude and longitude. 943 rows have coordinates, and only these were converted to RDF.
- Flag split into country or military organisation; original text kept.
- Cause of loss and vessel type derived from the Notes by keyword matching. Rows with no match are "unknown", never guessed.
- Sunk year parsed where a clear year exists (157 of the 943 rows); the original date text is kept as sunkDateRaw.
- All steps are in data/prepare_data.py.

Linked data

- rdf/generate_rdf.py (Python, rdflib) creates one ont:Shipwreck, also a schema:Event, per row.
- 655 of 890 operator links (73.6%) point to Wikidata, using a hand-made lookup for flags seen at least 20 times. Other operators stay local resources typed Country or NavalForce.

Metadata

DCAT records for one dataset and two distributions (original CSV, FAIRified Turtle) were created in a FAIR Data Point (version 1.18.0) using our own SHACL shapes, then exported to metadata/.

Known limitations

- The exported records use http://localhost/… as internal addresses, because the FAIR Data Point ran locally. The W3ID identifier is stored in dct:identifier and dcat:downloadURL.
- The FAIR Data Point was temporary, so F4 (indexed in a search resource) is only partly met.
- Metadata and data are in the same repository, so A2 (metadata outlives data) is only partly met.
- Cause of loss and vessel type come from keyword matching and are unknown for a share of the wrecks.

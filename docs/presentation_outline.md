# Presentation outline - Group 26 - Shipwrecks FAIRification
Per the project description's required presentation structure. Split evenly between Kishor and Akshaya (suggested split marked below - adjust to who actually did which parts, since Q&A will test this).

**Suggested split:** Kishor presents slides 1-6 (dataset + planning + data prep), Akshaya presents slides 7-12 (semantic model + metadata + publication + FAIRness). Both must be ready for questions on *everything*, since questions assess individual understanding, not who clicked which slide.

---

## Slide 1 - Title
- Group 26: FAIRification of the Shipwrecks (Sunk Ships) Dataset
- Kishor Sriraman (s3688232), Akshaya Suresh
- FAIR Data Engineering, University of Twente, 2026

## Slide 2 - The dataset
- **What**: Shipwreck events - ship name, flag/operator, sunk date, free-text notes, coordinates
- **Where found**: Kaggle (diaaessam/shipwrecks-sunk-ships), likely originally compiled from Wikipedia's "List of shipwrecks" articles (CC BY-SA)
- **Current format**: plain CSV, 3,959 rows x 5 columns
- **Existing metadata**: almost none - just a Kaggle page title/description, no PID, no structured schema, no confirmed license (speak to your Initial FAIRness Assessment table here)

## Slide 3 - Why this dataset / scoping decision
- Small, understandable, genuinely obscure for this kind of course exercise
- Only ~24% of rows (943) have usable coordinates -> we scoped the FAIRification to that subset, since location drives our reuse scenarios and keeps RDF transformation fast
- Show the column table (Ship, Flag, Sunk date, Notes, Coordinates) with missing-value counts

## Slide 4 - FAIRification planning (GO-Plan)
- Goals: give data+ontology PIDs (F1), rich DCAT metadata via FDP (F2-F4), open HTTPS access (A1-A2), RDF with shared vocabularies + Wikidata links (I1-I3), documented provenance/license (R1)
- Target stakeholders: us (domain + FAIR experts in training)
- Reuse stakeholders: maritime historians, marine archaeologists, genealogists, Wikidata contributors, app developers
- Competency questions (pick 2-3 to show): "Which ships operated by a given navy were lost in the same decade as X conflict?", "How many ships lost per decade, by cause of loss?"

## Slide 5 - Data preparation
- Explain what was ignored/split/merged/reconciled:
  - Dropped 18 rows with no ship name
  - Split `Coordinates` (DMS string) -> `latitude`/`longitude` (decimal degrees)
  - Parsed `Sunk date` (free text) -> `sunk_year` (regex for 4-digit year)
  - **Derived two brand-new columns from free-text `Notes`** via keyword matching: `cause_of_loss` (torpedoed, mined, ran aground, storm, ...) and `vessel_type` (submarine, destroyer, cargo ship, ...)
  - Be honest: ~45% of cause_of_loss and ~42% of vessel_type stayed "unknown" - free text isn't always specific enough
- Show the before/after: 5 raw columns -> ~7-8 meaningful properties

## Slide 6 - Semantic data model
- Show the diagram (`docs/semantic_model.png`)
- Central class `ont:Shipwreck` (subclass of `schema:Event`)
- `ont:operatedBy` -> `ont:Operator` (split into `ont:Country` / `ont:NavalForce` because the raw Flag column mixes both)
- `ont:hasVesselType` / `ont:hasCauseOfLoss` -> our own controlled-vocabulary concepts (`skos:Concept`), because no existing ontology covered this classification at the right granularity
- Literal properties reuse external vocab where possible: `geo:lat`/`geo:long` (WGS84), `dct:date`-aligned `sunkYear`
- Ontology IRI: `https://w3id.org/FAIR-course-UT/2026/group26/ont`

## Slide 7 - Making data linkable (triplification)
- Used a **Python/rdflib RDF-generation script** (explicitly allowed as an alternative to OpenRefine's RDF extension) over the 943-row coordinate subset
- One URI per shipwreck under Base URI `https://w3id.org/FAIR-course-UT/2026/group26/data#`
- `Flag` values reconciled against a Wikidata lookup table for the most frequent operators (Royal Navy -> wd:Q172771, etc.); unmatched values still represented as local, typed resources so nothing is lost
- Result: **10,621 RDF triples**, Turtle syntax
- Show the short Turtle excerpt (HMS Amphion example) from the report

## Slide 8 - Semantic metadata model (SHACL)
- Three things modelled with DCAT: Dataset record, original-CSV Distribution, FAIRified-RDF Distribution
- Show the key properties required by our `DatasetShape`: title, description, identifier, license, creator, publisher, keywords, spatial/temporal coverage, `dct:conformsTo` our ontology, and a link to both distributions
- `DistributionShape` requires: title, description, identifier, license, downloadURL (must be our W3ID identifier), mediaType (`text/csv` vs `text/turtle`)

## Slide 9 - Identifiers (W3ID)
- Explain *why*: F1 (globally unique + persistent) and A1 (resolvable) require a real PID scheme, not just a GitHub/Kaggle URL
- Our namespace: `https://w3id.org/FAIR-course-UT/2026/group26/`
- `/ont` -> our ontology; `/dataset` -> Dataset metadata record; `/data` -> FAIRified RDF; `/data/original` -> original CSV
- Content negotiation: RDF Accept header -> raw file; browser (HTML) -> readable GitHub page
- Submitted as a pull request to the course's `pid-relay` GitHub repo, auto-checked and merged

## Slide 10 - Publication (FAIR Data Point)
- Deployed FDP (Docker), configured it with our SHACL schemas (dataset-shape.ttl, distribution-shape.ttl)
- Created one catalog -> one Dataset record -> two Distribution records (original + FAIRified)
- `downloadURL` of each distribution points to its W3ID identifier, which resolves to the file in our GitHub repo
- Extracted the 3 metadata records as RDF ("View RDF") and committed them to the repo too

## Slide 11 - FAIRness improvements
- Side-by-side: Initial assessment table vs Final assessment table (from the report)
- Call out the biggest jumps: F1 (no PID -> W3ID), I1 (plain CSV -> RDF with shared vocab + Wikidata links), A2 (metadata tied to data -> metadata independently resolvable via FDP/GitHub)

## Slide 12 - Integration potential + limitations + conclusion
- Linking points: Operator -> Wikidata, coordinates -> GeoNames/marine regions, cause_of_loss -> conflict datasets
- Honest limitations: only 24% of rows had coordinates so we scoped down; ~45% of derived cause/type stayed "unknown"; license still needs final confirmation
- What we'd do with more time: reconcile more Operator values, add a SPARQL endpoint (bonus), expand keyword extraction with NLP instead of regex
- Thank you / questions

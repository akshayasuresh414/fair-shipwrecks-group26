# Group 26 
```
project/
  data/
    raw_shipwrecks.csv          <- your original Kaggle file, untouched
    prepare_data.py             <- cleans + enriches the data (run this first)
    shipwrecks_clean.csv        <- output: all 3,941 usable rows, enriched
    shipwrecks_clean_coords.csv <- output: the 943-row FAIRified subset
  ontology/
    group26-ont.ttl             <- your mini ontology (Protege-compatible)
  rdf/
    generate_rdf.py             <- transforms the 943 rows into RDF
    data.ttl                    <- output: 10,621 triples
  metadata/
    dataset-shape.ttl           <- SHACL schema for the Dataset metadata
    distribution-shape.ttl      <- SHACL schema for Distribution metadata
    sample_dataset_record.ttl   <- DRAFT example of a filled-in Dataset record
    sample_distribution_records.ttl <- DRAFT example of both Distribution records
  w3id/
    .htaccess                   <- your W3ID redirect rules (needs your GitHub repo URL)
    tests.yaml                  <- required tests for the pid-relay pull request
    OWNERS.yaml                 <- needs your two GitHub usernames
  docs/
    semantic_model.dot / .png   <- diagram of your semantic data model
    report_sections_2_3.tex     <- LaTeX for report Sections 2 and 3 (planning + process start)
    presentation_outline.md     <- full slide-by-slide content outline
  README.md                     <- this file
```

Everything above already ran successfully and was validated (all Turtle
files parse correctly, the RDF script produced 10,621 triples from 943
rows). You do not need to re-run anything unless you change the data.

---



### Step 1 - Create your GitHub (or GitLab) repository (~10 min)
1. Create a new **public** repo, e.g. `fair-shipwrecks-group26`.
2. Upload this whole `project/` folder's contents into it, keeping the
   same subfolder structure (`data/`, `ontology/`, `rdf/`, `metadata/`).
   You do not need to upload the `w3id/` folder itself into this repo -
   those three files go into a *different* repo (the course's pid-relay,
   see Step 3).
3. Note your repo's URL, e.g. `https://github.com/yourname/fair-shipwrecks-group26`.

### Step 2 - Fix the placeholders now that you have a repo URL (~5 min)
In `w3id/.htaccess` and `w3id/tests.yaml`, replace every occurrence of:
- `GITHUB_USER` -> your actual GitHub username/organisation
- `REPO_NAME` -> your actual repository name (e.g. `fair-shipwrecks-group26`)

Also create `metadata/dataset.ttl` in your GitHub repo once you have your
real FDP-exported Dataset record (Step 6) - the `.htaccess` `/dataset`
rule expects it at exactly that path.

### Step 3 - Claim your W3ID namespace (~15 min)
1. Fork https://github.com/luizbonino/pid-relay and clone your fork.
2. Copy `w3id/.htaccess`, `w3id/tests.yaml`, and `w3id/OWNERS.yaml` (with
   your two GitHub usernames filled in) into
   `rules/FAIR-course-UT/2026/group26/` in your fork, **overwriting** the
   existing placeholder `OWNERS.yaml` there.
3. Commit, push, open a pull request to `luizbonino/pid-relay`.
4. Wait for the automatic check (may need the professor's first-time
   approval to run). Fix anything it flags, push again.
5. Once merged, test resolution:
   `https://w3id.org/FAIR-course-UT/2026/group26/ont` and `.../data`
   should redirect correctly. You can also check hop-by-hop at
   https://fair-testbed.eemcs.utwente.nl/pid-manager/resolve

> Note on the version mismatch: the official written project description
> you pasted says the base pattern is
> `https://w3id.org/FAIR-course-UT/2024-2025/{group#}/ont#` - that's
> stale text left over from last year's course page. The professor's
> actual Canvas announcements (which you pasted) say clearly: this
> year's base is `https://w3id.org/FAIR-course-UT/2026/groupNN/`. All
> the files here use the 2026 path, which is correct - trust the
> announcement over the static page text.

### Step 4 - Open the ontology in Protege and double-check it (~15 min)
1. Open Protege, File -> Open -> `ontology/group26-ont.ttl`.
2. Check Ontology IRI reads `https://w3id.org/FAIR-course-UT/2026/group26/ont`.
3. In Protege Preferences -> New Entities, confirm "Followed by" is set to `#`.
4. Browse the class hierarchy (Shipwreck, Operator/Country/NavalForce,
   VesselType, CauseOfLoss) so you can explain it confidently.
5. You don't have to rebuild it from scratch in Protege - opening and
   verifying it (and understanding it) is what matters for the exam/Q&A.

### Step 5 - Deploy the FAIR Data Point (~45-60 min, the slowest manual step)
1. Follow https://fairdatapoint.readthedocs.io/ with FDP and FDP Client
   image versions set to **1.18** (per the professor's instructions).
   Typically this is a `docker-compose up` once you have the compose file
   from that documentation - needs Docker installed on your machine or a
   VM.
2. Log in to the admin area.
3. Go to the metadata schema settings. Paste the contents of
   `metadata/dataset-shape.ttl` into the **Dataset** schema, and
   `metadata/distribution-shape.ttl` into the **Distribution** schema.
   (The professor's announcement mentions the Contour extension can also
   help you build/export SHACL visually if you prefer that over pasting
   raw Turtle.)
4. Create a new **Catalog**.
5. Inside it, create the **Dataset** record - use
   `metadata/sample_dataset_record.ttl` as your reference for what to
   fill in (title, description, license, creator, keywords, etc.). Your
   `dct:identifier` and the record's own W3ID-resolvable URL should be
   `https://w3id.org/FAIR-course-UT/2026/group26/dataset`.
6. Create the two **Distribution** records inside that dataset - use
   `metadata/sample_distribution_records.ttl` as reference. Their
   `downloadURL` fields MUST be your W3ID identifiers
   (`.../group26/data/original` and `.../group26/data`), not raw GitHub
   links directly - that's the whole point of having PIDs.
7. Verify each `downloadURL` actually resolves (open it in a browser).

### Step 6 - Extract the real metadata records (~10 min)
For the Dataset record and each of the 2 Distribution records in FDP:
1. Open the record, click **Edit** (top right).
2. Scroll to the bottom, click the arrow next to **View RDF**.
3. Copy the Turtle shown.
4. Save as `metadata/dataset.ttl`, `metadata/distribution-original.ttl`,
   `metadata/distribution-fairified.ttl` respectively.
5. **Replace** the two `sample_*.ttl` DRAFT files in your repo with these
   real exports (or keep both, clearly labelled - your call, but the
   real FDP exports are the actual deliverable).
6. Push to your GitHub repo.

### Step 7 - Finish the FAIRness assessment (~15 min)
`docs/report_sections_2_3.tex` already has your **initial** assessment
table filled in. Once Steps 1-6 are done, fill in the **final**
assessment table the same way (template Section 3.6), now scoring your
*FAIRified* resource - it should score much higher on F1/F2/F3/F4/A1/A2/I1
(you'll have real values to point to: the W3ID identifier, the DCAT
metadata, the RDF, the Wikidata links).



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


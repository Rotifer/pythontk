# Reselection of samples

## Background

We need to choose samples from timepoints that have both anti-HBs and HBsAg data

The 91 participants to select samples from are listed in table ___pcpts_selected_for_abbott_collab__

CREATE VIEW vw_samples AS 
SELECT barcode, 
concat(protocol, '.', screening_id) AS usubjid, 
visit, 
sample_name, 
status, "location" 
FROM samples 
WHERE ("location" ~~ 'GCL-%');
# Reselection of samples

## Background

We need to choose samples from timepoints that have both anti-HBs and HBsAg data

The 91 participants to select samples from are listed in table __pcpts_selected_for_abbott_collab__

This view creates a listing of samples with usubjid that can be joined to table __pcpts_selected_for_abbott_collab__.

```sql
CREATE VIEW vw_samples AS 
    SELECT barcode, 
    concat(protocol, '.', screening_id) AS usubjid, 
    visit, 
    sample_name, 
    status, 
    "location" 
FROM 
    samples 
WHERE 
    ("location" ~~ 'GCL-%');
```

## Creation of a view for selected samples

The following view creates the barcode sample list for the selected samples to ship to abbott by

- Joining  _vw_samples_ to _pcpts_selected_for_abbott_collab_ using _usubjid_
- Filtering for sample name _HBcrAg Aliq 2_
- Only returniing rows for the selected timepoints
- 
```sql
CREATE OR  REPLACE VIEW vw_samples_for_abbott_collab AS
SELECT
  pcpts.usubjid,
  pcpts.response_category,
  vw.barcode,
  vw.sample_name,
  vw.visit   
FROM vw_samples vw
JOIN 
  pcpts_selected_for_abbott_collab pcpts
  ON 
    vw.usubjid = pcpts.usubjid
WHERE
    sample_name = 'HBcrAg Aliq 2';
```

## Create a pivot version of view _vw_samples_for_abbott_collab_

A pivot makes it easier to identify missing samples.

```sql
CREATE OR REPLACE TABLE pvt_samples_for_abb_collab AS 
PIVOT vw_samples_for_abbott_collab
ON visit
USING MAX(barcode);
```

## Export _pvt_samples_for_abbott_collab_ to Excel

```sql
LOAD spatial;
COPY pvt_samples_for_abb_collab 
TO  'pvt_samples_for_abbott_collab_20240918.xlsx' 
WITH (FORMAT GDAL, DRIVER 'xlsx');
```

We only have four _HBcrAg Aliq 2_ samples for four of the six timepoints chosen.

## Summarise sample type availability for all timepoints 

For the 91 selected participants, summarise which samples are available at each timepoint.

This query does the pivot and exports the data to Excel:

```sql
LOAD SPATIAL;
COPY(
PIVOT 
(SELECT
  pcpts.usubjid,
  pcpts.response_category,
  vw.barcode,
  vw.sample_name,
  vw.visit   
FROM vw_samples vw
JOIN 
  pcpts_selected_for_abbott_collab pcpts
  ON 
    vw.usubjid = pcpts.usubjid)
ON visit
USING COUNT(barcode))
TO  'pvt_select_smpls_20240919.xlsx' 
WITH (FORMAT GDAL, DRIVER 'xlsx');
```

### Pivot on visits to get analyte counts

This was exported to the Excel file _pvt_select_smpl_types_avlbl_ and columns not needed were removed and the column order was changed to present timepoints consecutively (earliest to latest).

```sql
PIVOT
(SELECT 
  av.usubjid,
  pcpts.response_category,
  av.visit,
  av.paramcd,
  av.param
FROM 
  adlb_virology av
JOIN 
  pcpts_selected_for_abbott_collab pcpts
  ON 
    av.usubjid = pcpts.usubjid)
ON visit
USING COUNT(paramcd)
```

### Group count visit/parameter

Get a count of how many of the participants selected for Abbott have data for each visit/measurement parameter combination

```sql
LOAD SPATIAL;
COPY(SELECT 
  abt_only.visit_number,
  v_p_all.visit,
  v_p_all.param,
  COALESCE(abt_only.pcpt_count, 0) pcpt_count
FROM
(SELECT DISTINCT
  v.visit,
  p.param
FROM
(SELECT DISTINCT visit FROM adlb_virology) v 
CROSS JOIN 
(SELECT DISTINCT param FROM adlb_virology) p
WHERE 
  REGEXP_MATCHES(v.visit, '^WK|OT')) v_p_all
LEFT OUTER JOIN (
SELECT
  vc.visit_number,
  av.visit,
  av.param,
  COUNT(usubjid) pcpt_count
FROM 
  adlb_virology av
  JOIN 
    visit_codes vc
    ON 
      av.visit = vc.visit  
WHERE 
  EXISTS(
    SELECT 1
    FROM 
      pcpts_selected_for_abbott_collab pcpts
    WHERE 
      av.usubjid = pcpts.usubjid)
GROUP BY 
  vc.visit_number,
  av.visit,
  av.param
) abt_only
ON 
  v_p_all.visit = abt_only.visit 
  AND 
    v_p_all.param = abt_only.param)
 TO 'visits_params_pcpt_counts_all_20240919.xlsx'
 WITH (FORMAT GDAL, DRIVER 'xlsx');
```

The generated spreadsheet _visits_params_pcpt_counts_all_20240919.xlsx_ was further manipulated in Excel to fill in the blank visit numbers using XLOOKUP.


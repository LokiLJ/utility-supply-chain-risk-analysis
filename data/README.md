# Data access

The case workbook, case text, and teaching note are not included in this repository. Access to the original Ivey materials must be obtained independently through the publisher or an authorized course channel.

To rerun the curated analysis notebook with an authorized workbook, place it at:

```text
data/private/Supplement_data.xlsx
```

The `data/private/` directory and Excel workbooks are ignored by Git. Keep the original sheet names and column headings expected by the notebook.

The public figures can be regenerated without that workbook. `scripts/build_figures.py` contains only the selected chart inputs transcribed from the original notebook's saved analytical summaries. These are historical case results, not a current company dataset or a substitute for the original case materials. See [figure source notes](../docs/figure_source_notes.md) for provenance and rounding.

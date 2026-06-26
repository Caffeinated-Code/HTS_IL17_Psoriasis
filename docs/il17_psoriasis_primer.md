# IL-17 Psoriasis Biology Primer

Plaque psoriasis is an inflammatory skin disease with strong involvement of the IL-23 / Th17 / IL-17 axis. IL-23 supports Th17 cell maintenance, Th17 cells produce IL-17-family cytokines, and IL-17 signaling can drive keratinocyte inflammatory programs.

```mermaid
flowchart LR
    A["IL-23 signaling"] --> B["Th17 cell maintenance"]
    B --> C["IL-17A / IL-17F production"]
    C --> D["Keratinocyte activation"]
    D --> E["Inflammatory skin phenotype"]
```

## Why It Matters Here

The workflow tests whether screening-style signals connect to disease evidence:

- expression changes in psoriatic skin
- protein-level evidence in lesional tissue
- cell-type context from single-cell datasets
- pathway interpretation around Th17, cytokine signaling, and keratinocyte activation

## Common Pitfalls

- IL-17 pathway relevance does not mean every pathway node is equally druggable.
- Broad inflammatory genes may score well but lack specificity.
- Upstream regulators can be biologically relevant while still being hard to modulate safely.

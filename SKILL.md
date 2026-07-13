---
name: prune-paper
description: Prune Markdown papers into -pruned and -reference companions for ingestion. Use when asked to prune an academic paper .md, split references, remove extraction noise, or deduplicate captions without summarizing.
---

# Prune Paper

## Contract

Input must be an academic paper in Markdown (`.md`). Create two derived UTF-8 files without changing the original:

- `<stem>-pruned.md`: substantive paper text, same wording and order, with noise removed.
- `<stem>-reference.md`: moved reference/bibliography section, preserved for citation tracing.

Pruning is deletion and movement only. Do not summarize, paraphrase, merge sections, or improve prose.

## Safety Rule

Prefer leftover noise over lost content. Keep any block that might contain a claim, method detail, limitation, definition, result, dataset, named system, figure/table meaning, caveat, ethical issue, or future-work item.

## Steps

1. Confirm the input is a Markdown paper.
2. Inspect headings to locate body, reference section, and extraction artifacts.
3. Create `<stem>-pruned.md` and `<stem>-reference.md`.
4. Move `References`, `Bibliography`, `Works cited`, or equivalent reference sections to `-reference.md`.
5. Remove clear extraction/admin noise from `-pruned.md`.
6. Scan removed and moved material against the safety rule.
7. Report removed classes and any uncertain leftovers retained.

## Remove From `-pruned.md`

- Publisher UI, update icons, navigation, cookie/banner, download/share boilerplate.
- Author affiliations, correspondence, equal-contribution notes, author contributions, acknowledgements, competing interests, publisher notes, additional information, rights/license boilerplate.
- Local image/hash filenames and standalone image syntax when caption or nearby text preserves figure meaning.
- Duplicate figure descriptions, especially repeated alt text followed by the same caption.
- Page headers/footers, line-wrap artifacts, isolated page numbers, journal mastheads, repeated article titles.

## Keep In `-pruned.md`

- Title, authors, publication date/year, DOI/URL/arXiv identifier.
- Abstract, substantive sections, headings, and paragraph order.
- Figure/table captions once when they encode a roadmap, taxonomy, architecture, task list, metric list, or conceptual distinction.
- Boxes, callouts, definitions, equations, algorithms, tables, appendices, limitations, ethics/societal-impact sections, and substantive data/code availability statements.
- Named datasets, systems, benchmarks, examples, methods, metrics, claims, limitations, assumptions, and future-work items.

## Done When

- Original file is unchanged.
- `-pruned.md` contains the full substantive paper body in original order.
- `-reference.md` contains the reference section when one existed, or a short note that no reference section was found.
- No removed-only material violates the safety rule.
- Any ambiguous boilerplate was retained or marked with `<!-- prune-review: ... -->`.
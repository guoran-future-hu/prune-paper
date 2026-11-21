---
name: prune-paper
description: Prune academic paper .md — split references/appendix, strip extraction noise. Use when asked to prune, clean, or deduplicate a paper markdown.
---

# Prune Paper

## Contract

Input: one academic paper `.md`. Produce three files by splitting + stripping — never summarize or reword.

- `<stem>-pruned.md` — body before references, noise removed
- `<stem>-reference.md` — reference/bibliography section
- `<stem>-appendix.md` — everything after references

## Workflow

### Phase 1: Split

```bash
python3 scripts/split_sections.py <paper.md>
```

Finds the reference heading (`## References`, `# Bibliography`, `## Works Cited`, etc. — case-insensitive), splits there: before → `-pruned.md`, ref section → `-reference.md`, after → `-appendix.md`.

### Phase 2: Review

Open all three files. Scan for obvious anomalies — wrong split point, section in wrong file, truncated content. Don't reason, just look. Fix if something's off.

### Phase 3: Prune

Open `-pruned.md`. Remove:

- Publisher UI, update icons, cookie/banner, download/share boilerplate
- Hash image filenames and standalone `![...](hash_img.jpg)` when caption nearby preserves figure meaning
- Duplicate figure descriptions (alt text repeated verbatim after its caption)
- Page headers/footers, line-wrap artifacts, isolated page numbers, journal mastheads

Keep:

- Author names, affiliations, equal-contribution notes, acknowledgements
- Abstract, all substantive sections in original order
- Figure/table captions once when substantive
- Equations, algorithms, tables, limitations, ethics sections, data/code availability
- Named datasets, systems, benchmarks, metrics, claims, future-work items

## Pitfalls

### Sequential `patch` fragility on extracted markdown

Extracted markdown from Datalab/MinerU often has repeating structural blocks (figures with alt-text + caption, tables, etc.). When you try to clean these with sequential `patch` calls, later patches can silently break. **Correct approach:** write a one-shot Python script in `/tmp/` that processes the entire file in a single pass, using regex replacement. Prefer this over chaining `patch` calls.

### JSON manifest edits

When editing `figure_manifest.json` to mark appendix items with `"skip": true`, do NOT use sequential `patch` on individual items. Use a `python3 -c "..."` one-liner to load, modify, and re-save the entire JSON in one atomic write.

### Journal masthead matching — use `startswith`, not `==`

Extracted markdown may carry journal/section mastheads like `# INFORMATION SCIENCE`. Exact string equality (`==`) fails on trailing spaces, Unicode variation, or extraction artifacts invisible to a visual scan. **Use `startswith` or `in` instead.** In the cleanup script:

```python
# WRONG — brittle
if stripped == '# INFORMATION SCIENCE':
    continue

# RIGHT — handles trailing spaces and extraction noise
if stripped.startswith('# INFORMATION SCIENCE'):
    continue
```

### Broken paragraph across page break — affiliation + figure splits a sentence

Datalab/MinerU extraction often places an affiliation block and a figure between a sentence tail and a fragment that starts the next paragraph. Common pattern:

```
...as
[pagination break]
Department of ... University ... Email ...
[pagination break]
![](figure.jpg)
**Figure 1.** ...
[pagination break]
illustrated in Figure 1. Real content continues...
```

**Fix:** replace the orphaned `illustrated in Figure 1.` prefix with `Illustrated in Figure 1.` (capitalized, standalone). Do NOT delete the fragment — it carries new content.

## Safety

Prefer leftover noise over lost content. If a block might contain a claim, method, result, or caveat — **keep it**. Mark ambiguous boilerplate with `<!-- prune-review: ... -->`.

## Done when

- Original unchanged
- Three output files produced
- `-pruned.md` contains body only, noise removed, original order
- `-reference.md` and `-appendix.md` each contain their section or a print saying none found
- No content lost that violates Safety

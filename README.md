# Prune Paper

Prune Paper conservatively trims academic papers in Markdown for more efficient downstream LLM workflows. It commonly reduces token count by **20–40%** while preserving the paper's substantive text, wording, and order.

## What it does

Given an academic paper in `.md` format, the skill creates two UTF-8 derived files without modifying the original:

- `<stem>-pruned.md` — the complete substantive paper body with extraction and publisher noise removed.
- `<stem>-reference.md` — the paper's reference or bibliography section, retained separately for citation tracing.

It removes only clear noise: publisher UI, author and license boilerplate, page furniture, local image filenames, and duplicated figure descriptions. It does not summarize, paraphrase, merge sections, or rewrite prose.

## Why use it

Academic-paper Markdown extracted from PDFs or publishers often includes large amounts of non-substantive material. Reducing that clutter lets later LLM stages spend their context budget on methods, evidence, limitations, and results instead.

## Use

Ask Codex to prune a Markdown paper, for example:

```text
Use $prune-paper to prune path/to/paper.md
```

The skill favors retaining uncertain material over risking loss of a claim, method detail, figure meaning, or citation-relevant information.

## Scope

This is a structural cleanup tool, not a summarizer. The original Markdown remains unchanged; the generated `-pruned.md` and `-reference.md` files are derived reading aids.

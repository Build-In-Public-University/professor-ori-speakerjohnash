# Mind simulator renderer

This repo uses a small projection pipeline instead of hand-writing the page directly.

The contract:

1. Receipts stay in data files.
2. The projection memory states the best legible version of the public material.
3. The renderer fills the README and HTML page from that memory.
4. Raw dumps stay out of git.

Files:

- `profile.json` — base ORI/public profile metadata.
- `data/x-satellite-summary.json` — derived X satellite summary. Counts, selected public URLs, link scan. No raw NDJSON.
- `data/mind-memory.json` — the projection memory: voice model, thesis, teaching sections, and receipt-backed claims.
- `scripts/render_mind_profile.py` — deterministic renderer.

Run:

```bash
python3 scripts/render_mind_profile.py
```

For another professor repo, repeat the same shape:

1. Build or update `profile.json`.
2. Add derived receipt summaries under `data/`.
3. Write `data/mind-memory.json` in the subject's best organized public voice.
4. Run the renderer.
5. Verify boundaries: no raw dumps, no numeric Discord IDs, no private records, no fake endorsement.

The renderer is deliberately simple. The judgment belongs in the memory file, where it can be inspected, corrected, and replaced.

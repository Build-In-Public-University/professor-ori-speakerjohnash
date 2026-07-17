#!/usr/bin/env python3
"""Render a Build In Public University mind projection page from public receipts.

This is intentionally boring: load receipts, load projection memory, fill the page
contract. The judgment lives in data/mind-memory.json; the renderer keeps receipts
visible and raw dumps out of the repo.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def load_receipts(root: Path) -> dict[str, Any]:
    receipts: dict[str, Any] = {
        "profile": load_json(root / "profile.json"),
        "mind": load_json(root / "data" / "mind-memory.json"),
    }
    summary_path = root / "data" / "x-satellite-summary.json"
    if summary_path.exists():
        receipts["x_summary"] = load_json(summary_path)
    return receipts


def render_readme(receipts: dict[str, Any]) -> str:
    profile = receipts["profile"]
    mind = receipts["mind"]
    x = receipts.get("x_summary", {})
    links = profile.get("link_scan", []) or x.get("link_scan", [])
    selected = x.get("selected_public_tweets", [])
    themes = x.get("theme_counts", {})

    memory_rows = "\n".join(
        f"- {m['name']}: {m['claim']}\n  - Receipt: {m['receipt']}"
        for m in mind["memory"]
    )
    sections = "\n\n".join(
        f"## {section['heading']}\n\n{section['body']}"
        for section in mind["template"]["sections"]
    )
    theme_rows = "\n".join(
        f"| {name} | {count} |" for name, count in themes.items()
    )
    selected_rows = "\n".join(
        f"- {t['created_at']} — {t['text']} ([source]({t['url']}))"
        for t in selected[:6]
    )
    link_rows = "\n".join(
        f"- [{item['label']}]({item['url']}) — {item['evidence']}"
        for item in links
    )

    return f"""# {mind['display_name']}\n\n> Modeled public projection for `{mind['handle']}`. Built from the receipts in this repo.\n\n{mind['projection_boundary']}\n
---

# {mind['template']['hero_title']}

{mind['template']['hero_subtitle']}

{mind['core_thesis']}

{sections}

## What the receipts say

- ORI public mirror messages: `{profile.get('message_count')}`
- Visible X records scanned: `{x.get('captured_rows')}`
- Visible authored X cards: `{x.get('speakerjohnash_tweets')}`
- X date range: `{x.get('date_range', {}).get('first')}` to `{x.get('date_range', {}).get('last')}`
- Visible engagement total: {x.get('visible_metrics_total', {}).get('likes_visible')} likes, {x.get('visible_metrics_total', {}).get('replies_visible')} replies, {x.get('visible_metrics_total', {}).get('reposts_visible')} reposts
- Link hub: {mind['receipts']['linktree']}

## Memory loaded into the projection

{memory_rows}

## Recurrent signal counts

| Signal | Count proxy |
|---|---:|
{theme_rows}

## Public surfaces

{link_rows}

## Selected public X receipts

{selected_rows}

## Boundary

This page is a projection system output. It is trying to make the best organized version of the public material legible. It should be corrected or removed if the person asks. It does not publish the raw X dump, raw Discord text, numeric Discord IDs, private records, hidden replies, actor-level likes, or private affiliation claims.

Generated from `{mind['schema']}`.
"""


def render_html(receipts: dict[str, Any]) -> str:
    profile = receipts["profile"]
    mind = receipts["mind"]
    x = receipts.get("x_summary", {})
    themes = x.get("theme_counts", {})
    links = profile.get("link_scan", []) or x.get("link_scan", [])
    selected = x.get("selected_public_tweets", [])[:4]
    sections = mind["template"]["sections"]

    css = """
:root{color-scheme:dark;--bg:#08090c;--panel:#11151b;--text:#f2efe7;--muted:#aaa297;--line:#303641;--gold:#e1b866;--violet:#b998ff;--blue:#8ab4f8}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at top left,#272034 0,#08090c 34rem);color:var(--text);font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.55}main{max-width:1100px;margin:0 auto;padding:48px 20px 80px}.hero,.card,.section{border:1px solid var(--line);background:rgba(17,21,27,.88);border-radius:24px;padding:28px}.eyebrow{color:var(--gold);text-transform:uppercase;letter-spacing:.16em;font-size:.78rem;font-weight:800}h1{font-size:clamp(2.4rem,6vw,5.5rem);line-height:.93;margin:.35em 0;max-width:980px}h2{color:var(--gold);margin:0 0 12px}a{color:var(--blue)}.muted{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:22px 0}.stack{display:grid;gap:16px}.metric{font-size:2rem;color:var(--gold);font-weight:900}.cta{display:inline-block;margin:14px 10px 0 0;background:var(--gold);color:#111;text-decoration:none;padding:12px 17px;border-radius:999px;font-weight:900}.ghost{background:transparent;color:var(--gold);border:1px solid var(--gold)}li{margin:.4rem 0}blockquote{border-left:3px solid var(--violet);padding-left:14px;color:#ddd;margin:18px 0}.receipt{font-size:.9rem;color:var(--muted)}
"""
    stat_cards = [
        ("ORI messages", profile.get("message_count")),
        ("visible X cards", x.get("speakerjohnash_tweets")),
        ("visible media tweets", x.get("media_tweets_visible")),
        ("visible likes", x.get("visible_metrics_total", {}).get("likes_visible")),
    ]
    html_sections = "".join(
        f"<section class='section'><h2>{esc(section['heading'])}</h2><p>{esc(section['body'])}</p></section>"
        for section in sections
    )
    theme_list = "".join(f"<li><b>{esc(k)}</b>: {esc(v)} count proxy</li>" for k, v in themes.items())
    link_list = "".join(f"<li><a href='{esc(item['url'])}'>{esc(item['label'])}</a> — {esc(item['evidence'])}</li>" for item in links)
    quote_list = "".join(f"<blockquote>{esc(t['text'])}</blockquote><p class='receipt'>{esc(t['created_at'])} · <a href='{esc(t['url'])}'>source</a></p>" for t in selected)
    cards = "".join(f"<div class='card'><div class='metric'>{esc(value)}</div><div>{esc(label)}</div></div>" for label, value in stat_cards)

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(mind['display_name'])} — mind projection</title><style>{css}</style></head><body><main><section class="hero"><div class="eyebrow">Build In Public University · mind projection</div><h1>{esc(mind['template']['hero_title'])}</h1><p class="muted">{esc(mind['template']['hero_subtitle'])}</p><p>{esc(mind['core_thesis'])}</p><p>{esc(mind['projection_boundary'])}</p><a class="cta" href="{esc(profile['professor_gate'])}">Open professor gate →</a><a class="cta ghost" href="{esc(mind['receipts']['linktree'])}">Linktree →</a></section><div class="grid">{cards}</div><div class="stack">{html_sections}</div><section class="section"><h2>Receipts loaded</h2><ul>{theme_list}</ul></section><section class="section"><h2>Public surfaces</h2><ul>{link_list}</ul></section><section class="section"><h2>Selected X receipts</h2>{quote_list}</section><section class="section"><h2>Boundary</h2><p>This is a public projection, not a private mind read. Raw dumps stay out of the repo.</p></section></main></body></html>\n"""


def update_profile(receipts: dict[str, Any]) -> dict[str, Any]:
    profile = receipts["profile"]
    mind = receipts["mind"]
    profile["mind_projection"] = {
        "schema": mind["schema"],
        "display_name": mind["display_name"],
        "role": mind["role"],
        "core_thesis": mind["core_thesis"],
        "projection_boundary": mind["projection_boundary"],
        "voice_model": mind["voice_model"],
        "memory_items": len(mind["memory"]),
        "renderer": "scripts/render_mind_profile.py",
    }
    return profile


def main() -> None:
    receipts = load_receipts(ROOT)
    (ROOT / "README.md").write_text(render_readme(receipts))
    (ROOT / "index.html").write_text(render_html(receipts))
    (ROOT / "profile.json").write_text(json.dumps(update_profile(receipts), indent=2, ensure_ascii=False) + "\n")
    print(f"rendered mind projection for {receipts['mind']['handle']}")


if __name__ == "__main__":
    main()

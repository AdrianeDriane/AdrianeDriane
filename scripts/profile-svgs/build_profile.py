"""Build header.svg and footer.svg for the GitHub profile README.

Both match lowlighter/metrics' classic template (480px wide, same font stack,
#777 text, #0366d6 headings, #959da5 icons) so header + metrics + footer read
as one card. Colors are theme-neutral so they work on GitHub light and dark;
"subtle" text uses opacity so the hierarchy holds on both backgrounds.

Run `bash scripts/profile-svgs/make.sh` instead of calling this directly; it
measures the rendered heights and writes both SVGs to the repo root.

Low-level usage (what make.sh does):
  python3 -I build_profile.py <icons_dir> measure <out.html>
      -> page whose <title> becomes "H=<header>,<footer>" once rendered
  python3 -I build_profile.py <icons_dir> build <out_dir> <header_h> <footer_h>

To add a tech: put its icon in icons/ (Simple Icons slug or an Octicon) and
add an entry to STACK.
"""
import re
import sys
from pathlib import Path

icons_dir, mode = Path(sys.argv[1]), sys.argv[2]


def icon(name, color, size=14):
    src = (icons_dir / f"{name}.svg").read_text()
    view = re.search(r'viewBox="([^"]+)"', src).group(1)
    body = "".join(f'<path d="{d}"/>' for d in re.findall(r'\sd="([^"]+)"', src))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" '
            f'width="{size}" height="{size}" style="fill:{color}">{body}</svg>')


NEUTRAL = "#959da5"
STACK = [
    ("Frontend", [
        ("TypeScript", "typescript", "#3178C6"),
        ("React", "react", "#61DAFB"),
        ("Next.js", "nextdotjs", NEUTRAL),
        ("Tailwind", "tailwindcss", "#06B6D4"),
    ]),
    ("Backend", [
        ("Node.js", "nodedotjs", "#5FA04E"),
        ("Express", "express", NEUTRAL),
        ("NestJS", "nestjs", "#E0234E"),
    ]),
    ("Data", [
        ("PostgreSQL", "postgresql", "#4169E1"),
        ("MongoDB", "mongodb", "#47A248"),
        ("Supabase", "supabase", "#3FCF8E"),
    ]),
    ("AI", [
        ("AI Integrations", "oct-sparkle-fill-16", "#a371f7"),
        ("Claude Code", "claude", "#D97757"),
        ("Codex", "oct-terminal-16", NEUTRAL),
    ]),
]
SPORTS = [("🏀", "Basketball"), ("⚽", "Football"), ("🥊", "MMA")]

CSS = """
svg{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji;color:#777;font-size:14px}
.wrap{width:480px;box-sizing:border-box;padding:4px 0 6px}
h2,h3{margin:8px 0 2px;padding:0;color:#0366d6;font-weight:400}
h2{font-size:16px}
.field{display:flex;align-items:center;margin:0 5px 2px;white-space:nowrap}
.field>svg{margin:0 8px;fill:#959da5;flex-shrink:0}
.hero{padding:6px 13px 12px}
.hello{font-size:26px;font-weight:600;line-height:1.25;margin:0;letter-spacing:-.3px}
.name{background:linear-gradient(90deg,#2f81f7 0%,#06b6d4 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}
.rocket{display:inline-block;margin-left:4px;font-size:22px;animation:float 3s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
.tagline{margin:4px 0 0;font-size:15px;color:#777}
.focus{margin:3px 0 0;font-size:12.5px;color:#777;opacity:.8}
.focus b{font-weight:400;color:#0366d6;margin:0 5px}
.role{display:inline-flex;align-items:center;gap:6px;margin-top:10px;padding:3px 10px 3px 8px;
  border-radius:999px;background:#7777771f;font-size:12.5px;color:#777}
.dot{width:7px;height:7px;border-radius:50%;background:#3fb950;box-shadow:0 0 0 0 #3fb95066;animation:pulse 2.4s ease-out infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 #3fb95066}70%{box-shadow:0 0 0 6px #3fb95000}100%{box-shadow:0 0 0 0 #3fb95000}}
.stack,.off{padding:2px 5px 0 13px}
.row{display:flex;align-items:flex-start;margin:6px 0}
.group{flex:0 0 76px;font-size:12.5px;color:#777;opacity:.75;padding-top:3px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:center;gap:5px;padding:2px 8px 2px 6px;border-radius:6px;
  background:#7777771f;font-size:12.5px;color:#777;line-height:18px}
.chip svg{flex-shrink:0}
.note{margin:4px 0 8px;font-size:13px;color:#777;opacity:.8}
.emo{font-size:13px;line-height:18px}
"""

rows = "".join(
    f'<div class="row"><span class="group">{group}</span><div class="chips">'
    + "".join(f'<span class="chip">{icon(slug, color)}{label}</span>' for label, slug, color in items)
    + "</div></div>"
    for group, items in STACK
)

HEADER = f"""<div class="wrap">
  <section class="hero">
    <p class="hello"><span class="name">Hello, I'm Adriane</span><span class="rocket">🚀</span></p>
    <p class="tagline">Building high‑impact, feature‑rich software.</p>
    <p class="focus">Full‑stack<b>•</b>AI integrations<b>•</b>AI‑assisted engineering</p>
    <span class="role"><span class="dot"></span>Software Engineer @ Pacific Equities</span>
  </section>
  <section>
    <h2 class="field">{icon("oct-stack-16", NEUTRAL, 16)}Tech Stack</h2>
    <div class="stack">{rows}</div>
  </section>
</div>"""

FOOTER = f"""<div class="wrap">
  <section>
    <h2 class="field">{icon("oct-trophy-16", NEUTRAL, 16)}Off‑hours</h2>
    <div class="off">
      <p class="note">Sports nerd. I love watching:</p>
      <div class="chips">{"".join(f'<span class="chip"><span class="emo">{e}</span>{label}</span>' for e, label in SPORTS)}</div>
    </div>
  </section>
</div>"""

PARTS = {
    "header": (HEADER, "Adriane: Building high-impact, feature-rich software. Software Engineer @ Pacific Equities."),
    "footer": (FOOTER, "Off-hours: Sports nerd. I love watching basketball, football and MMA."),
}


def svg(body, title, height):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="480" height="{height}" viewBox="0 0 480 {height}">
<title>{title}</title>
<style>{CSS}</style>
<foreignObject x="0" y="0" width="100%" height="100%">
<div xmlns="http://www.w3.org/1999/xhtml">{body}</div>
</foreignObject>
</svg>
"""


if mode == "measure":
    # Same markup inline (not as <img>) so each part's content height can be measured.
    blocks = "".join(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="1000"><style>{CSS}</style>'
        f'<foreignObject x="0" y="0" width="100%" height="100%"><div xmlns="http://www.w3.org/1999/xhtml" id="{k}">{body}</div></foreignObject></svg>'
        for k, (body, _) in PARTS.items()
    )
    ids = ",".join(f"'{k}'" for k in PARTS)
    Path(sys.argv[3]).write_text(
        f"""<!doctype html><meta charset="utf-8"><body style="margin:0">{blocks}
<script>document.title = 'H=' + [{ids}].map(id => Math.ceil(document.getElementById(id).getBoundingClientRect().height)).join(',')</script>"""
    )
elif mode == "build":
    out_dir = Path(sys.argv[3])
    for (k, (body, title)), h in zip(PARTS.items(), sys.argv[4:6]):
        (out_dir / f"{k}.svg").write_text(svg(body, title, int(h)))
        print("wrote", out_dir / f"{k}.svg", h)

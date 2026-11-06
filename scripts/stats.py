"""Gera assets/stats.svg com estatísticas reais do GitHub (tema hacker).

Uso (no GitHub Actions):  GITHUB_TOKEN=... python scripts/stats.py MTM4T3US assets/stats.svg
Teste local sem rede:      python scripts/stats.py MTM4T3US /tmp/stats.svg --mock
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from xml.sax.saxutils import escape

API = "https://api.github.com"
G, G2, G3, SOFT, BG = "#00ff41", "#00c832", "#0a7a2a", "#c4ffd3", "#001a0c"
MONO = "'Courier New', Courier, monospace"


def request(url, body=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch(user):
    q = """query($u:String!){ user(login:$u){
      contributionsCollection{ totalCommitContributions
        contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } } } }"""
    cal = request(f"{API}/graphql", {"query": q, "variables": {"u": user}})
    cc = cal["data"]["user"]["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]

    repos = request(f"{API}/users/{user}/repos?per_page=100&type=owner")
    langs = {}
    for r in repos:
        if r["fork"] or r["name"].lower() == user.lower():
            continue
        for name, size in request(r["languages_url"]).items():
            langs[name] = langs.get(name, 0) + size
    return {
        "total": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"],
        "repos": sum(1 for r in repos if not r["fork"]),
        "days": [(d["date"], d["contributionCount"]) for d in days],
        "langs": langs,
    }


def mock():
    import random
    random.seed(7)
    start = dt.date.today() - dt.timedelta(days=364)
    days = [((start + dt.timedelta(i)).isoformat(), random.choice([0, 0, 1, 2, 4])) for i in range(365)]
    return {"total": sum(c for _, c in days), "commits": 120, "repos": 4, "days": days,
            "langs": {"HTML": 52000, "Python": 41000, "CSS": 30000, "JavaScript": 4000}}


def streaks(days):
    counts = [c for _, c in sorted(days)]
    longest = cur = 0
    for c in counts:
        cur = cur + 1 if c else 0
        longest = max(longest, cur)
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:  # hoje ainda sem contribuição não quebra a sequência
        i -= 1
    current = 0
    while i >= 0 and counts[i]:
        current += 1
        i -= 1
    return current, longest


def render(user, s):
    current, longest = streaks(s["days"])
    total_bytes = sum(s["langs"].values()) or 1
    top = sorted(s["langs"].items(), key=lambda kv: -kv[1])[:5]

    W, fs, lh, left = 620, 17, 28, 26
    cw = fs * 0.6
    rows = [
        ("contribuições (1 ano)", s["total"]),
        ("commits (1 ano)", s["commits"]),
        ("repositórios públicos", s["repos"]),
        ("sequência atual", f"{current} dia" + ("s" if current != 1 else "")),
        ("maior sequência", f"{longest} dia" + ("s" if longest != 1 else "")),
    ]
    y = 74
    out = [f'<text x="{left}" y="{y}" font-size="{fs}"><tspan fill="{G}" font-weight="700">$</tspan>'
           f'<tspan fill="#e6ffec"> ./stats --user {escape(user)}</tspan></text>']
    delay = 0.3
    for label, val in rows:
        y += lh
        dots = "." * (30 - len(label))
        out.append(f'<text class="show" style="animation-delay:{delay:.2f}s" x="{left + 2 * cw:.1f}" y="{y}" font-size="{fs}">'
                   f'<tspan fill="{SOFT}">{escape(label)} </tspan><tspan fill="#3ddc6a" fill-opacity=".6">{dots}</tspan>'
                   f'<tspan fill="{G}" font-weight="700"> {escape(str(val))}</tspan></text>')
        delay += 0.15
    y += lh + 12
    out.append(f'<text class="show" style="animation-delay:{delay:.2f}s" x="{left}" y="{y}" font-size="{fs}">'
               f'<tspan fill="{G}" font-weight="700">$</tspan><tspan fill="#e6ffec"> ./linguagens --top {len(top)}</tspan></text>')
    bar_x, bar_w = left + 2 * cw + 13 * cw, 300
    shades = [G, "#22e05a", G2, "#169c3a", G3]
    for i, (name, size) in enumerate(top):
        y += lh
        pct = size / total_bytes * 100
        d = delay + 0.3 + i * 0.15
        out.append(f'<text class="show" style="animation-delay:{d:.2f}s" x="{left + 2 * cw:.1f}" y="{y}" font-size="{fs}" fill="{SOFT}">{escape(name[:12])}</text>')
        out.append(f'<rect x="{bar_x:.1f}" y="{y - 13}" width="{bar_w}" height="14" rx="2" fill="{G}" fill-opacity=".08" stroke="{G}" stroke-opacity=".25"/>')
        out.append(f'<rect class="bar" style="animation-delay:{d:.2f}s" x="{bar_x:.1f}" y="{y - 13}" width="{max(bar_w * pct / 100, 2):.1f}" height="14" rx="2" fill="{shades[i]}"/>')
        out.append(f'<text class="show" style="animation-delay:{d:.2f}s" x="{W - 26}" y="{y}" font-size="{fs - 2}" fill="{G}" text-anchor="end">{pct:.1f}%</text>')
    if not top:
        y += lh
        out.append(f'<text x="{left + 2 * cw:.1f}" y="{y}" font-size="{fs}" fill="{SOFT}">nenhuma linguagem encontrada</text>')
    y += lh + 6
    brasilia = dt.timezone(dt.timedelta(hours=-3))
    stamp = dt.datetime.now(brasilia).strftime("%d/%m/%Y %H:%M (Brasília)")
    out.append(f'<text x="{left}" y="{y}" font-size="13" fill="#3ddc6a">// atualizado em {stamp}</text>')
    H = y + 22
    per = 2 * (W + H)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Estatísticas do GitHub de {escape(user)}">
<defs><clipPath id="round"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="{G}" stroke-opacity=".08"/></pattern>
  <pattern id="lines" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1" fill="#000" fill-opacity=".22"/></pattern>
  <filter id="glowS" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="1.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>
  text {{ font-family: {MONO}; }}
  .show {{ opacity: 0; animation: appear .3s ease-out forwards; }}
  @keyframes appear {{ to {{ opacity: 1; }} }}
  .bar {{ transform-box: fill-box; transform-origin: left; transform: scaleX(0); animation: grow 1.2s ease-out forwards; }}
  @keyframes grow {{ to {{ transform: scaleX(1); }} }}
  .run {{ animation: run 6s linear infinite; }}
  @keyframes run {{ to {{ stroke-dashoffset: -{per}; }} }}
</style>
<g clip-path="url(#round)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="40" fill="#003a17"/>
  <line x1="0" y1="40" x2="{W}" y2="40" stroke="{G}" stroke-opacity=".5"/>
  <circle cx="22" cy="20" r="6" fill="{G}"/><circle cx="42" cy="20" r="6" fill="{G2}"/><circle cx="62" cy="20" r="6" fill="{G3}"/>
  <text x="{W / 2}" y="25" font-size="14" fill="#3ddc6a" text-anchor="middle">github-stats.sh</text>
  <rect y="40" width="{W}" height="{H}" fill="url(#grid)"/>
  {''.join(out)}
  <rect width="{W}" height="{H}" fill="url(#lines)"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13" fill="none" stroke="{G}" stroke-opacity=".45" stroke-width="2"/>
<rect class="run" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13" fill="none" stroke="{G}" stroke-width="3" stroke-dasharray="140 {per - 140}" filter="url(#glowS)"/>
</svg>"""


if __name__ == "__main__":
    user, path = sys.argv[1], sys.argv[2]
    data = mock() if "--mock" in sys.argv else fetch(user)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render(user, data))
    print("stats ok ->", path)

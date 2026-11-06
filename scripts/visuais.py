"""Gera os SVGs animados do perfil (tema hacker verde).

Uso: python scripts/visuais.py   (grava em assets/)
Para mudar textos, edite as listas no final do arquivo e rode de novo.
"""
import math
import os
import random
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(os.path.join(OUT, "projetos"), exist_ok=True)
random.seed(1337)

G = "#00ff41"       # verde neon
G2 = "#00c832"      # verde médio
G3 = "#0a7a2a"      # verde escuro
DIM = "#3ddc6a"     # verde para detalhes
SOFT = "#c4ffd3"    # texto claro
TBG = "#001a0c"     # fundo sólido das janelas
MONO = "'Courier New', Courier, monospace"
BOLD = "Consolas, 'SF Mono', Menlo, 'DejaVu Sans Mono', 'Courier New', monospace"
CW = 0.6            # largura do caractere (em) da fonte mono


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("ok", name)


def defs(W, H, R):
    """Gradiente verde, grade, scanlines, brilho e recorte arredondado."""
    return f"""
  <radialGradient id="bgg" cx="50%" cy="35%" r="80%">
    <stop offset="0" stop-color="#005c25"/>
    <stop offset=".5" stop-color="#002a11"/>
    <stop offset="1" stop-color="#000f06"/>
  </radialGradient>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">
    <path d="M22 0H0V22" fill="none" stroke="{G}" stroke-opacity=".08"/>
  </pattern>
  <pattern id="lines" width="3" height="3" patternUnits="userSpaceOnUse">
    <rect width="3" height="1" fill="#000" fill-opacity=".22"/>
  </pattern>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{G}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{G}" stop-opacity=".09"/>
    <stop offset="1" stop-color="{G}" stop-opacity="0"/>
  </linearGradient>
  <filter id="glow" x="-30%" y="-60%" width="160%" height="220%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glowS" x="-30%" y="-60%" width="160%" height="220%">
    <feGaussianBlur stdDeviation="1.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="round"><rect width="{W}" height="{H}" rx="{R}"/></clipPath>"""


def base_css(W, H, R):
    per = 2 * (W + H)
    return f"""
  text {{ font-family: {MONO}; }}
  .b {{ font-family: {BOLD}; font-weight: 700; }}
  .blink {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .scanbar {{ animation: scan 7s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateY(-120px); }} to {{ transform: translateY({H}px); }} }}
  .run {{ animation: run 6s linear infinite; }}
  @keyframes run {{ to {{ stroke-dashoffset: -{per}; }} }}
  .spin {{ transform-box: fill-box; transform-origin: center; animation: spin 8s linear infinite; }}
  .spinr {{ transform-box: fill-box; transform-origin: center; animation: spin 5s linear infinite reverse; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  .show {{ opacity: 0; animation: appear .2s ease-out forwards; }}
  @keyframes appear {{ to {{ opacity: 1; }} }}"""


def frame(W, H, R, lw=2):
    """Borda neon com um ponto de luz que corre em volta."""
    per = 2 * (W + H)
    return (
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{R-1}" fill="none" stroke="{G}" stroke-opacity=".45" stroke-width="{lw}"/>'
        f'<rect class="run" x="1" y="1" width="{W-2}" height="{H-2}" rx="{R-1}" fill="none" stroke="{G}" stroke-width="{lw+1}" '
        f'stroke-dasharray="140 {per - 140}" filter="url(#glowS)"/>'
    )


def bg(W, H):
    return f'<rect width="{W}" height="{H}" fill="url(#bgg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>'


def overlay(W, H):
    return f'<rect class="scanbar" width="{W}" height="120" fill="url(#scan)"/><rect width="{W}" height="{H}" fill="url(#lines)"/>'


def svg_open(W, H, label, extra_defs="", css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(label)}">'
        f"<defs>{defs(W, H, 14)}{extra_defs}</defs><style>{base_css(W, H, 14)}{css}</style>"
    )


# ===================================================================== banner
def banner():
    W, H, R = 1000, 360, 14
    n = 34
    step = W / n
    cols = []
    for i in range(n):
        x = step * i + step / 2
        length = random.randint(10, 20)
        dur = random.uniform(5, 11)
        delay = -random.uniform(0, dur)
        size = random.choice([14, 16, 18])
        tsp = "".join(
            f'<tspan x="{x:.0f}" dy="{size + 4}" fill="{"#eafff0" if k == length - 1 else G}" fill-opacity="{(k + 1) / length:.2f}">{random.choice("01")}</tspan>'
            for k in range(length)
        )
        cols.append(
            f'<g class="rain" style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s"><text font-size="{size}" text-anchor="middle">{tsp}</text></g>'
        )
    sub = "> Eng. de Software & Cyber Segurança"
    fs = 28
    cw = fs * CW
    tw = len(sub) * cw
    sx = (W - tw) / 2
    name = "MATEUS FERREIRA"
    binary = " ".join(format(ord(c), "08b") for c in "MATEUS")
    css = f"""
  .rain {{ animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
  @keyframes fall {{ from {{ transform: translateY(-460px); }} to {{ transform: translateY({H + 20}px); }} }}
  .g1 {{ animation: glitch1 5s steps(1) infinite; }}
  .g2 {{ animation: glitch2 5s steps(1) infinite; }}
  @keyframes glitch1 {{ 0%,91%,100% {{ opacity:0; transform:translate(0,0); }} 92% {{ opacity:.9; transform:translate(-5px,1px); }} 94% {{ opacity:.9; transform:translate(4px,-2px); }} 96% {{ opacity:0; }} }}
  @keyframes glitch2 {{ 0%,92%,100% {{ opacity:0; transform:translate(0,0); }} 93% {{ opacity:.8; transform:translate(5px,2px); }} 95% {{ opacity:.8; transform:translate(-3px,-1px); }} 97% {{ opacity:0; }} }}
  .flick {{ animation: flick 5s steps(1) infinite; }}
  @keyframes flick {{ 0%,91%,97%,100% {{ opacity:1; }} 92%,94% {{ opacity:.35; }} 93%,95% {{ opacity:.85; }} }}
  .type {{ animation: type 9s infinite; }}
  @keyframes type {{
    0% {{ transform: translateX(0); animation-timing-function: steps({len(sub)}); }}
    45% {{ transform: translateX({tw:.1f}px); animation-timing-function: linear; }}
    85% {{ transform: translateX({tw:.1f}px); animation-timing-function: steps({len(sub)}); }}
    100% {{ transform: translateX(0); }}
  }}"""
    PB = "#00150a"
    svg = svg_open(W, H, "Mateus Ferreira - Engenharia de Software e Cyber Segurança", css=css) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <g opacity=".75">{''.join(cols)}</g>
  <rect x="120" y="100" width="760" height="168" rx="8" fill="{PB}" fill-opacity=".97" stroke="{G}" stroke-opacity=".6"/>
  <path d="M120 124 V100 H144 M856 100 H880 V124 M880 244 V268 H856 M144 268 H120 V244" fill="none" stroke="{G}" stroke-width="3" filter="url(#glowS)"/>
  <text x="142" y="125" font-size="13" fill="{DIM}">// root@itumbiara:~# ./apresentar.sh</text>
  <g class="flick">
    <text class="b g1" x="{W/2}" y="190" font-size="62" letter-spacing="4" text-anchor="middle" fill="#9dffb6">{name}</text>
    <text class="b g2" x="{W/2}" y="190" font-size="62" letter-spacing="4" text-anchor="middle" fill="{G3}">{name}</text>
    <text class="b" x="{W/2}" y="190" font-size="62" letter-spacing="4" text-anchor="middle" fill="{G}" filter="url(#glow)">{name}</text>
  </g>
  <text x="{sx:.1f}" y="240" font-size="{fs}" fill="{SOFT}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{escape(sub)}</text>
  <g class="type">
    <rect x="{sx:.1f}" y="214" width="{tw + 4:.1f}" height="34" fill="{PB}"/>
    <rect class="blink" x="{sx + 1:.1f}" y="218" width="{cw - 2:.1f}" height="28" fill="{G}"/>
  </g>
  <rect x="20" y="20" width="238" height="26" rx="5" fill="{PB}" stroke="{G}" stroke-opacity=".5"/>
  <text x="32" y="38" font-size="14" fill="{G}">[ root@itumbiara-go ]</text>
  <rect x="{W-160}" y="20" width="140" height="26" rx="5" fill="{PB}" stroke="{G}" stroke-opacity=".5"/>
  <circle class="blink" cx="{W-142}" cy="33" r="5" fill="{G}" filter="url(#glowS)"/>
  <text x="{W-128}" y="38" font-size="14" fill="{G}">SYS ONLINE</text>
  <rect x="{W/2 - 280}" y="{H-44}" width="560" height="26" rx="5" fill="{PB}" stroke="{G}" stroke-opacity=".35"/>
  <text x="{W/2}" y="{H-26}" font-size="14" fill="{DIM}" text-anchor="middle" letter-spacing="1">{binary}</text>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save("banner.svg", svg)


# ===================================================================== divisor
def divider():
    W, H = 1000, 34
    chunk = "".join(random.choice("01") for _ in range(160))
    fs = 14
    tw = len(chunk) * fs * CW
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="divisor">
<defs>
  <linearGradient id="edge" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/>
    <stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#edge)"/></mask>
</defs>
<style>
  text {{ font-family: {MONO}; }}
  .s {{ animation: slide 30s linear infinite; }}
  @keyframes slide {{ to {{ transform: translateX(-{tw:.1f}px); }} }}
</style>
<g mask="url(#m)">
  <rect x="0" y="4" width="{W}" height="{H-8}" fill="#003314"/>
  <line x1="0" y1="4" x2="{W}" y2="4" stroke="{G}" stroke-opacity=".7"/>
  <line x1="0" y1="{H-4}" x2="{W}" y2="{H-4}" stroke="{G}" stroke-opacity=".7"/>
  <g class="s">
    <text x="0" y="22" font-size="{fs}" fill="{G}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{chunk}</text>
    <text x="{tw:.1f}" y="22" font-size="{fs}" fill="{G}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{chunk}</text>
  </g>
</g>
</svg>"""
    save("divider.svg", svg)


# ===================================================================== títulos
def heading(fname, label, num):
    W, H, R = 640, 64, 12
    fs = 28
    cw = fs * CW
    full = f"> {label}"
    tw = len(full) * cw
    x = 30
    svg = svg_open(W, H, label) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <rect x="0" y="0" width="7" height="{H}" fill="{G}" filter="url(#glowS)"/>
  <text class="b" x="{x}" y="42" font-size="{fs}" fill="{G}" filter="url(#glowS)" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{escape(full)}</text>
  <rect class="blink" x="{x + tw + 6:.1f}" y="20" width="{cw - 2:.1f}" height="26" fill="{G}"/>
  <text x="{W - 20}" y="39" font-size="14" fill="{DIM}" text-anchor="end">[ 0{num} ]</text>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save(fname, svg)


# ===================================================================== terminal
def terminal(lines):
    W, R = 620, 14
    fs, lh, top, left = 18, 30, 76, 26
    cw = fs * CW
    H = top + lh * (len(lines) - 1) + 40
    body, css = [], []
    t = 0.6
    for i, (kind, txt) in enumerate(lines):
        y = top + i * lh
        if kind in ("cmd", "end"):
            body.append(f'<text x="{left}" y="{y}" font-size="{fs}" fill="{G}" font-weight="700">$</text>')
            cx = left + 2 * cw
            if kind == "end":
                body.append(f'<g class="show" style="animation-delay:{t:.2f}s"><rect class="blink" x="{cx:.1f}" y="{y - fs + 3}" width="{cw:.1f}" height="{fs + 2}" fill="{G}"/></g>')
                break
            tw = len(txt) * cw
            dur = len(txt) * 0.055
            k = f"k{i}"
            css.append(f"@keyframes {k} {{ to {{ transform: translateX({tw + cw:.1f}px); }} }}")
            body.append(f'<text x="{cx:.1f}" y="{y}" font-size="{fs}" fill="#eafff0" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{escape(txt)}</text>')
            body.append(f'<rect style="animation:{k} {dur:.2f}s steps({len(txt)}) {t:.2f}s forwards" x="{cx - 1:.1f}" y="{y - fs}" width="{tw + cw + 4:.1f}" height="{fs + 8}" fill="{TBG}"/>')
            body.append(f'<rect class="cur" style="animation:{k} {dur:.2f}s steps({len(txt)}) {t:.2f}s forwards, on {dur + 0.25:.2f}s linear {t:.2f}s" x="{cx:.1f}" y="{y - fs + 3}" width="{cw:.1f}" height="{fs + 2}" fill="{G}"/>')
            t += dur + 0.35
        else:
            color = G if kind == "hi" else SOFT
            body.append(f'<text class="show" style="animation-delay:{t:.2f}s" x="{left + 2 * cw:.1f}" y="{y}" font-size="{fs}" fill="{color}">{escape(txt)}</text>')
            t += 0.18
            if i + 1 < len(lines) and lines[i + 1][0] in ("cmd", "end"):
                t += 0.45
    css.append(".cur { opacity: 0; } @keyframes on { from { opacity: 1; } to { opacity: 1; } }")
    label = "Terminal: " + " ".join(t for k, t in lines if k in ("out", "hi"))
    svg = svg_open(W, H, label, css="".join(css)) + f"""
<g clip-path="url(#round)">
  <rect width="{W}" height="{H}" fill="{TBG}"/>
  <rect width="{W}" height="40" fill="#003a17"/>
  <line x1="0" y1="40" x2="{W}" y2="40" stroke="{G}" stroke-opacity=".5"/>
  <circle cx="22" cy="20" r="6" fill="{G}"/><circle cx="42" cy="20" r="6" fill="{G2}"/><circle cx="62" cy="20" r="6" fill="{G3}"/>
  <text x="{W/2}" y="25" font-size="14" fill="{DIM}" text-anchor="middle">mateus@itumbiara: ~</text>
  {''.join(body)}
  <rect y="40" width="{W}" height="{H}" fill="url(#grid)"/>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save("terminal.svg", svg)


# ===================================================================== ícones
def icon_drone(cx, cy):
    rot = "".join(
        f'<ellipse class="rotor" style="animation-delay:-{d}s" cx="{cx + dx}" cy="{cy - 20}" rx="22" ry="3" fill="{G}" fill-opacity=".5" stroke="{G}"/>'
        for dx, d in ((-55, 0), (55, 0.1))
    )
    crops = "".join(
        f'<path d="M{x} 140 v-8 M{x} 136 l-4 -4 M{x} 136 l4 -4" stroke="{G2}" stroke-width="1.5" fill="none"/>'
        for x in range(cx - 95, cx + 100, 19)
    )
    return f"""
  <g class="hover">
    <path d="M{cx-14} {cy+16} L{cx+14} {cy+16} L{cx+52} {cy+56} L{cx-52} {cy+56} Z" fill="url(#beam)" class="beamp"/>
    <g fill="none" stroke="{G}" stroke-width="2.5" filter="url(#glowS)">
      <path d="M{cx-22} {cy-4} H{cx-55} V{cy-18} M{cx+22} {cy-4} H{cx+55} V{cy-18}"/>
      <rect x="{cx-24}" y="{cy-14}" width="48" height="26" rx="8" fill="{TBG}"/>
      <circle cx="{cx}" cy="{cy+16}" r="6" fill="{TBG}"/>
      <path d="M{cx-18} {cy+12} l-8 10 M{cx+18} {cy+12} l8 10"/>
    </g>
    <circle class="blink" cx="{cx}" cy="{cy-2}" r="3" fill="{G}"/>
    {rot}
  </g>
  {crops}"""


def icon_truck(cx, cy):
    wheels = "".join(
        f'<g><circle cx="{x}" cy="{cy+28}" r="10" fill="{TBG}" stroke="{G}" stroke-width="2.5"/>'
        f'<path class="spin" d="M{x-7} {cy+28} H{x+7} M{x} {cy+21} V{cy+35}" stroke="{G}" stroke-width="2"/></g>'
        for x in (cx - 44, cx + 30)
    )
    return f"""
  <line class="road" x1="{cx-110}" y1="{cy+40}" x2="{cx+110}" y2="{cy+40}" stroke="{G2}" stroke-width="2" stroke-dasharray="14 10"/>
  <g class="speed" stroke="{G}" stroke-width="2" stroke-linecap="round">
    <line x1="{cx-108}" y1="{cy-10}" x2="{cx-84}" y2="{cy-10}"/>
    <line x1="{cx-100}" y1="{cy+4}" x2="{cx-80}" y2="{cy+4}"/>
    <line x1="{cx-110}" y1="{cy+18}" x2="{cx-86}" y2="{cy+18}"/>
  </g>
  <g class="bounce">
    <g fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)">
      <rect x="{cx-70}" y="{cy-26}" width="80" height="50" rx="4"/>
      <path d="M{cx+12} {cy-8} H{cx+38} L{cx+54} {cy+8} V{cy+24} H{cx+12} Z"/>
    </g>
    <path d="M{cx+20} {cy-2} H{cx+36} L{cx+46} {cy+8} H{cx+20} Z" fill="{G}" fill-opacity=".35"/>
    <g fill="none" stroke="{G2}" stroke-width="1.6">
      <rect x="{cx-58}" y="{cy-14}" width="24" height="24"/><path d="M{cx-58} {cy-6} H{cx-34} M{cx-46} {cy-14} V{cy-6}"/>
      <rect x="{cx-28}" y="{cy-14}" width="24" height="24"/><path d="M{cx-28} {cy-6} H{cx-4} M{cx-16} {cy-14} V{cy-6}"/>
    </g>
    {wheels}
  </g>"""


def icon_book(cx, cy):
    def page(sign):
        x2 = cx + sign * 72
        return (f'M{cx} {cy-30} Q{cx + sign * 34} {cy-42} {x2} {cy-34} V{cy+30} '
                f'Q{cx + sign * 34} {cy+22} {cx} {cy+34} Z')
    lines = "".join(
        f'<path d="M{cx + s * 14} {cy - 18 + i * 11} Q{cx + s * 36} {cy - 25 + i * 11} {cx + s * 60} {cy - 21 + i * 11}" stroke="{G2}" stroke-width="1.5" fill="none"/>'
        for s in (-1, 1) for i in range(5)
    )
    bits = "".join(
        f'<text class="rise" style="animation-delay:{d}s" x="{cx + dx}" y="{cy - 30}" font-size="14" fill="{G}" text-anchor="middle">{b}</text>'
        for dx, d, b in ((-40, 0, "1"), (-10, 1.1, "0"), (22, 0.5, "1"), (50, 1.7, "0"), (0, 2.3, "1"))
    )
    return f"""
  {bits}
  <g fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)">
    <path d="{page(-1)}"/><path d="{page(1)}"/>
  </g>
  {lines}
  <path class="flip" d="{page(1)}" fill="#00331a" stroke="{G}" stroke-width="2"/>
  <line x1="{cx}" y1="{cy-30}" x2="{cx}" y2="{cy+34}" stroke="{G}" stroke-width="3"/>"""


def gear_path(cx, cy, r_out, r_in, teeth):
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4)
        r = r_out if i % 4 in (1, 2) else r_in
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"


def icon_code(cx, cy):
    return f"""
  <path class="spin" d="{gear_path(cx - 8, cy + 4, 50, 40, 10)}" fill="{TBG}" stroke="{G}" stroke-width="2.5" filter="url(#glowS)"/>
  <circle cx="{cx-8}" cy="{cy+4}" r="28" fill="#00331a" stroke="{G2}" stroke-width="2"/>
  <path class="spinr" d="{gear_path(cx + 44, cy - 40, 22, 16, 7)}" fill="{TBG}" stroke="{G2}" stroke-width="2"/>
  <text class="b" x="{cx-8}" y="{cy+11}" font-size="20" fill="{G}" text-anchor="middle" filter="url(#glowS)">&lt;/&gt;</text>"""


def icon_shield(cx, cy):
    return f"""
  <circle cx="{cx}" cy="{cy}" r="58" fill="none" stroke="{G}" stroke-opacity=".25"/>
  <circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{G}" stroke-opacity=".2"/>
  <path class="spin" d="M{cx} {cy} L{cx} {cy-58} A58 58 0 0 1 {cx + 58 * math.sin(math.radians(60)):.1f} {cy - 58 * math.cos(math.radians(60)):.1f} Z" fill="url(#sweep)" style="transform-origin:{cx}px {cy}px;transform-box:view-box;animation-duration:3s"/>
  <circle class="pulse" cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{G}" stroke-width="2"/>
  <path d="M{cx} {cy-44} L{cx+34} {cy-30} V{cy} Q{cx+34} {cy+30} {cx} {cy+46} Q{cx-34} {cy+30} {cx-34} {cy} V{cy-30} Z" fill="{TBG}" stroke="{G}" stroke-width="3" filter="url(#glowS)"/>
  <path class="shackle" d="M{cx-11} {cy-2} V{cy-12} A11 11 0 0 1 {cx+11} {cy-12} V{cy-2}" fill="none" stroke="{G}" stroke-width="3.5"/>
  <rect x="{cx-17}" y="{cy-3}" width="34" height="26" rx="4" fill="{G}"/>
  <circle cx="{cx}" cy="{cy+8}" r="4" fill="{TBG}"/><rect x="{cx-1.5}" y="{cy+9}" width="3" height="8" fill="{TBG}"/>"""


ICON_CSS = f"""
  .hover {{ animation: hover 3s ease-in-out infinite; }}
  @keyframes hover {{ 50% {{ transform: translateY(-6px); }} }}
  .rotor {{ transform-box: fill-box; transform-origin: center; animation: rotor .18s linear infinite; }}
  @keyframes rotor {{ 50% {{ transform: scaleX(.15); }} }}
  .beamp {{ animation: beam 1.6s ease-in-out infinite; }}
  @keyframes beam {{ 50% {{ opacity: .35; }} }}
  .road {{ animation: road .6s linear infinite; }}
  @keyframes road {{ to {{ stroke-dashoffset: 24; }} }}
  .bounce {{ animation: bounce .5s ease-in-out infinite; }}
  @keyframes bounce {{ 50% {{ transform: translateY(-2px); }} }}
  .speed {{ animation: speed .5s steps(2) infinite; }}
  @keyframes speed {{ 50% {{ opacity: .3; transform: translateX(-6px); }} }}
  .rise {{ opacity: 0; animation: rise 2.8s ease-out infinite; }}
  @keyframes rise {{ 0% {{ opacity: 0; transform: translateY(0); }} 20% {{ opacity: 1; }} 100% {{ opacity: 0; transform: translateY(-34px); }} }}
  .pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 2.4s ease-out infinite; }}
  @keyframes pulse {{ from {{ transform: scale(.8); opacity: .9; }} to {{ transform: scale(1.6); opacity: 0; }} }}
  .shackle {{ animation: lock 3s ease-in-out infinite; }}
  @keyframes lock {{ 0%,60%,100% {{ transform: translateY(0); }} 75% {{ transform: translateY(-5px); }} }}"""

ICON_DEFS = f"""
  <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{G}" stop-opacity=".55"/><stop offset="1" stop-color="{G}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="sweep" x1="0" y1="1" x2="1" y2="0">
    <stop offset="0" stop-color="{G}" stop-opacity=".05"/><stop offset="1" stop-color="{G}" stop-opacity=".5"/>
  </linearGradient>"""


# ===================================================================== cards
def tags_svg(tags, y, x0, max_w, fs=11):
    out, x = [], x0
    for tg in tags:
        w = len(tg) * fs * CW + 14
        out.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="{G}" fill-opacity=".12" stroke="{G}" stroke-opacity=".7"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + 15}" font-size="{fs}" fill="{G}" text-anchor="middle">{escape(tg)}</text>'
        )
        x += w + 6
    assert x - 6 - x0 <= max_w, f"tags largas demais: {tags}"
    return "".join(out)


def project_card(slug, title, desc, tags, icon, idx):
    W, H, R = 270, 350, 14
    fn = {"drone": icon_drone, "truck": icon_truck, "book": icon_book}[icon]
    cx, cy = W // 2, 74
    desc_svg = "".join(
        f'<text x="20" y="{232 + i * 20}" font-size="14" fill="{SOFT}">{escape(l)}</text>' for i, l in enumerate(desc)
    )
    css = ICON_CSS
    css += f".flip {{ transform-box: view-box; transform-origin: {cx}px 0; animation: flip 4s ease-in-out infinite; }}"
    css += "@keyframes flip { 0%,35% { transform: scaleX(1); } 65%,100% { transform: scaleX(-1); } }"
    svg = svg_open(W, H, f"Projeto {title}: {' '.join(desc)}", ICON_DEFS, css) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <rect x="14" y="14" width="{W-28}" height="140" rx="10" fill="#000f06" fill-opacity=".6" stroke="{G}" stroke-opacity=".3"/>
  <g clip-path="url(#iconclip)">{fn(cx, cy)}</g>
  <text x="22" y="32" font-size="11" fill="{DIM}">0{idx}</text>
  <text x="20" y="180" font-size="12" fill="{DIM}">~/projetos/</text>
  <text class="b" x="20" y="205" font-size="20" fill="{G}" filter="url(#glowS)">{escape(title)}</text>
  <rect class="blink" x="{20 + len(title) * 20 * CW + 6:.0f}" y="190" width="9" height="18" fill="{G}"/>
  {desc_svg}
  {tags_svg(tags, 292, 20, W - 40)}
  <text x="20" y="{H-16}" font-size="12" fill="{DIM}">&gt; abrir repositório_</text>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    svg = svg.replace("</defs>", f'<clipPath id="iconclip"><rect x="14" y="14" width="{W-28}" height="140" rx="10"/></clipPath></defs>', 1)
    save(f"projetos/{slug}.svg", svg)


def focus_card(slug, num, title_lines, desc, icon):
    W, H, R = 410, 200, 14
    fn = {"code": icon_code, "shield": icon_shield}[icon]
    cx, cy = 88, H // 2
    tx = 176
    title = "".join(
        f'<text class="b" x="{tx}" y="{72 + i * 26}" font-size="22" fill="{G}" filter="url(#glowS)">{escape(l)}</text>'
        for i, l in enumerate(title_lines)
    )
    y0 = 72 + len(title_lines) * 26 + 6
    d = "".join(f'<text x="{tx}" y="{y0 + i * 19}" font-size="13" fill="{SOFT}">{escape(l)}</text>' for i, l in enumerate(desc))
    svg = svg_open(W, H, f"Foco: {' '.join(title_lines)}. {' '.join(desc)}", ICON_DEFS, ICON_CSS) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <rect x="14" y="14" width="148" height="{H-28}" rx="10" fill="#000f06" fill-opacity=".6" stroke="{G}" stroke-opacity=".3"/>
  {fn(cx, cy)}
  <text x="{tx}" y="40" font-size="12" fill="{DIM}">[ foco_0{num} ]</text>
  {title}
  {d}
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save(f"foco-{slug}.svg", svg)


# ===================================================================== rodapé
def footer():
    W, H, R = 1000, 150, 14
    msg = "> conexão encerrada. obrigado pela visita"
    fs = 24
    cw = fs * CW
    tw = len(msg) * cw
    sx = (W - tw) / 2
    PB = "#00150a"
    binary = " ".join(format(ord(c), "08b") for c in "MATEUS")
    css = f"""
  .type {{ animation: type 8s infinite; }}
  @keyframes type {{
    0% {{ transform: translateX(0); animation-timing-function: steps({len(msg)}); }}
    45% {{ transform: translateX({tw:.1f}px); animation-timing-function: linear; }}
    100% {{ transform: translateX({tw:.1f}px); }}
  }}"""
    svg = svg_open(W, H, "Conexão encerrada. Obrigado pela visita!", css=css) + f"""
<g clip-path="url(#round)">
  {bg(W, H)}
  <rect x="{sx - 24:.1f}" y="38" width="{tw + 60:.1f}" height="46" rx="8" fill="{PB}" stroke="{G}" stroke-opacity=".5"/>
  <text x="{sx:.1f}" y="69" font-size="{fs}" fill="{G}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs" filter="url(#glowS)">{escape(msg)}</text>
  <g class="type">
    <rect x="{sx:.1f}" y="46" width="{tw + 4:.1f}" height="32" fill="{PB}"/>
    <rect class="blink" x="{sx + 1:.1f}" y="50" width="{cw - 2:.1f}" height="24" fill="{G}"/>
  </g>
  <text x="{W/2}" y="118" font-size="14" fill="{DIM}" text-anchor="middle" letter-spacing="1">{binary}</text>
  {overlay(W, H)}
</g>
{frame(W, H, R, 2)}
</svg>"""
    save("footer.svg", svg)


# ===================================================================== conteúdo
banner()
divider()
footer()
terminal([
    ("cmd", "whoami"),
    ("out", "Mateus Ferreira · 18 anos"),
    ("out", "Itumbiara - GO, Brasil"),
    ("cmd", "cat estudos.txt"),
    ("out", "3º ano do Ensino Médio"),
    ("out", "Técnico em Desenvolvimento de Sistemas"),
    ("cmd", "cat foco.txt"),
    ("hi", "[>] Engenharia de Software"),
    ("hi", "[>] Cyber Segurança"),
    ("cmd", "ls ~/stack"),
    ("out", "python  html  css  php  sql"),
    ("out", "c++  c#  javascript"),
    ("end", ""),
])
heading("titulo-sobre.svg", "sobre_mim", 1)
heading("titulo-foco.svg", "foco", 2)
heading("titulo-stack.svg", "tecnologias", 3)
heading("titulo-projetos.svg", "projetos", 4)
heading("titulo-stats.svg", "estatísticas", 5)
focus_card("software", 1, ["Engenharia de", "Software"], ["Projetar e construir", "sistemas bem feitos,", "do banco ao front-end."], "code")
focus_card("cyber", 2, ["Cyber", "Segurança"], ["Proteger sistemas,", "redes e dados contra", "ataques."], "shield")
project_card("fazendas_crud", "fazendas_crud", ["AgroVoo: monitoramento", "agrícola com drones,", "missões e relatórios."], ["Python", "Flask", "MySQL", "JS"], "drone", 1)
project_card("logistica_crud", "logistica_crud", ["Sistema de logística", "com CRUD web e", "relatórios com JOINs."], ["Flask", "SQLAlchemy", "MySQL"], "truck", 2)
project_card("biblioteca-crud-python", "biblioteca-crud", ["Biblioteca escolar:", "alunos, livros e", "empréstimos."], ["Python", "Flask", "SQLite", "pytest"], "book", 3)

#!/usr/bin/env python3
"""Generate self-contained dark-themed SVG assets for Laziz Shakarov's GitHub profile README."""

import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "assets"))

# ───────────────────────────── Design Tokens ─────────────────────────────
BG = "#0d1117"
PANEL = "#131820"
PANEL_ALT = "#161b22"
BORDER = "#30363d"
EMERALD = "#10b981"
SKY = "#0ea5e9"
INDIGO = "#6366f1"
AMBER = "#f59e0b"
TEXT = "#e6edf3"
MUTED = "#8b949e"
SOFT = "#9da7b3"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

GRAD_DEFS = (
    '<linearGradient id="brandGrad" x1="0" y1="0" x2="1" y2="1">'
    f'<stop offset="0" stop-color="{EMERALD}"/>'
    f'<stop offset="0.55" stop-color="{SKY}"/>'
    f'<stop offset="1" stop-color="{INDIGO}"/>'
    "</linearGradient>"
)

PILL_COLORS = {
    "Next.js 16": SKY,
    "Next.js": SKY,
    "React 19": SKY,
    "React": SKY,
    "Vite": SKY,
    "TypeScript": SKY,
    "Tailwind CSS": SKY,
    "Node.js": INDIGO,
    "NestJS": INDIGO,
    "Express": INDIGO,
    "PostgreSQL": INDIGO,
    "Redis": INDIGO,
    "Python": INDIGO,
    "Docker": EMERALD,
    "GitOps": EMERALD,
    "GitHub Actions": EMERALD,
    "CLI Tooling": EMERALD,
    "Escrow": AMBER,
    "AI Integration": AMBER,
}


def esc(text: str) -> str:
    """Escape XML special characters safely."""
    return html.escape(text, quote=False)


def estimate_width(text: str, size: float, mono: bool = False, bold: bool = False) -> float:
    """Estimate rendered text width in px for SVG pill sizing."""
    factor = 0.605 if mono else (0.63 if bold else 0.56)
    return len(text) * size * factor


def write_svg(filename: str, content: str) -> None:
    """Write SVG content to assets directory."""
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def svg_open(width: int, height: int, title: str, extra_defs: str = "") -> str:
    """Return standard SVG opening tag with accessible title and defs."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">\n'
        f"<title>{esc(title)}</title>\n"
        f"<defs>{extra_defs}</defs>\n"
    )


def render_pill(x: float, y: float, label_text: str, color: str, height: int = 24) -> tuple[str, float]:
    """Render a rounded tag pill and return (svg_markup, width)."""
    width = estimate_width(label_text, 11, bold=True) + 20
    markup = (
        f'<g transform="translate({x:.1f},{y})">'
        f'<rect width="{width:.1f}" height="{height}" rx="{height / 2}" '
        f'fill="{color}" fill-opacity="0.11" stroke="{color}" stroke-opacity="0.48"/>'
        f'<text x="{width / 2:.1f}" y="{height / 2 + 3.8}" text-anchor="middle" '
        f'font-family="{SANS}" font-size="11" font-weight="600" fill="{TEXT}">{esc(label_text)}</text>'
        "</g>"
    )
    return markup, width


def render_flow_pills(tags: list[str], x0: float, y0: float, max_w: float, gap: int = 8) -> tuple[str, float]:
    """Wrap pills cleanly across lines within max_w."""
    out = []
    x, y = x0, y0
    row_h, row_gap = 24, 8
    for tag in tags:
        pill_w = estimate_width(tag, 11, bold=True) + 20
        if x + pill_w > x0 + max_w and x > x0:
            x = x0
            y += row_h + row_gap
        markup, w = render_pill(x, y, tag, PILL_COLORS.get(tag, SKY), row_h)
        out.append(markup)
        x += w + gap
    return "".join(out), (y + row_h) - y0


# ───────────────────────────── Header Banner ─────────────────────────────
def build_header() -> None:
    """Generate top profile banner with monogram, title, and code snippet."""
    w, h = 860, 176
    defs = (
        GRAD_DEFS
        + '<linearGradient id="hdrGlow" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{EMERALD}" stop-opacity="0.16"/>'
        f'<stop offset="0.5" stop-color="{SKY}" stop-opacity="0.08"/>'
        f'<stop offset="1" stop-color="{INDIGO}" stop-opacity="0.16"/>'
        "</linearGradient>"
        + '<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<path d="M 24 0 L 0 0 0 24" fill="none" stroke="{BORDER}" stroke-width="0.6" stroke-opacity="0.35"/>'
        "</pattern>"
    )
    s = svg_open(w, h, "Laziz Shakarov - Frontend and Full-Stack Software Engineer", defs)
    s += f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="16" fill="{BG}" stroke="url(#brandGrad)" stroke-width="1.5"/>\n'
    s += f'<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="15" fill="url(#grid)"/>\n'
    s += f'<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="15" fill="url(#hdrGlow)"/>\n'

    # Left Monogram Badge
    s += (
        '<g transform="translate(28, 34)">'
        f'<rect width="74" height="74" rx="18" fill="{PANEL}" stroke="url(#brandGrad)" stroke-width="2"/>'
        f'<text x="37" y="47" text-anchor="middle" font-family="{MONO}" font-size="28" font-weight="800" fill="{EMERALD}">&lt;L/&gt;</text>'
        "</g>\n"
    )

    # Name & Role
    s += (
        '<g transform="translate(122, 42)">'
        f'<text x="0" y="24" font-family="{SANS}" font-size="30" font-weight="800" fill="#ffffff" letter-spacing="-0.4">Laziz Shakarov</text>'
        f'<text x="0" y="50" font-family="{SANS}" font-size="14.5" font-weight="600" fill="{SKY}">Frontend &amp; Full-Stack Software Engineer</text>'
        f'<text x="0" y="72" font-family="{MONO}" font-size="11.5" fill="{MUTED}">React · Next.js · TypeScript · Vite · Node.js · NestJS</text>'
        "</g>\n"
    )

    # Right Mini Code Window
    tx, ty, tw_box, th_box = 548, 26, 284, 124
    s += (
        f'<g transform="translate({tx}, {ty})">'
        f'<rect width="{tw_box}" height="{th_box}" rx="12" fill="{PANEL}" stroke="{BORDER}" stroke-width="1"/>'
        f'<circle cx="16" cy="15" r="4" fill="#ef4444"/>'
        f'<circle cx="30" cy="15" r="4" fill="{AMBER}"/>'
        f'<circle cx="44" cy="15" r="4" fill="{EMERALD}"/>'
        f'<text x="64" y="19" font-family="{MONO}" font-size="10" fill="{MUTED}">laziz.config.ts</text>'
        f'<line x1="0" y1="28" x2="{tw_box}" y2="28" stroke="{BORDER}" stroke-width="1"/>'
        f'<text x="14" y="49" font-family="{MONO}" font-size="11" fill="{INDIGO}">const <tspan fill="{TEXT}">laziz</tspan> = &#123;</text>'
        f'<text x="26" y="67" font-family="{MONO}" font-size="11" fill="{MUTED}">company: <tspan fill="{EMERALD}">"Aurent POS"</tspan>,</text>'
        f'<text x="26" y="85" font-family="{MONO}" font-size="11" fill="{MUTED}">stack: <tspan fill="{SKY}">["React", "Next", "TS"]</tspan>,</text>'
        f'<text x="26" y="103" font-family="{MONO}" font-size="11" fill="{MUTED}">focus: <tspan fill="{AMBER}">"Clean UI &amp; Scale"</tspan></text>'
        f'<text x="14" y="118" font-family="{MONO}" font-size="11" fill="{INDIGO}">&#125;;</text>'
        "</g>\n"
    )

    # Bottom accent bar
    s += f'<rect x="28" y="{h - 14}" width="{w - 56}" height="3" rx="1.5" fill="url(#brandGrad)" fill-opacity="0.75"/>\n'
    write_svg("header.svg", s + "</svg>\n")


# ───────────────────────────── Hero Bento Card ─────────────────────────────
def build_hero() -> None:
    """Generate 3-column bento overview card."""
    w, h = 860, 294
    card_w, card_h = 262, 146
    y_cards = 104
    y_bottom = 266

    defs = (
        GRAD_DEFS
        + f'<linearGradient id="glow1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{SKY}" stop-opacity="0.12"/><stop offset="1" stop-color="{SKY}" stop-opacity="0.01"/></linearGradient>'
        + f'<linearGradient id="glow2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{INDIGO}" stop-opacity="0.12"/><stop offset="1" stop-color="{INDIGO}" stop-opacity="0.01"/></linearGradient>'
        + f'<linearGradient id="glow3" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{EMERALD}" stop-opacity="0.12"/><stop offset="1" stop-color="{EMERALD}" stop-opacity="0.01"/></linearGradient>'
        + f'<linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="{EMERALD}"/></linearGradient>'
    )
    s = svg_open(w, h, "Engineering Overview - Frontend, Backend and Systems", defs)
    s += f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="16" fill="{BG}" stroke="url(#brandGrad)" stroke-width="1.5"/>\n'

    # Top bar
    s += (
        '<g transform="translate(24, 22)">'
        f'<rect x="0" y="0" width="210" height="26" rx="13" fill="{SKY}" fill-opacity="0.10" stroke="{SKY}" stroke-opacity="0.45"/>'
        f'<text x="105" y="17" text-anchor="middle" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{SKY}" letter-spacing="0.8">FRONTEND &amp; FULL-STACK</text>'
        f'<text x="0" y="58" font-family="{SANS}" font-size="21" font-weight="800" fill="url(#titleGrad)">Building fast, accessible UIs &amp; scalable full-stack platforms.</text>'
        f'<g transform="translate({w - 228}, 0)">'
        f'<rect x="0" y="0" width="180" height="26" rx="13" fill="{EMERALD}" fill-opacity="0.12" stroke="{EMERALD}" stroke-opacity="0.45"/>'
        f'<text x="90" y="17" text-anchor="middle" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{EMERALD}" letter-spacing="0.6">OPEN TO WORK</text>'
        "</g></g>\n"
    )

    columns = [
        (
            24,
            SKY,
            "glow1",
            "// 01 · FRONTEND UI",
            "React, Next.js &amp; Vite",
            "Responsive design systems, clean",
            "component architecture &amp; DX.",
            [("React 19", 64), ("Next.js 16", 74), ("TypeScript", 76)],
        ),
        (
            299,
            INDIGO,
            "glow2",
            "// 02 · FULL-STACK API",
            "Node.js, NestJS &amp; DBs",
            "RESTful APIs, auth/RBAC, Redis",
            "caching &amp; PostgreSQL schemas.",
            [("NestJS", 56), ("PostgreSQL", 78), ("Docker", 56)],
        ),
        (
            574,
            EMERALD,
            "glow3",
            "// 03 · WORK &amp; CS",
            "Aurent &amp; School 21",
            "Multi-vertical POS SPAs, Electron",
            "apps, C/Unix systems &amp; GitOps.",
            [("Aurent POS", 74), ("Electron", 66), ("C / Unix", 64)],
        ),
    ]

    for x, color, glow, tag, heading, line1, line2, badges in columns:
        s += (
            f'<g transform="translate({x}, {y_cards})">'
            f'<rect width="{card_w}" height="{card_h}" rx="12" fill="{PANEL}" stroke="{BORDER}" stroke-width="1"/>'
            f'<rect width="{card_w}" height="{card_h}" rx="12" fill="url(#{glow})"/>'
            f'<rect x="0" y="0" width="{card_w}" height="3" rx="1.5" fill="{color}"/>'
            f'<text x="16" y="28" font-family="{MONO}" font-size="11" font-weight="700" fill="{color}">{tag}</text>'
            f'<text x="16" y="52" font-family="{SANS}" font-size="16" font-weight="700" fill="#ffffff">{heading}</text>'
            f'<text x="16" y="74" font-family="{SANS}" font-size="12" fill="{MUTED}">{line1}</text>'
            f'<text x="16" y="92" font-family="{SANS}" font-size="12" fill="{MUTED}">{line2}</text>'
            '<g transform="translate(16, 112)">'
        )
        bx = 0
        for label_txt, bw in badges:
            s += (
                f'<rect x="{bx}" y="0" width="{bw}" height="22" rx="6" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.32"/>'
                f'<text x="{bx + bw / 2}" y="14.5" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="600" fill="{TEXT}">{label_txt}</text>'
            )
            bx += bw + 8
        s += "</g></g>\n"

    s += (
        f'<g transform="translate(24, {y_bottom})">'
        f'<line x1="0" y1="-10" x2="{w - 48}" y2="-10" stroke="{BORDER}" stroke-dasharray="3 5"/>'
        f'<text x="0" y="10" font-family="{MONO}" font-size="11" fill="{MUTED}">📍 Samarkand, Uzbekistan · UTC+5</text>'
        f'<text x="{(w - 48) / 2}" y="10" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">⚡ Clean Code · DRY · Scalable UI &amp; API</text>'
        f'<text x="{w - 48}" y="10" text-anchor="end" font-family="{MONO}" font-size="11" fill="{EMERALD}">github.com/Lazizdeveloper ↗</text>'
        "</g>\n"
    )
    write_svg("hero.svg", s + "</svg>\n")


# ───────────────────────────── Project Cards ─────────────────────────────
ICONS = {
    "market": '<path d="M11 16h18l-1.5 11.5a2 2 0 0 1-2 1.7H14.5a2 2 0 0 1-2-1.7L11 16z"/><path d="M15.5 16v-2.5a4.5 4.5 0 0 1 9 0V16"/>',
    "hotel": '<rect x="11" y="11" width="18" height="18" rx="3"/><path d="M15 15h2v2h-2zM21 15h2v2h-2zM15 21h2v2h-2zM21 21h2v2h-2z"/>',
    "book": '<path d="M12 12.5A2.5 2.5 0 0 1 14.5 10H28v18H14.5a2.5 2.5 0 0 0-2.5 2.5z"/><path d="M12 12.5V28"/>',
    "building": '<path d="M10 29h20M13 29V15l7-4 7 4v14"/><path d="M17 19h2v2h-2zM21 19h2v2h-2zM17 24h2v2h-2zM21 24h2v2h-2z"/>',
    "pulse": '<rect x="9.5" y="11.5" width="21" height="17" rx="3"/><path d="M13 20h3l2-4 3 8 2-4h4"/>',
    "terminal": '<rect x="9.5" y="11.5" width="21" height="17" rx="3"/><path d="M14.5 17l4 3-4 3M21 24h5"/>',
}

PROJECTS = [
    {
        "file": "card-bobododa.svg",
        "icon": "market",
        "accent": (SKY, EMERALD),
        "title": "Bobo-Doda Marketplace",
        "sub": "Central Asia Services Marketplace & Escrow",
        "status": "Active",
        "status_color": EMERALD,
        "desc": [
            "Two-sided service marketplace with milestone escrow,",
            "real-time workflows, and modern Next.js 16 / React 19 UI.",
        ],
        "tags": ["Next.js 16", "React 19", "TypeScript", "Tailwind CSS", "Escrow"],
        "link": "github.com/BoboLoladono/Bobo-Doda",
    },
    {
        "file": "card-safaar.svg",
        "icon": "hotel",
        "accent": (EMERALD, SKY),
        "title": "Safaarsave (SAFAAR.uz)",
        "sub": "Travel & Accommodation Booking Monorepo",
        "status": "Monorepo",
        "status_color": SKY,
        "desc": [
            "Full-stack booking and management platform for hotels,",
            "sanatoriums, and travel reservations across Uzbekistan.",
        ],
        "tags": ["Next.js", "NestJS", "TypeScript", "PostgreSQL", "Docker"],
        "link": "github.com/Lazizdeveloper/Safaarsave",
    },
    {
        "file": "card-bookback.svg",
        "icon": "book",
        "accent": (SKY, INDIGO),
        "title": "BookBack",
        "sub": "Interactive React 19 & Vite Web Application",
        "status": "Frontend",
        "status_color": SKY,
        "desc": [
            "Smooth, motion-enhanced web app built with React 19,",
            "Vite 6, Tailwind v4, Express API, and Gemini integration.",
        ],
        "tags": ["React 19", "Vite", "TypeScript", "Tailwind CSS", "Express"],
        "link": "github.com/Lazizdeveloper/bookback",
    },
    {
        "file": "card-mahalla.svg",
        "icon": "building",
        "accent": (INDIGO, SKY),
        "title": "Mahalla Yettiligi API",
        "sub": "Scalable GovTech Backend Architecture",
        "status": "Backend",
        "status_color": INDIGO,
        "desc": [
            "Production-grade RESTful API featuring RBAC security,",
            "Redis caching, PostgreSQL persistence, and Docker setup.",
        ],
        "tags": ["Node.js", "NestJS", "TypeScript", "PostgreSQL", "Redis"],
        "link": "github.com/Lazizdeveloper/Mahalla_yettiligi_backend",
    },
    {
        "file": "card-uptime.svg",
        "icon": "pulse",
        "accent": (EMERALD, INDIGO),
        "title": "GitOps Uptime Monitor",
        "sub": "Serverless API & Infrastructure Healthcheck",
        "status": "GitOps",
        "status_color": EMERALD,
        "desc": [
            "Zero-server automated endpoint monitoring powered by",
            "GitHub Actions cron schedules and Git-backed history.",
        ],
        "tags": ["GitHub Actions", "Node.js", "GitOps"],
        "link": "github.com/Lazizdeveloper/uptime-monitor",
    },
    {
        "file": "card-rotator.svg",
        "icon": "terminal",
        "accent": (AMBER, EMERALD),
        "title": "AGY Quota Rotator",
        "sub": "Multi-Account Hot-Swapper CLI for Antigravity",
        "status": "Open Source",
        "status_color": AMBER,
        "desc": [
            "Automated Python utility for monitoring quotas and",
            "seamlessly rotating accounts across AGY CLI & IDE.",
        ],
        "tags": ["Python", "CLI Tooling"],
        "link": "github.com/Lazizdeveloper/antigravity-multi-account-rotator",
    },
]


def status_pill(x_right: float, y: float, label_txt: str, color: str) -> str:
    """Render top-right status badge inside project card."""
    w = len(label_txt) * 7.2 + 24
    x = x_right - w
    return (
        f'<g transform="translate({x:.1f},{y})">'
        f'<rect width="{w:.1f}" height="22" rx="11" fill="{color}" fill-opacity="0.13" stroke="{color}" stroke-opacity="0.5"/>'
        f'<text x="{w / 2:.1f}" y="14.7" text-anchor="middle" font-family="{SANS}" font-size="10" font-weight="700" letter-spacing="0.7" fill="{color}">{esc(label_txt.upper())}</text>'
        "</g>"
    )


def build_project_cards() -> None:
    """Generate 2-column project showcase SVG cards."""
    w, h = 420, 212
    for proj in PROJECTS:
        a1, a2 = proj["accent"]
        cid = proj["file"].replace(".svg", "").replace("-", "")
        defs = (
            f'<linearGradient id="tile{cid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>'
            f'<radialGradient id="glow{cid}" cx="0.15" cy="0.15" r="0.8">'
            f'<stop offset="0" stop-color="{a1}" stop-opacity="0.14"/><stop offset="1" stop-color="{a1}" stop-opacity="0"/></radialGradient>'
        )
        s = svg_open(w, h, f'{proj["title"]} - {proj["sub"]}', defs)
        s += f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>\n'
        s += f'<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="13" fill="url(#glow{cid})"/>\n'
        s += f'<rect x="20" y="18" width="40" height="40" rx="10" fill="url(#tile{cid})"/>\n'
        s += f'<g fill="none" stroke="{BG}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="translate(20, 18)">{ICONS[proj["icon"]]}</g>\n'
        s += status_pill(w - 20, 22, proj["status"], proj["status_color"])
        s += f'<text x="72" y="34" font-family="{SANS}" font-size="16" font-weight="700" fill="#ffffff">{esc(proj["title"])}</text>\n'
        s += f'<text x="72" y="52" font-family="{SANS}" font-size="11.5" fill="{MUTED}">{esc(proj["sub"])}</text>\n'
        s += f'<text x="20" y="84" font-family="{SANS}" font-size="12.5" fill="{SOFT}">{esc(proj["desc"][0])}</text>\n'
        s += f'<text x="20" y="102" font-family="{SANS}" font-size="12.5" fill="{SOFT}">{esc(proj["desc"][1])}</text>\n'

        pills_svg, _ = render_flow_pills(proj["tags"], 20, 120, w - 40)
        s += pills_svg
        s += f'<line x1="20" y1="{h - 32}" x2="{w - 20}" y2="{h - 32}" stroke="{BORDER}" stroke-opacity="0.7"/>\n'
        s += f'<text x="20" y="{h - 13}" font-family="{MONO}" font-size="11" fill="{a1}">{esc(proj["link"])}</text>\n'
        s += f'<text x="{w - 20}" y="{h - 13}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">↗</text>\n'
        write_svg(proj["file"], s + "</svg>\n")


# ───────────────────────────── Section Headers ─────────────────────────────
def build_sections() -> None:
    """Generate numbered bilingual section divider banners."""
    sections = [
        ("section-about.svg", "01", "About · Men Haqimda", "// engineering profile"),
        ("section-stack.svg", "02", "Tech Stack · Texnologiyalar", "// frontend, backend & devops"),
        ("section-metrics.svg", "03", "GitHub Metrics · Statistika", "// real-time activity"),
        ("section-projects.svg", "04", "Featured Projects · Loyihalar", "// selected production & oss"),
        ("section-connect.svg", "05", "Connect · Bog'lanish", "// open to collaborate"),
    ]
    w, h = 860, 54
    for filename, idx, title, tag in sections:
        defs = GRAD_DEFS + (
            f'<linearGradient id="secLine" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{EMERALD}"/><stop offset="0.5" stop-color="{SKY}"/><stop offset="1" stop-color="{INDIGO}" stop-opacity="0"/></linearGradient>'
        )
        s = svg_open(w, h, title, defs)
        s += f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="13" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>\n'
        s += f'<rect x="14" y="11" width="32" height="32" rx="9" fill="url(#brandGrad)"/>\n'
        s += f'<text x="30" y="32" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="800" fill="{BG}">{idx}</text>\n'
        s += f'<text x="60" y="33.5" font-family="{SANS}" font-size="18" font-weight="700" fill="#ffffff">{esc(title)}</text>\n'
        s += f'<text x="{w - 20}" y="32" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{MUTED}">{esc(tag)}</text>\n'
        s += f'<rect x="14" y="{h - 4}" width="{w - 28}" height="2" rx="1" fill="url(#secLine)" fill-opacity="0.75"/>\n'
        write_svg(filename, s + "</svg>\n")


# ───────────────────────────── Labels, Chips & Pills ─────────────────────────────
def build_labels_and_chips() -> None:
    """Generate category labels, top status chips, and architecture pills."""
    labels = [
        ("label-frontend.svg", "FRONTEND & UI ENGINEERING", SKY),
        ("label-backend.svg", "BACKEND, DATABASES & API", INDIGO),
        ("label-devops.svg", "DEVOPS, SYSTEMS & TOOLING", EMERALD),
        ("label-paradigms.svg", "ARCHITECTURE & WORKFLOW", AMBER),
    ]
    for fname, text, color in labels:
        w = int(len(text) * 8.9 + 34)
        h = 30
        s = svg_open(w, h, text)
        s += f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="15" fill="{BG}" stroke="{color}" stroke-opacity="0.55" stroke-width="1.5"/>'
        s += f'<text x="{w / 2:.1f}" y="{h / 2 + 4}" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="0.9" fill="{TEXT}">{esc(text)}</text>'
        write_svg(fname, s + "</svg>\n")

    chips = [
        ("chip-location.svg", "Samarkand, Uzbekistan", SKY),
        ("chip-work.svg", "Frontend Dev @ Aurent", EMERALD),
        ("chip-education.svg", "School 21 · Najot Ta'lim", INDIGO),
        ("chip-role.svg", "Frontend & Full-Stack", AMBER),
    ]
    for fname, text, color in chips:
        h = 34
        w = int(estimate_width(text, 12.5, bold=True) + 32)
        s = svg_open(w, h, text)
        s += f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="{(h - 1.5) / 2}" fill="{BG}" stroke="{color}" stroke-opacity="0.55" stroke-width="1.5"/>'
        s += f'<text x="{w / 2:.1f}" y="{h / 2 + 4.3}" text-anchor="middle" font-family="{SANS}" font-size="12.5" font-weight="600" fill="{TEXT}">{esc(text)}</text>'
        write_svg(fname, s + "</svg>\n")

    # Architecture micro-pills cloud
    groups = [
        (SKY, ["Component Architecture", "Design Systems", "Responsive UI", "TanStack Query", "Zustand", "Tailwind v4"]),
        (INDIGO, ["Monorepos", "RESTful APIs", "JWT & RBAC", "Microservices", "GitOps", "Clean Code (DRY / SRP)"]),
    ]
    w_box, max_w, gap, ph = 860, 810, 10, 32
    items = [(tag, col) for col, tags in groups for tag in tags]
    rows, cur, cur_w = [], [], 0.0
    for tag, col in items:
        pw = estimate_width(tag, 12, bold=True) + 24
        add = pw + (gap if cur else 0)
        if cur and cur_w + add > max_w:
            rows.append(cur)
            cur, cur_w = [], 0.0
            add = pw
        cur.append((tag, col, pw))
        cur_w += add
    rows.append(cur)

    h_box = len(rows) * (ph + 12)
    s = svg_open(w_box, h_box, "Architecture and Workflow Capabilities")
    y = 6
    for row in rows:
        total = sum(pw for _, _, pw in row) + gap * (len(row) - 1)
        x = (w_box - total) / 2
        for tag, col, pw in row:
            s += (
                f'<g transform="translate({x:.1f},{y})">'
                f'<rect x="0.75" y="0.75" width="{pw - 1.5:.1f}" height="{ph - 1.5}" rx="{(ph - 1.5) / 2}" '
                f'fill="{BG}" stroke="{col}" stroke-opacity="0.55" stroke-width="1.5"/>'
                f'<text x="{pw / 2:.1f}" y="{ph / 2 + 4.2}" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="600" fill="{TEXT}">{esc(tag)}</text>'
                "</g>"
            )
            x += pw + gap
        y += ph + 12
    write_svg("pills.svg", s + "</svg>\n")


# ───────────────────────────── Social Buttons & Footer ─────────────────────────────
def build_socials_and_footer() -> None:
    """Generate social contact badges and decorative wave footer."""
    socials = [
        ("social-telegram.svg", "Telegram", "@Laziz_Shakarov", SKY),
        ("social-email.svg", "Email", "shakarovlaziz243@gmail.com", EMERALD),
        ("social-instagram.svg", "Instagram", "@laziz_shakarov", AMBER),
        ("social-github.svg", "GitHub", "Lazizdeveloper", INDIGO),
    ]
    for fname, platform, handle, color in socials:
        w = max(186, int(estimate_width(handle, 12, mono=True) + 42))
        h = 52
        s = svg_open(w, h, f"{platform} - {handle}")
        s += f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="12" fill="{BG}" stroke="{color}" stroke-opacity="0.55" stroke-width="1.5"/>\n'
        s += f'<rect x="12" y="13" width="4" height="26" rx="2" fill="{color}"/>\n'
        s += f'<text x="26" y="23" font-family="{SANS}" font-size="12.5" font-weight="700" fill="#ffffff">{esc(platform)}</text>\n'
        s += f'<text x="26" y="39" font-family="{MONO}" font-size="11" fill="{MUTED}">{esc(handle)}</text>\n'
        write_svg(fname, s + "</svg>\n")

    fw, fh = 860, 108
    fs = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{fw}" height="{fh}" viewBox="0 0 {fw} {fh}" role="img" aria-hidden="true">\n'
        "<defs>\n"
        '  <linearGradient id="fgrad" x1="0%" y1="0%" x2="100%" y2="0%">\n'
        f'    <stop offset="0%" stop-color="{EMERALD}" stop-opacity="0.7"/>\n'
        f'    <stop offset="50%" stop-color="{SKY}" stop-opacity="0.8"/>\n'
        f'    <stop offset="100%" stop-color="{INDIGO}" stop-opacity="0.8"/>\n'
        "  </linearGradient>\n"
        "</defs>\n"
        f'<path d="M 0,36 C 210,76 420,10 630,54 C 750,80 810,36 860,46 L 860,{fh} L 0,{fh} Z" fill="url(#fgrad)" fill-opacity="0.30"/>\n'
        f'<path d="M 0,56 C 230,94 440,28 650,72 C 770,96 820,56 860,64 L 860,{fh} L 0,{fh} Z" fill="{SKY}" fill-opacity="0.18"/>\n'
        "</svg>\n"
    )
    write_svg("footer.svg", fs)


if __name__ == "__main__":
    build_header()
    build_hero()
    build_project_cards()
    build_sections()
    build_labels_and_chips()
    build_socials_and_footer()
    print("Generated all SVG assets into", OUT_DIR)

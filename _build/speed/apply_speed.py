#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Snelheidslaag voor de statische sites (idempotent):
- fonts zelf gehost (gesubset, variabel) + preload, geen fonts.gstatic.com meer;
- /js/nav.js: prefetch bij intentie en zachte paginawissel (werkt in alle browsers, ook iOS Safari);
- /js/site.js met event-delegatie (template-sites) of minimaal (Brabant);
- /sw.js: service worker, statische bestanden cache-first, pagina's stale-while-revalidate, versie per build;
- Speculation Rules verwijderd (dubbel werk naast de router).
Gebruik: python3 apply_speed.py <repo> [template|brabant]
"""
import hashlib, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_FILES = {"inter": "/fonts/inter.woff2", "plusjakartasans": "/fonts/plusjakartasans.woff2", "manrope": "/fonts/manrope.woff2"}
GSTATIC_RE = re.compile(r"url\((?:'|\")?https://fonts\.gstatic\.com/s/([a-z]+)/v\d+/[^)'\"]+\.woff2(?:'|\")?\)")


def read(p): return open(p, encoding="utf-8").read()
def write(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(d)


def upgrade_html(d, kind):
    o = d
    used = set()
    def font(m):
        name = m.group(1)
        if name not in FONT_FILES: return m.group(0)
        used.add(name)
        return "url(%s)" % FONT_FILES[name]
    d = GSTATIC_RE.sub(font, d)
    for name, path in FONT_FILES.items():
        if "url(%s)" % path in d: used.add(name)
    d = d.replace("font-display:swap", "font-display:optional")
    # preconnect naar gstatic weg
    d = re.sub(r"\s*<link rel=\"preconnect\" href=\"https://fonts\.gstatic\.com\" crossorigin/?>", "", d)
    # preload van de gebruikte fonts (vóór de inline style)
    pre = "".join('<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' % FONT_FILES[n] for n in sorted(used))
    d = re.sub(r'<link rel="preload" href="/fonts/[a-z]+\.woff2" as="font" type="font/woff2" crossorigin>', "", d)
    if pre:
        d = d.replace("<style>", pre + "<style>", 1)
    # speculation rules weg
    d = re.sub(r'\s*<script type="speculationrules">.*?</script>', "", d, flags=re.S)
    # scripts
    if kind == "template":
        if '<script src="/js/nav.js" defer></script>' not in d:
            d = d.replace('<script src="/js/site.js" defer></script>', '<script src="/js/site.js" defer></script>\n<script src="/js/nav.js" defer></script>', 1)
    else:
        if '<script src="/js/site.js" defer></script>' not in d:
            d = d.replace("</body>", '<script src="/js/site.js" defer></script><script src="/js/nav.js" defer></script></body>', 1)
    return d, used


def apply(repo, kind="template"):
    import levertijd
    levertijd.apply_dir(repo)
    n = 0; fonts_used = set(); pages = []
    for root, dirs, files in os.walk(repo):
        if ".git" in root or "_build" in root: continue
        for f in files:
            if not f.endswith(".html"): continue
            p = os.path.join(root, f)
            d = read(p)
            nd, used = upgrade_html(d, kind)
            fonts_used |= used
            if nd != d:
                write(p, nd); n += 1
            if f == "index.html" and "noindex" not in nd:
                pages.append("/" + os.path.relpath(root, repo).replace(os.sep, "/").strip("./").rstrip("/") + "/")
    # fontbestanden
    for name in fonts_used:
        src = os.path.join(HERE, "fonts", name + ".woff2")
        dst = os.path.join(repo, FONT_FILES[name].lstrip("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst) or open(src, "rb").read() != open(dst, "rb").read():
            open(dst, "wb").write(open(src, "rb").read())
    # scripts
    write(os.path.join(repo, "js", "nav.js"), read(os.path.join(HERE, "nav.js")))
    write(os.path.join(repo, "js", "site.js"), read(os.path.join(HERE, "site-template.js" if kind == "template" else "site-brabant.js")))
    # service worker met versie = hash van alle html + js
    h = hashlib.sha1()
    for root, dirs, files in os.walk(repo):
        if ".git" in root or "_build" in root: continue
        for f in sorted(files):
            if f.endswith((".html", ".js", ".css", ".woff2")) and f != "sw.js":
                h.update(open(os.path.join(root, f), "rb").read())
    version = h.hexdigest()[:10]
    precache = ["/", "/js/site.js", "/js/nav.js"] + [FONT_FILES[n] for n in sorted(fonts_used)]
    sw = read(os.path.join(HERE, "sw.js")).replace("__BUILD__", version).replace("__PRECACHE__", "[%s]" % ",".join('"%s"' % x for x in precache))
    write(os.path.join(repo, "sw.js"), sw)
    print("%s: snelheidslaag op %d pagina's, fonts %s, sw-versie %s" % (os.path.basename(repo), n, ",".join(sorted(fonts_used)), version))


if __name__ == "__main__":
    apply(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "template")

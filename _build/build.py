#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bouwt een provincie-/landelijke site (Brabant, Gelderland, Holland): alle pagina's, sitemap.xml, robots.txt, llms.txt, llms-full.txt, manifest, favicon, 404.
Gebruik (vanuit de repo-root): python3 _build/build.py [--content <map>]  (standaard: _build/content)"""
import importlib.util, json, os, sys, types
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import common as C  # noqa
import pages as P  # noqa


def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def load_content(cdir):
    mods = [load(os.path.join(cdir, f)) for f in sorted(os.listdir(cdir)) if f.endswith(".py") and not f.startswith("_")]
    def collect(name):
        out = []
        for m in mods:
            out += list(getattr(m, name, []))
        return out
    def first(name):
        for m in mods:
            if hasattr(m, name): return getattr(m, name)
        raise KeyError(name)
    pages = {}
    for k in ("AREA_INDEX", "INFO_INDEX", "SERVICE_INDEX", "FAQ_INDEX", "CONTACT", "ABOUT", "TERMS", "PRIVACY"):
        pages[k] = first(k)
    hubs = collect("HUBS")
    return dict(home=first("HOME"), regions=hubs, places=collect("AREAS"), articles=collect("ARTICLES"), services=collect("SERVICE_PAGES"),
                faq_topics=collect("FAQ_TOPICS"), tanks=first("TANKS"), pages=pages, topic_hubs=collect("TOPIC_HUBS"))


def write(rel, data, binary=False):
    p = os.path.join(ROOT, rel.lstrip("/")); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb" if binary else "w", **({} if binary else {"encoding": "utf-8"})) as f: f.write(data)


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="%s"/>'
            '<path d="M21 15h8.6v26.4H45V49H21z" fill="#fff"/></svg>' % C.COLORS.get("--brand", "#b4350f"))


def main():
    cdir = sys.argv[sys.argv.index("--content") + 1] if "--content" in sys.argv else os.path.join(HERE, "content")
    if os.path.exists(os.path.join(cdir, "_site.py")):
        C.configure(load(os.path.join(cdir, "_site.py")).SITECFG)
    c = load_content(cdir)
    site = P.Site(**c)
    out = site.build_all()
    # dubbele paden / slugs controleren
    seen = set()
    for pg in out:
        assert pg["path"] not in seen, "dubbel pad " + pg["path"]; seen.add(pg["path"])
    ctx = {"footer_regions": [("/bezorggebied/%s/" % r["slug"], r["name"]) for r in c["regions"]] + [("/bezorggebied/", "Alle plaatsen")],
           "footer_info": [("/informatie/%s/" % h["slug"], h["h1"]) for h in c.get("topic_hubs", [])] + [("/informatie/%s/" % a["slug"], a["h1"]) for a in c["articles"][:4]] + [("/informatie/", "Alle informatie"), ("/veelgestelde-vragen/", "Veelgestelde vragen")],
           "footer_service": [("/service/%s/" % s["slug"], s["h1"]) for s in c["services"][:4]] + [("/service/%s/" % sl, t) for sl, t in (("zakelijk-bestellen", "Zakelijk bestellen"), ("bezorgvoorwaarden", "Bezorgvoorwaarden"), ("bestelling-wijzigen-of-annuleren", "Wijzigen of annuleren"), ("veilig-bestellen-oplichting-herkennen", "Veilig bestellen")) if any(x["slug"] == sl for x in c["services"])] + [("/lachgas-tanks/", "Lachgas tanks"), ("/over-ons/", "Over ons"), ("/contact/", "Contact")]}
    for pg in out:
        html = C.render(pg, ctx)
        rel = pg["path"]
        if rel.endswith("/"): rel += "index.html"
        write(rel, html)
    # sitemap.xml
    rows = ["  <url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>" % (C.SITE, pg["path"], C.TODAY, pg.get("changefreq", "monthly"), pg.get("priority", "0.6"))
            for pg in out if pg.get("sitemap", True) and "noindex" not in pg.get("robots", "")]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % C.SITE)
    write("CNAME", C.CNAME + "\n")
    write("favicon.svg", favicon())
    write("manifest.webmanifest", json.dumps({"name": C.BRAND, "short_name": C.BRAND, "description": C.MANIFEST_DESC, "id": "/", "start_url": "/", "scope": "/", "display": "standalone",
                                             "background_color": "#fbfaf8", "theme_color": C.THEME, "lang": "nl", "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2) + "\n")
    write(C.INDEXNOW_KEY + ".txt", C.INDEXNOW_KEY)
    # llms.txt + llms-full.txt
    idx = ["# %s" % C.BRAND, "", "> %s %s" % (C.BRAND, C.LLMS_BLURB), "",
           "Volledige tekst: %s/llms-full.txt" % C.SITE, "", "## Pagina's"]
    full = ["# %s - volledige inhoud" % C.BRAND, "", "WhatsApp: %s | E-mail: %s" % (C.WA_DISPLAY, C.EMAIL), ""]
    for pg in out:
        if not pg.get("sitemap", True) or "noindex" in pg.get("robots", ""): continue
        idx.append("- [%s](%s%s): %s" % (pg["title"], C.SITE, pg["path"], pg["description"]))
        full += ["---", "", "## " + pg["title"], "URL: " + C.SITE + pg["path"], "", C.page_text(pg), ""]
    idx += ["", "## Contact", "- WhatsApp: %s" % C.WA_DISPLAY, "- E-mail: %s" % C.EMAIL, "- Bereikbaar: 24/7", ""]
    write("llms.txt", "\n".join(idx)); write("llms-full.txt", "\n".join(full))
    sys.path.insert(0, os.path.join(HERE, "speed"))
    import apply_speed
    apply_speed.apply(ROOT, "brabant")
    print("%d pagina's gebouwd in %s" % (len(out), ROOT))


if __name__ == "__main__":
    main()

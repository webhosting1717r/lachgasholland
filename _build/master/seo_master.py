#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Master-standaard voor alle lachgas-sites (idempotent, draait als laatste pas over de gebouwde HTML, na apply_speed):
- head in vaste volgorde: titelconventie, description, robots, canonical, hreflang, Open Graph + Twitter compleet (met og:image:alt), geo, iconen, preloads;
- JSON-LD gelijkgetrokken: LocalBusiness + WebSite (@id-graaf, alternateName, logo, e-mail, contactPoint) op home, Article met image en
  publisher-logo, Service met provider/availableChannel, Product zonder lege offers, AboutPage/ContactPage/CollectionPage met isPartOf;
- toegankelijkheid: header-landmark, skip-link en main#inhoud (stadssites), kopvolgorde, contrast van hulptekst en WhatsApp-groen;
- afbeeldingen: hero alleen op desktop laden (picture + preload met media), lightbox met afmetingen;
- verfijning: zachte reveal bij scrollen en micro-interacties (gedeelde CSS, JS in site.js, respecteert prefers-reduced-motion);
- sitemap lastmod, llms.txt-titels, sw-versie, vercel.json en .vercelignore.
Gebruik: python3 seo_master.py <sitekey> [repo]   (instellingen in sites.py)
"""
import hashlib
import html as H
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = "2026-10-18"
ROBOTS_INDEX = "index, follow, max-image-preview:large"
ROBOTS_NOINDEX = "noindex, follow"
MAIN_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage", "Article", "Service", "Product", "LocalBusiness", "HowTo", "FAQPage")
AREA_TYPES = ("City", "Place")

# --- gedeelde CSS (identiek voor alle sites) ---------------------------------
CSS_COMMON = (
    "/*master*/"
    ".rv{opacity:0;transform:translateY(14px);transition:opacity .6s cubic-bezier(.2,.7,.2,1),transform .6s cubic-bezier(.2,.7,.2,1)}"
    ".rv.in{opacity:1;transform:none}"
    "@media print{.rv{opacity:1;transform:none}}"
    ".wa-float{transition:transform .15s,box-shadow .15s}.wa-float:hover{transform:translateY(-2px)}"
    "@keyframes mring{0%{box-shadow:0 0 0 0 rgba(21,128,61,.45)}70%{box-shadow:0 0 0 14px rgba(21,128,61,0)}100%{box-shadow:0 0 0 0 rgba(21,128,61,0)}}"
    ".wa-float:not(.animate-pulse-ring){animation:mring 2.4s infinite}"
    "a[href^=\"https://wa.me\"]:active,.btn:active,.chip:active{transform:scale(.97)}"
    "@media (prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}.wa-float{animation:none;transition:none}a[href^=\"https://wa.me\"]:active,.btn:active,.chip:active{transform:none}}"
)
CSS_STAD = (
    ".skip{position:absolute;left:-999px;top:8px;z-index:100;background:#fff;color:#1c1917;padding:8px 12px;border-radius:8px;font-weight:600}.skip:focus{left:8px}"
    # scrollbare tabelwrapper als containing block, zodat absoluut gepositioneerde hulptekst (sr-only) de pagina niet breder maakt op mobiel
    ".overflow-x-auto{position:relative}"
)
CSS_PROV = (
    ".card h2{font-size:1.125rem;font-weight:700;margin:0 0 6px;line-height:1.15}"
    ".cta p{color:rgba(255,255,255,.95)}"
    ".prose a,.lead a,.faq .a a,.card p a,.notice a{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}"
)
CSS_END = "/*master-end*/"

VERCEL = {
    "trailingSlash": True,
    "headers": [
        {"source": "/(.*)", "headers": [
            {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains"},
            {"key": "X-Content-Type-Options", "value": "nosniff"},
            {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
            {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=()"},
            {"key": "X-Frame-Options", "value": "DENY"},
            {"key": "Content-Security-Policy", "value": "frame-ancestors 'none'; base-uri 'self'; object-src 'none'"}]},
        {"source": "/fonts/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
        {"source": "/img/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=2592000, stale-while-revalidate=604800"}]},
        {"source": "/images/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=2592000, stale-while-revalidate=604800"}]},
        {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=2592000, stale-while-revalidate=604800"}]},
        {"source": "/js/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=86400, stale-while-revalidate=604800"}]},
        {"source": "/sw.js", "headers": [{"key": "Cache-Control", "value": "no-cache"}]},
    ],
}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def esc(s):
    return H.escape(s, quote=False).replace('"', "&quot;")


def strip_tags(s):
    return H.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def attrs(tag):
    return dict((k.lower(), H.unescape(v)) for k, v in re.findall(r'([a-zA-Z:_-]+)="([^"]*)"', tag))


def trim_desc(d):
    """Kort een te lange description (>160) netjes in, bij voorkeur op een zinsgrens en nooit korter dan 120 tekens."""
    if len(d) <= 160:
        return d
    cut = d[:156]
    k = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
    if k >= 120:
        return d[:k + 1]
    k = max(cut.rfind(", "), cut.rfind("; "))
    if k >= 120:
        return d[:k] + "."
    return cut[:cut.rfind(" ")].rstrip(",;:") + "."


def dumps(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# --- schema-bouwstenen ---------------------------------------------------------
def logo_obj(c):
    return {"@type": "ImageObject", "url": c["site"] + c["logo"], "width": 512, "height": 512}


def biz_ref(c):
    return {"@type": "LocalBusiness", "@id": c["site"] + "/#business", "name": c["brand"], "url": c["site"] + "/", "telephone": "+" + c["wa"]}


def publisher(c):
    return {"@type": "Organization", "@id": c["site"] + "/#business", "name": c["brand"], "url": c["site"] + "/", "logo": logo_obj(c)}


def website(c):
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": c["site"] + "/#website", "url": c["site"] + "/", "name": c["brand"],
            "alternateName": c["alt_names"], "inLanguage": c["lang"], "publisher": {"@id": c["site"] + "/#business"}}


def business(c, old):
    old = old or {}
    alt = [a for a in (old.get("alternateName") or []) if isinstance(a, str)] if isinstance(old.get("alternateName"), list) else ([old["alternateName"]] if old.get("alternateName") else [])
    alt += [a for a in c["alt_names"] if a not in alt]
    address = dict(old.get("address") or {"@type": "PostalAddress"})
    address.setdefault("@type", "PostalAddress")
    if c.get("city"):
        address.setdefault("addressLocality", c["city"])
    address["addressRegion"] = c["region"]
    address["addressCountry"] = c["country"]
    b = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": c["site"] + "/#business", "name": c["brand"], "alternateName": alt,
         "url": c["site"] + "/", "logo": logo_obj(c), "image": c["site"] + c["og"],
         "description": old.get("description") or "%s bezorgt lachgastanks aan volwassenen (18+). Bestellen via WhatsApp, prijs vooraf bevestigd, betalen bij levering." % c["brand"],
         "telephone": "+" + c["wa"], "email": c["mail"], "priceRange": "€€", "currenciesAccepted": "EUR", "paymentAccepted": c["payment"],
         "areaServed": old.get("areaServed") or {"@type": "AdministrativeArea", "name": c["region"]}, "address": address}
    if old.get("geo"):
        b["geo"] = old["geo"]
    elif c.get("geo"):
        b["geo"] = {"@type": "GeoCoordinates", "latitude": c["geo"][0], "longitude": c["geo"][1]}
    b["openingHoursSpecification"] = old.get("openingHoursSpecification") or [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}]
    b["contactPoint"] = {"@type": "ContactPoint", "contactType": "customer service", "telephone": "+" + c["wa"], "email": c["mail"],
                         "url": "https://wa.me/" + c["wa"], "availableLanguage": ["nl"]}
    b["sameAs"] = ["https://wa.me/" + c["wa"]] + [s for s in c["same_as"] if s]
    return b


def service_for(c, title, desc, url, h1):
    return {"@context": "https://schema.org", "@type": "Service", "serviceType": "Lachgas bezorgservice", "name": h1 or title, "description": desc, "url": url,
            "provider": biz_ref(c), "areaServed": {"@type": "City", "name": c["city"]} if c.get("city") else {"@type": "AdministrativeArea", "name": c["region"]},
            "availableChannel": {"@type": "ServiceChannel", "serviceUrl": "https://wa.me/" + c["wa"], "name": "WhatsApp"}}


def fix_schema(o, c, path, url, title, desc, h1):
    """Trekt één JSON-LD-object gelijk aan de standaard; geeft het aangepaste object terug."""
    t = o.get("@type")
    if t == "Article":
        o.setdefault("url", url)
        o.setdefault("mainEntityOfPage", url)
        o["inLanguage"] = c["lang"]
        if not o.get("image"):
            o["image"] = [c["site"] + c["og"]]
        o["author"] = {"@type": "Organization", "name": c["brand"], "url": c["site"] + "/"}
        o["publisher"] = publisher(c)
    elif t == "Service":
        o.setdefault("serviceType", "Lachgas bezorgservice")
        o.setdefault("url", url)
        o["provider"] = biz_ref(c)
        o.setdefault("availableChannel", {"@type": "ServiceChannel", "serviceUrl": "https://wa.me/" + c["wa"], "name": "WhatsApp"})
    elif t == "Product":
        o.pop("offers", None)
        o.setdefault("url", url)
        o["brand"] = {"@type": "Brand", "name": c["brand"]}
        if isinstance(o.get("image"), str) and o["image"].startswith("/"):
            o["image"] = c["site"] + o["image"]
        if not o.get("image"):
            o["image"] = c["site"] + c["og"]
    elif t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
        if path == "/over-ons/":
            o["@type"] = "AboutPage"
        if o["@type"] in ("AboutPage", "ContactPage"):
            o["mainEntity"] = {"@id": c["site"] + "/#business"}
        o.setdefault("name", title)
        if desc:
            o.setdefault("description", desc)
        o.setdefault("url", url)
        o["inLanguage"] = c["lang"]
        o["dateModified"] = TODAY
        o["isPartOf"] = {"@id": c["site"] + "/#website"}
    return o


def rebuild_schemas(scripts, c, path, url, title, desc, h1, has_itemlist):
    objs = []
    for s in scripts:
        try:
            objs.append(json.loads(s))
        except ValueError:
            objs.append(json.loads(H.unescape(s)))
    out = []
    if path == "/":
        old_biz = next((o for o in objs if o.get("@type") == "LocalBusiness"), None)
        out.append(business(c, old_biz))
        out.append(website(c))
        objs = [o for o in objs if o.get("@type") not in ("LocalBusiness", "WebSite")]
    types = [o.get("@type") for o in objs]
    if path != "/" and path != "/404.html" and not any(t in MAIN_TYPES for t in types) and path not in c["extra_service"]:
        o = {"@context": "https://schema.org", "@type": "CollectionPage" if has_itemlist or "ItemList" in types else "WebPage", "name": title, "description": desc, "url": url}
        out.append(fix_schema(o, c, path, url, title, desc, h1))
    if path in c["extra_service"] and "Service" not in types:
        out.append(fix_schema(service_for(c, title, desc, url, h1), c, path, url, title, desc, h1))
    for o in objs:
        out.append(fix_schema(o, c, path, url, title, desc, h1))
    # vaste volgorde: hoofdentiteit, kruimelpad, FAQ, rest
    order = {"BreadcrumbList": 2, "FAQPage": 3, "ItemList": 1}
    out.sort(key=lambda o: order.get(o.get("@type"), 0))
    return out


# --- titelconventie ------------------------------------------------------------
GENERIC_TAIL = re.compile(r"whatsapp|bezorgd|bezorging|aan de deur|24/7|18\+|snel|discreet|op tijd|bestellen", re.I)


def place_name(objs, path, c):
    parts = [p for p in path.split("/") if p]
    if len(parts) != 2 or parts[0] not in c["area_dirs"]:
        return None
    for o in objs:
        if o.get("@type") == "Service":
            a = o.get("areaServed") or {}
            if isinstance(a, dict) and a.get("@type") in AREA_TYPES and a.get("name"):
                return a["name"]
    return None


def new_title(old, path, c, place, noindex):
    brand = c["brand"]
    if path == "/":
        return c["home_title"]
    if noindex:
        return old
    if place:
        for cand in ("Lachgas %s bestellen | %s" % (place, brand), "Lachgas %s | %s" % (place, brand), "Lachgas %s bestellen" % place):
            if len(cand) <= 60:
                return cand
        return old
    if brand.lower() in old.lower():
        return old
    cand = old + " | " + brand
    if len(cand) <= 60:
        return cand
    # alleen een generieke USP-staart ("Snel bezorgd via WhatsApp", "| Breda", "| 18+") mag plaatsmaken voor het merk;
    # een staart met eigen inhoud (plaatsnamen, specifieke termen) blijft staan
    base, sep, tail = old.rpartition(" | ")
    tail = tail.strip()
    generic = tail.lower() in (c["word"].lower(), (c.get("city") or "\0").lower()) or (GENERIC_TAIL.search(tail) and len(tail.split()) <= 5 and not re.search(r"\d\s?KG|stappen", tail, re.I))
    if sep and generic:
        cand = base + " | " + brand
        if len(cand) <= 60:
            return cand
    return old


# --- head ----------------------------------------------------------------------
def parse_head(head):
    items = []
    pos = 0
    pat = re.compile(r"<(meta|link|title|style|script|noscript|base)\b", re.I)
    while True:
        m = pat.search(head, pos)
        if not m:
            break
        tag = m.group(1).lower()
        if tag in ("meta", "link", "base"):
            e = head.index(">", m.start()) + 1
        else:
            close = "</%s>" % tag
            e = head.index(close, m.start()) + len(close)
        items.append((tag, head[m.start():e]))
        pos = e
    return items


def build_head(doc_head, c, path, url, noindex, schemas, extra_preload=None):
    items = parse_head(doc_head)
    title = desc = robots = ogtype = theme = ""
    styles, scripts_other, fonts, img_preloads, icons, extra = [], [], [], [], {}, []
    for tag, raw in items:
        a = attrs(raw)
        if tag == "title":
            title = strip_tags(re.sub(r"</?title[^>]*>", "", raw))
        elif tag == "style":
            styles.append(raw)
        elif tag == "script":
            if a.get("type") == "application/ld+json":
                continue
            scripts_other.append(raw)
        elif tag == "meta":
            n = (a.get("name") or a.get("property") or "").lower()
            if a.get("charset") is not None or n in ("viewport", "og:site_name", "og:locale", "og:title", "og:description", "og:url", "og:image", "og:image:width", "og:image:height", "og:image:alt",
                                                     "twitter:card", "twitter:title", "twitter:description", "twitter:image", "twitter:image:alt", "geo.region", "geo.placename", "geo.position", "icbm"):
                continue
            elif n == "description":
                desc = a.get("content", "")
            elif n == "robots":
                robots = a.get("content", "")
            elif n == "og:type":
                ogtype = a.get("content", "website")
            elif n == "theme-color":
                theme = a.get("content", "")
            else:
                extra.append(raw)
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            if rel in ("canonical", "alternate", "preconnect", "dns-prefetch"):
                continue
            elif rel == "preload" and a.get("as") == "font":
                fonts.append(raw)
            elif rel == "preload" and a.get("as") == "image":
                img_preloads.append(raw)
            elif rel in ("icon", "apple-touch-icon", "manifest"):
                icons.setdefault(rel + ":" + (a.get("type") or a.get("sizes") or ""), raw)
            else:
                extra.append(raw)
        else:
            extra.append(raw)
    desc = trim_desc(H.unescape(desc))
    ogtype = ogtype or "website"
    theme = theme or c["theme"]
    og_img = c["site"] + c["og"]
    out = ['<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">', "<title>%s</title>" % esc(title),
           '<meta name="description" content="%s">' % esc(desc), '<meta name="robots" content="%s">' % (ROBOTS_NOINDEX if noindex else ROBOTS_INDEX)]
    if not noindex:
        out += ['<link rel="canonical" href="%s">' % url, '<link rel="alternate" hreflang="%s" href="%s">' % (c["hl"], url), '<link rel="alternate" hreflang="x-default" href="%s">' % url]
    out += ['<meta property="og:type" content="%s">' % ogtype, '<meta property="og:site_name" content="%s">' % esc(c["brand"]), '<meta property="og:locale" content="%s">' % c["locale"],
            '<meta property="og:title" content="%s">' % esc(title), '<meta property="og:description" content="%s">' % esc(desc)]
    if not noindex:
        out.append('<meta property="og:url" content="%s">' % url)
    out += ['<meta property="og:image" content="%s">' % og_img, '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
            '<meta property="og:image:alt" content="%s">' % esc(c["og_alt"]),
            '<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:title" content="%s">' % esc(title),
            '<meta name="twitter:description" content="%s">' % esc(desc), '<meta name="twitter:image" content="%s">' % og_img, '<meta name="twitter:image:alt" content="%s">' % esc(c["og_alt"]),
            '<meta name="theme-color" content="%s">' % theme, '<meta name="geo.region" content="%s">' % c["geo_region"], '<meta name="geo.placename" content="%s">' % esc(c["place"])]
    ic = [re.sub(r"\s*/>$", ">", raw) for raw in icons.values()]
    if not any("favicon.svg" in x for x in ic):
        ic.append('<link rel="icon" href="/favicon.svg" type="image/svg+xml">')
    if not any("favicon.ico" in x for x in ic):
        ic.append('<link rel="icon" href="/favicon.ico" sizes="32x32 48x48">')
    if not any("apple-touch-icon" in x for x in ic):
        ic.append('<link rel="apple-touch-icon" href="%s">' % c["apple"])
    if not any("manifest" in x for x in ic):
        ic.append('<link rel="manifest" href="/manifest.webmanifest">')

    def icon_rank(raw):
        a = attrs(raw)
        rel = a.get("rel", "")
        return 0 if rel == "icon" and "svg" in a.get("type", "") else 1 if rel == "icon" else 2 if rel == "apple-touch-icon" else 3
    out += sorted(ic, key=icon_rank)
    out += [re.sub(r"\s*/>$", ">", x) for x in extra]
    pre = img_preloads if extra_preload is None else extra_preload
    out += [re.sub(r"\s*/>$", ">", x) for x in pre]
    out += [re.sub(r"\s*/>$", ">", x) for x in fonts]
    out += styles
    out += ['<script type="application/ld+json">%s</script>' % dumps(s) for s in schemas]
    out += scripts_other
    return "".join(out), title, desc


# --- body ----------------------------------------------------------------------
def css_master(style, c):
    style = re.sub(r"/\*master\*/.*?/\*master-end\*/", "", style, flags=re.S)
    if c["family"] == "stad":
        # WhatsApp-groen en hulptekst naar AA-contrast (zelfde groen als de provinciesites), zonder andere kleuren te raken
        style = style.replace("rgb(32 189 90/", "rgb(21 128 61/").replace("rgba(32,189,90,", "rgba(21,128,61,")
        style = style.replace("rgb(29 168 81/", "rgb(22 101 52/").replace("rgba(29,168,81,", "rgba(22,101,52,")
        style = style.replace(".text-white\\/40{color:hsla(0,0%,100%,.4)}", ".text-white\\/40{color:hsla(0,0%,100%,.55)}")
        style = style.replace(".text-white\\/80{color:hsla(0,0%,100%,.8)}", ".text-white\\/80{color:hsla(0,0%,100%,.92)}")
    block = CSS_COMMON + (CSS_STAD if c["family"] == "stad" else CSS_PROV) + CSS_END
    return style.replace("</style>", block + "</style>", 1)


HERO_IMG = re.compile(r'<img\b[^>]*class="w-full h-auto rounded-2xl cursor-zoom-in"[^>]*>')
MOBILE_SRC = '<source media="(max-width: 1023px)" srcset="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'3\' height=\'2\'/%3E">'


def body_stad(body, path, c):
    # landmark + skip-link
    if "<header" not in body:
        m = re.search(r'<nav id="site-nav"', body)
        if m:
            end = body.index("</nav>", m.start()) + len("</nav>")
            assert body.count("<nav", m.start(), end) == 1
            body = body[:m.start()] + '<a class="skip" href="#inhoud">Direct naar inhoud</a><header>' + body[m.start():end] + "</header>" + body[end:]
    body = body.replace("<main>", '<main id="inhoud">', 1)
    # vaste balk iets minder doorzichtig, zodat het merkwoord in het logo ook boven een donkere paginakop AA-contrast haalt
    body = body.replace('<nav id="site-nav" class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 bg-white/80 backdrop-blur-sm"',
                        '<nav id="site-nav" class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 bg-white/95 backdrop-blur-sm"', 1)
    # kopvolgorde in de footer (H2 -> H4 werd H2 -> H3)
    fs = body.find("<footer")
    if fs >= 0:
        fe = body.index("</footer>", fs)
        body = body[:fs] + body[fs:fe].replace("<h4 ", "<h3 ").replace("</h4>", "</h3>") + body[fe:]
    # contrast hulptekst op lichte vlakken (eventuele extra attributen na class blijven staan)
    for cls in ("text-xs text-gray-400", "text-xs font-semibold text-gray-400", "mm-h text-gray-400", "pf-note text-xs text-gray-400", "mb-8 text-sm text-gray-400"):
        body = re.sub(r'<p class="%s"([^>]*)>' % re.escape(cls), lambda m, cls=cls: '<p class="%s"%s>' % (cls.replace("gray-400", "gray-500"), m.group(1)), body)
    body = re.sub(r'<dt class="text-gray-400"([^>]*)>', r'<dt class="text-gray-500"\1>', body)
    body = re.sub(r'(<th\b[^>]*class="[^"]*?)text-gray-400', r'\1text-gray-500', body)
    # lightbox-afbeelding met afmetingen
    body = re.sub(r'<img loading="lazy" decoding="async" id="image-lightbox-img" src="" alt="" class="([^"]*)"\s*/?>',
                  r'<img loading="lazy" decoding="async" id="image-lightbox-img" src="" alt="" width="1200" height="800" class="\1">', body)
    preload = None
    if path == "/":
        m = HERO_IMG.search(body)
        if m and not body[:m.start()].endswith(MOBILE_SRC):
            img = m.group(0)
            img = re.sub(r'\s*loading="lazy"', "", img)
            if 'fetchpriority="high"' not in img:
                img = img.replace("<img ", '<img fetchpriority="high" ', 1)
            body = body[:m.start()] + "<picture>" + MOBILE_SRC + img + "</picture>" + body[m.end():]
        m = HERO_IMG.search(body)
        if m:
            src = attrs(m.group(0)).get("src")
            preload = ['<link rel="preload" as="image" href="%s" type="image/webp" fetchpriority="high" media="(min-width: 1024px)">' % src] if src else []
    return body, preload


def body_prov(body, path, c):
    if path in ("/service/", "/veelgestelde-vragen/"):
        body = re.sub(r'(<a class="card" href="[^"]*">(?:<div class="ico">.*?</div>)?)<h3>(.*?)</h3>', r"\1<h2>\2</h2>", body)
    return body, None


# --- pagina --------------------------------------------------------------------
def upgrade(doc, path, c, stats):
    hs = doc.index("<head>") + len("<head>")
    he = doc.index("</head>")
    head, body = doc[hs:he], doc[he + len("</head>"):]
    pre = doc[:hs]
    pre = re.sub(r'<html\b[^>]*>', lambda m: re.sub(r'\slang="[^"]*"', "", m.group(0)).replace("<html", '<html lang="%s"' % c["html_lang"], 1), pre, count=1)
    noindex = "noindex" in (re.search(r'<meta name="robots" content="([^"]*)"', head) or [None, ""])[1] or path == "/404.html"
    url = c["site"] + path
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', head, re.S)
    objs = []
    for s in scripts:
        try:
            objs.append(json.loads(s))
        except ValueError:
            objs.append(json.loads(H.unescape(s)))
    old_title = strip_tags(re.search(r"<title>(.*?)</title>", head, re.S).group(1))
    h1m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    h1 = " ".join(strip_tags(h1m.group(1)).split()) if h1m else ""
    place = place_name(objs, path, c)
    title = new_title(old_title, path, c, place, noindex)
    if title != old_title:
        stats["titles"].append((path, old_title, title))
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % esc(title), head, count=1, flags=re.S)
    desc = trim_desc(H.unescape((re.search(r'<meta name="description" content="([^"]*)"', head) or [None, ""])[1]))
    has_itemlist = any(o.get("@type") == "ItemList" for o in objs)
    schemas = rebuild_schemas(scripts, c, path, url, title, desc, h1, has_itemlist)
    if c["family"] == "stad":
        body, preload = body_stad(body, path, c)
    else:
        body, preload = body_prov(body, path, c)
    new_head, _, _ = build_head(head, c, path, url, noindex, schemas, preload)
    new_head = css_master(new_head, c)
    sep = "\n" if "\n" in doc[hs:hs + 3] else ""
    return pre + sep + new_head + sep + "</head>" + body


def sw_version(repo):
    h = hashlib.sha1()
    for root, dirs, files in os.walk(repo):
        if "/.git" in root or "/_build" in root:
            continue
        for f in sorted(files):
            if f.endswith((".html", ".js", ".css", ".woff2")) and f != "sw.js":
                h.update(open(os.path.join(root, f), "rb").read())
    return h.hexdigest()[:10]


def resolve_cfg(site_url):
    """Instellingen voor een site: uit site.json naast dit script (in een repo-_build) of uit sites.py (werkmap)."""
    sj = os.path.join(HERE, "site.json")
    if os.path.exists(sj):
        c = json.load(open(sj, encoding="utf-8"))
        if c["site"] == site_url:
            return c
    sys.path.insert(0, HERE)
    from sites import SITES
    for c in SITES.values():
        if c["site"] == site_url:
            return c
    raise KeyError(site_url)


def apply_site(repo, site_url):
    return apply_cfg(repo, resolve_cfg(site_url))


def apply(key, repo=None):
    sys.path.insert(0, HERE)
    from sites import SITES
    c = SITES[key]
    return apply_cfg(repo or c["repo"], c)


def apply_cfg(repo, c):
    key = c["key"]
    stats = {"titles": [], "pages": 0, "changed": 0}
    titles = {}
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "_build", "node_modules")]
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, repo).replace(os.sep, "/")
            path = "/" if rel == "index.html" else ("/" + rel[:-len("index.html")] if rel.endswith("/index.html") else "/" + rel)
            d = read(p)
            nd = upgrade(d, path, c, stats)
            stats["pages"] += 1
            if nd != d:
                write(p, nd)
                stats["changed"] += 1
                stats.setdefault("changed_paths", []).append(path)
            titles[path] = strip_tags(re.search(r"<title>(.*?)</title>", nd, re.S).group(1))
    # css-bron van de stadssites synchroon houden met de inline stijl (validate.py leest css/site.css)
    cssp = os.path.join(repo, "css", "site.css")
    if c["family"] == "stad" and os.path.exists(cssp):
        css = re.sub(r"/\*master\*/.*?/\*master-end\*/\n?", "", read(cssp), flags=re.S).rstrip("\n") + "\n" + CSS_COMMON + CSS_STAD + CSS_END + "\n"
        if css != read(cssp):
            write(cssp, css)
    # site.js uit de gedeelde bron (zelfde als apply_speed), sitemap, llms, sw, vercel
    src = os.path.join(HERE, "..", "speed", "site-template.js" if c["family"] == "stad" else "site-brabant.js")
    js = read(src)
    jp = os.path.join(repo, "js", "site.js")
    if not os.path.exists(jp) or read(jp) != js:
        write(jp, js)
    smp = os.path.join(repo, "sitemap.xml")
    if os.path.exists(smp):
        write(smp, re.sub(r"<lastmod>[^<]*</lastmod>", "<lastmod>%s</lastmod>" % TODAY, read(smp)))
    lp = os.path.join(repo, "llms.txt")
    if os.path.exists(lp):
        def fix_line(m):
            u = m.group(2)
            pth = u.replace(c["site"], "") or "/"
            return "- [%s](%s)" % (titles.get(pth, m.group(1)), u)
        write(lp, re.sub(r"- \[([^\]]*)\]\((%s[^)]*)\)" % re.escape(c["site"]), fix_line, read(lp)))
    fp = os.path.join(repo, "llms-full.txt")
    if os.path.exists(fp):
        def fix_head(m):
            pth = m.group(2).replace(c["site"], "") or "/"
            return "## %s\nURL: %s" % (titles.get(pth, m.group(1)), m.group(2))
        write(fp, re.sub(r"## (.*)\nURL: (%s\S*)" % re.escape(c["site"]), fix_head, read(fp)))
    swp = os.path.join(repo, "sw.js")
    if os.path.exists(swp):
        write(swp, re.sub(r'var VERSION = "[^"]*"', 'var VERSION = "%s"' % sw_version(repo), read(swp)))
    write(os.path.join(repo, "vercel.json"), json.dumps(VERCEL, indent=2) + "\n")
    write(os.path.join(repo, ".vercelignore"), "_build\n")
    print("%s: %d pagina's, %d aangepast, %d titels gewijzigd%s" % (key, stats["pages"], stats["changed"], len(stats["titles"]),
                                                                   (" (" + ", ".join(stats["changed_paths"]) + ")") if 0 < stats["changed"] <= 6 else ""))
    return stats


if __name__ == "__main__":
    st = apply(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "titles_%s.tsv" % sys.argv[1]), "w", encoding="utf-8") as f:
        for p, o, n in st["titles"]:
            f.write("%s\t%s\t%s\n" % (p, o, n))

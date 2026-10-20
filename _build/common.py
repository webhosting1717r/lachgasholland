# -*- coding: utf-8 -*-
"""Gedeelde bouwstenen voor de provincie-/landelijke sites (Brabant, Gelderland, Holland): instellingen, componenten, schema's en de paginarenderer.
Site-specifieke instellingen komen uit _site.py in de contentmap (zie configure())."""
import html as _html
import json
import os
import re
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://lachgasbrabant.nl"
BRAND = "Lachgas Brabant"
BRAND_EM = "Brabant"            # het gekleurde woord in het logo
REGION = "Noord-Brabant"        # naam van het werkgebied
REGION_LONG = "heel Noord-Brabant"
AREA_TYPE = "AdministrativeArea"
HUB_KICKER = "Regio"            # kicker boven een hub-pagina (Regio / Provincie)
HUB_WORD = "regio"              # "deze regio" / "deze provincie"
OTHER_HUBS_TAG = "Ook in Brabant"
OTHER_HUBS_H2 = "Andere regio's"
ALL_PLACES_LABEL = "Alle plaatsen in Noord-Brabant"
STATUS_LINE = "In de grote Brabantse steden meestal binnen 15 tot 25 minuten"
SVC_TEXT = "Voor horeca, verenigingen en organisaties van West-Brabant tot de Kempen: zakelijk bestellen, onze bezorgvoorwaarden en hoe je een bestelling aanpast of annuleert."
FOOTER_BLURB = "Bezorging van lachgastanks aan volwassenen in heel Noord-Brabant. Bestellen via WhatsApp, prijs vooraf bevestigd, uitsluitend voor 18+."
BUSINESS_DESC = "Lachgas Brabant bezorgt lachgastanks aan volwassenen in heel Noord-Brabant. Bestellen via WhatsApp, prijs vooraf bevestigd, uitsluitend 18+."
WA_TEXT = "Hoi, ik wil graag lachgas bestellen in Brabant."
OG_IMAGE = "/assets/og-lachgas-brabant.png"
CNAME = "lachgasbrabant.nl"
MANIFEST_DESC = "Lachgas Brabant: lachgastanks bezorgd in heel Noord-Brabant, bestellen via WhatsApp."
LLMS_BLURB = "bezorgt lachgastanks aan volwassenen (18+) in heel Noord-Brabant. Bestellen via WhatsApp, prijs vooraf bevestigd, betalen bij levering."
WA_NUMBER = "31684626182"          # WhatsApp, zonder plus
WA_DISPLAY = "+31 6 84626182"
EMAIL = "info@lachgasbrabant.nl"
TODAY = "2026-10-03"
MONTH_NL = "oktober 2026"
THEME = "#1c1917"
COLORS = {}                       # overschrijft :root-kleuren uit site.css (bijv. {"--brand": "#1d6f42"})
INDEXNOW_KEY = "7e1a9c3b5d2f4a6c8e0b1d3f5a7c9e2b"
MM_REGION_LINKS = [("/bezorggebied/west-brabant/", "West-Brabant"), ("/bezorggebied/midden-brabant/", "Midden-Brabant"), ("/bezorggebied/noordoost-brabant/", "Noordoost-Brabant"), ("/bezorggebied/zuidoost-brabant/", "Zuidoost-Brabant")]
MM_REGION_TITLE = "Regio's"
CTA_H2 = "Klaar om te bestellen?"
CTA_TEXT = "Stuur ons een WhatsApp-bericht met je plaats, de gewenste maat en het tijdstip. Je krijgt direct de prijs en het levermoment terug."
PRODUCT_DESCS = ["Compact formaat voor een kleiner gezelschap. Verzegeld geleverd.", "Het middenformaat voor een avond met een grotere groep.", "Voor grotere feesten en evenementen, in overleg geleverd."]
PF_TEXT = "Het compacte formaat voor een kleiner gezelschap. Je krijgt de tank verzegeld aan de deur, met de prijs vooraf bevestigd via WhatsApp."
PF_FACTS = [("Inhoud", "2 kilo lachgas (N2O)"), ("Levering", "Verzegeld, aan de deur"), ("Levertijd", "Meestal binnen 15 tot 25 min"), ("Betalen", "Contant of Tikkie bij levering")]
ARTICLE_BOX = "deze pagina is geschreven en nagekeken door het team van %s en wordt bijgewerkt als regels of inzichten veranderen. Wij leveren uitsluitend aan volwassenen van 18 jaar en ouder en geven bewust geen gebruiksinstructies."


def configure(cfg):
    """Zet site-instellingen uit _site.py (dict) als modulevariabelen en herbouwt de afgeleide onderdelen."""
    g = globals()
    for k, v in cfg.items():
        if k.isupper(): g[k] = v
    css = _CSS_RAW
    for var, val in g["COLORS"].items():
        css = re.sub(r"(%s:)#[0-9a-fA-F]{3,6}" % re.escape(var), r"\g<1>" + val, css, count=1)
    g["CSS"] = _minify_css(css)
    g["MM_GROUPS"] = _mm_groups()


def _minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return re.sub(r"\s*\n\s*", "", css).replace(": ", ":").replace(" {", "{").replace("{ ", "{")


_CSS_RAW = open(os.path.join(HERE, "site.css"), encoding="utf-8").read()
CSS = _minify_css(_CSS_RAW)
FONTS = open(os.path.join(HERE, "fonts.css"), encoding="utf-8").read().strip()

NAV = [("/bezorggebied/", "Bezorggebied"), ("/lachgas-tanks/", "Lachgas tanks"), ("/informatie/", "Informatie"),
       ("/veelgestelde-vragen/", "Veelgestelde vragen"), ("/contact/", "Contact")]


def esc(s):
    return _html.escape(s, quote=False).replace('"', "&quot;")


def wa_link(text=None):
    text = text or WA_TEXT
    return "https://wa.me/%s?text=%s" % (WA_NUMBER, quote(text))


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def para(paragraphs, cls=""):
    return "".join('<p%s>%s</p>' % ((' class="%s"' % cls) if cls else "", p) for p in paragraphs)


# --- iconen ------------------------------------------------------------
ICON = {
    "wa": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2c-5.5 0-9.96 4.46-9.96 9.96 0 1.76.46 3.42 1.26 4.86L2 22l5.35-1.31c1.4.75 2.98 1.17 4.69 1.17 5.5 0 9.96-4.46 9.96-9.96S17.54 2 12.04 2zm0 18.15c-1.5 0-2.97-.4-4.25-1.16l-.3-.18-3.18.78.82-3.1-.2-.32a8.14 8.14 0 0 1-1.25-4.33c0-4.5 3.66-8.16 8.17-8.16 4.5 0 8.16 3.66 8.16 8.16s-3.66 8.16-8.17 8.16zm4.48-6.11c-.25-.12-1.45-.72-1.68-.8-.22-.08-.39-.12-.55.12-.17.25-.64.8-.78.97-.14.16-.29.18-.53.06-.25-.12-1.04-.38-1.98-1.22-.73-.65-1.22-1.46-1.37-1.7-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.16.04-.31-.02-.43-.06-.12-.55-1.33-.76-1.82-.2-.48-.4-.41-.55-.42h-.47c-.16 0-.43.06-.65.31-.22.25-.86.84-.86 2.05 0 1.21.88 2.38 1 2.54.12.17 1.73 2.65 4.2 3.71.59.25 1.05.4 1.4.52.59.19 1.13.16 1.55.1.47-.07 1.45-.59 1.65-1.17.2-.57.2-1.06.14-1.17-.06-.1-.22-.16-.47-.28z"/></svg>',
    "clock": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "pin": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "shield": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/></svg>',
    "eye": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>',
    "book": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    "tank": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="6" width="10" height="16" rx="3"/><path d="M10 6V4h4v2M12 2v2"/></svg>',
    "chat": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "menu": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
}


# --- schema's -----------------------------------------------------------
def business_schema():
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "/#business", "name": BRAND, "url": SITE + "/",
            "image": SITE + OG_IMAGE, "logo": SITE + "/assets/icon-512.png", "email": EMAIL, "telephone": "+" + WA_NUMBER,
            "description": BUSINESS_DESC,
            "priceRange": "€€", "currenciesAccepted": "EUR", "paymentAccepted": "Contant, Tikkie",
            "areaServed": {"@type": AREA_TYPE, "name": REGION},
            "address": {"@type": "PostalAddress", "addressRegion": REGION, "addressCountry": "NL"},
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}],
            "contactPoint": {"@type": "ContactPoint", "contactType": "customer service", "telephone": "+" + WA_NUMBER, "email": EMAIL, "availableLanguage": "nl"},
            "sameAs": ["https://wa.me/" + WA_NUMBER]}


def website_schema():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND, "inLanguage": "nl-NL",
            "publisher": {"@id": SITE + "/#business"}}


def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h} for i, (n, h) in enumerate(items) if h]}


def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in items]}


def service_schema(name, desc, path, area, area_type="City"):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc, "url": SITE + path, "serviceType": "Lachgas bezorgservice",
            "provider": {"@id": SITE + "/#business"}, "areaServed": {"@type": area_type, "name": area}, "availableChannel": {"@type": "ServiceChannel", "serviceUrl": "https://wa.me/" + WA_NUMBER, "name": "WhatsApp"}}


def article_schema(title, desc, path, modified=TODAY):
    return {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "inLanguage": "nl-NL",
            "mainEntityOfPage": SITE + path, "datePublished": TODAY, "dateModified": modified, "author": {"@type": "Organization", "name": BRAND, "url": SITE + "/"},
            "publisher": {"@id": SITE + "/#business"}}


def webpage_schema(title, desc, path):
    return {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": SITE + path, "inLanguage": "nl-NL", "isPartOf": {"@id": SITE + "/#website"}}


def itemlist_schema(name, items):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": name, "itemListOrder": "https://schema.org/ItemListUnordered",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": SITE + h} for i, (n, h) in enumerate(items)]}


MM_ICON = {
    "tank": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="6" width="10" height="16" rx="3"/><path d="M10 6V3h4v3"/><path d="M7 11h10"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>',
}
MM_TILES = [("/lachgas-tanks/", "Lachgas tanks", "tank"), ("/bezorggebied/", "Bezorggebied", "pin"), ("/informatie/", "Informatie", "book"), ("/veelgestelde-vragen/", "Veelgestelde vragen", "chat")]
def _mm_groups():
    return [
        ("Bestellen", [("/lachgas-tanks/2kg/", "Lachgastank 2KG"), ("/lachgas-tanks/4kg/", "Lachgastank 4KG"), ("/lachgas-tanks/10kg/", "Lachgastank 10KG"),
                       ("/service/bestellen-via-whatsapp/", "Zo werkt bestellen"), ("/service/betalen-bij-levering/", "Betalen bij levering"), ("/service/zakelijk-bestellen/", "Zakelijk bestellen")]),
        (MM_REGION_TITLE, list(MM_REGION_LINKS) + [("/service/bezorgtijden-per-regio/", "Bezorgtijden")]),
        ("Informatie", [("/informatie/veiligheid-en-gezondheid/", "Veiligheid en gezondheid"), ("/informatie/regels-en-wetgeving/", "Regels en wetgeving"),
                        ("/informatie/eerste-keer-lachgas-bestellen/", "Voor het eerst bestellen"), ("/informatie/is-lachgas-legaal-in-nederland/", "Is lachgas legaal?")]),
        ("Service", [("/service/bezorgvoorwaarden/", "Bezorgvoorwaarden"), ("/service/bestelling-wijzigen-of-annuleren/", "Wijzigen of annuleren"),
                     ("/service/veilig-bestellen-oplichting-herkennen/", "Veilig bestellen"), ("/over-ons/", "Over ons"), ("/contact/", "Contact")]),
    ]
MM_GROUPS = _mm_groups()


def mobile_menu(path):
    cur = lambda h: ' aria-current="page"' if h == path else ""
    tiles = "".join('<a class="mm-tile" href="%s"%s>%s%s</a>' % (h, cur(h), MM_ICON[i], esc(t)) for h, t, i in MM_TILES)
    groups = "".join('<div class="mm-group"><p class="mm-h">%s</p>%s</div>' % (esc(g), "".join('<a class="mm-link" href="%s"%s><span>%s</span>%s</a>' % (h, cur(h), esc(t), MM_ICON["chev"]) for h, t in items)) for g, items in MM_GROUPS)
    return ('<nav class="menu-panel" aria-label="Mobiel menu">'
            '<div class="mm-status"><span class="mm-dot"></span><span><strong>24/7 bereikbaar via WhatsApp</strong><br>%s</span></div>'
            '<div class="mm-tiles">%s</div>'
            '<a class="mm-prod" href="/lachgas-tanks/2kg/"><img src="/assets/lachgastank-2kg-160.webp" width="56" height="56" alt="" loading="lazy" decoding="async"><span><strong>Lachgastank 2KG</strong><small>Verzegeld geleverd &middot; bekijk de tank</small></span></a>'
            '%s<div class="mm-foot"><a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s WhatsApp ons nu</a>'
            '<p class="mm-trust"><span>18+ met legitimatie</span><span>Verzegeld</span><span>Betalen aan de deur</span></p></div></nav>'
            % (esc(STATUS_LINE), tiles, groups, wa_link(), ICON["wa"]))


def product_feature(heading="h3"):
    facts = PF_FACTS
    return ('<div class="pf"><div class="pf-img"><img src="/assets/lachgastank-2kg.webp" srcset="/assets/lachgastank-2kg-300.webp 300w, /assets/lachgastank-2kg.webp 480w" sizes="(min-width: 768px) 300px, 70vw" width="480" height="640" alt="Verzegelde lachgastank 2KG van %s" loading="lazy" decoding="async"></div>'
            '<div><span class="badge">Uitgelicht</span><%s>Lachgastank 2KG</%s><p>%s</p>'
            '<dl class="pf-facts">%s</dl><div class="pf-ctas"><a class="btn btn-dark" href="/lachgas-tanks/2kg/">Bekijk de 2KG</a><a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s Bestel via WhatsApp</a></div>'
            '<p class="pf-note">Uitsluitend voor 18+, met legitimatie aan de deur.</p></div></div>'
            % (esc(BRAND), heading, heading, esc(PF_TEXT), "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (esc(k), esc(v)) for k, v in facts), wa_link("Hoi, ik wil graag een lachgastank 2KG bestellen."), ICON["wa"]))


# --- componenten --------------------------------------------------------
def header(path):
    links = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if path.startswith(h) else "", t) for h, t in NAV)
    return ('<a class="skip" href="#inhoud">Direct naar inhoud</a><header class="hdr"><div class="wrap">'
            '<a class="logo" href="/" aria-label="%s, naar de homepage"><b>L</b><span>Lachgas <em>%s</em></span></a>'
            '<nav class="nav" aria-label="Hoofdmenu">%s</nav>'
            '<div style="display:flex;gap:10px;align-items:center"><a class="btn btn-wa btn-sm" href="%s" target="_blank" rel="noopener">%s<span>WhatsApp</span></a>'
            '<details class="menu"><summary aria-label="Menu openen">%s</summary>%s</details></div>'
            '</div></header>' % (BRAND, esc(BRAND_EM), links, wa_link(), ICON["wa"], ICON["menu"], mobile_menu(path)))


def footer(regions, info_links, service_links):
    def ul(items):
        return "<ul>" + "".join('<li><a href="%s">%s</a></li>' % (h, esc(t)) for h, t in items) + "</ul>"
    return ('<footer class="ftr"><div class="wrap"><div class="ftr-grid"><div>'
            '<a class="logo" href="/"><b>L</b><span>Lachgas <em style="color:#fff">%s</em></span></a>'
            '<p style="margin-top:14px;max-width:34ch">%s</p>'
            '<p><a href="%s" target="_blank" rel="noopener">WhatsApp %s</a><br><a href="mailto:%s">%s</a></p></div>'
            '<div><h3>Bezorggebied</h3>%s</div><div><h3>Informatie</h3>%s</div><div><h3>Service</h3>%s</div></div>'
            '<div class="legal"><span>&copy; 2026 %s. Verkoop uitsluitend aan personen van 18 jaar en ouder.</span>'
            '<span><a href="/algemene-voorwaarden/">Algemene voorwaarden</a> &middot; <a href="/privacy/">Privacy</a> &middot; <a href="/sitemap/">Sitemap</a></span></div></div></footer>'
            '<a class="wa-float" href="%s" target="_blank" rel="noopener" aria-label="WhatsApp ons">%s</a>'
            % (esc(BRAND_EM), esc(FOOTER_BLURB), wa_link(), WA_DISPLAY, EMAIL, EMAIL, ul(regions), ul(info_links), ul(service_links), BRAND, wa_link(), ICON["wa"].replace('width="18" height="18"', 'width="26" height="26"')))


def crumbs(items):
    lis = []
    for n, h in items:
        lis.append('<li><a href="%s">%s</a></li>' % (h, esc(n)) if h else '<li aria-current="page">%s</li>' % esc(n))
    return '<nav aria-label="Kruimelpad"><ol class="crumbs">%s</ol></nav>' % "".join(lis)


def page_head(crumb_items, kicker, h1, lead):
    return ('<section class="phead"><div class="wrap">%s<span class="kicker">%s</span><h1>%s</h1><p class="lead">%s</p></div></section>'
            % (crumbs(crumb_items), esc(kicker), esc(h1), lead))


def section(inner, alt=False, id_=None):
    return '<section class="sec%s"%s><div class="wrap">%s</div></section>' % (" sec-alt" if alt else "", (' id="%s"' % id_) if id_ else "", inner)


def sec_head(tag, h2, text=None, level="h2"):
    return '<div class="sec-head"><span class="tag">%s</span><%s>%s</%s>%s</div>' % (esc(tag), level, esc(h2), level, ('<p>%s</p>' % text) if text else "")


def cards(items, cols=3, icon=None):
    out = []
    for it in items:
        href, title, text = it[0], it[1], it[2]
        more = it[3] if len(it) > 3 else "Lees meer"
        ico = ('<div class="ico">%s</div>' % ICON[icon]) if icon else ""
        out.append('<a class="card" href="%s">%s<h3>%s</h3><p>%s</p><span class="more">%s &rarr;</span></a>' % (href, ico, esc(title), esc(text), esc(more)))
    return '<div class="grid g%d">%s</div>' % (cols, "".join(out))


def chips(items, dark=False):
    return '<div class="chips">%s</div>' % "".join('<a class="chip%s" href="%s">%s</a>' % (" chip-dark" if dark else "", h, esc(t)) for h, t in items)


def faq(items, open_first=True):
    out = []
    for i, (q, a) in enumerate(items):
        out.append('<details%s><summary>%s</summary><div class="a">%s</div></details>' % (" open" if (i == 0 and open_first) else "", esc(q), a))
    return '<div class="faq">%s</div>' % "".join(out)


def steps(items):
    return '<div class="steps">%s</div>' % "".join('<div><h3>%s</h3><p>%s</p></div>' % (esc(t), d) for t, d in items)


def usp_strip(items):
    return '<div class="wrap"><div class="usp">%s</div></div>' % "".join('<div>%s<b>%s</b><small>%s</small></div>' % ('<div class="ico" style="margin:0 auto 10px">%s</div>' % ICON[i] if i else "", esc(b), esc(s)) for i, b, s in items)


def cta(h2=None, text=None, wa_text=None):
    h2 = h2 or CTA_H2
    text = text or CTA_TEXT
    return ('<section class="cta"><div class="wrap"><h2>%s</h2><p>%s</p><a class="btn btn-light" href="%s" target="_blank" rel="noopener">%s WhatsApp ons nu</a></div></section>'
            % (esc(h2), text, wa_link(wa_text) if wa_text else wa_link(), ICON["wa"]))


def products(intro=None):
    items = [("2KG", "/lachgas-tanks/2kg/", "Lachgastank 2KG", PRODUCT_DESCS[0]),
             ("4KG", "/lachgas-tanks/4kg/", "Lachgastank 4KG", PRODUCT_DESCS[1]),
             ("10KG", "/lachgas-tanks/10kg/", "Lachgastank 10KG", PRODUCT_DESCS[2])]
    return ('<div class="grid g3 products">%s</div>' % "".join('<a class="card" href="%s"><span class="size">%s</span><h3>%s</h3><p>%s</p><span class="more">Bekijk de tank &rarr;</span></a>' % (h, s, t, d) for s, h, t, d in items))


def toc(headings):
    return '<nav class="toc" aria-label="Inhoud"><strong>Op deze pagina</strong><ol>%s</ol></nav>' % "".join('<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in headings)


def slug_id(t):
    s = re.sub(r"[^a-z0-9]+", "-", strip_tags(t).lower().replace("ë", "e").replace("é", "e").replace("ï", "i")).strip("-")
    return s[:60]


def article_body(sections, note=None, updated=MONTH_NL, with_toc=True):
    heads = [(slug_id(s["h2"]), s["h2"]) for s in sections]
    out = ['<p class="meta">Laatst bijgewerkt: %s</p>' % updated]
    if with_toc and len(sections) >= 4:
        out.append(toc(heads))
    for (hid, _), s in zip(heads, sections):
        out.append('<h2 id="%s">%s</h2>' % (hid, esc(s["h2"])))
        out.append(para(s.get("paragraphs", [])))
        if s.get("bullets"):
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % b for b in s["bullets"]))
    if note:
        out.append('<div class="notice"><strong>Let op:</strong> %s</div>' % note)
    return '<div class="prose">%s</div>' % "".join(out)


# --- renderer -----------------------------------------------------------
SPEC = ('<script type="speculationrules">{"prerender":[{"where":{"and":[{"href_matches":"/*"},{"not":{"href_matches":"/*\\\\?*"}}]},"eagerness":"moderate"}]}</script>')


def render(page, ctx):
    """page: dict met path, title, description, body, schemas, og_type, robots, modified. ctx: dict met footerlijsten."""
    path = page["path"]
    url = SITE + path
    title = page["title"]
    desc = page["description"]
    schemas = page.get("schemas", [])
    if path == "/":
        schemas = [business_schema(), website_schema()] + schemas
    ld = "".join('<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") for s in schemas)
    robots = page.get("robots", "index,follow,max-image-preview:large")
    og_img = SITE + OG_IMAGE
    preload = page.get("preload", "")
    head = ('<!DOCTYPE html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>%s</title><meta name="description" content="%s"><meta name="robots" content="%s"><link rel="canonical" href="%s">'
            '<link rel="alternate" hreflang="nl" href="%s"><link rel="alternate" hreflang="x-default" href="%s">'
            '<meta property="og:type" content="%s"><meta property="og:site_name" content="%s"><meta property="og:locale" content="nl_NL"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s">'
            '<meta name="theme-color" content="%s"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="32x32 48x48"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="manifest" href="/manifest.webmanifest">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>%s<style>%s%s</style>%s%s</head>'
            % (esc(title), esc(desc), robots, url, url, url, page.get("og_type", "website"), BRAND, esc(title), esc(desc), url, og_img, esc(title), esc(desc), og_img,
               THEME, preload, FONTS, CSS, ld, SPEC))
    body = header(path) + '<main id="inhoud">' + page["body"] + "</main>" + footer(ctx["footer_regions"], ctx["footer_info"], ctx["footer_service"])
    return head + "<body>" + body + "</body></html>\n"


def page_text(page):
    """Platte tekst van de hoofdinhoud (voor llms-full.txt en controles)."""
    b = re.sub(r"<(script|style|svg)\b.*?</\1>", "", page["body"], flags=re.S)
    b = re.sub(r"</(p|li|h1|h2|h3|dd|dt|tr|div|section|summary)>", "\n", b)
    t = _html.unescape(strip_tags(b))
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()

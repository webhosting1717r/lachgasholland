# -*- coding: utf-8 -*-
"""Paginabouwers voor de provincie-/landelijke sites: zetten contentmodules om in pagina-dicts voor common.render()."""
import common as C
from common import esc, para, section, sec_head, cards, chips, faq, steps, cta, products, page_head, article_body, ICON

AREA_DIR = "/lachgas-bezorgen"


def area_href(slug):
    return "%s/%s/" % (AREA_DIR, slug)


class Site:
    def __init__(self, home, regions, places, articles, services, faq_topics, tanks, pages, topic_hubs=None):
        self.home, self.regions, self.places, self.articles, self.services, self.faq_topics, self.tanks, self.pages = home, regions, places, articles, services, faq_topics, tanks, pages
        self.topic_hubs = topic_hubs or []
        self.place_by = {p["slug"]: p for p in places}
        self.region_by = {r["slug"]: r for r in regions}
        self.art_by = {a["slug"]: a for a in articles}
        self.svc_by = {s["slug"]: s for s in services}
        self.out = []

    # -- helpers -----------------------------------------------------------
    def place_link(self, slug):
        p = self.place_by[slug]
        return (area_href(slug), p["name"])

    def related_links(self, slugs):
        out = []
        for s in slugs:
            if s in self.art_by:
                out.append(("/informatie/%s/" % s, self.art_by[s]["h1"]))
            elif s in self.svc_by:
                out.append(("/service/%s/" % s, self.svc_by[s]["h1"]))
            elif s in self.place_by:
                out.append(self.place_link(s))
            elif s in self.region_by:
                out.append(("/bezorggebied/%s/" % s, self.region_by[s]["name"]))
        return out

    def add(self, **page):
        self.out.append(page)

    # -- homepage -----------------------------------------------------------
    def home_page(self):
        H = self.home
        hero = ('<section class="hero"><div class="wrap hero-grid"><div><span class="kicker"><i></i>%s</span><h1>%s</h1><p class="lead">%s</p>'
                '<div class="ctas"><a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s WhatsApp ons nu</a><a class="btn btn-ghost" href="/lachgas-tanks/">Bekijk de tanks</a></div>'
                '<ul class="checks">%s</ul></div>'
                '<aside class="hero-card"><h2>%s</h2><dl>%s</dl><a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s Bestel via WhatsApp</a></aside></div></section>'
                % (esc(H["kicker"]), H["h1"], H["lead"], C.wa_link(), ICON["wa"], "".join("<li>%s</li>" % c for c in H["checks"]),
                   esc(H["card_title"]), "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (esc(k), esc(v)) for k, v in H["card_facts"]), C.wa_link(), ICON["wa"]))
        usp = C.usp_strip(H["usps"])
        reg = section(sec_head("Bezorggebied", H["regions_h2"], H["regions_text"]) + cards([("/bezorggebied/%s/" % r["slug"], r["name"], r["card"], "Bekijk de regio") for r in self.regions], 4, "pin")
                      + '<div style="margin-top:22px;text-align:center"><a class="btn btn-dark" href="/bezorggebied/">%s</a></div>' % esc(C.ALL_PLACES_LABEL))
        top = section(sec_head("Steden", H["cities_h2"], H["cities_text"]) + chips([self.place_link(s) for s in H["city_slugs"] if s in self.place_by], dark=True), alt=True)
        tanks = section(sec_head("Assortiment", H["tanks_h2"], H["tanks_text"]) + C.product_feature() + products())
        how = section(sec_head("Zo werkt het", H["steps_h2"], H["steps_text"]) + steps(H["steps"]), alt=True)
        why = section(sec_head("Waarom %s" % C.BRAND, H["why_h2"], H["why_text"]) + cards([(h, t, d, m) for h, t, d, m in H["why_cards"]], 3, "shield"))
        info_items = [("/informatie/%s/" % h["slug"], h["h1"], h["description"], "Bekijk het thema") for h in self.topic_hubs] + [("/informatie/%s/" % a["slug"], a["h1"], a["description"]) for a in self.articles if a["slug"] in H["info_slugs"]]
        info = section(sec_head("Informatie", H["info_h2"], H["info_text"]) + cards(info_items[:6], 3, "book") + '<div style="margin-top:22px;text-align:center"><a class="btn btn-dark" href="/informatie/">Alle informatie</a></div>', alt=True)
        fq = section('<div class="narrow">' + sec_head("Veelgestelde vragen", H["faq_h2"], H["faq_text"]) + faq(H["faq"]) + '<p style="text-align:center;margin-top:18px"><a href="/veelgestelde-vragen/"><strong>Alle veelgestelde vragen &rarr;</strong></a></p></div>')
        svc_items = [("/service/%s/" % self.svc_by[sl]["slug"], self.svc_by[sl]["h1"], self.svc_by[sl]["description"]) for sl in ("zakelijk-bestellen", "bezorgvoorwaarden", "bestelling-wijzigen-of-annuleren", "veilig-bestellen-oplichting-herkennen") if sl in self.svc_by]
        svc = section(sec_head("Service", "Zakelijk, voorwaarden en wijzigen", C.SVC_TEXT) + cards(svc_items, 2, "clock")) if svc_items else ""
        body = hero + usp + reg + top + tanks + how + why + info + svc + fq + cta()
        self.add(path="/", title=H["title"], description=H["description"], body=body, schemas=[C.faq_schema(H["faq"])], priority="1.0", changefreq="weekly",
                 preload="")

    # -- bezorggebied-overzicht ----------------------------------------------
    def area_index(self):
        A = self.pages["AREA_INDEX"]
        groups = ""
        for r in self.regions:
            pl = [self.place_link(s) for s in r["places"] if s in self.place_by]
            groups += ('<div style="margin-bottom:34px"><h2 style="font-size:1.375rem"><a href="/bezorggebied/%s/">%s</a></h2><p style="color:var(--muted)">%s</p>%s</div>'
                       % (r["slug"], esc(r["name"]), r["card"], chips(pl)))
        body = (page_head([("Home", "/"), ("Bezorggebied", None)], "Bezorggebied", A["h1"], A["lead"])
                + section('<div class="prose">%s</div>' % para(A["intro"]))
                + section(groups, alt=True)
                + section('<div class="narrow">' + sec_head("Vragen", "Veelgestelde vragen over het bezorggebied") + faq(A["faq"]) + "</div>")
                + cta())
        self.add(path="/bezorggebied/", title=A["title"], description=A["description"], body=body, priority="0.9", changefreq="weekly",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Bezorggebied", "/bezorggebied/")]), C.faq_schema(A["faq"]),
                          C.itemlist_schema("Bezorggebied %s" % C.REGION, [("/bezorggebied/%s/" % r["slug"], r["name"]) for r in self.regions])])

    # -- regio-hub ----------------------------------------------------------
    def region_page(self, r):
        path = "/bezorggebied/%s/" % r["slug"]
        pl = [self.place_link(s) for s in r["places"] if s in self.place_by]
        crumbs = [("Home", "/"), ("Bezorggebied", "/bezorggebied/"), (r["name"], None)]
        gem = ""
        if r.get("gemeenten"):
            gem = '<h2 style="margin-top:36px">Gemeenten in %s</h2><div class="tbl-wrap"><table class="tbl"><thead><tr><th>Gemeente</th><th>Kernen waar wij bezorgen</th><th>Levertijd (indicatie)</th></tr></thead><tbody>%s</tbody></table></div>' % (
                esc(r["name"]), "".join("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td></tr>" % (esc(g[0]), g[1], esc(g[2])) for g in r["gemeenten"]))
        body = (page_head(crumbs, C.HUB_KICKER, r["h1"], r["lead"])
                + section('<div class="two"><div class="prose">%s</div><div><h2 style="font-size:1.25rem">Plaatsen in deze %s</h2>%s</div></div>%s' % (para(r["intro"]), esc(C.HUB_WORD), chips(pl, dark=True), gem))
                + section(sec_head("Werkwijze", "Zo bestel je in %s" % r["name"]) + steps(self.home["steps"]), alt=True)
                + section('<div class="narrow">' + sec_head("Vragen", "Veelgestelde vragen over %s" % r["name"]) + faq(r["faq"]) + "</div>")
                + section(sec_head(C.OTHER_HUBS_TAG, C.OTHER_HUBS_H2) + chips([("/bezorggebied/%s/" % x["slug"], x["name"]) for x in self.regions if x["slug"] != r["slug"]] + [("/bezorggebied/", C.REGION_LONG[0].upper() + C.REGION_LONG[1:])]), alt=True)
                + cta(wa_text="Hoi, ik wil graag lachgas bestellen in %s." % r["name"]))
        self.add(path=path, title=r["title"], description=r["description"], body=body, priority="0.9", changefreq="weekly",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Bezorggebied", "/bezorggebied/"), (r["name"], path)]), C.service_schema("Lachgas bezorgen in %s" % r["name"], r["description"], path, r["name"], "AdministrativeArea"), C.faq_schema(r["faq"]),
                          C.itemlist_schema("Plaatsen in %s" % r["name"], pl)])

    # -- plaatspagina ----------------------------------------------------------
    def place_page(self, p):
        path = area_href(p["slug"])
        r = self.region_by[p["region"]]
        crumbs = [("Home", "/"), ("Bezorggebied", "/bezorggebied/"), (r["name"], "/bezorggebied/%s/" % r["slug"]), (p["name"], None)]
        facts = [("Regio", r["name"]), ("Levertijd", p["levertijd"]), ("Bestellen", "24/7 via WhatsApp"), ("Betalen", "Contant of Tikkie bij levering")]
        if p.get("gemeente") and p["gemeente"] != p["name"]:
            facts.insert(1, ("Gemeente", p["gemeente"]))
        side = ('<aside class="hero-card" style="position:sticky;top:84px"><h2>Lachgas bezorgen in %s</h2><dl>%s</dl><a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s WhatsApp ons</a></aside>'
                % (esc(p["name"]), "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (esc(k), esc(v)) for k, v in facts), C.wa_link("Hoi, ik wil graag lachgas bestellen in %s." % p["name"]), ICON["wa"]))
        intro = para(p["intro"]) + '<p><strong>%s in %s:</strong> %s.</p>' % ("Wijken en buurten" if p.get("kind") in ("stad", "wijk") else "Kernen en buurten", esc(p["name"]), esc((p.get("kernen") or p.get("wijken", "")).rstrip(".")))
        near = [self.place_link(s) for s in p["nearby"] if s in self.place_by] + [("/bezorggebied/%s/" % r["slug"], "Heel %s" % r["name"])]
        body = (page_head(crumbs, "Bezorggebied", p["h1"], p["lead"])
                + section('<div class="two"><div class="prose">%s</div>%s</div>' % (intro, side))
                + section(sec_head("Assortiment", "Lachgastanks in %s" % p["name"], "Verzegeld geleverd, prijs vooraf bevestigd via WhatsApp.") + products(), alt=True)
                + section('<div class="narrow">' + sec_head("Vragen", "Veelgestelde vragen over lachgas in %s" % p["name"]) + faq(p["faq"]) + "</div>")
                + section(sec_head("In de buurt", "Wij bezorgen ook hier") + chips(near), alt=True)
                + cta(wa_text="Hoi, ik wil graag lachgas bestellen in %s." % p["name"]))
        self.add(path=path, title=p["title"], description=p["description"], body=body, priority="0.8", changefreq="weekly",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Bezorggebied", "/bezorggebied/"), (r["name"], "/bezorggebied/%s/" % r["slug"]), (p["name"], path)]),
                          dict(C.service_schema("Lachgas bezorgen in %s" % p["name"], p["description"], path, p["name"], "City"), **({"areaServed": {"@type": "City", "name": p["name"], "geo": {"@type": "GeoCoordinates", "latitude": p["lat"], "longitude": p["lon"]}}} if p.get("lat") else {})),
                          C.faq_schema(p["faq"])])

    # -- informatie ----------------------------------------------------------
    def info_index(self):
        I = self.pages["INFO_INDEX"]
        groups = ""
        if self.topic_hubs:
            groups += '<h2 style="margin:28px 0 14px;font-size:1.375rem">Thema\'s</h2>%s' % cards([("/informatie/%s/" % h["slug"], h["h1"], h["description"], "Bekijk het thema") for h in self.topic_hubs], 2, "book")
        seen = set()
        for g in I["groups"]:
            arts = [a for a in self.articles if a["slug"] in g["slugs"]]
            seen |= {a["slug"] for a in arts}
            groups += '<h2 style="margin:28px 0 14px;font-size:1.375rem">%s</h2>%s' % (esc(g["h2"]), cards([("/informatie/%s/" % a["slug"], a["h1"], a["description"]) for a in arts], 3, "book"))
        rest = [a for a in self.articles if a["slug"] not in seen]
        if rest:
            groups += '<h2 style="margin:28px 0 14px;font-size:1.375rem">Kennisbank: praktijk en achtergrond</h2>%s' % cards([("/informatie/%s/" % a["slug"], a["h1"], a["description"]) for a in rest], 3, "book")
        body = (page_head([("Home", "/"), ("Informatie", None)], "Kennisbank", I["h1"], I["lead"]) + section('<div class="prose">%s</div>%s' % (para(I["intro"]), groups)) + cta())
        self.add(path="/informatie/", title=I["title"], description=I["description"], body=body, priority="0.9",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Informatie", "/informatie/")]), C.itemlist_schema("Lachgas informatie", [("/informatie/%s/" % a["slug"], a["h1"]) for a in self.articles])])

    def article_page(self, a):
        path = "/informatie/%s/" % a["slug"]
        crumbs = [("Home", "/"), ("Informatie", "/informatie/"), (a["h1"], None)]
        rel = self.related_links(a.get("related", [])) + [("/informatie/", "Alle informatie")]
        words = sum(len(C.strip_tags(x).split()) for sec in a["sections"] for x in sec.get("paragraphs", []) + sec.get("bullets", []))
        mins = max(1, round(words / 220))
        updated = "%s &middot; Leestijd ongeveer %d %s &middot; Geschreven en gecontroleerd door het team van %s" % (C.MONTH_NL, mins, "minuut" if mins == 1 else "minuten", C.BRAND)
        box = ('<div class="notice" style="margin-top:28px"><strong>Over deze informatie:</strong> %s Vraag of fout gezien? <a href="/contact/">Neem contact met ons op</a>.</div>' % (C.ARTICLE_BOX % C.BRAND))
        body = (page_head(crumbs, a["label"], a["h1"], a["lead"]) + section(article_body(a["sections"], a.get("note"), updated=updated) + box)
                + section(sec_head("Verder lezen", "Gerelateerde onderwerpen") + chips(rel), alt=True) + cta())
        self.add(path=path, title=a["title"], description=a["description"], body=body, og_type="article", priority="0.7",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Informatie", "/informatie/"), (a["h1"], path)]), C.article_schema(a["title"], a["description"], path)])

    # -- service ---------------------------------------------------------------
    def service_page(self, s):
        path = "/service/%s/" % s["slug"]
        crumbs = [("Home", "/"), ("Service", "/service/"), (s["h1"], None)]
        rel = self.related_links(s.get("related", []))
        body = (page_head(crumbs, s["label"], s["h1"], s["lead"]) + section(article_body(s["sections"], s.get("note"), with_toc=False))
                + section('<div class="narrow">' + sec_head("Vragen", "Veelgestelde vragen") + faq(s["faq"]) + "</div>", alt=True)
                + (section(sec_head("Verder lezen", "Gerelateerde pagina's") + chips(rel)) if rel else "") + cta())
        self.add(path=path, title=s["title"], description=s["description"], body=body, priority="0.8",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Service", "/service/"), (s["h1"], path)]), C.service_schema(s["h1"], s["description"], path, C.REGION, C.AREA_TYPE), C.faq_schema(s["faq"])])

    def service_index(self):
        S = self.pages["SERVICE_INDEX"]
        body = (page_head([("Home", "/"), ("Service", None)], "Service", S["h1"], S["lead"]) + section('<div class="prose">%s</div>' % para(S["intro"]) + cards([("/service/%s/" % s["slug"], s["h1"], s["description"]) for s in self.services], 3, "clock")) + cta())
        self.add(path="/service/", title=S["title"], description=S["description"], body=body, priority="0.8",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Service", "/service/")]), C.itemlist_schema("Service", [("/service/%s/" % s["slug"], s["h1"]) for s in self.services])])

    # -- tanks -------------------------------------------------------------------
    def tanks_index(self):
        T = self.tanks["INDEX"]
        rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in T["table"])
        body = (page_head([("Home", "/"), ("Lachgas tanks", None)], "Assortiment", T["h1"], T["lead"])
                + section('<div class="prose">%s</div>' % para(T["intro"]) + C.product_feature("h2") + products())
                + section(sec_head("Vergelijken", T["table_h2"], T["table_text"]) + '<div class="tbl-wrap"><table class="tbl"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % ("".join("<th>%s</th>" % esc(h) for h in T["table_head"]), rows), alt=True)
                + section('<div class="narrow">' + sec_head("Vragen", "Veelgestelde vragen over onze tanks") + faq(T["faq"]) + "</div>") + cta())
        self.add(path="/lachgas-tanks/", title=T["title"], description=T["description"], body=body, priority="0.9",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Lachgas tanks", "/lachgas-tanks/")]), C.faq_schema(T["faq"]), C.itemlist_schema("Lachgastanks", [("/lachgas-tanks/%s/" % t["slug"], t["h1"]) for t in self.tanks["TANKS"]])])

    def tank_page(self, t):
        path = "/lachgas-tanks/%s/" % t["slug"]
        crumbs = [("Home", "/"), ("Lachgas tanks", "/lachgas-tanks/"), (t["h1"], None)]
        photo = ('<div class="pf-img"><img src="/assets/lachgastank-2kg.webp" srcset="/assets/lachgastank-2kg-300.webp 300w, /assets/lachgastank-2kg.webp 480w" sizes="200px" width="480" height="640" alt="Verzegelde lachgastank 2KG van %s" loading="lazy" decoding="async"></div>' % esc(C.BRAND)) if t["slug"] == "2kg" else ""
        facts = '<aside class="hero-card" style="position:sticky;top:84px">' + photo + '<h2>%s</h2><dl>%s</dl><a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s Bestel via WhatsApp</a></aside>' % (
            esc(t["h1"]), "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (esc(k), esc(v)) for k, v in t["facts"]), C.wa_link("Hoi, ik wil graag een %s bestellen." % t["h1"].lower()), ICON["wa"])
        body = (page_head(crumbs, "Lachgastank", t["h1"], t["lead"]) + section('<div class="two">%s%s</div>' % (article_body(t["sections"], t.get("note"), with_toc=False), facts))
                + section('<div class="narrow">' + sec_head("Vragen", "Veelgestelde vragen over de %s" % t["h1"].lower()) + faq(t["faq"]) + "</div>", alt=True)
                + section(sec_head("Andere formaten", "Vergelijk met de andere tanks") + chips([("/lachgas-tanks/%s/" % x["slug"], x["h1"]) for x in self.tanks["TANKS"] if x["slug"] != t["slug"]] + [("/lachgas-tanks/", "Alle tanks vergelijken")])) + cta())
        schema = {"@context": "https://schema.org", "@type": "Product", "name": t["h1"], "description": t["description"], "url": C.SITE + path, "brand": {"@type": "Brand", "name": C.BRAND},
                  **({"image": C.SITE + "/assets/lachgastank-2kg.webp"} if t["slug"] == "2kg" else {}),
                  "offers": {"@type": "Offer", "availability": "https://schema.org/InStock", "priceCurrency": "EUR", "url": C.SITE + path, "seller": {"@id": C.SITE + "/#business"}, "priceSpecification": {"@type": "PriceSpecification", "priceCurrency": "EUR", "description": "Prijs op aanvraag via WhatsApp"}}}
        self.add(path=path, title=t["title"], description=t["description"], body=body, priority="0.8",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Lachgas tanks", "/lachgas-tanks/"), (t["h1"], path)]), schema, C.faq_schema(t["faq"])])

    # -- FAQ -----------------------------------------------------------------------
    def faq_index(self):
        F = self.pages["FAQ_INDEX"]
        body = (page_head([("Home", "/"), ("Veelgestelde vragen", None)], "FAQ", F["h1"], F["lead"])
                + section('<div class="prose">%s</div>' % para(F["intro"]) + cards([("/veelgestelde-vragen/%s/" % t["slug"], t["h1"], t["description"], "Bekijk de vragen") for t in self.faq_topics], 3, "chat"))
                + section('<div class="narrow">' + sec_head("Meest gesteld", F["top_h2"]) + faq(F["top"]) + "</div>", alt=True) + cta())
        self.add(path="/veelgestelde-vragen/", title=F["title"], description=F["description"], body=body, priority="0.8",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Veelgestelde vragen", "/veelgestelde-vragen/")]), C.faq_schema(F["top"])])

    def faq_topic_page(self, t):
        path = "/veelgestelde-vragen/%s/" % t["slug"]
        crumbs = [("Home", "/"), ("Veelgestelde vragen", "/veelgestelde-vragen/"), (t["h1"], None)]
        body = (page_head(crumbs, "FAQ", t["h1"], t["lead"]) + section('<div class="narrow"><div class="prose">%s</div>%s</div>' % (para(t["intro"]), faq(t["items"])))
                + section(sec_head("Meer vragen", "Andere onderwerpen") + chips([("/veelgestelde-vragen/%s/" % x["slug"], x["h1"]) for x in self.faq_topics if x["slug"] != t["slug"]] + self.related_links(t.get("related", []))), alt=True) + cta())
        self.add(path=path, title=t["title"], description=t["description"], body=body, priority="0.7",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Veelgestelde vragen", "/veelgestelde-vragen/"), (t["h1"], path)]), C.faq_schema(t["items"])])

    # -- overige pagina's ------------------------------------------------------
    def simple_page(self, key, path, crumb, kicker, priority="0.5", extra_faq=None, robots=None):
        P = self.pages[key]
        body = page_head([("Home", "/"), (crumb, None)], kicker, P["h1"], P["lead"]) + section(article_body(P["sections"], P.get("note"), with_toc=len(P["sections"]) >= 5))
        if extra_faq:
            body += section('<div class="narrow">' + sec_head("Vragen", "Veelgestelde vragen") + faq(extra_faq) + "</div>", alt=True)
        body += cta()
        pg = dict(path=path, title=P["title"], description=P["description"], body=body, priority=priority,
                  schemas=[C.crumbs_schema([("Home", "/"), (crumb, path)]), C.webpage_schema(P["title"], P["description"], path)])
        if robots:
            pg["robots"] = robots
        self.add(**pg)

    def contact_page(self):
        P = self.pages["CONTACT"]
        body = (page_head([("Home", "/"), ("Contact", None)], "Contact", P["h1"], P["lead"])
                + section('<div class="two"><div class="prose">%s</div><aside class="hero-card"><h2>Direct contact</h2><dl><div><dt>WhatsApp</dt><dd>%s</dd></div><div><dt>E-mail</dt><dd><a href="mailto:%s" style="color:#fff">%s</a></dd></div><div><dt>Bereikbaar</dt><dd>24 uur per dag, 7 dagen per week</dd></div><div><dt>Werkgebied</dt><dd>%s</dd></div></dl><a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s Open WhatsApp</a></aside></div>'
                          % (para(P["intro"]), C.WA_DISPLAY, C.EMAIL, C.EMAIL, esc(C.REGION_LONG[0].upper() + C.REGION_LONG[1:]), C.wa_link(), ICON["wa"]))
                + section('<div class="narrow">' + sec_head("Vragen", "Veelgestelde vragen over contact en bestellen") + faq(P["faq"]) + "</div>", alt=True))
        self.add(path="/contact/", title=P["title"], description=P["description"], body=body, priority="0.7",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Contact", "/contact/")]), {"@context": "https://schema.org", "@type": "ContactPage", "name": P["title"], "url": C.SITE + "/contact/", "mainEntity": {"@id": C.SITE + "/#business"}}, C.faq_schema(P["faq"])])

    def sitemap_page(self):
        groups = [("Hoofdpagina's", [("/", "Home"), ("/bezorggebied/", "Bezorggebied"), ("/lachgas-tanks/", "Lachgas tanks"), ("/informatie/", "Informatie"), ("/service/", "Service"), ("/veelgestelde-vragen/", "Veelgestelde vragen"), ("/over-ons/", "Over ons"), ("/contact/", "Contact")]),
                  (C.MM_REGION_TITLE, [("/bezorggebied/%s/" % r["slug"], r["name"]) for r in self.regions])]
        for r in self.regions:
            groups.append(("Plaatsen in %s" % r["name"], [self.place_link(s) for s in r["places"] if s in self.place_by]))
        groups += [("Lachgas tanks", [("/lachgas-tanks/%s/" % t["slug"], t["h1"]) for t in self.tanks["TANKS"]]),
                   ("Informatie", [("/informatie/%s/" % a["slug"], a["h1"]) for a in self.articles]),
                   ("Service", [("/service/%s/" % s["slug"], s["h1"]) for s in self.services]),
                   ("Veelgestelde vragen", [("/veelgestelde-vragen/%s/" % t["slug"], t["h1"]) for t in self.faq_topics]),
                   ("Juridisch", [("/algemene-voorwaarden/", "Algemene voorwaarden"), ("/privacy/", "Privacyverklaring")])]
        inner = "".join('<h2 style="font-size:1.25rem;margin-top:26px">%s</h2><ul style="columns:2;column-gap:24px">%s</ul>' % (esc(h), "".join('<li><a href="%s">%s</a></li>' % (u, esc(n)) for u, n in items)) for h, items in groups)
        body = page_head([("Home", "/"), ("Sitemap", None)], "Overzicht", "Sitemap", "Alle pagina's van %s op een rij." % C.BRAND) + section('<div class="prose" style="max-width:900px">%s<p style="margin-top:20px"><a href="/sitemap.xml">XML-sitemap voor zoekmachines</a></p></div>' % inner)
        self.add(path="/sitemap/", title="Sitemap | %s" % C.BRAND, description="Overzicht van alle pagina's van %s: bezorggebied per %s en plaats, lachgastanks, informatie, service en veelgestelde vragen." % (C.BRAND, C.HUB_WORD), body=body, priority="0.3",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Sitemap", "/sitemap/")])])

    def not_found(self):
        body = page_head([("Home", "/"), ("Pagina niet gevonden", None)], "404", "Pagina niet gevonden", "Deze pagina bestaat niet (meer). Kies hieronder waar je heen wilt.") + section(chips([("/", "Home"), ("/bezorggebied/", "Bezorggebied"), ("/lachgas-tanks/", "Lachgas tanks"), ("/informatie/", "Informatie"), ("/veelgestelde-vragen/", "Veelgestelde vragen"), ("/contact/", "Contact")], dark=True)) + cta()
        self.add(path="/404.html", title="Pagina niet gevonden | %s" % C.BRAND, description="De opgevraagde pagina bestaat niet. Ga terug naar de homepage van %s of kies een van de hoofdpagina's." % C.BRAND, body=body, robots="noindex,follow", sitemap=False)

    # -- alles ---------------------------------------------------------------
    # -- thema-hub ------------------------------------------------------------
    def topic_hub_page(self, h):
        path = "/informatie/%s/" % h["slug"]
        crumbs = [("Home", "/"), ("Informatie", "/informatie/"), (h["h1"], None)]
        groups = ""
        listed = []
        for i, g in enumerate(h["groups"]):
            arts = [self.art_by[s] for s in g["slugs"] if s in self.art_by]
            if not arts: continue
            listed += [a["slug"] for a in arts]
            groups += section(sec_head("Thema", g["h2"], g.get("text")) + cards([("/informatie/%s/" % a["slug"], a["h1"], a["description"]) for a in arts], 3, "book"), alt=(i % 2 == 0))
        body = (page_head(crumbs, h.get("label", "Thema"), h["h1"], h["lead"]) + section('<div class="prose">%s</div>' % para(h["intro"])) + groups
                + section('<div class="narrow">' + sec_head("Vragen", "Veelgestelde vragen") + faq(h["faq"]) + "</div>") + cta())
        self.add(path=path, title=h["title"], description=h["description"], body=body, priority="0.8",
                 schemas=[C.crumbs_schema([("Home", "/"), ("Informatie", "/informatie/"), (h["h1"], path)]), C.faq_schema(h["faq"]), C.webpage_schema(h["title"], h["description"], path),
                          C.itemlist_schema(h["h1"], [("/informatie/%s/" % s, self.art_by[s]["h1"]) for s in listed])])

    def build_all(self):
        self.home_page(); self.area_index()
        for r in self.regions: self.region_page(r)
        for p in self.places: self.place_page(p)
        self.tanks_index()
        for t in self.tanks["TANKS"]: self.tank_page(t)
        self.info_index()
        for a in self.articles: self.article_page(a)
        for h in self.topic_hubs: self.topic_hub_page(h)
        self.service_index()
        for s in self.services: self.service_page(s)
        self.faq_index()
        for t in self.faq_topics: self.faq_topic_page(t)
        self.simple_page("ABOUT", "/over-ons/", "Over ons", "Over ons", "0.6")
        self.contact_page()
        self.simple_page("TERMS", "/algemene-voorwaarden/", "Algemene voorwaarden", "Juridisch", "0.3")
        self.simple_page("PRIVACY", "/privacy/", "Privacyverklaring", "Juridisch", "0.3")
        self.sitemap_page(); self.not_found()
        return self.out

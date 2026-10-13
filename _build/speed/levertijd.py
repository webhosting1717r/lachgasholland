# -*- coding: utf-8 -*-
"""Uniforme bezorgtijd: elke tijdsband (bijv. '20 tot 30 minuten', '45-60 min') wordt '15 tot 25 minuten' / '15-25 min'.
Wordt gebruikt op de contentbronnen, de generatorcode en als laatste stap op de gebouwde HTML en tekstbestanden."""
import os, re
NUM = re.compile(r"\b(\d{1,2})( ?)(tot|en|-|–)( ?)(\d{2,3})( ?)(minuten|min)\b")
def fix(t):
    t = NUM.sub(lambda m: "15%s%s%s25%s%s" % (m.group(2), "-" if m.group(3) == "–" else m.group(3), m.group(4), m.group(6), m.group(7)), t)
    t = t.replace("±25min", "±20min").replace("&plusmn;25min", "&plusmn;20min")
    return t
def domain(repo):
    dom = ""
    cn = os.path.join(repo, "CNAME")
    if os.path.exists(cn): dom = open(cn).read().strip()
    if not dom:
        idx = os.path.join(repo, "index.html")
        if os.path.exists(idx):
            m = re.search(r'<link rel="canonical" href="https?://([^/"]+)', open(idx, encoding="utf-8").read())
            dom = m.group(1) if m else ""
    return dom
def load_fixes(repo):
    import json
    here = os.path.dirname(os.path.abspath(__file__))
    dom = domain(repo)
    f = os.path.join(here, "basis_fix", dom + ".json")
    return json.load(open(f, encoding="utf-8")) if dom and os.path.exists(f) else []
def copy_images(repo):
    """Afbeeldingen met de bezorgtijd in beeld (hero, OG) vervangen door de 15-25-versie uit levertijd_img/<domein>/."""
    import shutil
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "levertijd_img", domain(repo))
    for root, dirs, files in os.walk(src):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), src); dst = os.path.join(repo, rel)
            if os.path.exists(dst): shutil.copyfile(os.path.join(root, f), dst)
def apply_dir(repo):
    copy_images(repo)
    n = 0
    fixes = load_fixes(repo)
    for root, dirs, files in os.walk(repo):
        if ".git" in root or "_build" in root: continue
        for f in files:
            if f.endswith((".html", ".txt", ".xml", ".json", ".webmanifest")):
                p = os.path.join(root, f); d = open(p, encoding="utf-8").read(); nd = fix(d)
                for e in fixes:
                    if e["oud"] in nd: nd = nd.replace(e["oud"], e["nieuw"])
                if nd != d: open(p, "w", encoding="utf-8").write(nd); n += 1
    return n

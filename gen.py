# -*- coding: utf-8 -*-
# Génère le site : python gen.py   (textes dans content/site.json et content/games/*.json)
import json,os,glob,datetime
from urllib.parse import quote
BASE="https://cardforgestudio.github.io"   # sans slash final ; sert aux canonical, hreflang et sitemap
UTM_SOURCE="cardforgestudio-site"
SITEMAP_HREFLANG=False   # True = ajoute les liens hreflang dans le sitemap (déjà présents dans le <head> des pages)
ROOT=os.path.dirname(os.path.abspath(__file__))
LANGS=["fr","en","de","es","it"]
VERIF='<meta name="google-site-verification" content="8SDHUerU7Fc-hJMIeVGXjvIDedUCsISQvQDIxCLT-1o" />'
S=json.load(open(os.path.join(ROOT,"content","site.json"),encoding="utf-8"))
G=sorted((json.load(open(f,encoding="utf-8")) for f in glob.glob(os.path.join(ROOT,"content","games","*.json"))),key=lambda g:g.get("order",99))
missing=[]
def P(l): return "" if l=="fr" else "../"
def U(l,file): return BASE+"/"+("" if l=="fr" else l+"/")+("" if file=="index.html" else file)
def href(a,b,page): return ("" if a=="fr" else "../")+("" if b=="fr" else b+"/")+page
def shot(l,n):
    for e in(".png",".jpg",".jpeg",".webp"):
        if os.path.exists(os.path.join(ROOT,"images","screenshots",l,n+e)): return f'{P(l)}images/screenshots/{l}/{n}{e}'
    missing.append(f"images/screenshots/{l}/{n}.(png|jpg)"); return f'{P(l)}images/screenshots/{l}/{n}.png'
def play_url(g,l,pl):
    ref=f"utm_source={UTM_SOURCE}&utm_medium=website&utm_campaign={g['slug']}_{l}&utm_content={pl}"
    return g["play"]+"&referrer="+quote(ref,safe="")
def badge(l,t,g,pl="site"): return f'<a class="badge" href="{play_url(g,l,pl).replace("&","&amp;")}" rel="noopener"><img src="{P(l)}images/logo/google-play-badge-logo.svg" alt="{t["badge"]}" height="64"></a>'
def block(l,b):
    if "p" in b: return f'<p>{b["p"]}</p>'
    if "note" in b: return f'<p class="note">{b["note"]}</p>'
    if "table" in b:
        t=b["table"];return '<div class="tw"><table><thead><tr>'+"".join(f"<th>{h}</th>" for h in t["head"])+'</tr></thead><tbody>'+"".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in t["rows"])+'</tbody></table></div>'
    if "fig" in b: f=b["fig"];return f'<figure><img src="{shot(l,f["img"])}" width="1200" height="538" loading="lazy" alt="{f["cap"]}"><figcaption>{f["cap"]}</figcaption></figure>'
    return ""
def page(l,file,title,desc,body):
    t=S["lang"][l];p=P(l);pf=f"{BASE}/{'' if l=='fr' else l+'/'}{file}"
    seo=(f'<link rel="canonical" href="{U(l,file)}">'+"".join(f'<link rel="alternate" hreflang="{x}" href="{U(x,file)}">' for x in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{U("fr",file)}">') if BASE else ""
    cur,pg=' aria-current="true"',' aria-current="page"'
    sw="".join(f'<a href="{href(l,x,file)}" hreflang="{x}" lang="{x}"{cur if x==l else ""}>{x.upper()}</a>' for x in LANGS)
    rules=G[0]["slug"]+".html"
    nav=f'<nav><div class="w"><a class="logo" href="{href(l,l,"index.html")}">Card<span>Forge</span>Studio</a><ul><li><a href="{href(l,l,"index.html")}#jeux">{t["nav"][0]}</a></li><li><a href="{href(l,l,rules)}"{pg if file!="index.html" else ""}>{t["nav"][1]}</a></li><li class="lg">{sw}</li></ul></div></nav>'
    foot=f'<footer><div class="w"><span>&copy; 2026 {S["brand"]}</span><span><a href="{p}privacy-policy.html">{t["priv"]}</a> · <a href="mailto:{S["email"]}">{t["contact"]}</a></span></div></footer>'
    ico=f'<link rel="icon" href="{p}favicon.ico" sizes="48x48"><link rel="icon" href="{p}favicon.svg" type="image/svg+xml"><link rel="icon" href="{p}icon-192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="{p}apple-touch-icon.png">'
    v=VERIF if (l=="fr" and file=="index.html") else ""
    return f'<!DOCTYPE html>\n<html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n{v}\n<title>{title}</title><meta name="description" content="{desc}">{seo}{ico}<link rel="stylesheet" href="{p}styles.css"></head><body>\n{nav}\n<main>{body}</main>\n{foot}\n</body></html>\n'
def out(l,file,html):
    d=os.path.join(ROOT,"" if l=="fr" else l);os.makedirs(d,exist_ok=True)
    open(os.path.join(d,file),"w",encoding="utf-8").write(html)
for l in LANGS:
    t=S["lang"][l];p=P(l);g0=G[0]["lang"][l]
    fan="".join(f'<div class="pc"><img src="{p}images/cards/{c}.svg" alt="" loading="lazy"></div>' for c in S["fan"])
    cards="".join(f'<div class="card"><div class="ic">{s}</div><h3>{a}</h3><p class="muted">{b}</p></div>' for s,(a,b) in zip(["&#9824;","&#9829;","&#9830;","&#9827;"],t["sc"]))
    games=""
    for g in G:
        gl=g["lang"][l]
        games+=f'<div class="game"><div>{"".join(f"<span class=tag>{x}</span>" for x in gl["tags"])}<h3>{gl["name"]}</h3><p>{gl["gp"]}</p><div class="cta">{badge(l,t,g,"index_card")}<a class="btn ghost" href="{g["slug"]}.html">{gl["gr"]}</a></div></div><img src="{shot(l,g["hero"])}" width="1200" height="538" loading="lazy" alt="{gl["name"]}"></div>'
    idx=f'''<div class="w"><header class="hero"><div><p class="suits" aria-hidden="true">&#9824; &#9829; &#9830; &#9827;</p><h1>{t["h1"]}</h1><p class="lead">{t["lead"]}</p><div class="cta">{badge(l,t,G[0],"index_hero")}<a class="btn ghost" href="{G[0]["slug"]}.html">{t["b_rules"]}</a></div></div><div class="fan" aria-hidden="true">{fan}</div></header></div>
<section class="s" id="studio"><div class="w"><h2>{t["sh"]}</h2><div class="grid">{cards}</div></div></section>
<section class="s" id="jeux"><div class="w"><h2>{t["gh"]}</h2>{games}<p class="muted" style="margin-top:1.5rem">{t["soon"]}</p></div></section>
<div class="w"><div class="banner"><h2>{t["bh"]}</h2><p class="muted">{g0["bp"]}</p>{badge(l,t,G[0],"index_banner")}</div></div>'''
    out(l,"index.html",page(l,"index.html",t["t_i"],t["d_i"],idx))
    for g in G:
        gl=g["lang"][l]
        toc="".join(f'<li><a href="#{s["id"]}">{s["title"]}</a></li>' for s in gl["sections"])
        arts="".join(f'<article id="{s["id"]}"><h2>{s["title"]}</h2>'+"".join(block(l,b) for b in s["blocks"])+'</article>' for s in gl["sections"])
        body=f'''<div class="w"><header style="padding:3.5rem 0 1.5rem" class="n"><p class="suits" aria-hidden="true">&#9824; &#9829; &#9830; &#9827;</p><h1>{gl["rt"]}</h1><p class="lead muted">{gl["rl"]}</p>{('<p class="note">'+gl["aka"]+"</p>") if gl.get("aka") else ""}<div class="cta">{badge(l,t,g,"rules_header")}</div></header>
<div class="layout"><aside class="toc"><strong class="muted">{t["toc"]}</strong><ol>{toc}</ol></aside><div class="rules">{arts}</div></div><div class="banner"><h2>{gl["fh"]}</h2><p class="muted">{gl["fp"]}</p>{badge(l,t,g,"rules_banner")}</div></div>'''
        out(l,g["slug"]+".html",page(l,g["slug"]+".html",gl["t_r"],gl["d_r"],body))
if BASE:
    today=datetime.date.today().isoformat()
    files=["index.html"]+[g["slug"]+".html" for g in G]
    urls=""
    for f in files:
        for l in LANGS:
            alts=("".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{U(x,f)}"/>' for x in LANGS)+f'<xhtml:link rel="alternate" hreflang="x-default" href="{U("fr",f)}"/>') if SITEMAP_HREFLANG else ""
            urls+=f"<url><loc>{U(l,f)}</loc><lastmod>{today}</lastmod>{alts}</url>\n"
    urls+=f"<url><loc>{BASE}/privacy-policy.html</loc><lastmod>{today}</lastmod></url>\n"
    open(os.path.join(ROOT,"sitemap.xml"),"w",encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'+(' xmlns:xhtml="http://www.w3.org/1999/xhtml"' if SITEMAP_HREFLANG else "")+'>\n'+urls+"</urlset>\n")
    open(os.path.join(ROOT,"robots.txt"),"w",encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
print("ok")
if missing: print("ATTENTION, captures introuvables :",*sorted(set(missing)),sep="\n  ")

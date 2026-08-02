# -*- coding: utf-8 -*-
"""
Horse-Play Lovas Sportegyesület — statikus oldalgenerátor.
Futtatás:  python3 build.py
A közös fejléc/lábléc egy helyen szerkeszthető, a kimenet sima HTML.
"""
import os, re, datetime

OUT = "site"
BASE = "https://www.horse-play.hu"          # <<< VÉGLEGES DOMAINRE CSERÉLENDŐ
SITE = "Horse-Play Lovas Sportegyesület"
SHORT = "Horse-Play LSE"
LAT, LON = "46.06264", "17.83478"
FB = "https://www.facebook.com/horseplaylovarda"
MAPS_EMBED = "https://www.google.com/maps?q={},{}&z=15&hl=hu&output=embed".format(LAT, LON)
MAPS_DIR = "https://www.google.com/maps/dir/?api=1&destination={},{}".format(LAT, LON)
TODAY = "2026. augusztus 2."

TEL = "[KITÖLTENDŐ: telefonszám]"
EMAIL = "[KITÖLTENDŐ: e-mail cím]"
CIM = "7911 Botykapeterd, [KITÖLTENDŐ: utca, házszám / hrsz.]"

NAV = [("index.html", "Főoldal"), ("rolunk.html", "Rólunk"),
       ("szolgaltatasok.html", "Szolgáltatások"), ("lovaink.html", "Lovaink"),
       ("galeria.html", "Galéria"), ("kapcsolat.html", "Kapcsolat")]

LEGAL = [("impresszum.html", "Impresszum"),
         ("adatkezelesi-tajekoztato.html", "Adatkezelési tájékoztató"),
         ("cookie-tajekoztato.html", "Süti- (cookie-) tájékoztató"),
         ("akadalymentessegi-nyilatkozat.html", "Akadálymentességi nyilatkozat")]

def F(t):
    """Kitöltendő mező kiemelése."""
    return '<span class="tofill">%s</span>' % t

SHOE = ('<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false">'
        '<path d="M14 34A18 18 0 0 1 50 34V51a3.5 3.5 0 0 1-7 0V34a11 11 0 0 0-22 0v17a3.5 3.5 0 0 1-7 0Z" fill="#E2A32B"/>'
        '<circle cx="17.5" cy="44" r="1.7" fill="#20402F"/><circle cx="46.5" cy="44" r="1.7" fill="#20402F"/>'
        '<circle cx="18.2" cy="34" r="1.7" fill="#20402F"/><circle cx="45.8" cy="34" r="1.7" fill="#20402F"/>'
        '<circle cx="22.6" cy="24.5" r="1.7" fill="#20402F"/><circle cx="41.4" cy="24.5" r="1.7" fill="#20402F"/></svg>')

HOOF = ('<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3c-5 0-8.4 3.6-8.4 8.6 0 4.6 2 7 2 10.4 0 2.6-1.6 3.4-1.6 5.2C8 28.7 9.2 29.6 11 29.6s3-1 3-2.8c0-2.6-1-4-1-6.6 0-3.2 1.4-4.8 3-4.8s3 1.6 3 4.8c0 2.6-1 4-1 6.6 0 1.8 1.2 2.8 3 2.8s3-.9 3-2.4c0-1.8-1.6-2.6-1.6-5.2 0-3.4 2-5.8 2-10.4C24.4 6.6 21 3 16 3Z"/></svg>')

IC = {
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H8v3h2v7h3v-7h2.5l.5-3H13v-2c0-.6.4-1 1-1Z"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5l-8-3Z"/></svg>',
 "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 4 13c0-6 6-10 16-10 0 10-4 16-9 17Z"/><path d="M8 16c2-4 5-6 9-7"/></svg>',
 "map": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 4-6 2v14l6-2 6 2 6-2V4l-6 2-6-2Z"/><path d="M9 4v14M15 6v14"/></svg>',
}

# ----------------------------------------------------------------- elrendezés
def layout(slug, title, desc, body, jsonld="", crumb=None, head_extra=""):
    nav_items = ""
    for href, label in NAV:
        cur = ' aria-current="page"' if href == slug else ""
        nav_items += '\n        <li><a href="%s"%s>%s</a></li>' % (href, cur, label)
    nav_items += ('\n        <li><a class="btn btn--primary" href="kapcsolat.html">'
                  'Hogyan találsz ide?</a></li>')

    foot_nav = "".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in NAV)
    foot_legal = "".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in LEGAL)
    legal_inline = "".join('<a href="%s">%s</a>' % (h, l) for h, l in LEGAL)

    return """<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="{site}">
<meta name="theme-color" content="#20402F">
<link rel="canonical" href="{base}/{slug}">
<meta property="og:type" content="website">
<meta property="og:locale" content="hu_HU">
<meta property="og:site_name" content="{site}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{base}/{slug}">
<meta property="og:image" content="{base}/assets/img/og-kep.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/favicon.svg">
<link rel="preload" href="assets/fonts/lora-600.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="assets/fonts/poppins-400.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
{head_extra}{jsonld}
</head>
<body>
<a class="skip" href="#tartalom">Ugrás a tartalomra</a>
<div class="scrollbar" aria-hidden="true"></div>

<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="{site} — főoldal">
      {shoe}
      <span class="bt"><b>Horse-Play</b><span>Lovas Sportegyesület</span></span>
    </a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="fomenu" aria-label="Menü megnyitása">
      <span></span><span></span><span></span>
    </button>
    <nav aria-label="Fő navigáció">
      <ul class="nav-links" id="fomenu">{nav_items}
      </ul>
    </nav>
    <div class="nav-cta"><a class="btn btn--primary" href="kapcsolat.html">Hogyan találsz ide?</a></div>
  </div>
</header>

<main id="tartalom">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="index.html">{shoe}<span class="bt"><b>Horse-Play</b><span>Lovas Sportegyesület</span></span></a>
        <p>Családias lovarda Botykapeterden, a Zselic peremén. Gyerekeknek és felnőtteknek egyaránt.</p>
        <div class="social">
          <a href="{fb}" target="_blank" rel="noopener noreferrer" aria-label="Facebook-oldalunk (új lapon nyílik)">{ic_fb}</a>
          <a href="{maps_dir}" target="_blank" rel="noopener noreferrer" aria-label="Útvonaltervezés Google Térképen (új lapon nyílik)">{ic_map}</a>
        </div>
      </div>
      <div><h2 class="foot-h">Oldalak</h2><ul>{foot_nav}</ul></div>
      <div><h2 class="foot-h">Jogi tudnivalók</h2><ul>{foot_legal}
        <li><a href="#" data-cookie-reopen>Sütibeállítások módosítása</a></li></ul></div>
      <div><h2 class="foot-h">Elérhetőség</h2><ul>
        <li>{cim}</li>
        <li>Telefon: {tel}</li>
        <li>E-mail: {email}</li>
      </ul></div>
    </div>
    <div class="foot-bottom">
      <p>© <span id="ev">2026</span> {site}. Minden jog fenntartva.</p>
      <nav aria-label="Jogi oldalak">{legal_inline}</nav>
    </div>
  </div>
</footer>

<!-- Süti / hozzájárulás sáv — hozzájárulásig semmilyen külső tartalom nem töltődik be -->
<section class="cookiebar" id="cookiebar" role="dialog" aria-modal="false"
         aria-labelledby="cookiebar-cim" aria-describedby="cookiebar-szoveg">
  <h2 id="cookiebar-cim">Sütik és beágyazott térkép</h2>
  <p id="cookiebar-szoveg">Ez a weboldal a működéséhez nem használ nyomkövető sütit, és nem gyűjt
    látogatói statisztikát. A <strong>Google Térkép</strong> beágyazása azonban a Google
    szervereihez kapcsolódik, ezért csak a hozzájárulásoddal töltjük be. Részletek a
    <a href="cookie-tajekoztato.html">süti-tájékoztatóban</a>.</p>
  <div class="cookie-toggle">
    <input type="checkbox" id="cookie-necessary" checked disabled>
    <label for="cookie-necessary"><strong>Működéshez szükséges</strong>
      <span>A választásod tárolása. Nem kapcsolható ki, és nem alkalmas azonosításra.</span></label>
  </div>
  <div class="cookie-toggle">
    <input type="checkbox" id="cookie-maps">
    <label for="cookie-maps"><strong>Google Térkép beágyazása</strong>
      <span>Adattovábbítás a Google Ireland Limited felé (IP-cím, eszközadatok).</span></label>
  </div>
  <div class="row">
    <button class="btn btn--primary" type="button" id="cookie-accept">Elfogadom</button>
    <button class="btn btn--outline" type="button" id="cookie-save">Kiválasztottak mentése</button>
    <button class="btn btn--outline" type="button" id="cookie-reject">Elutasítom</button>
  </div>
</section>

<script src="assets/js/main.js" defer></script>
</body>
</html>
""".format(title=title, desc=desc, base=BASE, slug=slug, site=SITE, shoe=SHOE,
           nav_items=nav_items, foot_nav=foot_nav, foot_legal=foot_legal,
           legal_inline=legal_inline, fb=FB, maps_dir=MAPS_DIR, ic_fb=IC["fb"],
           ic_map=IC["map"], cim=CIM, tel=TEL, email=EMAIL, body=body,
           jsonld=jsonld, head_extra=head_extra)


def page_head(h1, lead, crumb):
    items = '<li><a href="index.html">Főoldal</a></li><li aria-hidden="true">›</li><li>%s</li>' % crumb
    return """<section class="page-head">
  <div class="wrap">
    <ol class="crumbs">%s</ol>
    <h1>%s</h1>
    <p>%s</p>
  </div>
  <svg class="hero-wave" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true">
    <path d="M0 54c150-34 280 22 430 14s250-46 400-32 240 52 380 40 230-30 230-30V90H0Z" fill="#F7F2E4"/>
  </svg>
</section>""" % (items, h1, lead)


def cta_band():
    return """<section class="section"><div class="wrap">
  <div class="cta-band" data-reveal>
    <h2>Gyere el, nézz körül</h2>
    <p>Nem foglalunk online és nem kérünk előleget. Hívj minket vagy írj egy üzenetet,
       és megbeszéljük, mikor tudsz kijönni.</p>
    <p class="mt-24"><a class="btn btn--primary" href="kapcsolat.html">Elérhetőségek és térkép %s</a></p>
  </div>
</div></section>""" % IC["arrow"]


LOVAK = [
 ("lo-1.jpg", "Rigó", "Magyar sportló · 14 éves",
  "A lovarda nagy öregje. Türelmes és kiszámítható — a legtöbb kezdő vele ül először nyeregbe.",
  ["Kezdőknek", "Higgadt"]),
 ("lo-2.jpg", "Csillag", "Kisbéri félvér · 9 éves",
  "Élénk, figyelmes kanca. Haladóknak igazi élmény, mert a legkisebb jelzésre is azonnal reagál.",
  ["Haladóknak", "Élénk"]),
 ("lo-3.jpg", "Manó", "Póni · 11 éves",
  "A gyerekek kedvence. Alacsony, barátságos, és pontosan tudja, mikor kell nagyon óvatosnak lennie.",
  ["Gyerekeknek", "Barátságos"]),
 ("lo-4.jpg", "Szellő", "Magyar félvér · 12 éves",
  "Kiegyensúlyozott, jó mozgású ló. Terepen otthonosan mozog, hosszabb kilovaglásokhoz is ideális.",
  ["Terepre", "Kitartó"]),
 ("lo-5.jpg", "Pletyka", "Póni · 8 éves",
  "Kíváncsi és társaságkedvelő. Imádja, ha ápolják, ezért a legkisebbek szívesen barátkoznak vele.",
  ["Gyerekeknek", "Kíváncsi"]),
 ("lo-6.jpg", "Bátor", "Magyar sportló · 10 éves",
  "Nyugodt természetű herélt, aki a bizonytalanabb lovasokat is megnyugtatja a nyeregben.",
  ["Kezdőknek", "Nyugodt"]),
]


def horse_card(img, name, meta, txt, tags, delay=0):
    t = "".join("<li>%s</li>" % x for x in tags)
    return """<article class="horse" data-reveal data-delay="%d">
      <div class="horse-img"><img src="assets/img/%s" alt="%s, a lovarda lova"
        width="1000" height="750" loading="lazy" decoding="async"></div>
      <div class="horse-body">
        <h3>%s</h3>
        <p class="horse-meta">%s</p>
        <p>%s</p>
        <ul class="tags">%s</ul>
      </div>
    </article>""" % (delay, img, name, name, meta, txt, t)


# ============================================================== 1. FŐOLDAL
def build_index():
    jsonld = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SportsActivityLocation",
  "name": "Horse-Play Lovas Sportegyesület",
  "alternateName": "Horse-Play LSE",
  "description": "Családias lovarda és lovas sportegyesület Botykapeterden, Baranya vármegyében. Lovasoktatás, séta- és tereplovaglás gyerekeknek és felnőtteknek.",
  "url": "%s/",
  "image": "%s/assets/img/og-kep.jpg",
  "sameAs": ["%s"],
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[KITÖLTENDŐ: utca, házszám]",
    "addressLocality": "Botykapeterd",
    "postalCode": "7911",
    "addressRegion": "Baranya",
    "addressCountry": "HU"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": %s, "longitude": %s },
  "telephone": "[KITÖLTENDŐ: telefonszám]",
  "email": "[KITÖLTENDŐ: e-mail cím]",
  "areaServed": "Baranya vármegye, Szigetvár és környéke",
  "knowsLanguage": "hu"
}
</script>""" % (BASE, BASE, FB, LAT, LON)

    services = [
        ("01", "Lovasoktatás",
         "Egyéni és kiscsoportos órák minden korosztálynak. Kezdőknek vezetőszáron, "
         "saját tempóban, türelmes lovakkal — nálunk nincs stopper."),
        ("02", "Séta- és tereplovaglás",
         "Kísért séta a lovardán belül a legkisebbeknek, haladóknak pedig kilovaglás "
         "a környék erdei útjain, a Zselic peremén."),
        ("03", "Ismerkedés a lovakkal",
         "Lóápolás, etetés, felszerszámozás oktató kíséretében — azoknak is, "
         "akik még nem szeretnének nyeregbe ülni."),
    ]
    scards = ""
    for i, (n, h, p) in enumerate(services):
        scards += """<article class="card" data-reveal data-delay="%d">
        <div class="card-num">%s</div><h3>%s</h3><p>%s</p></article>\n      """ % (i + 1, n, h, p)

    horses = "".join(horse_card(*LOVAK[i], delay=i + 1) for i in range(3))

    marquee_items = ["Lovasoktatás", "Sétalovaglás", "Tereplovaglás", "Lóápolás",
                     "Gyerekbarát", "Türelmes lovak", "Zselic"]
    one = "".join('<span>%s</span><i>◆</i>' % m for m in marquee_items)

    body = """
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="badge">%s Botykapeterd · Szigetvár mellett</p>
      <h1>Gyere, ismerd meg a <em>lovainkat</em>.</h1>
      <p class="hero-lead">Családias lovarda, ahol a gyerek első vezetőszáras körétől a felnőtt
        tereplovaglásig mindenkinek jut idő és türelem. Nem versenyistálló vagyunk —
        itt a ló és az ember kapcsolata a lényeg.</p>
      <div class="hero-cta">
        <a class="btn btn--primary" href="lovaink.html">Nézd meg a lovakat %s</a>
        <a class="btn btn--ghost" href="kapcsolat.html">Hogyan találsz ide?</a>
      </div>
    </div>
    <div class="hero-media">
      <div class="arch" data-parallax>
        <img src="assets/img/hero.jpg" alt="Lovas a Horse-Play lovardában, Botykapeterden"
             width="1000" height="1060" fetchpriority="high" decoding="async">
      </div>
      <span class="hoof hoof--1" aria-hidden="true">%s</span>
      <span class="hoof hoof--2" aria-hidden="true">%s</span>
      <span class="hoof hoof--3" aria-hidden="true">%s</span>
    </div>
  </div>
  <svg class="hero-wave" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true">
    <path d="M0 54c150-34 280 22 430 14s250-46 400-32 240 52 380 40 230-30 230-30V90H0Z" fill="#F7F2E4"/>
  </svg>
</section>

<div class="wrap">
  <div class="chips">
    <span class="chip">%s Kezdőknek vezetőszáron</span>
    <span class="chip">%s Kis létszámú csoportok</span>
    <span class="chip">%s Védősisak biztosítva</span>
    <span class="chip">%s Nyugodt, zöld környezet</span>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <div class="shead" data-reveal>
      <span class="eyebrow">Amit kínálunk</span>
      <h2>Három út a nyeregbe</h2>
      <p>Mindenkit ott fogadunk, ahol éppen tart. A cél az, hogy jól érezd magad a ló mellett —
         a többi jön magától.</p>
    </div>
    <div class="grid grid--3">
      %s
    </div>
    <p class="center mt-38" data-reveal>
      <a class="btn btn--outline" href="szolgaltatasok.html">Részletes leírás %s</a></p>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track"><div>%s</div><div>%s</div></div>
</div>

<section class="section section--white">
  <div class="wrap split">
    <div class="split-media" data-reveal>
      <img src="assets/img/rolunk-1.jpg" alt="A Horse-Play lovarda karámja Botykapeterden"
           width="1200" height="960" loading="lazy" decoding="async">
    </div>
    <div data-reveal data-delay="1">
      <span class="eyebrow">Az egyesületről</span>
      <h2>Nem istálló. Közösség.</h2>
      <p>A Horse-Play Lovas Sportegyesület Botykapeterden működik, Szigetvártól néhány percre.
         Nálunk nincs versenykényszer: a legkisebbek vezetőszáron kezdenek, a felnőttek pedig
         gyakran évek kihagyása után térnek vissza a nyeregbe. Mindkettőre van időnk.</p>
      <ul class="checklist">
        <li>%s<div><strong>Kis létszámú, személyre szabott órák</strong> — mindenki a saját tempójában halad.</div></li>
        <li>%s<div><strong>Türelmes, jól ismert lovak</strong> minden tudásszinthez.</div></li>
        <li>%s<div><strong>Biztonság elsőként</strong> — védősisak a lovardában is elérhető.</div></li>
      </ul>
      <p class="mt-28"><a class="btn btn--outline" href="rolunk.html">Bővebben rólunk %s</a></p>
    </div>
  </div>
</section>

<section class="section section--forest">
  <div class="wrap">
    <div class="shead" data-reveal>
      <span class="eyebrow">Lovaink</span>
      <h2>Ismerd meg a csapatot</h2>
      <p>Mindegyiküknek megvan a maga természete. Az első alkalommal együtt találjuk meg,
         melyikük illik hozzád.</p>
    </div>
    <div class="grid grid--3">%s</div>
    <p class="center mt-40" data-reveal>
      <a class="btn btn--primary" href="lovaink.html">Az összes lovunk %s</a></p>
  </div>
</section>

<section class="section section--cream2">
  <div class="wrap">
    <div class="shead" data-reveal>
      <span class="eyebrow">Néhány szám</span>
      <h2>Rólunk röviden</h2>
    </div>
    <div class="stats" data-reveal>
      <div class="stat"><b data-count="12">12</b><span>Lovunk</span></div>
      <div class="stat"><b data-count="4" data-suffix="+">4+</b><span>Éves kortól</span></div>
      <div class="stat"><b data-count="1" data-suffix=" fő">1 fő</b><span>Kezdőknek oktató</span></div>
      <div class="stat"><b data-count="100" data-suffix="%%">100%%</b><span>Szabad levegő</span></div>
    </div>
    <p class="center mt-26 small muted-txt">
      %s</p>
  </div>
</section>

%s
""" % (IC["pin"], IC["arrow"], HOOF, HOOF, HOOF,
       IC["check"], IC["users"], IC["shield"], IC["leaf"],
       scards, IC["arrow"], one, one,
       IC["check"], IC["check"], IC["shield"], IC["arrow"],
       horses, IC["arrow"],
       F("[KITÖLTENDŐ: a fenti számokat pontosítsátok — lovak száma, oktatók száma, alapítás éve]"),
       cta_band())

    return layout("index.html",
        "Horse-Play Lovas Sportegyesület — lovarda Botykapeterden, Szigetvár mellett",
        "Családias lovarda és lovas sportegyesület Botykapeterden, Baranya vármegyében. "
        "Lovasoktatás, séta- és tereplovaglás gyerekeknek és felnőtteknek, türelmes lovakkal.",
        body, jsonld)


# ============================================================== 2. RÓLUNK
def build_rolunk():
    body = page_head("Rólunk",
        "Kik vagyunk, hol találsz minket, és mit várhatsz az első alkalomtól.", "Rólunk") + """
<section class="section">
  <div class="wrap split">
    <div data-reveal>
      <span class="eyebrow">Az egyesület</span>
      <h2>Egy lovarda a Zselic peremén</h2>
      <p>A Horse-Play Lovas Sportegyesület Botykapeterden működik, Baranya vármegyében,
         Szigetvártól néhány percnyi autóútra. A lovardánk nem versenyistálló:
         itt nincs stopper és nincs teljesítménykényszer.</p>
      <p>Azért vagyunk, hogy a lovaglás öröme mindenki számára elérhető legyen —
         a négyéves kisgyereknek, aki most ül először pónira, és a felnőttnek is,
         aki évtizedek után szeretne visszatérni a nyeregbe.</p>
      <p>%s</p>
    </div>
    <div class="split-media" data-reveal data-delay="1">
      <img src="assets/img/rolunk-1.jpg" alt="A Horse-Play lovarda karámja" width="1200" height="960"
           loading="lazy" decoding="async">
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="shead" data-reveal>
      <span class="eyebrow">Az első alkalom</span>
      <h2>Mire számíthatsz?</h2>
      <p>Sokan bizonytalanul érkeznek, mert még sosem voltak lovarda közelében.
         Ez teljesen rendben van — így szokott kezdődni.</p>
    </div>
    <div class="grid grid--4">
      <article class="card" data-reveal data-delay="1"><div class="card-num">01</div>
        <h3>Megbeszéljük</h3><p>Telefonon vagy e-mailben egyeztetünk egy időpontot. Elmondod,
        kinek és milyen tapasztalattal jöttök, mi pedig javaslunk egy lovat.</p></article>
      <article class="card" data-reveal data-delay="2"><div class="card-num">02</div>
        <h3>Ismerkedés</h3><p>Először nem nyeregbe ülünk, hanem a ló mellé állunk:
        megsimogatod, megismerkedtek. Ez a legfontosabb lépés.</p></article>
      <article class="card" data-reveal data-delay="3"><div class="card-num">03</div>
        <h3>Felkészülés</h3><p>Védősisakot kapsz, átbeszéljük a legfontosabb biztonsági
        tudnivalókat, és felszerszámozzuk a lovat — együtt.</p></article>
      <article class="card" data-reveal data-delay="4"><div class="card-num">04</div>
        <h3>Nyeregben</h3><p>Kezdőknek vezetőszáron, a karámban. Onnantól már csak rajtad múlik,
        milyen tempóban haladtok tovább.</p></article>
    </div>
  </div>
</section>

<section class="section section--forest">
  <div class="wrap split split--rev">
    <div class="split-media" data-reveal>
      <img src="assets/img/rolunk-2.jpg" alt="Ló és lovas a lovarda karámjában" width="1200" height="960"
           loading="lazy" decoding="async">
    </div>
    <div data-reveal data-delay="1">
      <span class="eyebrow">Biztonság</span>
      <h2>Amit komolyan veszünk</h2>
      <p>A ló nagy testű, saját akarattal rendelkező állat. Nálunk minden alkalom
         a biztonsági tudnivalók átbeszélésével kezdődik, és senki nem ül olyan lóra,
         amelyik nem illik a tudásszintjéhez.</p>
      <ul class="checklist">
        <li>%s<div>Védősisak viselése kötelező, a lovardában is elérhető.</div></li>
        <li>%s<div>Kezdő lovas kizárólag oktató jelenlétében ül nyeregbe.</div></li>
        <li>%s<div>Zárt cipő és hosszú nadrág szükséges — ezt kérjük, hozd magaddal.</div></li>
        <li>%s<div>14 év alatti gyermek csak szülői kísérettel vehet részt.</div></li>
      </ul>
      <div class="note note--onforest">
        <p class="m-0"><strong>Fontos:</strong> a lovaglás sporttevékenység,
        amely baleseti kockázattal jár. A részvétel saját felelősségre történik.
        %s</p>
      </div>
    </div>
  </div>
</section>
""" % (F("[KITÖLTENDŐ: az egyesület alapításának éve és rövid története]"),
       IC["check"], IC["check"], IC["check"], IC["check"],
       F("[KITÖLTENDŐ: van-e felelősségbiztosítás / részvételi nyilatkozat]")) + cta_band()

    return layout("rolunk.html", "Rólunk — %s" % SITE,
        "Ismerd meg a Horse-Play Lovas Sportegyesületet: kik vagyunk, hol találsz minket "
        "Botykapeterden, és mire számíthatsz az első alkalommal.", body, crumb="Rólunk")


# ============================================================== 3. SZOLGÁLTATÁSOK
def build_szolg():
    blocks = [
        ("Lovasoktatás", "szolgaltatas-1.jpg", False,
         ["Egyéni és kiscsoportos órák minden korosztálynak, a teljesen kezdőktől a haladókig.",
          "A kezdők vezetőszáron, zárt karámban indulnak — a tempót mindig a lovas szabja meg, nem az óra."],
         ["Egyéni óra oktatóval", "Kiscsoportos óra (max. 3 fő)", "Gyermekóra 4 éves kortól",
          "Visszatérőknek felfrissítő alkalom"]),
        ("Séta- és tereplovaglás", "rolunk-2.jpg", True,
         ["A legkisebbeknek kísért sétalovaglás a lovardán belül — a szülő végig a ló mellett sétálhat.",
          "Haladóknak kilovaglás a környék erdei és mezei útjain, oktató kíséretében."],
         ["Kísért sétalovaglás a karámban", "Rövid kilovaglás a lovarda körül",
          "Hosszabb tereplovaglás haladóknak", "Fotózási lehetőség a lovakkal"]),
        ("Ismerkedés a lovakkal", "rolunk-1.jpg", False,
         ["Nem mindenki akar rögtön nyeregbe ülni — és ez teljesen rendben van.",
          "Lóápolás, etetés, felszerszámozás oktató kíséretében: sokszor ez a leghasznosabb első lépés."],
         ["Lóápolás és kefélés", "Etetés felügyelettel", "A felszerelés megismerése",
          "Alapvető lovas ismeretek"]),
    ]
    out = ""
    for i, (title, img, rev, paras, items) in enumerate(blocks):
        ps = "".join("<p>%s</p>" % p for p in paras)
        lis = "".join("<li>%s<div>%s</div></li>" % (IC["check"], x) for x in items)
        cls = "section section--white" if i % 2 else "section"
        rc = " split--rev" if rev else ""
        out += """
<section class="%s">
  <div class="wrap split%s">
    <div class="split-media" data-reveal>
      <img src="assets/img/%s" alt="%s a Horse-Play lovardában" width="1200" height="960"
           loading="lazy" decoding="async">
    </div>
    <div data-reveal data-delay="1">
      <span class="eyebrow">0%d</span>
      <h2>%s</h2>
      %s
      <ul class="checklist">%s</ul>
    </div>
  </div>
</section>""" % (cls, rc, img, title, i + 1, title, ps, lis)

    prices = """
<section class="section section--cream2">
  <div class="wrap narrow">
    <div class="shead" data-reveal>
      <span class="eyebrow">Jó tudni</span>
      <h2>Árak és időpontok</h2>
      <p>Az árakat és a szabad időpontokat telefonon vagy e-mailben egyeztetjük,
         mert minden alkalom más — más ló, más létszám, más hosszúság.</p>
    </div>
    <div class="note" data-reveal>
      <p><strong>Ez a weboldal nem foglalási felület.</strong> Nem kérünk online fizetést és nem
         tárolunk foglalási adatokat: egyszerűen hívj minket vagy írj egy e-mailt, és megbeszéljük
         a részleteket.</p>
      <p class="mb-0">%s</p>
    </div>
    <div class="grid grid--2 mt-34">
      <article class="card" data-reveal data-delay="1"><h3>Mit hozz magaddal?</h3>
        <ul class="checklist">
          <li>%s<div>Zárt, kemény talpú cipő (nem szandál).</div></li>
          <li>%s<div>Hosszú nadrág — a rövidnadrág feltöri a lábat.</div></li>
          <li>%s<div>Az időjárásnak megfelelő réteges öltözet.</div></li>
          <li>%s<div>Védősisakot mi biztosítunk, de sajátot is hozhatsz.</div></li>
        </ul></article>
      <article class="card" data-reveal data-delay="2"><h3>Jó, ha tudod</h3>
        <ul class="checklist">
          <li>%s<div>Előzetes egyeztetés nélkül sajnos nem tudunk fogadni.</div></li>
          <li>%s<div>Tartós esőben és viharban nem lovagolunk.</div></li>
          <li>%s<div>14 év alatt szülői kíséret szükséges.</div></li>
          <li>%s<div>A lovakat etetni csak engedéllyel szabad.</div></li>
        </ul></article>
    </div>
  </div>
</section>""" % (F("[KITÖLTENDŐ: árak, alkalmak hossza, nyitvatartás / egyeztethető időpontok]"),
                 IC["check"], IC["check"], IC["check"], IC["check"],
                 IC["check"], IC["check"], IC["check"], IC["check"])

    body = page_head("Szolgáltatások",
        "Lovasoktatás, séta- és tereplovaglás, valamint ismerkedés a lovakkal — "
        "gyerekeknek és felnőtteknek egyaránt.", "Szolgáltatások") + out + prices + cta_band()

    return layout("szolgaltatasok.html", "Szolgáltatások — %s" % SITE,
        "Lovasoktatás, sétalovaglás, tereplovaglás és lóápolás Botykapeterden. "
        "Kezdőknek vezetőszáron, haladóknak terepen — minden korosztálynak.", body)


# ============================================================== 4. LOVAINK
def build_lovaink():
    cards = "".join(horse_card(*LOVAK[i], delay=(i % 3) + 1) for i in range(len(LOVAK)))
    body = page_head("Lovaink",
        "Mindegyiküknek megvan a maga természete. Az első alkalommal együtt találjuk meg, "
        "melyikük illik hozzád.", "Lovaink") + """
<section class="section">
  <div class="wrap">
    <h2 class="visually-hidden">Lovaink egyesével</h2>
    <div class="grid grid--3">%s</div>
    <div class="note mt-40" data-reveal>
      <p class="mb-0"><strong>Figyelem:</strong> %s</p>
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap narrow">
    <div class="shead" data-reveal>
      <span class="eyebrow">Hogyan válasszunk?</span>
      <h2>Melyik ló való neked?</h2>
      <p>Nem kell előre eldöntened. Az első beszélgetésen kiderül, mire vágysz,
         és mi javaslunk egy lovat — ha nem passzol, kipróbálunk másikat.</p>
    </div>
    <ul class="checklist" data-reveal>
      <li>%s<div><strong>Teljesen kezdő vagy?</strong> Higgadt, kiszámítható lóval indulunk,
        vezetőszáron, zárt karámban.</div></li>
      <li>%s<div><strong>Gyereknek keresel lovat?</strong> A pónik alacsonyabbak, könnyebb
        melléjük állni, és hozzászoktak a gyerekekhez.</div></li>
      <li>%s<div><strong>Régen lovagoltál?</strong> Egy felfrissítő alkalommal kiderül,
        mennyi maradt meg — ez általában több, mint gondolnád.</div></li>
      <li>%s<div><strong>Haladó vagy?</strong> Élénkebb, érzékenyebb lovaink terepen is
        élményt adnak.</div></li>
    </ul>
  </div>
</section>
""" % (cards,
       F("[KITÖLTENDŐ: a lovak nevei, fajtái, életkora és jellemzése — a fentiek példaszövegek]"),
       IC["check"], IC["check"], IC["check"], IC["check"]) + cta_band()

    return layout("lovaink.html", "Lovaink — %s" % SITE,
        "Ismerd meg a Horse-Play lovarda lovait: kezdőbarát, higgadt lovak, gyerekeknek való pónik "
        "és haladóknak való élénkebb lovak Botykapeterden.", body)


# ============================================================== 5. GALÉRIA
def build_galeria():
    caps = ["A lovarda karámja", "Reggeli etetés", "Vezetőszáras óra kezdőknek",
            "Lóápolás a boxok előtt", "Kilovaglás a mezei úton", "Póni a legkisebbeknek",
            "Nyugalom a legelőn", "Felszerszámozás", "Naplemente a lovarda felett"]
    items = ""
    for i, c in enumerate(caps, 1):
        items += """<button type="button" data-full="assets/img/galeria-%d.jpg"
        data-caption="%s" aria-label="Kép nagyítása: %s">
        <img src="assets/img/galeria-%d.jpg" alt="%s" width="1400" height="1050"
             loading="lazy" decoding="async"></button>\n      """ % (i, c, c, i, c)

    body = page_head("Galéria",
        "Pillanatképek a lovardából. Kattints a képekre a nagyításhoz.", "Galéria") + """
<section class="section">
  <div class="wrap">
    <div class="gallery" data-reveal>
      %s
    </div>
    <div class="note mt-36" data-reveal>
      <p class="mb-0"><strong>Képek cseréje:</strong> %s</p>
    </div>
  </div>
</section>

<div class="lightbox" id="lightbox" aria-hidden="true" role="dialog" aria-modal="true"
     aria-label="Képnagyító">
  <button class="lb-btn lb-close" type="button" aria-label="Bezárás">
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"
      stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
  <button class="lb-btn lb-prev" type="button" aria-label="Előző kép">
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"
      stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg></button>
  <button class="lb-btn lb-next" type="button" aria-label="Következő kép">
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"
      stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg></button>
  <figure class="m-0">
    <img src="assets/img/galeria-1.jpg" alt="">
    <figcaption></figcaption>
  </figure>
</div>
""" % (items, F("[KITÖLTENDŐ: cseréljétek le a képeket az assets/img/galeria-1.jpg … galeria-9.jpg "
                "fájlokra — a méret és a fájlnév maradjon ugyanaz]")) + cta_band()

    return layout("galeria.html", "Galéria — %s" % SITE,
        "Képek a Horse-Play lovardáról Botykapeterden: karám, lovak, oktatás és kilovaglás.", body)


# ============================================================== 6. KAPCSOLAT
def build_kapcsolat():
    body = page_head("Kapcsolat",
        "Ez egy bemutatkozó oldal, nem foglalási felület — hívj minket vagy írj egy e-mailt, "
        "és megbeszéljük a részleteket.", "Kapcsolat") + """
<section class="section">
  <div class="wrap contact-grid">
    <div data-reveal>
      <span class="eyebrow">Elérhetőségeink</span>
      <h2>Így érsz el minket</h2>
      <ul class="contact-list">
        <li><span class="contact-ico">%s</span><div><b>Cím</b>
          <span>%s</span></div></li>
        <li><span class="contact-ico">%s</span><div><b>Telefon</b>
          <span>%s</span></div></li>
        <li><span class="contact-ico">%s</span><div><b>E-mail</b>
          <span>%s</span></div></li>
        <li><span class="contact-ico">%s</span><div><b>Mikor keress?</b>
          <span>%s</span></div></li>
        <li><span class="contact-ico">%s</span><div><b>Facebook</b>
          <a href="%s" target="_blank" rel="noopener noreferrer">Horse-Play Lovarda
            <span class="visually-hidden">(új lapon nyílik)</span></a></div></li>
      </ul>
      <div class="note">
        <p class="mb-0">Kérjük, <strong>előzetes egyeztetés nélkül ne érkezz</strong>,
        mert a lovak napirendje kötött, és így nem tudunk téged megfelelően fogadni.</p>
      </div>
    </div>

    <div data-reveal data-delay="1">
      <span class="eyebrow">Hol vagyunk?</span>
      <h2>Térkép és megközelítés</h2>
      <div class="map-box" data-map-src="%s"
           data-map-title="A Horse-Play lovarda helye a Google Térképen">
        <div class="map-consent">
          <div class="inner">
            %s
            <h3>A térkép betöltéséhez hozzájárulás szükséges</h3>
            <p>A Google Térkép beágyazása kapcsolatot létesít a Google szervereivel, és
               továbbítja az IP-címedet. Ezért csak akkor töltjük be, ha ehhez hozzájárulsz.</p>
            <p><button class="btn btn--primary" type="button" data-map-consent>
              Térkép betöltése</button></p>
            <p class="mb-0 xsmall">
              <a href="%s" target="_blank" rel="noopener noreferrer">Vagy nyisd meg
              külön lapon a Google Térképen</a> ·
              <a href="cookie-tajekoztato.html">Süti-tájékoztató</a></p>
          </div>
        </div>
      </div>
      <ul class="checklist mt-24">
        <li>%s<div><strong>Autóval:</strong> Szigetvár felől %s</div></li>
        <li>%s<div><strong>GPS-koordináta:</strong> %s, %s</div></li>
        <li>%s<div><strong>Parkolás:</strong> %s</div></li>
      </ul>
    </div>
  </div>
</section>
""" % (IC["pin"], CIM, IC["phone"], TEL, IC["mail"], EMAIL, IC["clock"],
       F("[KITÖLTENDŐ: mikor vagytok elérhetők telefonon]"),
       IC["fb"], FB, MAPS_EMBED, IC["map"], MAPS_DIR,
       IC["check"], F("[KITÖLTENDŐ: útvonal leírása]"),
       IC["check"], LAT, LON,
       IC["check"], F("[KITÖLTENDŐ: parkolási lehetőség]"))

    return layout("kapcsolat.html", "Kapcsolat — %s" % SITE,
        "A Horse-Play Lovas Sportegyesület elérhetőségei és a lovarda pontos helye "
        "Botykapeterden, Baranya vármegyében. Térkép és megközelítés.", body)


# ============================================================== 7. IMPRESSZUM
def build_impresszum():
    body = page_head("Impresszum",
        "A weboldal üzemeltetőjének adatai az elektronikus kereskedelemről szóló "
        "2001. évi CVIII. törvény 4. §-a alapján.", "Impresszum") + """
<section class="section"><div class="wrap prose">
  <h2>A weboldal üzemeltetője</h2>
  <table>
    <tr><th>Szervezet neve</th><td>Horse-Play Lovas Sportegyesület</td></tr>
    <tr><th>Rövidített név</th><td>Horse-Play LSE</td></tr>
    <tr><th>Székhely</th><td>%s</td></tr>
    <tr><th>Nyilvántartó bíróság</th><td>%s</td></tr>
    <tr><th>Nyilvántartási szám</th><td>%s</td></tr>
    <tr><th>Adószám</th><td>%s</td></tr>
    <tr><th>Képviselő</th><td>%s</td></tr>
    <tr><th>E-mail</th><td>%s</td></tr>
    <tr><th>Telefon</th><td>%s</td></tr>
  </table>

  <h2>Tárhelyszolgáltató</h2>
  <table>
    <tr><th>Név</th><td>MEDIACENTER HUNGARY Informatikai, Szolgáltató és Üzemeltető Kft.
      (MediaCenter Hungary Kft.)</td></tr>
    <tr><th>Székhely</th><td>6000 Kecskemét, Erkel Ferenc utca 5.</td></tr>
    <tr><th>Cégjegyzékszám</th><td>03-09-114492</td></tr>
    <tr><th>Adószám</th><td>13922546-2-03</td></tr>
    <tr><th>Telefon</th><td>+36 21 201 0505</td></tr>
    <tr><th>Weboldal</th><td><a href="https://www.mediacenter.hu" target="_blank"
      rel="noopener noreferrer">www.mediacenter.hu</a></td></tr>
  </table>
  <p class="note">A domainnév regisztrációját és a tárhelyszolgáltatást egyaránt a
     MediaCenter Hungary Kft. biztosítja.</p>

  <h2>A weboldal célja és jellege</h2>
  <p>Ez a weboldal az egyesület tevékenységének <strong>bemutatására</strong> szolgál.
     A weboldalon keresztül <strong>nem lehet online foglalni, rendelni vagy fizetni</strong>,
     így az oldal nem minősül a fogyasztó és a vállalkozás közötti szerződések részletes
     szabályairól szóló 45/2014. (II. 26.) Korm. rendelet szerinti webáruháznak.
     A szolgáltatások igénybevétele minden esetben előzetes, személyes vagy telefonos
     egyeztetés alapján történik.</p>

  <h2>Szerzői jogok</h2>
  <p>A weboldalon megjelenő szövegek, fényképek, grafikai elemek és a weboldal szerkezete
     a szerzői jogról szóló 1999. évi LXXVI. törvény védelme alatt állnak. Ezek felhasználása,
     másolása, terjesztése vagy átdolgozása kizárólag az üzemeltető előzetes írásbeli
     hozzájárulásával lehetséges. A weboldalra mutató hivatkozás (link) elhelyezése
     szabadon megengedett.</p>

  <h2>Felelősség</h2>
  <p>Az üzemeltető mindent megtesz azért, hogy a weboldalon közölt információk pontosak és
     naprakészek legyenek, de az esetleges elírásokért, illetve az információk felhasználásából
     eredő károkért felelősséget nem vállal. A weboldalon szereplő árak, időpontok és leírások
     tájékoztató jellegűek, és nem minősülnek a Polgári Törvénykönyv szerinti ajánlattételnek.</p>
  <p>A weboldalról külső oldalakra mutató hivatkozások tartalmáért az üzemeltető nem felel.</p>

  <h2>Panaszkezelés, jogorvoslat</h2>
  <p>Panaszával elsősorban közvetlenül az egyesülethez fordulhat a fenti elérhetőségeken.
     Ezen felül a lakóhelye szerint illetékes <strong>vármegyei békéltető testülethez</strong>,
     a területileg illetékes <strong>fogyasztóvédelmi hatósághoz</strong>, illetve
     <strong>bírósághoz</strong> is fordulhat.</p>

  <p class="updated">Utolsó frissítés: %s</p>
</div></section>
""" % (CIM,
       F("[KITÖLTENDŐ: pl. Pécsi Törvényszék]"),
       F("[KITÖLTENDŐ: nyilvántartási szám]"),
       F("[KITÖLTENDŐ: adószám]"),
       F("[KITÖLTENDŐ: elnök / képviselő neve]"),
       EMAIL, TEL, TODAY)

    return layout("impresszum.html", "Impresszum — %s" % SITE,
        "A Horse-Play Lovas Sportegyesület és a weboldal üzemeltetőjének hivatalos adatai.", body)


# ============================================================== 8. ADATKEZELÉS
def build_adat():
    body = page_head("Adatkezelési tájékoztató",
        "Hogyan kezeljük a személyes adatokat az általános adatvédelmi rendelet (GDPR) alapján.",
        "Adatkezelési tájékoztató") + """
<section class="section"><div class="wrap prose">
  <div class="note">
    <p class="mb-0"><strong>Röviden:</strong> ez a weboldal nem használ nyomkövető sütit,
    nem futtat látogatottság-mérőt, nincs rajta űrlap, és nem hoz létre felhasználói fiókot.
    Személyes adat gyakorlatilag csak akkor kerül hozzánk, ha te magad írsz vagy telefonálsz.</p>
  </div>

  <h2>1. Az adatkezelő</h2>
  <table>
    <tr><th>Adatkezelő</th><td>Horse-Play Lovas Sportegyesület</td></tr>
    <tr><th>Székhely</th><td>%s</td></tr>
    <tr><th>Nyilvántartási szám</th><td>%s</td></tr>
    <tr><th>E-mail</th><td>%s</td></tr>
    <tr><th>Telefon</th><td>%s</td></tr>
  </table>
  <p>Adatvédelmi tisztviselő kijelölésére az egyesület nem kötelezett, ezért ilyet nem alkalmaz.
     Adatvédelmi kérdéseivel a fenti elérhetőségeken fordulhat hozzánk.</p>

  <h2>2. Az irányadó jogszabályok</h2>
  <ul>
    <li>Az Európai Parlament és a Tanács (EU) 2016/679 rendelete (GDPR)</li>
    <li>2011. évi CXII. törvény az információs önrendelkezési jogról és az
        információszabadságról (Infotv.)</li>
    <li>2001. évi CVIII. törvény az elektronikus kereskedelmi szolgáltatásokról (Ekertv.)</li>
    <li>2003. évi C. törvény az elektronikus hírközlésről (Eht.)</li>
  </ul>

  <h2>3. Milyen adatokat kezelünk?</h2>

  <h3>3.1. Szervernaplók (technikai adatok)</h3>
  <table>
    <tr><th>Kezelt adatok</th><td>IP-cím, a lekérés időpontja, a megtekintett oldal címe,
      böngésző- és operációsrendszer-azonosító (user agent), hivatkozó oldal</td></tr>
    <tr><th>Az adatkezelés célja</th><td>A weboldal biztonságos és hibamentes működésének
      biztosítása, visszaélések és támadások kivizsgálása</td></tr>
    <tr><th>Jogalap</th><td>GDPR 6. cikk (1) f) pont — az adatkezelő jogos érdeke a
      szolgáltatás biztonságos üzemeltetéséhez</td></tr>
    <tr><th>Időtartam</th><td>%s</td></tr>
    <tr><th>Adatfeldolgozó</th><td>MediaCenter Hungary Kft. (tárhelyszolgáltató),
      6000 Kecskemét, Erkel Ferenc utca 5.</td></tr>
  </table>

  <h3>3.2. A sütibeállításod tárolása</h3>
  <table>
    <tr><th>Kezelt adatok</th><td>A hozzájárulási döntésed és annak időpontja, a böngésződ
      helyi tárolójában (localStorage), <em>hp_consent_v1</em> néven</td></tr>
    <tr><th>Az adatkezelés célja</th><td>Hogy ne kelljen minden oldalletöltésnél újra döntened</td></tr>
    <tr><th>Jogalap</th><td>GDPR 6. cikk (1) f) pont — jogos érdek, illetve a hozzájárulás
      igazolhatósága (GDPR 7. cikk (1))</td></tr>
    <tr><th>Időtartam</th><td>Amíg te magad nem törlöd; a böngésződben tárolódik,
      hozzánk nem kerül el</td></tr>
  </table>
  <p>Ez az adat nem alkalmas a személyed azonosítására, és nem hagyja el a saját eszközödet.</p>

  <h3>3.3. Kapcsolatfelvétel e-mailben vagy telefonon</h3>
  <table>
    <tr><th>Kezelt adatok</th><td>Név, e-mail cím vagy telefonszám, valamint minden más adat,
      amit az üzenetedben megadsz</td></tr>
    <tr><th>Az adatkezelés célja</th><td>A megkeresésed megválaszolása, időpont egyeztetése</td></tr>
    <tr><th>Jogalap</th><td>GDPR 6. cikk (1) b) pont — szerződéskötést megelőző lépések,
      illetve 6. cikk (1) f) pont — jogos érdek a kapcsolattartáshoz</td></tr>
    <tr><th>Időtartam</th><td>A megkeresés lezárását követő %s</td></tr>
  </table>
  <p>Kérjük, hogy e-mailben <strong>ne küldj</strong> egészségügyi adatot vagy más különleges
     adatot. Ha ilyet mégis megadsz, azt a válaszadást követően törüljük.</p>

  <h3>3.4. Fényképek a weboldalon és a Facebook-oldalunkon</h3>
  <p>Ha a lovardában készült fényképen felismerhető személy szerepel, a felvétel közzétételéhez
     az érintett (kiskorú esetén a törvényes képviselő) hozzájárulását kérjük
     (GDPR 6. cikk (1) a) pont; Ptk. 2:48. §). A hozzájárulás bármikor, indokolás nélkül
     visszavonható a fenti elérhetőségeken — ilyenkor a képet haladéktalanul eltávolítjuk.</p>

  <h2>4. Külső szolgáltatók, adattovábbítás</h2>

  <h3>4.1. Google Térkép</h3>
  <p>A Kapcsolat oldalon beágyazott Google Térkép <strong>csak a kifejezett hozzájárulásod után</strong>
     töltődik be. A betöltéskor a böngésződ közvetlenül a Google szervereihez kapcsolódik, és
     továbbítja többek között az IP-címedet, az eszközöd és a böngésződ adatait.</p>
  <table>
    <tr><th>Szolgáltató</th><td>Google Ireland Limited (Gordon House, Barrow Street, Dublin 4,
      Írország)</td></tr>
    <tr><th>Jogalap</th><td>GDPR 6. cikk (1) a) pont — a te hozzájárulásod</td></tr>
    <tr><th>Harmadik országba továbbítás</th><td>A Google adatokat továbbíthat az Amerikai
      Egyesült Államokba. A továbbítás jogalapja az Európai Bizottság EU–USA adatvédelmi
      keretrendszerre vonatkozó megfelelőségi határozata, illetve általános szerződési
      feltételek (SCC).</td></tr>
    <tr><th>További információ</th><td><a href="https://policies.google.com/privacy?hl=hu"
      target="_blank" rel="noopener noreferrer">Google adatvédelmi irányelvek</a></td></tr>
  </table>
  <p>A hozzájárulásodat bármikor visszavonhatod a
     <a href="#" data-cookie-reopen>sütibeállítások módosítása</a> hivatkozásra kattintva.
     A visszavonás nem érinti a visszavonás előtti adatkezelés jogszerűségét.</p>

  <h3>4.2. Facebook</h3>
  <p>A weboldalon a Facebook-oldalunkra csak egy egyszerű hivatkozás mutat — <strong>nincs
     beágyazott Facebook-tartalom vagy nyomkövető pixel</strong>, így pusztán a weboldal
     megtekintésével a Meta felé nem történik adattovábbítás. Ha rákattintasz a hivatkozásra,
     a Facebook saját adatkezelése lép életbe.</p>

  <h2>5. Automatizált döntéshozatal, profilalkotás</h2>
  <p>A weboldalon automatizált döntéshozatal és profilalkotás nem történik.</p>

  <h2>6. Adatbiztonság</h2>
  <p>A weboldal titkosított (HTTPS) kapcsolaton keresztül érhető el. A tárhelyszolgáltató
     szerverei zárt, védett szerverteremben üzemelnek. Az adatokhoz kizárólag az egyesület
     erre feljogosított képviselője fér hozzá.</p>

  <h2>7. Az érintett jogai</h2>
  <p>A GDPR alapján a következő jogok illetnek meg. Kérelmedre legkésőbb
     <strong>egy hónapon belül</strong> válaszolunk, díjmentesen.</p>
  <ul>
    <li><strong>Tájékoztatáshoz és hozzáféréshez való jog</strong> (GDPR 15. cikk) — megkérdezheted,
      kezelünk-e rólad adatot, és arról másolatot kérhetsz.</li>
    <li><strong>Helyesbítéshez való jog</strong> (16. cikk) — a pontatlan adat kijavítását kérheted.</li>
    <li><strong>Törléshez való jog</strong> (17. cikk) — az „elfeledtetéshez való jog”.</li>
    <li><strong>Az adatkezelés korlátozásához való jog</strong> (18. cikk).</li>
    <li><strong>Adathordozhatósághoz való jog</strong> (20. cikk).</li>
    <li><strong>Tiltakozáshoz való jog</strong> (21. cikk) — a jogos érdeken alapuló
      adatkezelés ellen bármikor tiltakozhatsz.</li>
    <li><strong>A hozzájárulás visszavonásának joga</strong> (7. cikk (3)) — bármikor,
      indokolás nélkül.</li>
  </ul>

  <h2>8. Jogorvoslati lehetőségek</h2>
  <p>Ha úgy érzed, hogy az adatkezelésünk sérti a jogaidat, kérjük, először fordulj hozzánk
     közvetlenül — a legtöbb kérdés így rendezhető a leggyorsabban.</p>
  <p>Panasszal a felügyeleti hatósághoz is fordulhatsz:</p>
  <table>
    <tr><th>Hatóság</th><td>Nemzeti Adatvédelmi és Információszabadság Hatóság (NAIH)</td></tr>
    <tr><th>Cím</th><td>1055 Budapest, Falk Miksa utca 9–11.</td></tr>
    <tr><th>Postacím</th><td>1363 Budapest, Pf. 9.</td></tr>
    <tr><th>Telefon</th><td>+36 1 391 1400</td></tr>
    <tr><th>E-mail</th><td>ugyfelszolgalat@naih.hu</td></tr>
    <tr><th>Weboldal</th><td><a href="https://naih.hu" target="_blank"
      rel="noopener noreferrer">naih.hu</a></td></tr>
  </table>
  <p>Jogaid megsértése esetén bírósághoz is fordulhatsz. A per — választásod szerint — a
     lakóhelyed vagy tartózkodási helyed szerinti törvényszék előtt is megindítható.</p>

  <h2>9. A tájékoztató módosítása</h2>
  <p>Fenntartjuk a jogot, hogy ezt a tájékoztatót egyoldalúan módosítsuk. A mindenkor hatályos
     változat ezen az oldalon érhető el.</p>

  <p class="updated">Hatályos: %s-tól. Utolsó frissítés: %s</p>
</div></section>
""" % (CIM, F("[KITÖLTENDŐ: nyilvántartási szám]"), EMAIL, TEL,
       F("[KITÖLTENDŐ: a tárhelyszolgáltató naplómegőrzési ideje, jellemzően 30 nap]"),
       F("[KITÖLTENDŐ: pl. 1 év]"), TODAY, TODAY)

    return layout("adatkezelesi-tajekoztato.html", "Adatkezelési tájékoztató — %s" % SITE,
        "A Horse-Play Lovas Sportegyesület weboldalának GDPR szerinti adatkezelési tájékoztatója.",
        body)


# ============================================================== 9. SÜTIK
def build_cookie():
    body = page_head("Süti- (cookie-) tájékoztató",
        "Milyen adatokat tárol a böngésződ, amikor ezt az oldalt nézed.",
        "Süti-tájékoztató") + """
<section class="section"><div class="wrap prose">
  <div class="note">
    <p class="mb-0"><strong>A lényeg:</strong> ez a weboldal <strong>nem használ
    nyomkövető sütit</strong>, nem futtat Google Analyticset vagy más látogatottság-mérőt,
    és nem használ reklámkövetőket. Alapállapotban egyetlen külső szolgáltató felé sem
    továbbítunk adatot.</p>
  </div>

  <h2>Mi az a süti?</h2>
  <p>A süti (cookie) egy kis adatfájl, amelyet a meglátogatott weboldal helyez el a böngésződben,
     hogy a következő látogatáskor felismerje azt. Hasonló célt szolgál a
     <em>localStorage</em> is, amely szintén a böngésződben tárol adatot — ez a weboldal ezt
     használja, sütik helyett.</p>

  <h2>Amit ez a weboldal tárol</h2>
  <table>
    <tr><th>Név</th><th>Típus</th><th>Cél</th><th>Élettartam</th></tr>
    <tr>
      <td><code>hp_consent_v1</code></td>
      <td>localStorage (nem süti)</td>
      <td>A sütibeállításokra vonatkozó döntésed megjegyzése, hogy ne kelljen minden
          oldalon újra választanod</td>
      <td>Amíg te magad nem törlöd</td>
    </tr>
  </table>
  <p>Ez a bejegyzés a te eszközödön marad, hozzánk nem jut el, és nem alkalmas
     a személyed azonosítására. Az elektronikus hírközlésről szóló törvény és a GDPR alapján
     a működéshez feltétlenül szükséges tárolás előzetes hozzájárulás nélkül is jogszerű.</p>

  <h2>Hozzájárulás alapján betöltődő tartalom</h2>
  <table>
    <tr><th>Szolgáltatás</th><th>Mikor tölt be?</th><th>Mit továbbít?</th></tr>
    <tr>
      <td>Google Térkép (Google Ireland Limited)</td>
      <td>Csak akkor, ha ehhez a süti-sávon vagy a térkép helyén lévő gombbal kifejezetten
          hozzájárulsz</td>
      <td>IP-cím, böngésző- és eszközadatok; a Google saját sütiket helyezhet el</td>
    </tr>
  </table>
  <p>A Google adatkezeléséről a
     <a href="https://policies.google.com/privacy?hl=hu" target="_blank"
     rel="noopener noreferrer">Google adatvédelmi irányelveiben</a> olvashatsz.</p>

  <h2>A döntésed módosítása</h2>
  <p>A beállításaidat bármikor megváltoztathatod:</p>
  <p><a class="btn btn--primary" href="#" data-cookie-reopen>Sütibeállítások módosítása</a></p>

  <h2>Sütik törlése a böngészőben</h2>
  <p>A tárolt adatokat a böngésződ beállításaiban is törölheted, illetve előre letilthatod
     a sütik elhelyezését:</p>
  <ul>
    <li><strong>Chrome:</strong> Beállítások → Adatvédelem és biztonság → Böngészési adatok törlése</li>
    <li><strong>Firefox:</strong> Beállítások → Adatvédelem és biztonság → Sütik és oldaladatok</li>
    <li><strong>Safari:</strong> Beállítások → Adatvédelem → Webhelyadatok kezelése</li>
    <li><strong>Edge:</strong> Beállítások → Cookie-k és webhelyengedélyek</li>
  </ul>
  <p>Felhívjuk a figyelmet, hogy a böngésző tárolójának törlése után a süti-sáv újra megjelenik.</p>

  <p>A személyes adatok kezeléséről részletesen az
     <a href="adatkezelesi-tajekoztato.html">adatkezelési tájékoztatóban</a> olvashatsz.</p>

  <p class="updated">Utolsó frissítés: %s</p>
</div></section>
""" % TODAY

    return layout("cookie-tajekoztato.html", "Süti- (cookie-) tájékoztató — %s" % SITE,
        "Milyen sütiket és tárolt adatokat használ a Horse-Play LSE weboldala, és hogyan "
        "módosíthatod a beállításaidat.", body)


# ============================================================== 10. AKADÁLYMENTESSÉG
def build_akad():
    body = page_head("Akadálymentességi nyilatkozat",
        "Elkötelezettségünk amellett, hogy a weboldalt mindenki használni tudja.",
        "Akadálymentességi nyilatkozat") + """
<section class="section"><div class="wrap prose">
  <h2>Elkötelezettségünk</h2>
  <p>A Horse-Play Lovas Sportegyesület elkötelezett amellett, hogy a weboldala a lehető
     legtöbb ember számára használható legyen — beleértve a látás-, hallás-, mozgás- vagy
     kognitív nehézséggel élő látogatókat is.</p>

  <h2>Megfelelőségi szint</h2>
  <p>A weboldal a <strong>WCAG 2.1 (Web Content Accessibility Guidelines) AA szintű</strong>
     követelményeihez igazodva készült. Ez nem jogszabályi kötelezettség teljesítése, hanem
     önként vállalt szakmai mérce.</p>

  <h2>Amit megvalósítottunk</h2>
  <ul>
    <li>Szemantikus HTML-szerkezet, logikus címsorhierarchia és tereplandmarkok
        (<code>header</code>, <code>nav</code>, <code>main</code>, <code>footer</code>).</li>
    <li>„Ugrás a tartalomra” hivatkozás a billentyűzettel navigálók számára.</li>
    <li>Teljes billentyűzetes használhatóság, jól látható fókuszjelöléssel.</li>
    <li>A szöveg és a háttér közötti kontrasztarány eléri a WCAG AA szintet
        (normál szövegnél legalább 4,5:1).</li>
    <li>Minden tartalmi képhez alternatív szöveg tartozik; a dekoratív elemek
        <code>aria-hidden</code> jelöléssel rejtettek a felolvasó elől.</li>
    <li>A mozgásra érzékeny látogatók számára a <code>prefers-reduced-motion</code>
        beállítás tiszteletben tartása: bekapcsolt állapotban minden animáció leáll.</li>
    <li>Reszponzív elrendezés, amely 320 képpont szélességtől és 200%%-os
        szövegnagyításnál is használható marad.</li>
    <li>A képnagyító (galéria) billentyűzetről is kezelhető, fókuszcsapdával és
        Esc-billentyűs bezárással.</li>
    <li>A weboldal nyelve gépi olvasás számára jelölt (<code>lang="hu"</code>).</li>
  </ul>

  <h2>Ismert korlátok</h2>
  <ul>
    <li>A beágyazott Google Térkép akadálymentességét a Google biztosítja, arra nincs
        ráhatásunk. A térkép helyett a Kapcsolat oldalon a cím és a GPS-koordináta
        szövegesen is szerepel.</li>
    <li>A régebben feltöltött fényképek alternatív szövegeit folyamatosan pontosítjuk.</li>
  </ul>

  <h2>Visszajelzés</h2>
  <p>Ha akadályba ütközöl a weboldal használata során, kérjük, jelezd — igyekszünk gyorsan
     orvosolni, és szükség esetén az információt más módon (telefonon, e-mailben)
     eljuttatni hozzád.</p>
  <table>
    <tr><th>E-mail</th><td>%s</td></tr>
    <tr><th>Telefon</th><td>%s</td></tr>
  </table>
  <p>A visszajelzésekre 30 napon belül válaszolunk.</p>

  <p class="updated">A nyilatkozat elkészítésének módja: az üzemeltető saját értékelése.
     Utolsó felülvizsgálat: %s</p>
</div></section>
""" % (EMAIL, TEL, TODAY)

    return layout("akadalymentessegi-nyilatkozat.html", "Akadálymentességi nyilatkozat — %s" % SITE,
        "A Horse-Play LSE weboldalának akadálymentességi nyilatkozata a WCAG 2.1 AA szint alapján.",
        body)


# ============================================================== 11. 404
def build_404():
    body = """<section class="page-head">
  <div class="wrap head-center">
    <p class="badge mi-auto">Hiba 404</p>
    <h1>Ez az oldal elkóborolt</h1>
    <p class="mi-auto">Úgy tűnik, a keresett oldal nem létezik, vagy időközben
       új címre költözött. Nézz körül a főoldalon — biztosan megtalálod, amit keresel.</p>
    <p class="mt-30">
      <a class="btn btn--primary" href="index.html">Vissza a főoldalra</a>
      <a class="btn btn--ghost" href="kapcsolat.html">Kapcsolat</a></p>
  </div>
  <svg class="hero-wave" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true">
    <path d="M0 54c150-34 280 22 430 14s250-46 400-32 240 52 380 40 230-30 230-30V90H0Z" fill="#F7F2E4"/>
  </svg>
</section>
<section class="section"><div class="wrap">
  <div class="grid grid--3">
    <a class="card" href="szolgaltatasok.html" class="plain">
      <h2>Szolgáltatások</h2><p>Lovasoktatás, séta- és tereplovaglás, ismerkedés a lovakkal.</p></a>
    <a class="card" href="lovaink.html" class="plain">
      <h2>Lovaink</h2><p>Ismerd meg a lovardánk lovait és a természetüket.</p></a>
    <a class="card" href="kapcsolat.html" class="plain">
      <h2>Kapcsolat</h2><p>Elérhetőségek, térkép és megközelítés.</p></a>
  </div>
</div></section>"""
    html = layout("404.html", "A keresett oldal nem található — %s" % SITE,
        "A keresett oldal nem található a Horse-Play Lovas Sportegyesület weboldalán.", body)
    return html.replace('<meta name="robots" content="index, follow, max-image-preview:large">',
                        '<meta name="robots" content="noindex, follow">')


# ============================================================== segédfájlok
FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="#20402F"/>
<path d="M14 34A18 18 0 0 1 50 34V51a3.5 3.5 0 0 1-7 0V34a11 11 0 0 0-22 0v17a3.5 3.5 0 0 1-7 0Z" fill="#E2A32B"/>
<circle cx="17.5" cy="44" r="1.7" fill="#20402F"/><circle cx="46.5" cy="44" r="1.7" fill="#20402F"/>
<circle cx="18.2" cy="34" r="1.7" fill="#20402F"/><circle cx="45.8" cy="34" r="1.7" fill="#20402F"/>
<circle cx="22.6" cy="24.5" r="1.7" fill="#20402F"/><circle cx="41.4" cy="24.5" r="1.7" fill="#20402F"/>
</svg>"""

ROBOTS = """User-agent: *
Allow: /
Disallow: /404.html

Sitemap: %s/sitemap.xml
""" % BASE

HTACCESS = r"""# ============================================================
#  Horse-Play LSE — Apache beállítások (MediaCenter tárhely)
# ============================================================

# --- Alapértelmezett kódolás -------------------------------
AddDefaultCharset UTF-8

# --- Hibaoldalak -------------------------------------------
ErrorDocument 404 /404.html

# --- Könyvtárlistázás tiltása ------------------------------
Options -Indexes

<IfModule mod_rewrite.c>
  RewriteEngine On

  # HTTPS kikényszerítése
  RewriteCond %{HTTPS} !=on
  RewriteCond %{HTTP:X-Forwarded-Proto} !https
  RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]

  # www nélküli változat -> www (ha fordítva kell, cseréld meg a két blokkot)
  RewriteCond %{HTTP_HOST} ^horse-play\.hu$ [NC]
  RewriteRule ^(.*)$ https://www.horse-play.hu/$1 [R=301,L]

  # index.html elrejtése a címsorból
  RewriteCond %{THE_REQUEST} \s/+index\.html[\s?] [NC]
  RewriteRule ^ / [R=301,L]
</IfModule>

# --- Biztonsági fejlécek -----------------------------------
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=(), interest-cohort=()"
  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
  # Csak a Google Térkép engedélyezett külső forrásként (hozzájárulás után)
  Header always set Content-Security-Policy "default-src 'self'; img-src 'self' data: https://*.googleapis.com https://*.gstatic.com https://maps.google.com; frame-src https://www.google.com https://maps.google.com; script-src 'self'; style-src 'self'; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'; upgrade-insecure-requests"
  # A betűtípusok CORS-engedélye
  <FilesMatch "\.(woff|woff2|ttf)$">
    Header set Access-Control-Allow-Origin "*"
  </FilesMatch>
</IfModule>

# --- Tömörítés ---------------------------------------------
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css
  AddOutputFilterByType DEFLATE application/javascript application/x-javascript
  AddOutputFilterByType DEFLATE image/svg+xml application/json
</IfModule>

# --- Böngészőoldali gyorsítótár ----------------------------
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html                 "access plus 0 seconds"
  ExpiresByType text/css                  "access plus 1 year"
  ExpiresByType application/javascript    "access plus 1 year"
  ExpiresByType image/jpeg                "access plus 6 months"
  ExpiresByType image/png                 "access plus 6 months"
  ExpiresByType image/webp                "access plus 6 months"
  ExpiresByType image/svg+xml             "access plus 6 months"
  ExpiresByType font/woff                 "access plus 1 year"
  ExpiresByType font/woff2                "access plus 1 year"
</IfModule>

# --- MIME-típusok ------------------------------------------
<IfModule mod_mime.c>
  AddType font/woff  .woff
  AddType font/woff2 .woff2
  AddType image/webp .webp
  AddType image/svg+xml .svg
</IfModule>

# --- Rejtett fájlok védelme --------------------------------
<FilesMatch "^\.">
  Require all denied
</FilesMatch>
"""


def sitemap(pages):
    today = datetime.date(2026, 8, 2).isoformat()
    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, prio, freq in pages:
        loc = BASE + "/" + ("" if slug == "index.html" else slug)
        x.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
                 "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
                 % (loc, today, freq, prio))
    x.append("</urlset>")
    return "\n".join(x)


# ============================================================== futtatás
def main():
    os.makedirs(OUT, exist_ok=True)
    pages = {
        "index.html": build_index(),
        "rolunk.html": build_rolunk(),
        "szolgaltatasok.html": build_szolg(),
        "lovaink.html": build_lovaink(),
        "galeria.html": build_galeria(),
        "kapcsolat.html": build_kapcsolat(),
        "impresszum.html": build_impresszum(),
        "adatkezelesi-tajekoztato.html": build_adat(),
        "cookie-tajekoztato.html": build_cookie(),
        "akadalymentessegi-nyilatkozat.html": build_akad(),
        "404.html": build_404(),
    }
    for name, html in pages.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(html)

    with open(os.path.join(OUT, "assets/img/favicon.svg"), "w", encoding="utf-8") as f:
        f.write(FAVICON)
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(ROBOTS)
    with open(os.path.join(OUT, ".htaccess"), "w", encoding="utf-8") as f:
        f.write(HTACCESS)
    sm = [("index.html", "1.0", "monthly"), ("rolunk.html", "0.8", "yearly"),
          ("szolgaltatasok.html", "0.9", "monthly"), ("lovaink.html", "0.8", "monthly"),
          ("galeria.html", "0.7", "monthly"), ("kapcsolat.html", "0.9", "yearly"),
          ("impresszum.html", "0.3", "yearly"),
          ("adatkezelesi-tajekoztato.html", "0.3", "yearly"),
          ("cookie-tajekoztato.html", "0.3", "yearly"),
          ("akadalymentessegi-nyilatkozat.html", "0.3", "yearly")]
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap(sm))

    print("Kész: %d oldal + segédfájlok" % len(pages))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Erzeugt beide Produktseiten aus EINEM Template, damit Layout und Design identisch bleiben.
Nur die Vertrauenssignale unterscheiden sich (VARIANTS unten).

Bilder austauschen: Datei mit gleichem Namen als .jpg/.webp/.png nach public/assets/img/ legen
(z. B. bild-1.jpg ersetzt bild-1.svg) und `python3 build.py` erneut ausfuehren.
"""
from pathlib import Path

ROOT = Path(__file__).parent / "public"
import hashlib
ASSET_V = hashlib.sha1(b"".join(f.read_bytes() for f in sorted((ROOT / "assets").rglob("*")) if f.is_file())).hexdigest()[:8]
IMG = ROOT / "assets" / "img"
IMG.mkdir(parents=True, exist_ok=True)

CLARITY_ID = "u4cvaeeek5"                  # Projekt-ID aus clarity.microsoft.com eintragen, dann `python3 build.py`
PHONE = "0461 0991 240"           # bewusst ungueltige Rufnummer (Teilnehmernummer beginnt mit 0)
MAIL = "service@nordmasche.de"

# ---------------------------------------------------------------- Platzhalterbilder
SWEATER = ('<path d="M70 32 Q100 50 130 32 L168 50 L190 122 L166 130 L150 88 L150 176 L50 176 L50 88 '
           'L34 130 L10 122 L32 50 Z" fill="#DCD3C3" stroke="#22313F" stroke-width="2.2" stroke-linejoin="round"/>'
           '<path d="M70 32 Q100 54 130 32" fill="none" stroke="#22313F" stroke-width="2.2"/>'
           '<path d="M50 166 H150 M58 166 V176 M70 166 V176 M82 166 V176 M94 166 V176 M106 166 V176 M118 166 V176 M130 166 V176 M142 166 V176" stroke="#22313F" stroke-width="1.4"/>')
PLACEHOLDERS = {
    "bild-1": "Modellfoto vorne",
    "bild-2": "Detail: Strick",
    "bild-3": "Detail: Kragen",
    "bild-4": "Modellfoto hinten",
    "kunde-1": "Kundenfoto",
    "kunde-2": "Kundenfoto",
    "team": "Teamfoto",
}
for name, label in PLACEHOLDERS.items():
    p = IMG / f"{name}.svg"
    if not p.exists():
        p.write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500"><rect width="400" height="500" fill="#EFE8DC"/>'
            f'<g transform="translate(70 110) scale(1.3)">{SWEATER}</g>'
            f'<text x="200" y="440" text-anchor="middle" font-family="sans-serif" font-size="18" fill="#7A7368">{label}</text></svg>')


def img(name):
    for ext in ("jpg", "jpeg", "webp", "png", "svg"):
        if (IMG / f"{name}.{ext}").exists():
            return f"/assets/img/{name}.{ext}"
    raise FileNotFoundError(name)


# ---------------------------------------------------------------- Icons
I = {
    "return": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
    "bag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18M16 10a4 4 0 0 1-8 0"/></svg>',
    "heart": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#22313F" stroke-width="2"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/></svg>',
}


STAR = "M10 1.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L10 14.8l-5.2 2.8 1-5.8L1.5 7.7l5.9-.9z"
_star_id = [0]


def stars(v, size=16):
    """Sterne als SVG mit anteiliger Fuellung – unabhaengig vom Stylesheet."""
    _star_id[0] += 1
    cid = f"st{_star_id[0]}"
    w = size * 5 + 8
    paths = "".join(f'<path transform="translate({i * (size + 2)} 0) scale({size / 20})" d="{STAR}"/>' for i in range(5))
    fill_w = w * max(0.0, min(1.0, v / 5))
    label = str(v).replace(".", ",")
    return (f'<svg class="stars" width="{w}" height="{size}" viewBox="0 0 {w} {size}" role="img" aria-label="{label} von 5 Sternen">'
            f'<defs><clipPath id="{cid}"><rect width="{fill_w:.1f}" height="{size}"/></clipPath></defs>'
            f'<g fill="#D9D2C5">{paths}</g><g fill="#C9A14A" clip-path="url(#{cid})">{paths}</g></svg>')


def rating_block(score, count, dist):
    """Gleiches Bewertungsmodul fuer beide Seiten. dist = Anzahl fuer 5..1 Sterne."""
    total = sum(dist)
    rows = "".join(
        f'<div><span>{n} {"Stern" if n == 1 else "Sterne"}</span><span class="bar"><span style="width:{(c / total * 100) if total else 0:.0f}%"></span></span><span>{c}</span></div>'
        for n, c in zip([5, 4, 3, 2, 1], dist))
    word = "Bewertung" if count == 1 else "Bewertungen"
    return (f'<div class="reviews-head"><div><div class="score">{str(score).replace(".", ",")}</div>{stars(score)}'
            f'<div style="font-size:14px;color:var(--muted);margin-top:6px">aus {count} {word}</div></div>'
            f'<div class="dist">{rows}</div></div>')


PAY_LOGOS = {"PayPal": ["paypal"], "Kreditkarte": ["mastercard", "visa"]}
PAY_NAMES = {"paypal": "PayPal", "mastercard": "Mastercard", "visa": "Visa"}


def pay_html(methods):
    out = []
    for m in methods:
        if m in PAY_LOGOS:
            out += [f'<img class="paylogo" src="/assets/pay/{f}.svg?v={ASSET_V}" alt="{PAY_NAMES[f]}" width="47" height="30">' for f in PAY_LOGOS[m]]
        else:
            out.append(f'<span class="paytext">{m}</span>')
    return "".join(out)


# ---------------------------------------------------------------- Bewertungen
REVIEWS_A = [   # Durchschnitt 3,6 aus 128 – gemischtes Bild
    dict(name="Julia K.", meta="Größe M · 1,68 m", date="12.10.2026", s=5, title="Kratzt kein bisschen",
         text="Ich bin bei Wolle empfindlich, aber den kann ich direkt auf der Haut tragen. Farbe wie auf den Fotos.", photo="kunde-1"),
    dict(name="Tobias R.", meta="Größe L · 1,86 m", date="28.09.2026", s=4, title="Warm, aber nicht zu dick",
         text="Passt gut unter die Jacke. Nach zwei Wäschen leicht gefusselt, sonst wie neu.", photo="kunde-2"),
    dict(name="Sandra M.", meta="Größe S · 1,72 m", date="03.10.2026", s=3, title="Schöne Qualität, Passform eher kurz",
         text="Material ist gut. Für meine Größe ist er am Bauch etwas kurz, die Ärmel dafür lang. Würde eine Größe größer nehmen.", photo=None),
    dict(name="Daniel H.", meta="Größe M · 1,79 m", date="17.09.2026", s=2, title="Für den Preis enttäuscht",
         text="Nach drei Wochen Pilling an den Ärmeln. Die Rücksendung lief aber unkompliziert, Geld war nach ein paar Tagen zurück.", photo=None),
]
REVIEWS_B = [   # Durchschnitt 4,8 aus 5
    dict(name="Lena", meta="", date="02.11.2026", s=5, title="Super Pulli!", text="Sehr schön und richtig weich.", photo=None),
    dict(name="Max", meta="", date="29.10.2026", s=5, title="Top", text="Gerne wieder.", photo=None),
    dict(name="Anna", meta="", date="21.10.2026", s=5, title="Mein neuer Lieblingspulli", text="Passt perfekt.", photo=None),
    dict(name="Jonas", meta="", date="14.10.2026", s=5, title="Klasse", text="Absolut empfehlenswert!", photo=None),
    dict(name="Sophie", meta="", date="09.10.2026", s=4, title="Schön", text="Ganz zufrieden.", photo=None),
]


def review_html(r, verified):
    who = f'<b>{r["name"]}</b>'
    if r["meta"]:
        who += f'<small>{r["meta"]}</small>'
    if r["date"]:
        who += f'<small>{r["date"]}</small>'
    if verified:
        who += '<span class="verified">✓ Verifizierter Kauf</span>'
    photo = f'<div class="rphoto"><img src="{img(r["photo"])}" alt="Kundenfoto"></div>' if r["photo"] else ""
    return (f'<div class="review"><div class="who">{who}</div><div>{stars(r["s"])}'
            f'<h3>{r["title"]}</h3><p>{r["text"]}</p>{photo}</div></div>')


# ---------------------------------------------------------------- Varianten (nur hier unterscheiden sich die Seiten)
A_SPEC = """
<section class="block" id="details"><div class="wrap details">
  <div><h2>Produktdetails</h2>
    <table class="spec">
      <tr><td>Material</td><td>100 % Merinowolle, extrafein (19,5 Mikron)</td></tr>
      <tr><td>Verarbeitung</td><td>Feinstrick, Rundhals, Rippbündchen an Saum und Ärmeln</td></tr>
      <tr><td>Gewicht</td><td>ca. 380 g (Größe M)</td></tr>
      <tr><td>Herkunft</td><td>Wolle aus Uruguay, gestrickt in Portugal</td></tr>
      <tr><td>Pflege</td><td>Wollwaschgang 30 °C oder Handwäsche, liegend trocknen</td></tr>
      <tr><td>Artikelnummer</td><td>NM-2041</td></tr>
    </table>
  </div>
  <div id="groessen"><h2>Größentabelle</h2>
    <table class="sizetable">
      <tr><th>Größe</th><th>XS</th><th>S</th><th>M</th><th>L</th><th>XL</th></tr>
      <tr><td>Brustweite (cm)</td><td>96</td><td>102</td><td>108</td><td>114</td><td>120</td></tr>
      <tr><td>Länge (cm)</td><td>64</td><td>66</td><td>68</td><td>70</td><td>72</td></tr>
      <tr><td>Ärmellänge (cm)</td><td>60</td><td>62</td><td>64</td><td>65</td><td>66</td></tr>
    </table>
    <div class="note"><b>Passform:</b> fällt normal aus, gerader Schnitt. Zwischen zwei Größen? Für einen lockeren Sitz eine Größe größer wählen.</div>
  </div>
</div></section>"""

VARIANTS = {
    "pullover-1": dict(   # Seite A – starke Signale
        title="Merino-Pullover Lyng",
        rating=f'{stars(3.6)}<b>3,6</b><a href="#bewertungen">128 Bewertungen</a>',
        price_note="inkl. MwSt., zzgl. 4,90 € Versand · Lieferung in 2–3 Werktagen",
        lead="Klassischer Rundhalspullover aus extrafeiner Merinowolle. Temperaturausgleichend, geruchsneutral und weich genug, um ihn direkt auf der Haut zu tragen.",
        size_link='<a href="#groessen">Größentabelle &amp; Passform</a>',
        stock='<div class="stock">Auf Lager · in allen Größen lieferbar</div>',
        usp=f"""<ul class="usp">
          <li>{I['return']}<span><b>30 Tage kostenlose Rückgabe</b> – Rücksendeetikett liegt bei. <a href="rueckgabe">Details</a></span></li>
          <li>{I['shield']}<span><b>2 Jahre Garantie auf Verarbeitung</b></span></li>
          <li>{I['chat']}<span>Fragen zur Größe? {PHONE} · {MAIL}<br><small>Antwort innerhalb von 24 Stunden</small></span></li>
        </ul>""",
        pay=["Kauf auf Rechnung", "PayPal", "Kreditkarte", "Lastschrift"],
        details=A_SPEC,
        reviews_head=rating_block(3.6, 128, [42, 30, 26, 18, 12]),
        reviews="".join(review_html(r, True) for r in REVIEWS_A) + '<a class="more" href="#bewertungen">Alle 128 Bewertungen anzeigen</a>',
        reviews_title="Bewertungen",
        footer_about='<p style="color:var(--muted);margin:14px 0">Merino-Strick aus Flensburg.</p><a href="#" aria-label="Instagram">Instagram @nordmasche</a>',
        footer_cols=f"""
          <div><h4>Service</h4><ul><li>{PHONE}</li><li>{MAIL}</li><li style="color:var(--muted)">Mo–Fr, Antwort in 24 h</li><li><a href="rueckgabe">Versand &amp; Rückgabe</a></li></ul></div>
          <div><h4>Unternehmen</h4><ul><li><a href="ueber-uns">Über uns</a></li></ul></div>
          <div><h4>Rechtliches</h4><ul><li><a href="impressum">Impressum</a></li><li><a href="#">Datenschutz</a></li><li><a href="#">AGB</a></li><li><a href="rueckgabe#widerruf">Widerrufsrecht</a></li></ul></div>""",
    ),
    "pullover-2": dict(   # Seite B – schwache Signale
        title="Merino-Pullover Lyng",
        rating=f'{stars(4.8)}<b>4,8</b><a href="#bewertungen">5 Bewertungen</a>',
        price_note="",
        lead="Unser Lieblingspullover für die kalte Jahreszeit. Weich, warm und einfach zeitlos schön.",
        size_link="",
        stock="",
        usp="",
        pay=["Vorkasse", "Kreditkarte"],
        details="",
        reviews_head=rating_block(4.8, 5, [4, 1, 0, 0, 0]),
        reviews="".join(review_html(r, False) for r in REVIEWS_B),
        reviews_title="Bewertungen",
        footer_about="",
        footer_cols=f"""
          <div><h4>Kontakt</h4><ul><li>{MAIL}</li></ul></div>
          <div></div>
          <div><h4>Rechtliches</h4><ul><li><a href="impressum">Impressum</a></li><li><a href="agb">AGB</a></li></ul></div>""",
    ),
}

# ---------------------------------------------------------------- Gemeinsames Template
HEAD = """<!DOCTYPE html>
<html lang="de"><head>
<meta charset="utf-8"><meta name="robots" content="noindex, nofollow">
<title>{title} – Nordmasche</title>
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/shop.css?v={asset_v}">
</head><body>
<div class="topbar">Die neue Herbstkollektion ist da</div>
<header class="site"><div class="wrap">
  <a href="#"><img src="/assets/logo-nordmasche.svg" alt="Nordmasche"></a>
  <nav class="main"><a href="#">Damen</a><a href="#">Herren</a><a href="#">Accessoires</a><a href="#">Neu</a></nav>
  <div class="icons"><a href="#">Suche</a><a href="#">Konto</a>
    <a class="cart" href="#">""" + I["bag"] + """<span class="count" id="cartcount">0</span></a></div>
</div></header>
"""


CONSENT = """
<div id="consent" style="display:none;position:fixed;left:0;right:0;bottom:0;z-index:50;background:#fff;border-top:1px solid var(--line);box-shadow:0 -6px 24px rgba(34,49,63,.08)">
  <div class="wrap" style="display:flex;align-items:center;justify-content:space-between;gap:24px;padding:16px 0;font-size:14px">
    <span>Wir verwenden Cookies, um die Nutzung unserer Seite zu analysieren und sie zu verbessern.</span>
    <span style="display:flex;gap:10px;flex:none">
      <button id="c-no" class="size" style="width:auto;padding:0 18px">Ablehnen</button>
      <button id="c-yes" class="btn" style="flex:none;height:46px;padding:0 22px;font-size:15px">Akzeptieren</button>
    </span>
  </div>
</div>
<script>
(function(){
  var ID="__CLARITY_ID__";
  // Teilnehmer-Nummer aus ?t=3 merken (bleibt fuer beide Seiten und Unterseiten gespeichert)
  try{var t=new URLSearchParams(location.search).get('t'); if(t) localStorage.setItem('nm_t',t);}catch(e){}
  function load(){
    if(!ID) return;
    (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
      t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script",ID);
    window.clarity('consentv2',{ad_Storage:'denied',analytics_Storage:'granted'});
    var tn=null; try{tn=localStorage.getItem('nm_t');}catch(e){}
    if(tn) window.clarity('set','teilnehmer',tn);
    window.clarity('set','seite',location.pathname.split('/')[1]||'start');
  }
  var c=null; try{c=localStorage.getItem('nm_consent');}catch(e){}
  if(c==='yes') load();
  else if(c!=='no') document.getElementById('consent').style.display='block';
  document.getElementById('c-yes').onclick=function(){try{localStorage.setItem('nm_consent','yes')}catch(e){};document.getElementById('consent').style.display='none';load();};
  document.getElementById('c-no').onclick=function(){try{localStorage.setItem('nm_consent','no')}catch(e){};document.getElementById('consent').style.display='none';};
})();
</script>""".replace("__CLARITY_ID__", CLARITY_ID)


def footer(v):
    return f"""<footer class="site"><div class="wrap">
  <div class="cols"><div><img src="/assets/logo-nordmasche.svg" alt="Nordmasche">{v['footer_about']}</div>{v['footer_cols']}</div>
  <div class="legal"><span>© 2026 Nordmasche</span><span></span></div>
</div></footer>{CONSENT}"""


SCRIPT = """<script>
document.querySelectorAll('.thumb').forEach(t=>t.addEventListener('click',()=>{
  document.querySelectorAll('.thumb').forEach(x=>x.classList.remove('active'));t.classList.add('active');
  document.getElementById('mainimg').src=t.dataset.src;}));
document.querySelectorAll('.swatch').forEach(s=>s.addEventListener('click',()=>{
  document.querySelectorAll('.swatch').forEach(x=>x.classList.remove('active'));s.classList.add('active');
  document.getElementById('colorname').textContent=s.dataset.name;}));
let size=null;
document.querySelectorAll('.size').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('.size').forEach(x=>x.classList.remove('active'));b.classList.add('active');size=b.textContent;}));
document.getElementById('addbtn').addEventListener('click',()=>{
  const msg=document.getElementById('added');
  if(!size){msg.style.color='#8C3A24';msg.textContent='Bitte wähle eine Größe.';return;}
  const c=document.getElementById('cartcount');c.textContent=+c.textContent+1;
  msg.style.color='';msg.textContent='Größe '+size+' wurde in den Warenkorb gelegt.';});
</script>"""


def pdp(slug, v):
    gallery = [("bild-1", "Modell vorne"), ("bild-2", "Strick"), ("bild-3", "Kragen"), ("bild-4", "Modell hinten")]
    thumbs = "".join(
        f'<div class="thumb{" active" if i == 0 else ""}" data-src="{img(n)}"><img src="{img(n)}" alt="{a}"></div>'
        for i, (n, a) in enumerate(gallery))
    sizes = "".join(f'<button class="size">{s}</button>' for s in ["XS", "S", "M", "L", "XL"])
    chips = pay_html(v["pay"])
    price_note = f'<div class="price-note">{v["price_note"]}</div>' if v["price_note"] else ""
    return HEAD.format(title=v["title"], asset_v=ASSET_V) + f"""
<main class="wrap">
  <div class="crumbs"><a href="#">Startseite</a> / <a href="#">Pullover</a> / {v['title']}</div>
  <div class="pdp">
    <div class="gallery">
      <div class="thumbs">{thumbs}</div>
      <div class="mainimg"><img id="mainimg" src="{img('bild-1')}" alt="{v['title']}"></div>
      <div class="caption">Model ist 1,84 m groß und trägt Größe M.</div>
    </div>
    <div class="info">
      <div class="eyebrow">Unisex · Merino</div>
      <h1>{v['title']}</h1>
      <div class="rating-line">{v['rating']}</div>
      <div class="price">89,00 €</div>{price_note}
      <p class="lead">{v['lead']}</p>
      <div class="opt-label"><span>Farbe: <span id="colorname" style="font-weight:400">Fjordblau</span></span></div>
      <div class="swatches">
        <span class="swatch active" data-name="Fjordblau" style="background:#2C3E50"></span>
        <span class="swatch" data-name="Anthrazit" style="background:#4A4A4A"></span>
        <span class="swatch" data-name="Natur" style="background:#E6DCC8"></span>
      </div>
      <div class="opt-label"><span>Größe</span>{v['size_link']}</div>
      <div class="sizes">{sizes}</div>
      {v['stock']}
      <div class="buy"><button class="btn" id="addbtn">In den Warenkorb</button><button class="btn-ghost" aria-label="Merken">{I['heart']}</button></div>
      <div class="added" id="added"></div>
      {v['usp']}
      <div class="pay"><div class="t">Bezahlen mit</div><div class="chips">{chips}</div></div>
    </div>
  </div>
</main>
{v['details']}
<section class="block" id="bewertungen"><div class="wrap">
  <h2>{v['reviews_title']}</h2>{v['reviews_head']}{v['reviews']}
</div></section>
{footer(v)}
{SCRIPT}
</body></html>"""


def textpage(v, title, body):
    return HEAD.format(title=title, asset_v=ASSET_V) + f'<main class="wrap"><div class="page">{body}</div></main>{footer(v)}</body></html>'


# ---------------------------------------------------------------- Unterseiten
SUB = {
    "pullover-1": {
        "impressum": ("Impressum", f"""<h1>Impressum</h1>
<p><b>Nordmasche GmbH</b><br>Maschenweg 7<br>24937 Flensburg<br>Deutschland</p>
<p>Vertreten durch die Geschäftsführerin Maren Holst</p>
<h2>Kontakt</h2><p>Telefon: {PHONE}<br>E-Mail: {MAIL}<br>Erreichbar Mo–Fr, 9–17 Uhr</p>
<h2>Registereintrag</h2><p>Registergericht: Amtsgericht Flensburg<br>Registernummer: HRB 21487 FL</p>
<h2>Umsatzsteuer-ID</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: DE 318 604 275</p>
<h2>Verbraucherstreitbeilegung</h2><p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>"""),
        "rueckgabe": ("Versand & Rückgabe", f"""<h1>Versand &amp; Rückgabe</h1>
<h2 id="versand">Versand</h2><p>Wir versenden innerhalb Deutschlands mit DHL. Die Lieferzeit beträgt 2–3 Werktage, die Versandkosten 4,90 €.</p>
<h2>30 Tage kostenlose Rückgabe</h2><p>Passt etwas nicht? Du kannst jeden Artikel innerhalb von 30 Tagen nach Erhalt kostenlos zurückschicken. Ein Rücksendeetikett liegt jeder Bestellung bei. Den Kaufpreis erstatten wir innerhalb von 5 Werktagen nach Eingang der Rücksendung auf dem ursprünglichen Zahlungsweg.</p>
<h2 id="widerruf">Widerrufsrecht</h2><p>Unabhängig von unserer freiwilligen Rückgabe-Garantie hast du ein gesetzliches Widerrufsrecht von 14 Tagen. Fragen dazu beantworten wir gern unter {MAIL}.</p>"""),
        "ueber-uns": ("Über uns", f"""<h1>Über uns</h1>
<p>Nordmasche haben wir 2021 in Flensburg gegründet, weil wir einen Pullover wollten, der warm ist, nicht kratzt und viele Winter hält. Heute arbeiten wir zu fünft an einer kleinen Kollektion aus Merinowolle.</p>
<div class="teamimg"><img src="{img('team')}" alt="Team" style="height:100%;border-radius:10px"></div>
<p>Unsere Wolle kommt aus Uruguay, gestrickt wird in einem Familienbetrieb in Portugal, mit dem wir seit dem ersten Tag zusammenarbeiten.</p>"""),
    },
    "pullover-2": {
        "impressum": ("Impressum", f"""<h1>Impressum</h1><p>Nordmasche<br>M. Holst<br>{MAIL}</p>"""),
        "agb": ("AGB", """<h1>Allgemeine Geschäftsbedingungen</h1>
<p>§ 1 Geltungsbereich. Diese AGB gelten für alle Bestellungen über unseren Online-Shop.</p>
<p>§ 2 Vertragsschluss. Mit Absenden der Bestellung gibt der Kunde ein verbindliches Angebot ab.</p>
<p>§ 3 Preise und Versand. Alle Preise in Euro. Versandkosten werden im Bestellprozess angezeigt.</p>
<p>§ 4 Zahlung. Die Zahlung erfolgt per Vorkasse oder Kreditkarte.</p>
<p>§ 5 Rückgabe. Rücksendungen sind innerhalb der gesetzlichen Frist möglich. Die Kosten der Rücksendung trägt der Kunde.</p>"""),
    },
}

def absolute(html, slug):
    # Unterseiten-Links absolut machen, damit sie mit und ohne Slash am Ende funktionieren
    for name in ["impressum", "rueckgabe", "ueber-uns", "agb"]:
        html = html.replace(f'href="{name}', f'href="/{slug}/{name}')
    return html


for slug, v in VARIANTS.items():
    d = ROOT / slug
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(absolute(pdp(slug, v), slug), encoding="utf-8")
    for name, (title, body) in SUB[slug].items():
        (d / f"{name}.html").write_text(absolute(textpage(v, title, body), slug), encoding="utf-8")
print("gebaut:", ", ".join(VARIANTS))

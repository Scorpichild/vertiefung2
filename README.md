# Nordmasche – Studien-Prototyp

Statische Produktseiten (fiktiver Merino-Shop) für die THWS-Fokusgruppe.
Läuft als nginx-Container, getrennt vom Teeshop, unter https://vertiefung.loramondo.de.

- `/pullover-1`, `/pullover-2`: die zwei Produktseiten
- Alles ist `noindex`; nach der Studie Resource in Coolify löschen.

Lokal testen:

    docker build -t nordmasche . && docker run --rm -p 8080:80 nordmasche
    # http://localhost:8080/pullover-1

## Seiten bearbeiten

Beide Produktseiten werden aus `build.py` erzeugt (ein Template, nur die Signale unterscheiden sich).
Nach Änderungen: `python3 build.py`, dann committen und pushen.

Bilder: `public/assets/img/bild-1.jpg` (bzw. .webp/.png) ersetzt `bild-1.svg` – danach `python3 build.py`.
- bild-1 … bild-4: Galerie (auf beiden Seiten identisch)
- kunde-1, kunde-2: Kundenfotos in den Bewertungen (nur Seite 1)
- team: Teamfoto auf „Über uns“ (nur Seite 1)

Zahlungslogos (`public/assets/pay/`): aus dem npm-Paket `payment-icons` (MPL-2.0).

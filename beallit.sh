#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Domain beállítása
#
#  Használat:
#      bash beallit.sh a-domainem.hu ["Székhely cím"] ["Nyilvántartási szám"]
#
#  Ez behelyettesíti a domaint az index.html, adatkezeles.html, robots.txt,
#  sitemap.xml és config.php fájlokba, beírja a mai dátumot a sitemapbe,
#  és — ha megadod — kitölti a székhelyet és a nyilvántartási számot
#  az adatkezelési tájékoztatóban.
# ─────────────────────────────────────────────────────────────
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Hiba: add meg a domaint."
  echo "Használat: bash beallit.sh a-domainem.hu"
  exit 1
fi

DOMAIN="$1"
DOMAIN="${DOMAIN#http://}"; DOMAIN="${DOMAIN#https://}"; DOMAIN="${DOMAIN#www.}"; DOMAIN="${DOMAIN%/}"

if ! printf '%s' "$DOMAIN" | grep -Eq '^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$'; then
  echo "Hiba: érvénytelen domain: $DOMAIN"
  exit 1
fi

csere() {
  if sed --version >/dev/null 2>&1; then sed -i "s/DOMAIN\.HU/${DOMAIN}/g" "$1"
  else sed -i '' "s/DOMAIN\.HU/${DOMAIN}/g" "$1"; fi
  echo "  ✓ $1"
}

for f in *.html *.xml *.txt config.php; do
  [ -f "$f" ] && grep -q "DOMAIN\.HU" "$f" && csere "$f"
done

# ── Székhely és nyilvántartási szám az impresszumba ──
SED_I() { if sed --version >/dev/null 2>&1; then sed -i "$1" "$2"; else sed -i '' "$1" "$2"; fi }

if grep -q SZEKHELYCIM adatkezeles.html 2>/dev/null; then
  if [ $# -ge 2 ] && [ -n "${2:-}" ]; then
    SZEK=$(printf '%s' "$2" | sed 's/[&/\\]/\\&/g')
    SED_I "s/SZEKHELYCIM/${SZEK}/g" adatkezeles.html
    echo "  ✓ székhely beírva"
  else
    echo "  ! FIGYELEM: a székhely helyén még SZEKHELYCIM áll az adatkezeles.html-ben."
  fi
else
  echo "  ✓ székhely már ki van töltve"
fi

if grep -q NYILVSZAM adatkezeles.html 2>/dev/null; then
  if [ $# -ge 3 ] && [ -n "${3:-}" ]; then
    NYSZ=$(printf '%s' "$3" | sed 's/[&/\\]/\\&/g')
    SED_I "s/NYILVSZAM/${NYSZ}/g" adatkezeles.html
    echo "  ✓ nyilvántartási szám beírva"
  else
    echo "  ! FIGYELEM: a nyilvántartási szám helyén még NYILVSZAM áll az adatkezeles.html-ben."
  fi
else
  echo "  ✓ nyilvántartási szám már ki van töltve"
fi

TODAY=$(date +%Y-%m-%d)
if sed --version >/dev/null 2>&1; then
  sed -i "s|<lastmod>.*</lastmod>|<lastmod>${TODAY}</lastmod>|" sitemap.xml
else
  sed -i '' "s|<lastmod>.*</lastmod>|<lastmod>${TODAY}</lastmod>|" sitemap.xml
fi

echo ""
echo "Kész. Az oldal címe: https://${DOMAIN}/"
echo ""
echo "Ellenőrzés — maradt-e helykitöltő:"
if grep -rn "DOMAIN\.HU" . --exclude=beallit.sh --exclude=BEALLITAS.md 2>/dev/null; then
  echo "  ↑ ezeket még át kell írni"
else
  echo "  ✓ nem maradt egy sem"
fi
echo ""
echo "Ne felejtsd: a config.php-ba be kell írni a Resend API kulcsot!"

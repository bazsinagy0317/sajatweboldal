#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Domain beállítása
#
#  Használat:
#      bash beallit.sh a-domainem.hu
#
#  Ez behelyettesíti a domaint az index.html, robots.txt, sitemap.xml
#  és config.php fájlokba, és beírja a mai dátumot a sitemapbe.
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

for f in index.html robots.txt sitemap.xml config.php; do
  [ -f "$f" ] && csere "$f"
done

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

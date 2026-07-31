# Nagy Balázs — weboldal

Egyoldalas bemutatkozó weboldal GitHub Pagesre.
A kapcsolati űrlap egy ingyenes Cloudflare Workeren keresztül a **Resend**-del küldi az e-mailt.

**Az oldal címe a feltöltés után:**

```
https://bazsinagy0317.github.io/sajatweboldal/
```

Minden hivatkozás, a sitemap és a közösségi előnézet már erre a címre van beállítva —
nincs benne kitöltendő helykitöltő.

---

## Mit tartalmaz a csomag

| Fájl | Mire való |
|---|---|
| `index.html` | Maga a weboldal — minden stílus és script benne van, nincs külső függősége |
| `404.html` | Egyedi hibaoldal rossz cím esetén |
| `og.png` | Előnézeti kép Facebookra, Messengerbe, LinkedInre |
| `favicon.svg` | Böngészőfül ikon |
| `apple-touch-icon.png` | Ikon, ha valaki kirakja az oldalt iPhone kezdőképernyőre |
| `site.webmanifest` | Alkalmazás-leíró (ikonok, színek) |
| `robots.txt` | Keresőrobotoknak: minden indexelhető |
| `sitemap.xml` | Oldaltérkép a Google-nek |
| `.nojekyll` | Kell a GitHub Pageshez, különben furcsán dolgozza fel a fájlokat |
| `worker/` | A Cloudflare Worker, ami az űrlapot e-mailre váltja |

---

## 1. lépés — Feltöltés GitHubra

Hozz létre egy **publikus** repót `sajatweboldal` néven, majd a fájlok mappájában:

```bash
git init
git add .
git commit -m "Weboldal"
git branch -M main
git remote add origin https://github.com/bazsinagy0317/sajatweboldal.git
git push -u origin main
```

Ezután a repóban:

**Settings → Pages → Source: Deploy from a branch → Branch: `main` / `(root)` → Save**

Pár perc múlva él. A HTTPS automatikusan bekapcsol.

> **Fontos:** a repó neve pontosan `sajatweboldal` legyen. Ha másra nevezed el,
> a `404.html`-ben lévő `/sajatweboldal/` hivatkozásokat és az abszolút címeket
> (`index.html`, `robots.txt`, `sitemap.xml`) is át kell írni.

---

## 2. lépés — Az űrlap bekötése (Resend + Cloudflare Worker)

**Miért kell Worker?** A GitHub Pages csak fájlokat szolgál ki, programot nem futtat.
A Resend API-kulcs pedig nem kerülhet a weboldal kódjába, mert azt bárki elolvashatná
és a te nevedben küldhetne leveleket. A Worker egy pici, ingyenes közvetítő:
az oldal neki szól, ő ismeri a kulcsot, és ő hívja meg a Resendet.

### 2.1 Resend API-kulcs

1. Lépj be a [resend.com](https://resend.com) fiókodba
2. **API Keys → Create API Key** — másold ki (`re_...` kezdetű)

### 2.2 Worker telepítése

```bash
cd worker
npx wrangler login          # böngészőben belépteti a Cloudflare fiókodba
npx wrangler secret put RESEND_API_KEY
#   ↑ ide illeszd be a re_... kulcsot (nem kerül a repóba)
npx wrangler deploy
```

A végén kiír egy címet, valami ilyet:

```
https://kapcsolati-urlap.bazsinagy0317.workers.dev
```

### 2.3 A cím beírása a weboldalba

Nyisd meg az `index.html`-t, keresd meg a script elején ezt a sort:

```js
var FORM_ENDPOINT = '';
```

Írd bele a Worker címét:

```js
var FORM_ENDPOINT = 'https://kapcsolati-urlap.bazsinagy0317.workers.dev';
```

Mentsd, `git add . && git commit -m "Urlap" && git push`. Ennyi.

> **Amíg üresen hagyod:** az űrlap a látogató levelezőprogramját nyitja meg
> előre kitöltött üzenettel. Működik, csak kevesebben küldik el így.

---

## Feladó cím — fontos tudnivaló

A `worker/wrangler.toml`-ban most ez áll:

```toml
MAIL_FROM = "onboarding@resend.dev"
MAIL_TO   = "bazsinagy0317@gmail.com"
```

Az `onboarding@resend.dev` a Resend teszt címe. **Csak a saját Resend-fiókod e-mail
címére tud küldeni** — mivel a levél úgyis hozzád érkezik, ez indulásnak elég.

Ha később saját domained lesz:

1. Resend → **Domains → Add Domain**
2. A kapott DNS rekordokat vidd fel a domain szolgáltatódnál
3. Ha zöld a státusz, írd át: `MAIL_FROM = "noreply@a-domained.hu"`
4. `npx wrangler deploy`

---

## Mi van beépítve

**Keresőoptimalizálás**
- 49 karakteres oldalcím, 150 karakteres leírás (mindkettő elfér a Google találatban)
- Canonical cím — nem lesz duplikált tartalom
- Open Graph és Twitter kártya + előnézeti kép
- Strukturált adatok (JSON-LD): szolgáltatás, árak, GYIK — ettől a Google
  a keresési találatnál is meg tudja jeleníteni a kérdéseket
- `robots.txt` és `sitemap.xml`
- Egy `h1`, alatta szekciónként `h2` — helyes címsor-szerkezet

**Megjelenés**
- Végigmérve 320-tól 1920 pixelig: iPhone SE, iPhone 14, iPad álló és fekvő, laptop, nagy monitor
- Töréspontok: 360, 480, 720, 900, 1024, 1180 px
- 900 px alatt mobilmenü, tabletnél kétoszlopos elrendezés
- Minden gomb és link legalább 40–52 px magas
- Az űrlapmezők mobilon 16 px betűsek, így az iPhone nem nagyít rá fókusznál

**Akadálymentesítés**
- „Ugrás a tartalomra" link billentyűzetes navigáláshoz
- A mobilmenü gombja `aria-expanded`-et állít, Escape-re bezár
- Az űrlap hibaüzenete `aria-live`-val érkezik, a hibás mező `aria-invalid`-ot kap
- Látható fókuszkeret mindenhol
- `prefers-reduced-motion` esetén minden animáció kikapcsol

**Spamvédelem**
- Rejtett csapdamező (a robot kitölti, az ember nem)
- Elutasítja a 2,5 másodpercnél gyorsabb beküldést
- A Worker csak a `https://bazsinagy0317.github.io` címről fogad kérést
- A beküldött szöveg escape-elve kerül a levélbe

---

## Későbbi teendők (nem sürgős)

**Google Search Console** — [search.google.com/search-console](https://search.google.com/search-console)
Add hozzá az oldalt, és küldd be a sitemapet:
`https://bazsinagy0317.github.io/sajatweboldal/sitemap.xml`
Így hetek helyett napok alatt bekerül a találatok közé.

**Saját domain** — ha veszel egyet, akkor érdemes átállni, mert rövidebb és
komolyabb, mint a github.io-s cím. Ilyenkor:
- tegyél egy `CNAME` nevű fájlt a repó gyökerébe, benne a domain neve
- állítsd a DNS-t a GitHub szervereire
- írd át az abszolút címeket (`index.html`, `robots.txt`, `sitemap.xml`, `404.html`)

**Analitika** — ha érdekel a látogatottság, a Google Analytics vagy a Plausible
pár sorral beköthető.

---

## Módosítás

Az `index.html` egyetlen fájl. Ha szöveget akarsz cserélni, keress rá a mondatra
és írd át — nincs mögötte fordítás vagy build lépés. Mentés, commit, push, és pár
másodpercen belül él az új változat.

A színek a fájl elején, a `:root` blokkban vannak — ha az egészet át akarod hangolni,
elég az ott lévő pár értéket átírni.

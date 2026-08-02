# Horse-Play Lovas Sportegyesület — weboldal

Statikus, keretrendszer nélküli weboldal. Nincs adatbázis, nincs PHP, nincs külső
JavaScript-könyvtár — sima HTML, CSS és egyetlen JS-fájl. Bármelyik tárhelyen elindul,
a MediaCenteren különösebb beállítás nélkül működik.

---

## 1. Feltöltés a MediaCenter tárhelyre

1. Csatlakozz FTP-vel vagy a MediaCenter fájlkezelőjével.
2. Töltsd fel a `site` mappa **teljes tartalmát** a `public_html` (vagy `web`) könyvtárba —
   nem magát a `site` mappát, hanem ami benne van.
3. Ügyelj rá, hogy a **`.htaccess`** is felkerüljön. Sok FTP-program alapból elrejti a ponttal
   kezdődő fájlokat — kapcsold be a rejtett fájlok mutatását.
4. Ha a tárhelyen van SSL-tanúsítvány (a MediaCenternél a Let's Encrypt ingyenes),
   kapcsold be, mielőtt élesíted — a `.htaccess` HTTPS-re irányít át.

### Fájlszerkezet

```
index.html                        Főoldal
rolunk.html                       Rólunk
szolgaltatasok.html               Szolgáltatások
lovaink.html                      Lovaink
galeria.html                      Galéria
kapcsolat.html                    Kapcsolat + térkép
impresszum.html                   Impresszum
adatkezelesi-tajekoztato.html     GDPR
cookie-tajekoztato.html           Sütik
akadalymentessegi-nyilatkozat.html
404.html                          Hibaoldal
robots.txt  sitemap.xml  .htaccess
assets/css/style.css              Stílusok
assets/js/main.js                 Interakciók
assets/fonts/*.woff               Fraunces + Plus Jakarta Sans (saját tárhelyről)
assets/img/*.jpg                  Fotók (jelenleg helyőrzők)
```

---

## 2. Amit ki kell tölteni

A weboldalon minden hiányzó adat **sárga háttérrel, `[KITÖLTENDŐ: …]` formában** jelenik meg,
így egyetlen szem alatt megtalálható. Keress rá a `KITÖLTENDŐ` szóra bármelyik szerkesztőben.

| Hol | Mit |
|---|---|
| **Minden oldal (lábléc)** | Pontos cím, telefonszám, e-mail cím |
| **Kapcsolat** | Telefonos elérhetőség ideje, útvonalleírás, parkolás |
| **Impresszum** | Nyilvántartó bíróság, nyilvántartási szám, adószám, képviselő neve |
| **Adatkezelési tájékoztató** | Nyilvántartási szám, naplómegőrzési idő, e-mailek megőrzési ideje |
| **Rólunk** | Alapítás éve, rövid történet, felelősségbiztosítás ténye |
| **Szolgáltatások** | Árak, alkalmak hossza, egyeztethető időpontok |
| **Lovaink** | A lovak valódi neve, fajtája, kora, jellemzése |
| **Főoldal** | A négy szám (lovak száma, oktatók száma stb.) |

Ezeket a `build.py` tetején lévő állandókban érdemes egyszerre átírni
(`TEL`, `EMAIL`, `CIM`), majd újrafuttatni — így minden oldalon egyszerre frissül.

---

## 3. A domain beállítása

A `build.py` fájl tetején:

```python
BASE = "https://www.horse-play.hu"   # <<< a végleges domainre cserélendő
```

Ez a cím kerül a `canonical` hivatkozásokba, az Open Graph adatokba, a `sitemap.xml`-be
és a `robots.txt`-be. A `.htaccess`-ben szintén szerepel a `www` átirányításnál —
ott is át kell írni.

---

## 4. Képek cseréje

A képek helyőrzők, minden képen rajta van a saját fájlneve és az ajánlott méret.
Cseréld le őket ugyanolyan néven, hogy semmi mást ne kelljen módosítani:

| Fájl | Méret | Hol jelenik meg |
|---|---|---|
| `hero.jpg` | 1000 × 1060 | Főoldal, ívelt kép |
| `rolunk-1.jpg`, `rolunk-2.jpg` | 1200 × 960 | Rólunk, Főoldal |
| `szolgaltatas-1.jpg` | 1200 × 960 | Szolgáltatások |
| `lo-1.jpg` … `lo-6.jpg` | 1000 × 750 | Lovaink |
| `galeria-1.jpg` … `galeria-9.jpg` | 1400 × 1050 | Galéria |
| `og-kep.jpg` | 1200 × 630 | Facebook/Messenger megosztás |

Ha lecseréled a képeket, **a HTML-ben lévő `alt` szövegeket is írd át** a valós tartalomra —
ez akadálymentességi és SEO-szempontból egyaránt fontos.

> Fontos: felismerhető személyt ábrázoló fényképet csak az érintett (kiskorúnál a szülő)
> hozzájárulásával tegyetek ki. Ezt az adatkezelési tájékoztató 3.4. pontja is rögzíti.

---

## 5. Újragenerálás

A közös fejléc és lábléc egy helyen, a `build.py` fájlban van. Ha ott módosítasz,
futtasd le:

```bash
python3 build.py
```

Ez felülírja a `site` mappában lévő HTML-fájlokat. A CSS-t, a JS-t és a képeket
**nem érinti**, azokat közvetlenül szerkesztheted.

---

## 6. Jogi megfelelés — mi van megoldva

- **Impresszum** az Ekertv. (2001. évi CVIII. tv.) 4. §-a szerinti tartalommal,
  a tárhelyszolgáltató hivatalos adataival együtt.
- **Adatkezelési tájékoztató** a GDPR 13–14. cikke szerint: adatkezelő, célok,
  jogalapok, időtartamok, adatfeldolgozók, érintetti jogok, NAIH-elérhetőség.
- **Süti-tájékoztató** és **hozzájárulás-kezelő sáv.** Hozzájárulásig **egyetlen külső
  kérés sem indul** — ezt teszteltük. A Google Térkép csak külön gombnyomásra töltődik be,
  és a döntés bármikor visszavonható a láblécből.
- **Nincs süti.** A választást a böngésző `localStorage`-a tárolja, ami nem hagyja el
  a látogató eszközét.
- **Nincs Google Analytics, nincs Facebook-pixel, nincs Google Fonts CDN** — a betűtípusok
  saját tárhelyről töltődnek, így nincs adattovábbítás a Google felé.
- **Akadálymentességi nyilatkozat**, WCAG 2.1 AA szinthez igazodva.
- **Az oldal nem foglalási felület**, ezt az impresszum és a Szolgáltatások oldal is
  kimondja — így nem vonatkoznak rá a távollévők közötti szerződések (45/2014. Korm. rend.)
  szabályai.

### Amit még el kell intézni

- A hiányzó jogi adatok pótlása (nyilvántartási szám, adószám, képviselő).
- Ha később mégis kerül **kapcsolatfelvételi űrlap** az oldalra, az adatkezelési
  tájékoztatót ki kell egészíteni az űrlapadatok kezelésével.
- Ha felismerhető személyt ábrázoló képet tesztek ki, szerezzétek be a hozzájárulást írásban.

---

## 7. Technikai megoldások

- **Reszponzív** 320 képponttól felfelé, vízszintes túlcsordulás nélkül.
- **Animációk:** görgetésre megjelenés, finom parallax, számlálók, futó feliratsáv,
  görgetésjelző sáv, kártya-hover, képnagyító. A `prefers-reduced-motion` beállítást
  tiszteletben tartja — bekapcsolva minden animáció leáll.
- **Akadálymentesség:** „Ugrás a tartalomra" link, szemantikus szerkezet, egyetlen `h1`
  oldalanként, ugrás nélküli címsorhierarchia, látható fókuszjelölés, billentyűzetes
  képnagyító fókuszcsapdával, WCAG AA kontrasztarányok.
- **SEO:** oldalankénti egyedi `title` és leírás, `canonical`, Open Graph,
  `SportsActivityLocation` JSON-LD strukturált adat, `sitemap.xml`, `robots.txt`.
- **Biztonság** (`.htaccess`): HTTPS-átirányítás, HSTS, `X-Content-Type-Options`,
  `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` és szigorú
  `Content-Security-Policy` — `unsafe-inline` **nélkül**, sem szkriptre, sem stílusra.
- **Teljesítmény:** a teljes főoldal 8 kérés, a betűkészlet magyar karakterkészletre
  szűkítve összesen 86 KB. Nincs külső könyvtár, nincs build-lánc.
- **Betűtípusok:** Fraunces (címsorok, SOFT 60 / WONK 1 beállítással, változó optikai
  mérettel) és Plus Jakarta Sans (szöveg, 200–800 vastagság egyetlen fájlban).
  Mindkettő SIL Open Font License alatt, saját tárhelyről töltődik — nincs Google Fonts CDN.

---

*Készítette: Nagy Balázs — webfejlesztés · nagybalazsweb.com*

# Nagy Balázs — weboldal (MediaCenter tárhely)

Egyoldalas bemutatkozó weboldal. A kapcsolati űrlap közvetlenül a tárhelyről,
PHP-n keresztül küldi az e-mailt a **Resend**-del — nincs szükség külső szolgáltatásra.

---

## Mit tartalmaz a csomag

| Fájl | Mire való |
|---|---|
| `index.html` | Maga a weboldal — minden stílus és script benne van |
| `adatkezeles.html` | **Adatkezelési tájékoztató és impresszum** — jogilag kötelező tartalom |
| `404.html` | Egyedi hibaoldal rossz cím esetén |
| `betu/` | A weboldal betűtípusai (saját tárhelyről, nem a Google-tól) |
| `mail.php` | Fogadja az űrlapot és elküldi az e-mailt a Resenden át |
| `stat.php` | Süti nélküli látogatottság-mérés (nem tárol IP-címet) |
| `statisztika.php` | Jelszóval védett nézet a látogatottsághoz |
| `adatok/` | Ide gyűlik a napi statisztika (böngészőből nem érhető el) |
| `config.php` | **Ide kell beírni a Resend API kulcsot és a statisztika jelszavát** |
| `.htaccess` | HTTPS-kényszerítés, www eltávolítás, hibaoldal, tömörítés, gyorsítótár, biztonsági fejlécek |
| `og.png` | Előnézeti kép Facebookra, Messengerbe, LinkedInre |
| `favicon.svg`, `apple-touch-icon.png` | Ikonok |
| `site.webmanifest` | Alkalmazás-leíró |
| `robots.txt`, `sitemap.xml` | Keresőoptimalizálás |
| `beallit.sh` | Behelyettesíti a domaint minden fájlba |

---

## 1. lépés — Domain beírása

A fájlokban `DOMAIN.HU` helykitöltő szerepel. Egy paranccsal cserélhető:

```bash
bash beallit.sh a-domainem.hu "7621 Pécs, Példa utca 1." "51234567"
```

A második és harmadik érték a **székhelycímed** és az **egyéni vállalkozói
nyilvántartási számod** — ezek az impresszumba kerülnek, és jogszabály írja elő őket.
Ha elhagyod, a script figyelmeztet, és a helyükön `SZEKHELYCIM` / `NYILVSZAM` marad.

A script a végén ellenőrzi, maradt-e valahol helykitöltő.

> Ha nem tudsz parancssort futtatni, szólj — átírom neked, és kész csomagot kapsz.
> Kézzel ezekben a fájlokban van: `index.html`, `adatkezeles.html`, `404.html`,
> `robots.txt`, `sitemap.xml`, `config.php`.

---

## 2. lépés — Resend API kulcs

1. [resend.com](https://resend.com) → **API Keys → Create API Key**
2. Másold ki a `re_...` kezdetű kulcsot
3. Nyisd meg a `config.php`-t, és írd be:

```php
'resend_api_key' => 're_ide_jon_a_kulcs',
```

**Ezt a fájlt soha ne tedd fel GitHubra és ne oszd meg.**
A `.htaccess` letiltja, hogy böngészőből bárki elérje.

---

## 3. lépés — Feltöltés a tárhelyre

FTP-vel (FileZilla) vagy a MediaCenter felületén lévő fájlkezelővel töltsd fel
**az összes fájlt a tárhely gyökérkönyvtárába** — abba a mappába, ahonnan a
weboldal kiszolgálódik. Ez a szolgáltatónál jellemzően `public_html` vagy `web`
néven fut; FTP-n belépve az a mappa, amelyikben már ott van egy `index.html`
vagy egy `.htaccess`.

Figyelj rá, hogy a **`.htaccess` is felkerüljön** — a ponttal kezdődő fájlokat
sok FTP-program alapból elrejti. FileZillában: *Szerver → Rejtett fájlok
megjelenítésének kényszerítése*.

Feltöltés után nyisd meg a domaint. Az oldalnak azonnal jönnie kell.

---

## 4. lépés — SSL (https) bekapcsolása

A MediaCenter ügyfélfelületén kapcsold be az ingyenes tanúsítványt a domainre.
Amint aktív, a `.htaccess` automatikusan átirányít https-re, és a `www.`-t is
levágja, hogy a Google-nek egyetlen egységes cím legyen.

> Amíg az SSL nem aktív, az átirányítás végtelen körbe futhat. Ezért:
> **először SSL, utána élesítés.** Ha addig is nézni akarod, a `.htaccess`-ben
> ideiglenesen kikommentelheted a HTTPS-blokkot egy `#` jellel a sorok elején.

---

## 5. lépés — Feladó cím rendbe tétele

A `config.php`-ban most ez áll:

```php
'mail_from' => 'onboarding@resend.dev',
```

Ez a Resend teszt címe: **csak a saját Resend-fiókod e-mail címére tud küldeni.**
Mivel a levél úgyis hozzád érkezik, ez indulásnak működik — de a feladó
`resend.dev` lesz, ami nem szép.

Ha megvan a domain, érdemes rögtön hitelesíteni:

1. Resend → **Domains → Add Domain** → add meg a domaint
2. A kapott DNS rekordokat (SPF, DKIM) vidd fel a MediaCenter DNS-kezelőjében
3. Ha zöld a státusz, írd át a `config.php`-ban:
   `'mail_from' => 'noreply@a-domainem.hu',`

Ettől kezdve saját nevedről megy a levél, és bárhová tud küldeni.

> Ezt a részt meg tudom csinálni helyetted — csak a domainnév kell hozzá,
> és megkapod a pontos DNS rekordokat.

---

## Ellenőrző lista élesítés után

- [ ] Az oldal megnyílik https-en, a `www.` átirányít
- [ ] Egy nem létező cím (pl. `/teszt`) a saját 404 oldalra visz
- [ ] Az űrlap kitöltve elmegy, és megérkezik a levél
- [ ] A levélre válaszolva az érdeklődőhöz megy a válasz (reply-to)
- [ ] Mobilon is jól néz ki
- [ ] Google Search Console: domain hozzáadva, sitemap beküldve
      (`https://a-domainem.hu/sitemap.xml`)

---

## Mi van beépítve

**Keresőoptimalizálás**
- 49 karakteres oldalcím, 150 karakteres leírás
- Canonical cím, Open Graph és Twitter kártya előnézeti képpel
- Strukturált adatok (JSON-LD): szolgáltatás, árak, GYIK — ettől a Google
  a keresési találatnál is meg tudja jeleníteni a kérdéseket
- `robots.txt`, `sitemap.xml`, egyedi 404 oldal
- Egy `h1`, alatta szekciónként `h2`

**Megjelenés**
- Végigmérve 320-tól 1920 pixelig: iPhone SE, iPhone 14, iPad álló és fekvő, laptop, nagy monitor
- 900 px alatt mobilmenü, tabletnél kétoszlopos elrendezés
- Minden gomb és link legalább 40–52 px magas
- Az űrlapmezők mobilon 16 px betűsek, így az iPhone nem nagyít rá fókusznál

**Biztonság és sebesség**
- HTTPS-kényszerítés, HSTS, `X-Frame-Options`, `X-Content-Type-Options`, Referrer-Policy
- A `config.php` böngészőből nem érhető el
- Gzip tömörítés és böngésző-gyorsítótár beállítva
- Könyvtárlistázás kikapcsolva

**Spamvédelem az űrlapon**
- Rejtett csapdamező (a robot kitölti, az ember nem)
- Elutasítja a 2,5 másodpercnél gyorsabb beküldést
- IP-nként legfeljebb 5 küldés óránként
- A beküldött szöveg escape-elve kerül a levélbe

---

## Módosítás

Az `index.html` egyetlen fájl, nincs mögötte fordítás vagy build lépés.
Keress rá a mondatra, írd át, töltsd fel újra.

A színek a fájl elején, a `:root` blokkban vannak.

---

## Az adatkezelési tájékoztatóról

Az `adatkezeles.html` a te tényleges adatkezelésedre készült: a kapcsolati űrlapra,
a Resend levélküldésre, a MediaCenter tárhelyre és a saját, süti nélküli mérésre.
**Két mezőt kötelező kitölteni benne** (a `beallit.sh` megcsinálja):

- `SZEKHELYCIM` — a vállalkozásod bejegyzett székhelye
- `NYILVSZAM` — az egyéni vállalkozói nyilvántartási számod

> Ez a szöveg gondos, de nem helyettesíti a jogi felülvizsgálatot. Ha nagyobb
> ügyfélkörrel dolgozol, érdemes egyszer átnézetni egy ügyvéddel.

Ha később változik a működés — például hírlevelet indítasz, vagy webshopot
üzemeltetsz —, a tájékoztatót is frissíteni kell.

---

## Automatikus visszaigazoló levél

A `config.php`-ben a `'visszaigazolas' => false` sor kapcsolja.

Amíg a feladó cím az `onboarding@resend.dev`, **hagyd `false`-on**: a Resend
a teszt címről csak a saját fiókod e-mail címére enged küldeni, tehát az
érdeklődőhöz nem jutna el a levél.

Ha a domainedet hitelesítetted a Resendben (Domains → Add Domain, majd a
DNS rekordok beállítása a MediaCenter felületén):

1. `'mail_from' => 'noreply@a-domainem.hu'`
2. `'visszaigazolas' => true`

Ettől kezdve minden beküldő kap egy rövid visszaigazolást is.

---

## Látogatottság-mérés

Süti nélküli, teljesen a saját tárhelyeden fut — semmilyen külső szolgáltatóhoz
nem kerül adat, és nincs szükség süti-elfogadó sávra.

1. A `config.php`-ban add meg a jelszót: `'stat_jelszo' => 'valami-erős-jelszó'`
2. Az adatok a `statisztika.php` címen nézhetők meg (felhasználónevet hagyj üresen,
   jelszónak a fentit add meg)
3. Kikapcsolni a `'stat_be' => false` sorral lehet

Az `adatok/` mappát a `.htaccess` letiltja a böngészőből — ha a tárhelyen
mégis elérhető lenne, szólj, és átteszem a webgyökér fölé.

> A mérés IP-címet nem tárol, csak egy naponta cserélődő, visszafejthetetlen
> lenyomatot használ az egyedi látogatók becsléséhez.

---

## Betűtípusok

A `betu/` mappában a weboldal két betűtípusa található, a magyar karakterkészletre
szűkítve (összesen kb. 58 KB). Ezek a saját tárhelyről töltődnek, tehát a
látogatók IP-címe **nem jut el a Google-höz** — ez a német bírósági gyakorlat
óta visszatérő adatvédelmi kifogás a Google Fonts használatával szemben.

A licencfeltételek a `betu/LICENC.txt` fájlban vannak. Ezt a fájlt hagyd a
csomagban, ne töröld.

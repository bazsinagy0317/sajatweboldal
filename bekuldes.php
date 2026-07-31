<?php
/**
 * Azonnali indexelés-értesítő (IndexNow)
 * --------------------------------------
 * Egyetlen hívással szól a Bingnek, a Yandexnek és a Seznamnak, hogy
 * változott az oldal — így órák alatt indexelhetnek napok helyett.
 * A Google nem használja az IndexNow-t; oda a Search Console-on át megy a jelzés.
 *
 * Használat böngészőből:
 *   https://a-domainem.hu/bekuldes.php?jelszo=...          → minden cím a sitemapból
 *   https://a-domainem.hu/bekuldes.php?jelszo=...&url=/uj-oldal.html
 */
declare(strict_types=1);
header('Content-Type: text/plain; charset=utf-8');

$cfg = @include __DIR__ . '/config.php';
$jelszo = is_array($cfg) ? (string)($cfg['stat_jelszo'] ?? '') : '';
if ($jelszo === '' || $jelszo === 'IDE_JON_EGY_JELSZO') {
    http_response_code(503); exit("Előbb állítsd be a stat_jelszo értéket a config.php-ben.\n");
}
if (!hash_equals($jelszo, (string)($_GET['jelszo'] ?? ''))) {
    http_response_code(401); exit("Hibás jelszó.\n");
}

$kulcsFajl = __DIR__ . '/indexnow-kulcs.txt';
if (!is_readable($kulcsFajl)) { http_response_code(500); exit("Hiányzik az indexnow-kulcs.txt.\n"); }
$kulcs = trim((string)file_get_contents($kulcsFajl));

$host = (string)($_SERVER['HTTP_HOST'] ?? '');
$host = preg_replace('~[^A-Za-z0-9.\-]~', '', $host) ?: '';
if ($host === '') { http_response_code(500); exit("Nem állapítható meg a domain.\n"); }
$alap = 'https://' . $host;

$cimek = [];
if (!empty($_GET['url'])) {
    $u = '/' . ltrim((string)$_GET['url'], '/');
    $u = preg_replace('~[^A-Za-z0-9/._\-]~', '', $u) ?: '/';
    $cimek[] = $alap . $u;
} else {
    $sm = @file_get_contents(__DIR__ . '/sitemap.xml');
    if ($sm === false) { http_response_code(500); exit("Nem olvasható a sitemap.xml.\n"); }
    if (preg_match_all('~<loc>\s*(.*?)\s*</loc>~i', $sm, $m)) {
        foreach ($m[1] as $loc) {
            $u = parse_url(trim($loc), PHP_URL_PATH) ?: '/';
            $cimek[] = $alap . $u;
        }
    }
}
$cimek = array_values(array_unique($cimek));
if (!$cimek) { exit("Nincs beküldendő cím.\n"); }
$cimek = array_slice($cimek, 0, 10000);

$torzs = json_encode([
    'host'        => $host,
    'key'         => $kulcs,
    'keyLocation' => $alap . '/' . $kulcs . '.txt',
    'urlList'     => $cimek,
], JSON_UNESCAPED_SLASHES);

$ch = curl_init('https://api.indexnow.org/IndexNow');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $torzs,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 20,
    CURLOPT_HTTPHEADER => ['Content-Type: application/json; charset=utf-8'],
]);
$valasz = curl_exec($ch);
$statusz = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
$hiba = curl_error($ch);
curl_close($ch);

echo "Beküldött címek: " . count($cimek) . "\n";
echo "Válasz kódja: {$statusz}\n";
if ($statusz === 200 || $statusz === 202) {
    echo "Rendben — a keresők megkapták az értesítést.\n";
} else {
    echo "Nem sikerült. " . ($hiba !== '' ? $hiba : (string)$valasz) . "\n";
}
echo "\nA Google nem használja az IndexNow-t: oda a Search Console → Sitemapek menüben\n";
echo "kell egyszer beküldeni a sitemap.xml-t, utána magától követi a változásokat.\n";

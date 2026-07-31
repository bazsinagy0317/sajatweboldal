<?php
/**
 * Kapcsolati űrlap → Resend
 * MediaCenter tárhelyen fut, PHP 8.x
 *
 * Az API kulcs a config.php-ben van, hogy ne kerüljön bele ebbe a fájlba.
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

function ki(array $adat, int $kod = 200): never {
    http_response_code($kod);
    echo json_encode($adat, JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    ki(['ok' => false, 'error' => 'Csak POST kérés engedélyezett.'], 405);
}

$cfg = @include __DIR__ . '/config.php';
if (!is_array($cfg) || empty($cfg['resend_api_key'])) {
    error_log('mail.php: hiányzó vagy hibás config.php');
    ki(['ok' => false, 'error' => 'A szolgáltatás jelenleg nem elérhető.'], 500);
}

/* ── Egyszerű sebességkorlát: IP-nként 5 küldés óránként ── */
$ip   = (string)($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
$kulcs = sys_get_temp_dir() . '/urlap_' . hash('sha256', $ip) . '.txt';
$most  = time();
$idok  = [];
if (is_readable($kulcs)) {
    $idok = array_filter(
        array_map('intval', explode(',', (string)file_get_contents($kulcs))),
        fn(int $t): bool => $t > $most - 3600
    );
}
if (count($idok) >= 5) {
    ki(['ok' => false, 'error' => 'Túl sok küldés. Kérem, próbálja újra később.'], 429);
}

/* ── Bejövő adat ── */
$nyers = file_get_contents('php://input') ?: '';
$d = json_decode($nyers, true);
if (!is_array($d)) {
    ki(['ok' => false, 'error' => 'Hibás kérés.'], 400);
}

/* Csapda mező: a valódi látogató nem tölti ki, a robot igen */
if (!empty($d['website'])) {
    ki(['ok' => true]);
}
/* Túl gyors beküldés = robot */
if (isset($d['elapsed']) && is_numeric($d['elapsed']) && (int)$d['elapsed'] < 2500) {
    ki(['ok' => false, 'error' => 'Túl gyors beküldés.'], 400);
}

$vag = static fn(string $mezo, int $max): string =>
    mb_substr(trim((string)($d[$mezo] ?? '')), 0, $max);

$nev    = $vag('nev', 120);
$ceg    = $vag('ceg', 160);
$email  = $vag('email', 200);
$tel    = $vag('tel', 40);
$uzenet = $vag('uzenet', 5000);

if ($nev === '' || $uzenet === '') {
    ki(['ok' => false, 'error' => 'Hiányzó kötelező mező.'], 400);
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || !preg_match('/\.[a-z]{2,}$/i', $email)) {
    ki(['ok' => false, 'error' => 'Érvénytelen e-mail cím.'], 400);
}

$e = static fn(string $s): string => htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
/* Fejléc-injektálás elleni tisztítás a Reply-To mezőhöz */
$fejlec = static fn(string $s): string => mb_substr(str_replace(["\r", "\n"], ' ', $s), 0, 200);

$targy = 'Új érdeklődés — ' . ($ceg !== '' ? $ceg : $nev);

$html = '<div style="font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;font-size:15px;line-height:1.65;color:#1a1a1a">'
  . '<h2 style="margin:0 0 18px;font-size:19px;color:#C4471F">Új érdeklődés a weboldalról</h2>'
  . '<table cellpadding="0" cellspacing="0" style="border-collapse:collapse;width:100%;max-width:600px">'
  . '<tr><td style="padding:8px 0;color:#666;width:110px">Név</td><td style="padding:8px 0;font-weight:600">' . $e($nev) . '</td></tr>'
  . '<tr><td style="padding:8px 0;color:#666">Cég</td><td style="padding:8px 0">' . ($ceg !== '' ? $e($ceg) : '—') . '</td></tr>'
  . '<tr><td style="padding:8px 0;color:#666">E-mail</td><td style="padding:8px 0"><a href="mailto:' . $e($email) . '" style="color:#C4471F">' . $e($email) . '</a></td></tr>'
  . '<tr><td style="padding:8px 0;color:#666">Telefon</td><td style="padding:8px 0">' . ($tel !== '' ? $e($tel) : '—') . '</td></tr>'
  . '</table>'
  . '<div style="margin:22px 0 8px;color:#666">Üzenet</div>'
  . '<div style="white-space:pre-wrap;background:#f6f5f2;border-left:3px solid #C4471F;padding:14px 16px">' . $e($uzenet) . '</div>'
  . '<p style="margin-top:24px;font-size:12px;color:#999">Válaszolj közvetlenül erre a levélre — a válasz a feladóhoz megy.</p>'
  . '</div>';

$szoveg = "Új érdeklődés a weboldalról\n\n"
  . "Név: {$nev}\n"
  . 'Cég: ' . ($ceg !== '' ? $ceg : '—') . "\n"
  . "E-mail: {$email}\n"
  . 'Telefon: ' . ($tel !== '' ? $tel : '—') . "\n\n"
  . "Üzenet:\n{$uzenet}\n";

$torzs = json_encode([
    'from'     => $cfg['mail_from'],
    'to'       => [$cfg['mail_to']],
    'subject'  => $targy,
    'html'     => $html,
    'text'     => $szoveg,
    'reply_to' => $fejlec($email),
], JSON_UNESCAPED_UNICODE);

$ch = curl_init('https://api.resend.com/emails');
curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => $torzs,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 15,
    CURLOPT_HTTPHEADER     => [
        'Authorization: Bearer ' . $cfg['resend_api_key'],
        'Content-Type: application/json',
    ],
]);
$valasz = curl_exec($ch);
$statusz = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlHiba = curl_error($ch);
curl_close($ch);

if ($valasz === false || $statusz < 200 || $statusz >= 300) {
    error_log('mail.php Resend hiba: ' . $statusz . ' ' . (string)$valasz . ' ' . $curlHiba);
    ki(['ok' => false, 'error' => 'Az e-mail küldése nem sikerült.'], 502);
}

/* ── Automatikus visszaigazolás az érdeklődőnek ──
   Csak akkor megy ki, ha a config.php-ban be van kapcsolva. A hitelesítetlen
   teszt-feladóval a Resend csak a saját fiók címére enged küldeni, ezért
   alapértelmezésben ki van kapcsolva. Ha nem sikerül, az érdemi levelet
   ez már nem befolyásolja. */
if (!empty($cfg['visszaigazolas'])) {
    $vhtml = '<div style="font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;font-size:15px;line-height:1.7;color:#1a1a1a">'
      . '<p>Kedves ' . $e($nev) . ',</p>'
      . '<p>köszönöm a megkeresést — az üzenete megérkezett. Munkanapokon <b>24 órán belül</b> válaszolok, '
      . 'és ha elég információm van hozzá, rögtön küldök egy tételes, fix összegű árajánlatot is.</p>'
      . '<p>Ez egy automatikus visszaigazolás, nem szükséges rá válaszolni. '
      . 'Ha időközben eszébe jut valami, nyugodtan írjon erre a levélre.</p>'
      . '<div style="margin:22px 0 8px;color:#666;font-size:13px">Amit elküldött:</div>'
      . '<div style="white-space:pre-wrap;background:#f6f5f2;border-left:3px solid #C4471F;padding:14px 16px;font-size:14px">' . $e($uzenet) . '</div>'
      . '<p style="margin-top:26px">Üdvözlettel:<br><b>Nagy Balázs</b><br>'
      . '<span style="color:#666;font-size:13px">Weboldal- és webshopfejlesztés · Pécs<br>'
      . '+36 70 416 4210 · bazsinagy0317@gmail.com</span></p>'
      . '</div>';

    $vszoveg = "Kedves {$nev},\n\n"
      . "köszönöm a megkeresést — az üzenete megérkezett. Munkanapokon 24 órán belül válaszolok.\n\n"
      . "Ez egy automatikus visszaigazolás, nem szükséges rá válaszolni.\n\n"
      . "Amit elküldött:\n{$uzenet}\n\n"
      . "Üdvözlettel:\nNagy Balázs\nWeboldal- és webshopfejlesztés, Pécs\n+36 70 416 4210\n";

    $vtorzs = json_encode([
        'from'     => $cfg['mail_from'],
        'to'       => [$fejlec($email)],
        'subject'  => 'Megkaptam az üzenetét — Nagy Balázs',
        'html'     => $vhtml,
        'text'     => $vszoveg,
        'reply_to' => $cfg['mail_to'],
    ], JSON_UNESCAPED_UNICODE);

    $vch = curl_init('https://api.resend.com/emails');
    curl_setopt_array($vch, [
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => $vtorzs,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 10,
        CURLOPT_HTTPHEADER     => [
            'Authorization: Bearer ' . $cfg['resend_api_key'],
            'Content-Type: application/json',
        ],
    ]);
    $vvalasz = curl_exec($vch);
    $vstatusz = (int)curl_getinfo($vch, CURLINFO_HTTP_CODE);
    curl_close($vch);
    if ($vvalasz === false || $vstatusz < 200 || $vstatusz >= 300) {
        error_log('mail.php: a visszaigazolás nem ment ki (' . $vstatusz . ')');
    }
}

/* Sikeres küldés rögzítése a sebességkorláthoz */
$idok[] = $most;
@file_put_contents($kulcs, implode(',', $idok), LOCK_EX);

ki(['ok' => true]);
